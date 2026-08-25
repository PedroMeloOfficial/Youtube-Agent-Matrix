"""
Search YouTube for videos by keyword, or inside one channel.

============================ READ THIS FIRST ============================
``search.list`` costs **100 quota units per call**. The daily budget is 10,000
units (``references/benchmarks.md`` §10), so this script can run roughly **100
times a day, total, across everything** -- and a single loop over ten keywords
burns a tenth of the day.

Every other script in this folder costs 1-5 units per call. This one costs 100.

**Before using it, check whether you need it at all:**

  * Listing one known channel's videos? Use ``fetch_channel_data.py``. The
    uploads-playlist path returns the same data for a handful of units. This
    script refuses a channel-only listing unless you pass ``--force``.
  * Looking up a channel by @handle? ``fetch_channel_data.py`` resolves handles
    for 1 unit.
  * Genuinely searching a *topic* across channels you cannot name in advance?
    That is what this script is for. Batch your thinking, run it once, and reuse
    the result for the rest of the session.

The script checks the quota ledger before spending, refuses when the call will
not fit, and prints a warning both in the JSON output and on stderr every time
it runs.
=========================================================================

Public data only. A competitor's retention, impressions, click-through rate and
revenue are not obtainable through this or any other API -- do not imply otherwise
in a deliverable. What you can read from public data: view counts, publish dates,
durations, engagement ratios, title and thumbnail patterns, and which videos
outperform their own channel's median.

Credentials: ``YOUTUBE_API_KEY`` in the environment.

Usage:
    python execution/search_competitor_videos.py "topic keyword"
    python execution/search_competitor_videos.py "topic keyword" --max-results 25 --order viewCount
    python execution/search_competitor_videos.py "topic" --days 90 --region-code BR --language pt
    python execution/search_competitor_videos.py --channel-id UC... --force

Exit 0 with ``{"ok": true, ...}``; exit 1 with ``{"ok": false, "error": {...}}``.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from statistics import median

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import quota_tracker  # noqa: E402
from utils.youtube_auth import (  # noqa: E402
    ApiCallFailed,
    ExecutionError,
    InputInvalid,
    build_data_client,
    die,
    emit,
    explain_api_error,
    install_excepthook,
)
from fetch_channel_data import parse_iso_duration  # noqa: E402

SEARCH_COST = quota_tracker.cost_of("search.list")
MAX_RESULTS = 50
OUTLIER_MULTIPLIER = 3.0

RUNTIME_WARNING = (
    f"search.list costs {SEARCH_COST} quota units per call -- roughly 1% of the entire "
    "daily budget. If you only need one known channel's videos, cancel and use "
    "fetch_channel_data.py instead (a few units for the same data)."
)


def _execute(request, operation, count=1):
    try:
        response = request.execute()
    except Exception as exc:  # noqa: BLE001 -- always surfaced as JSON
        if isinstance(exc, ExecutionError):
            raise
        raise explain_api_error(exc)
    quota_tracker.record(operation, count)
    return response


def _int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def run_search(service, args):
    """One search.list call, then one cheap videos.list to enrich the results."""
    params = {
        "part": "id,snippet",
        "type": "video",
        "maxResults": min(args.max_results, MAX_RESULTS),
        "order": args.order,
    }
    if args.query:
        params["q"] = args.query
    if args.channel_id:
        params["channelId"] = args.channel_id
    if args.region_code:
        params["regionCode"] = args.region_code
    if args.language:
        params["relevanceLanguage"] = args.language
    if args.days:
        cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
        params["publishedAfter"] = cutoff.strftime("%Y-%m-%dT00:00:00Z")

    response = _execute(service.search().list(**params), "search.list")

    snippets = {}
    for item in response.get("items", []):
        video_id = item.get("id", {}).get("videoId")
        if video_id:
            snippets[video_id] = item.get("snippet", {})

    if not snippets:
        return []

    details = _execute(
        service.videos().list(part="statistics,contentDetails", id=",".join(snippets)),
        "videos.list",
    )
    stats_by_id = {item["id"]: item for item in details.get("items", [])}

    videos = []
    for video_id, snippet in snippets.items():
        item = stats_by_id.get(video_id, {})
        stats = item.get("statistics", {})
        content = item.get("contentDetails", {})

        views = _int(stats.get("viewCount"))
        likes = _int(stats.get("likeCount"), None)
        comments = _int(stats.get("commentCount"), None)
        engagement = None
        if views and likes is not None:
            engagement = round(((likes + (comments or 0)) / views) * 100, 2)

        videos.append({
            "video_id": video_id,
            "title": snippet.get("title"),
            "channel_id": snippet.get("channelId"),
            "channel_title": snippet.get("channelTitle"),
            "published_at": snippet.get("publishedAt"),
            "description": snippet.get("description", "")[:300],
            "duration_iso": content.get("duration"),
            "duration_seconds": parse_iso_duration(content.get("duration")),
            "views": views,
            "likes": likes,
            "comments": comments,
            "engagement_rate_pct": engagement,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url"),
        })

    videos.sort(key=lambda video: video["views"], reverse=True)
    return videos


def flag_outliers(videos, multiplier=OUTLIER_MULTIPLIER):
    """
    Mark videos that beat their own channel's median inside this result set.

    Only meaningful where a channel contributed at least three videos -- with fewer,
    the median is noise and the flag would be a fabricated signal.
    """
    by_channel = {}
    for video in videos:
        by_channel.setdefault(video.get("channel_id") or "unknown", []).append(video)

    for group in by_channel.values():
        if len(group) < 3:
            for video in group:
                video["vs_channel_median"] = None
                video["is_outlier"] = None
            continue
        channel_median = median(video["views"] for video in group) or 0
        for video in group:
            ratio = round(video["views"] / channel_median, 1) if channel_median else None
            video["vs_channel_median"] = ratio
            video["is_outlier"] = bool(ratio and ratio >= multiplier)
    return videos


def main():
    install_excepthook()
    parser = argparse.ArgumentParser(
        description=f"Search YouTube videos by keyword or channel. "
                    f"WARNING: costs {SEARCH_COST} quota units per call. Outputs JSON on stdout.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            f"QUOTA WARNING: search.list costs {SEARCH_COST} units against a 10,000/day budget --\n"
            "about 100 calls per day for everything combined.\n\n"
            "To list a known channel's videos, use fetch_channel_data.py instead: same data,\n"
            "a fraction of the cost. This script refuses --channel-id without a query unless\n"
            "you pass --force.\n\n"
            "Public metrics only. Competitor retention, CTR and revenue are not obtainable."
        ),
    )
    parser.add_argument("query", nargs="?", default="", help="Search keywords.")
    parser.add_argument("--channel-id", help="Restrict the search to one channel (UC...).")
    parser.add_argument("--max-results", type=int, default=10,
                        help=f"Results to return (default: 10, max: {MAX_RESULTS}).")
    parser.add_argument("--order", choices=["relevance", "viewCount", "date", "rating", "title"],
                        default="relevance", help="Result ordering (default: relevance).")
    parser.add_argument("--days", type=int, help="Only videos published in the last N days.")
    parser.add_argument("--region-code", help="ISO country code for the target market, e.g. BR.")
    parser.add_argument("--language", help="Relevance language code for the target market, e.g. pt.")
    parser.add_argument("--no-outliers", dest="outliers", action="store_false",
                        help="Skip the per-channel outlier flags.")
    parser.add_argument("--force", action="store_true",
                        help="Run a channel-only listing anyway, despite the cheaper alternative.")
    parser.set_defaults(outliers=True)
    args = parser.parse_args()

    try:
        if not args.query and not args.channel_id:
            die(InputInvalid(
                "Nothing to search for.",
                fix=["Pass a keyword query, or --channel-id, or both."],
            ))

        if args.channel_id and not args.query and not args.force:
            die(InputInvalid(
                f"Listing one channel's videos through search.list costs {SEARCH_COST} units. "
                "The uploads-playlist path costs a handful.",
                fix=[
                    f"Use: python execution/fetch_channel_data.py {args.channel_id} --videos 30",
                    "If you genuinely need search ranking inside this channel, add --force.",
                ],
            ))

        if args.max_results < 1 or args.max_results > MAX_RESULTS:
            die(InputInvalid(f"--max-results must be between 1 and {MAX_RESULTS}."))

        # Loud, before spending anything.
        print(f"WARNING: {RUNTIME_WARNING}", file=sys.stderr)

        budget = quota_tracker.can_afford("search.list")
        if budget.get("warning"):
            print(f"WARNING: {budget['warning']}", file=sys.stderr)
        if not budget["allowed"]:
            die(ApiCallFailed(
                budget["error"],
                fix=[
                    "Wait for the midnight-Pacific reset before searching again.",
                    "For a known channel today, use fetch_channel_data.py -- it still fits in "
                    "what is left.",
                    "Otherwise fall back to WebSearch and read the SERP qualitatively "
                    "(references/data-sources.md §6).",
                ],
                details={"quota": budget},
            ))

        service = build_data_client()
        videos = run_search(service, args)
        if args.outliers:
            videos = flag_outliers(videos)

        quota_state = quota_tracker.snapshot()
        warnings = [RUNTIME_WARNING]
        if quota_state.get("warning"):
            warnings.append(quota_state["warning"])

        emit({
            "ok": True,
            "query": args.query or None,
            "channel_filter": args.channel_id,
            "filters": {
                "order": args.order,
                "days": args.days,
                "region_code": args.region_code,
                "relevance_language": args.language,
            },
            "result_count": len(videos),
            "videos": videos,
            "quota": {
                "search_list_cost": SEARCH_COST,
                "spent_this_call": budget["cost"] + 1,
                "remaining_today": quota_state["remaining"],
                "searches_left_today": quota_state["remaining"] // SEARCH_COST,
            },
            "warnings": warnings,
            "data_scope": "public metrics only -- competitor retention, CTR, impressions and "
                          "revenue are not obtainable through any official API",
            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        })

    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
