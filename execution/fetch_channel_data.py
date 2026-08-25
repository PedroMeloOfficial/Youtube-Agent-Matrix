"""
Fetch a channel's public profile and its recent videos, cheaply.

Takes a channel URL, @handle or channel ID and returns channel statistics plus the
last N uploads with their public metrics, as JSON on stdout.

**It uses the uploads-playlist path, never search.list.** To list a channel's
videos this script calls:

    channels.list        -> statistics + the uploads playlist ID   (1 unit)
    playlistItems.list   -> video IDs, 50 per page                 (1 unit/page)
    videos.list          -> full metadata, 50 IDs per call         (1 unit/call)

That is a handful of units for 50 videos. The same job via ``search.list`` costs
100 units per call -- two orders of magnitude more, for less data. This is the
difference between analysing dozens of channels a day and analysing a few.

Public data only. Retention, impressions, click-through rate and revenue are not
in the Data API for any channel, including the creator's own -- those come from
``fetch_video_analytics.py`` (OAuth, own channel only).

Credentials: ``YOUTUBE_API_KEY`` in the environment. Nothing is read from or
written to the plugin folder. Missing key produces a JSON error naming the fix
and the manual fallback, never a stack trace.

Usage:
    python execution/fetch_channel_data.py UC________________________
    python execution/fetch_channel_data.py @somehandle --videos 30
    python execution/fetch_channel_data.py "https://www.youtube.com/@somehandle"
    python execution/fetch_channel_data.py @somehandle --videos 50 --full-descriptions

Exit 0 with ``{"ok": true, ...}``; exit 1 with ``{"ok": false, "error": {...}}``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
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

MAX_VIDEOS = 200
BATCH_SIZE = 50
DESCRIPTION_PREVIEW_CHARS = 300

CHANNEL_ID_RE = re.compile(r"^UC[\w-]{22}$")
URL_PATTERNS = [
    (re.compile(r"youtube\.com/channel/(UC[\w-]{22})"), "id"),
    (re.compile(r"youtube\.com/@([\w.\-]+)"), "handle"),
    (re.compile(r"youtube\.com/user/([\w.\-]+)"), "username"),
    (re.compile(r"youtube\.com/c/([\w.\-]+)"), "vanity"),
]

ISO_DURATION_RE = re.compile(
    r"^P(?:(?P<days>\d+)D)?T?(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?$"
)


# --------------------------------------------------------------------------- #
# Input parsing
# --------------------------------------------------------------------------- #

def parse_channel_input(raw):
    """Classify the creator's input as an ID, a handle, a legacy username or a vanity URL."""
    value = (raw or "").strip().strip("/")
    if not value:
        raise InputInvalid("No channel given.", fix=["Pass a channel URL, an @handle, or a UC... channel ID."])

    if CHANNEL_ID_RE.match(value):
        return {"kind": "id", "value": value}

    for pattern, kind in URL_PATTERNS:
        match = pattern.search(value)
        if match:
            return {"kind": kind, "value": match.group(1)}

    if value.startswith("@"):
        return {"kind": "handle", "value": value[1:]}

    if value.startswith("http"):
        raise InputInvalid(
            f"Could not read a channel out of that URL: {value}",
            fix=["Open the channel page and copy the URL that contains /@handle or /channel/UC..."],
        )

    return {"kind": "handle", "value": value}


def parse_iso_duration(value):
    """ISO-8601 duration -> whole seconds. Returns None on anything unexpected."""
    if not value:
        return None
    match = ISO_DURATION_RE.match(value)
    if not match:
        return None
    parts = {k: int(v) if v else 0 for k, v in match.groupdict().items()}
    return parts["days"] * 86400 + parts["hours"] * 3600 + parts["minutes"] * 60 + parts["seconds"]


def _int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _parse_ts(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


# --------------------------------------------------------------------------- #
# API calls
# --------------------------------------------------------------------------- #

def _execute(request, operation, count=1):
    """Run one API request, translate failures, and record the quota it spent."""
    try:
        response = request.execute()
    except Exception as exc:  # noqa: BLE001 -- always surfaced as JSON
        if isinstance(exc, ExecutionError):
            raise
        raise explain_api_error(exc)
    quota_tracker.record(operation, count)
    return response


def resolve_channel(service, parsed):
    """
    Resolve any accepted input to a channel resource, using cheap reads only.

    A vanity /c/ URL has no cheap lookup -- resolving it would need search.list at
    100 units. Rather than spend that silently, this asks for the @handle instead.
    """
    part = "snippet,statistics,contentDetails,brandingSettings,topicDetails"

    if parsed["kind"] == "id":
        request = service.channels().list(part=part, id=parsed["value"])
    elif parsed["kind"] == "handle":
        request = service.channels().list(part=part, forHandle=parsed["value"])
    elif parsed["kind"] == "username":
        request = service.channels().list(part=part, forUsername=parsed["value"])
    else:
        raise InputInvalid(
            f"A /c/ vanity URL cannot be resolved without an expensive search "
            f"(100 quota units): {parsed['value']}",
            fix=[
                "Open the channel page -- the address bar shows the @handle. Pass that instead.",
                "Or pass the UC... channel ID from the channel's About panel.",
            ],
        )

    response = _execute(request, "channels.list")
    items = response.get("items", [])
    if not items:
        raise ApiCallFailed(
            f"No channel found for {parsed['kind']} '{parsed['value']}'.",
            fix=[
                "Check the spelling of the handle, or pass the UC... channel ID.",
                "Handles are case-insensitive but must be exact otherwise.",
            ],
        )
    return items[0]


def shape_channel(raw):
    snippet = raw.get("snippet", {})
    stats = raw.get("statistics", {})
    branding = raw.get("brandingSettings", {}).get("channel", {})
    uploads = raw.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")

    subscriber_count = _int(stats.get("subscriberCount"), None)
    return {
        "channel_id": raw.get("id"),
        "title": snippet.get("title"),
        "handle": snippet.get("customUrl"),
        "description": snippet.get("description", ""),
        "published_at": snippet.get("publishedAt"),
        "country": snippet.get("country"),
        "default_language": snippet.get("defaultLanguage") or branding.get("defaultLanguage"),
        "subscriber_count": subscriber_count,
        "subscriber_count_hidden": bool(stats.get("hiddenSubscriberCount")),
        "total_views": _int(stats.get("viewCount")),
        "video_count": _int(stats.get("videoCount")),
        "keywords": branding.get("keywords", ""),
        "topics": raw.get("topicDetails", {}).get("topicCategories", []),
        "uploads_playlist_id": uploads,
        "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url"),
    }


def collect_video_ids(service, uploads_playlist_id, wanted):
    """Page through the uploads playlist for the most recent `wanted` video IDs."""
    ids = []
    page_token = None
    while len(ids) < wanted:
        request = service.playlistItems().list(
            part="contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=min(BATCH_SIZE, wanted - len(ids)),
            pageToken=page_token,
        )
        response = _execute(request, "playlistItems.list")
        for item in response.get("items", []):
            video_id = item.get("contentDetails", {}).get("videoId")
            if video_id:
                ids.append(video_id)
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return ids[:wanted]


def fetch_videos(service, video_ids, full_descriptions=False):
    """Fetch metadata and public counts for up to 50 video IDs per call."""
    videos = []
    for start in range(0, len(video_ids), BATCH_SIZE):
        batch = video_ids[start:start + BATCH_SIZE]
        request = service.videos().list(
            part="snippet,statistics,contentDetails,status",
            id=",".join(batch),
        )
        response = _execute(request, "videos.list")
        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            stats = item.get("statistics", {})
            content = item.get("contentDetails", {})

            views = _int(stats.get("viewCount"))
            likes = _int(stats.get("likeCount"), None)
            comments = _int(stats.get("commentCount"), None)
            description = snippet.get("description", "")

            engagement = None
            if views and likes is not None:
                engagement = round(((likes + (comments or 0)) / views) * 100, 2)

            videos.append({
                "video_id": item.get("id"),
                "title": snippet.get("title"),
                "published_at": snippet.get("publishedAt"),
                "description": description if full_descriptions
                else description[:DESCRIPTION_PREVIEW_CHARS],
                "description_truncated": (not full_descriptions)
                and len(description) > DESCRIPTION_PREVIEW_CHARS,
                "tags": snippet.get("tags", []),
                "duration_iso": content.get("duration"),
                "duration_seconds": parse_iso_duration(content.get("duration")),
                "definition": content.get("definition"),
                "caption_available": content.get("caption") == "true",
                "made_for_kids": item.get("status", {}).get("madeForKids"),
                "views": views,
                "likes": likes,
                "comments": comments,
                "engagement_rate_pct": engagement,
                "url": f"https://www.youtube.com/watch?v={item.get('id')}",
                "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url"),
            })

    order = {vid: i for i, vid in enumerate(video_ids)}
    videos.sort(key=lambda v: order.get(v["video_id"], 10**6))
    return videos


# --------------------------------------------------------------------------- #
# Derived summary -- computed from the fetched set, never a benchmark
# --------------------------------------------------------------------------- #

def summarize(videos):
    """Descriptive statistics over the fetched sample. No benchmarks, no judgements."""
    if not videos:
        return {"sample_size": 0}

    views = [v["views"] for v in videos]
    durations = [v["duration_seconds"] for v in videos if v["duration_seconds"]]
    dates = sorted(d for d in (_parse_ts(v["published_at"]) for v in videos) if d)

    summary = {
        "sample_size": len(videos),
        "views_median": int(median(views)),
        "views_mean": int(sum(views) / len(views)),
        "views_max": max(views),
        "views_min": min(views),
        "duration_seconds_median": int(median(durations)) if durations else None,
    }

    median_views = summary["views_median"]
    if median_views:
        best = max(videos, key=lambda v: v["views"])
        summary["top_video"] = {
            "video_id": best["video_id"],
            "title": best["title"],
            "views": best["views"],
            "vs_median": round(best["views"] / median_views, 1),
        }
        summary["outliers_vs_median"] = [
            {"video_id": v["video_id"], "title": v["title"], "views": v["views"],
             "vs_median": round(v["views"] / median_views, 1)}
            for v in videos if v["views"] >= median_views * 3
        ]

    if len(dates) >= 2:
        gaps = [(dates[i + 1] - dates[i]).total_seconds() / 86400 for i in range(len(dates) - 1)]
        summary["median_days_between_uploads"] = round(median(gaps), 1)
        summary["newest_upload"] = dates[-1].date().isoformat()
        summary["oldest_upload_in_sample"] = dates[0].date().isoformat()
        age_days = (datetime.now(timezone.utc) - dates[-1]).total_seconds() / 86400
        summary["days_since_last_upload"] = round(age_days, 1)

    summary["note"] = (
        "Descriptive statistics over the fetched sample only. Compare against "
        "references/benchmarks.md -- never treat these figures as benchmarks."
    )
    return summary


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main():
    install_excepthook()
    parser = argparse.ArgumentParser(
        description="Fetch public channel statistics and recent videos via the cheap "
                    "uploads-playlist path. Outputs JSON on stdout.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Needs YOUTUBE_API_KEY in the environment.\n"
            "Public data only -- retention, CTR, impressions and revenue are not available here."
        ),
    )
    parser.add_argument("channel", help="Channel URL, @handle, or UC... channel ID.")
    parser.add_argument("--videos", type=int, default=10,
                        help=f"How many recent videos to fetch (default: 10, max: {MAX_VIDEOS}).")
    parser.add_argument("--full-descriptions", action="store_true",
                        help="Return complete descriptions instead of a preview.")
    parser.add_argument("--no-summary", action="store_true",
                        help="Skip the derived summary block.")
    args = parser.parse_args()

    if args.videos < 0 or args.videos > MAX_VIDEOS:
        die(InputInvalid(
            f"--videos must be between 0 and {MAX_VIDEOS}.",
            fix=[f"Try --videos {min(max(args.videos, 0), MAX_VIDEOS)}."],
        ))

    try:
        parsed = parse_channel_input(args.channel)

        # Budget: 1 channels.list + 1 playlistItems.list per 50 + 1 videos.list per 50.
        pages = (args.videos + BATCH_SIZE - 1) // BATCH_SIZE
        estimate = 1 + pages * 2
        budget = quota_tracker.can_afford("videos.list", estimate)
        if not budget["allowed"]:
            die(ApiCallFailed(
                budget["error"],
                fix=[
                    "Wait for the midnight-Pacific reset, or lower --videos.",
                    "Meanwhile: ask the creator for the channel URL, subscriber count, and the "
                    "last 10 titles with view counts and publish dates.",
                ],
                details={"quota": budget},
            ))

        service = build_data_client()
        channel = shape_channel(resolve_channel(service, parsed))

        videos = []
        warnings = []
        if args.videos and channel.get("uploads_playlist_id"):
            video_ids = collect_video_ids(service, channel["uploads_playlist_id"], args.videos)
            if video_ids:
                videos = fetch_videos(service, video_ids, args.full_descriptions)
            else:
                warnings.append("The uploads playlist is empty or returned no items.")
        elif args.videos:
            warnings.append("This channel exposes no uploads playlist, so no videos were fetched.")

        quota_state = quota_tracker.snapshot()
        if quota_state.get("warning"):
            warnings.append(quota_state["warning"])

        payload = {
            "ok": True,
            "channel": channel,
            "videos": videos,
            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "quota": {
                "method": "uploads-playlist path (no search.list)",
                "estimated_units": estimate,
                "remaining_today": quota_state["remaining"],
            },
            "data_scope": "public only -- retention, impressions, CTR and revenue are not in the Data API",
        }
        if not args.no_summary:
            payload["summary"] = summarize(videos)
        if warnings:
            payload["warnings"] = warnings

        emit(payload)

    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
