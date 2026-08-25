"""
Pull private YouTube Analytics for a channel the creator owns.

This is the only script in the matrix that can see the numbers an audit or an
analytics report actually needs: impressions and click-through rate, average view
duration and percentage, watch time, subscribers gained and lost, where the traffic
came from, and revenue when the channel is monetized.

**OAuth only, own channel only.** There is no path -- through this API or any other
-- to a competitor's retention, CTR or revenue. If someone asks for a competitor's
private metrics, the honest answer is that they are not obtainable.

When OAuth is not configured, this script does not fail vaguely: it exits with a
JSON error that names the exact YouTube Studio screens to screenshot and the exact
numbers to paste, so the analysis continues without it. Missing analytics degrades
the deliverable; it never blocks it.

Metric availability varies by channel, video type and date range. Rather than fail
the whole query when one metric is unsupported, this script retries with the
unsupported metric dropped and reports what it could not get in
``unavailable_metrics``.

Credentials: OAuth client secret path from ``YOUTUBE_OAUTH_CLIENT_SECRET`` (or the
user config dir), token cached in the user config dir. Never in the plugin folder.
Authorise once with ``python execution/utils/youtube_auth.py --authorize``.

Usage:
    python execution/fetch_video_analytics.py --days 28                 # whole channel
    python execution/fetch_video_analytics.py VIDEO_ID --days 90
    python execution/fetch_video_analytics.py VID1 VID2 --start 2026-01-01 --end 2026-03-31
    python execution/fetch_video_analytics.py VIDEO_ID --daily --revenue
    python execution/fetch_video_analytics.py --days 28 --no-traffic-sources

Exit 0 with ``{"ok": true, ...}``; exit 1 with ``{"ok": false, "error": {...}}``.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils.youtube_auth import (  # noqa: E402
    ExecutionError,
    InputInvalid,
    build_analytics_client,
    die,
    emit,
    explain_api_error,
    install_excepthook,
    resolve_owned_channel_id,
)

# Ordered by how much the matrix relies on them: the first four are the backbone of
# every diagnosis, the rest are dropped first if the API rejects them.
CORE_METRICS = [
    "views",
    "estimatedMinutesWatched",
    "averageViewDuration",
    "averageViewPercentage",
    "engagedViews",
    "impressions",
    "impressionClickThroughRate",
    "subscribersGained",
    "subscribersLost",
    "likes",
    "dislikes",
    "shares",
    "comments",
]

REQUIRED_METRICS = {"views", "estimatedMinutesWatched"}

REVENUE_METRICS = [
    "estimatedRevenue",
    "estimatedAdRevenue",
    "grossRevenue",
    "cpm",
    "playbackBasedCpm",
    "monetizedPlaybacks",
]

TRAFFIC_METRICS = ["views", "estimatedMinutesWatched", "averageViewDuration"]
DAILY_METRICS = ["views", "estimatedMinutesWatched", "subscribersGained", "subscribersLost"]

MAX_RESULTS = 200

STUDIO_FALLBACK = {
    "why": "Private analytics require OAuth for the channel that owns the videos.",
    "ask_the_creator_for": [
        "Studio > Analytics > Overview, last 28 days: views, watch time (hours), "
        "average view duration, impressions, and impressions click-through rate.",
        "Studio > Analytics > Content > 'How viewers find you': the traffic-source "
        "breakdown, top 5 sources with percentages.",
        "Studio > Analytics > Audience: returning vs new viewers, and the top 5 "
        "countries with percentages.",
        "For a single video: open it > Analytics > Engagement -- a screenshot of the "
        "retention curve, plus retention at 30 seconds and the timestamp of the "
        "biggest drop-off.",
        "If monetized: Studio > Analytics > Revenue -- RPM and estimated revenue for "
        "the same date range.",
    ],
    "note": "A screenshot of the retention curve is worth more than any single number. "
            "Date every pasted figure -- an undated metric is unusable in three weeks.",
    "reference": "references/data-sources.md §3",
}


# --------------------------------------------------------------------------- #
# Dates
# --------------------------------------------------------------------------- #

def parse_date(value, label):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise InputInvalid(
            f"{label} must be in YYYY-MM-DD format, got '{value}'.",
            fix=["Example: --start 2026-01-01 --end 2026-01-28"],
        )


def resolve_range(args):
    today = date.today()
    if args.start or args.end:
        if not (args.start and args.end):
            raise InputInvalid(
                "--start and --end must be used together.",
                fix=["Pass both, or use --days N instead."],
            )
        start = parse_date(args.start, "--start")
        end = parse_date(args.end, "--end")
    else:
        end = today - timedelta(days=1)   # today's data is incomplete
        start = end - timedelta(days=max(args.days, 1) - 1)

    if start > end:
        raise InputInvalid("--start is after --end.", fix=["Swap the two dates."])
    return start.isoformat(), end.isoformat()


# --------------------------------------------------------------------------- #
# Querying, with metric-by-metric degradation
# --------------------------------------------------------------------------- #

def _rows_to_dicts(response):
    headers = [h["name"] for h in response.get("columnHeaders", [])]
    return [dict(zip(headers, row)) for row in response.get("rows", [])]


def _unsupported_metrics(message, candidates):
    """Pick the metric names the API complained about out of its error message."""
    lowered = (message or "").lower()
    return [m for m in candidates if m.lower() in lowered]


def query(service, channel_id, metrics, start, end, dimensions=None, filters=None,
          sort=None, required=None, max_drops=6):
    """
    Run an Analytics query, dropping metrics the API refuses rather than failing.

    Returns (rows, used_metrics, dropped_metrics).
    """
    required = required or set()
    metrics = list(metrics)
    dropped = []

    for _ in range(max_drops + 1):
        params = {
            "ids": f"channel=={channel_id}",
            "startDate": start,
            "endDate": end,
            "metrics": ",".join(metrics),
            "maxResults": MAX_RESULTS,
        }
        if dimensions:
            params["dimensions"] = dimensions
        if filters:
            params["filters"] = filters
        if sort:
            params["sort"] = sort

        try:
            response = service.reports().query(**params).execute()
            return _rows_to_dicts(response), metrics, dropped
        except Exception as exc:  # noqa: BLE001 -- degrade, do not crash
            err = explain_api_error(exc)
            message = err.message
            bad = [m for m in _unsupported_metrics(message, metrics) if m not in required]
            if not bad:
                # Nothing named: drop the least essential remaining metric and retry once more.
                optional = [m for m in metrics if m not in required]
                if not optional:
                    raise err
                bad = [optional[-1]]
            metrics = [m for m in metrics if m not in bad]
            dropped.extend(bad)
            if not metrics:
                raise err

    return [], metrics, dropped


def video_filter(video_ids):
    return f"video=={','.join(video_ids)}" if video_ids else None


# --------------------------------------------------------------------------- #
# Report assembly
# --------------------------------------------------------------------------- #

def build_report(service, channel_id, video_ids, start, end, args):
    filters = video_filter(video_ids)
    dimensions = "video" if video_ids else None
    unavailable = []

    rows, used, dropped = query(
        service, channel_id, CORE_METRICS, start, end,
        dimensions=dimensions, filters=filters, required=REQUIRED_METRICS,
    )
    unavailable.extend(dropped)

    report = {
        "scope": "video" if video_ids else "channel",
        "metrics_returned": used,
        "rows": rows,
    }

    sections = {}

    if args.traffic_sources:
        try:
            traffic_rows, _, traffic_dropped = query(
                service, channel_id, TRAFFIC_METRICS, start, end,
                dimensions="insightTrafficSourceType", filters=filters,
                required=REQUIRED_METRICS,
            )
            total = sum(r.get("views", 0) for r in traffic_rows) or 0
            for row in traffic_rows:
                row["share_of_views_pct"] = (
                    round(row.get("views", 0) / total * 100, 1) if total else None
                )
            traffic_rows.sort(key=lambda r: r.get("views", 0), reverse=True)
            sections["traffic_sources"] = traffic_rows
            unavailable.extend(traffic_dropped)
        except ExecutionError as err:
            sections["traffic_sources"] = {"unavailable": err.message}

    if args.daily:
        try:
            daily_rows, _, daily_dropped = query(
                service, channel_id, DAILY_METRICS, start, end,
                dimensions="day", filters=filters, sort="day", required=REQUIRED_METRICS,
            )
            sections["daily"] = daily_rows
            unavailable.extend(daily_dropped)
        except ExecutionError as err:
            sections["daily"] = {"unavailable": err.message}

    if args.geography:
        try:
            geo_rows, _, geo_dropped = query(
                service, channel_id, ["views", "estimatedMinutesWatched"], start, end,
                dimensions="country", filters=filters, sort="-views", required=REQUIRED_METRICS,
            )
            sections["geography"] = geo_rows[:15]
            unavailable.extend(geo_dropped)
        except ExecutionError as err:
            sections["geography"] = {"unavailable": err.message}

    if args.revenue:
        try:
            revenue_rows, revenue_used, revenue_dropped = query(
                service, channel_id, REVENUE_METRICS, start, end,
                dimensions=dimensions, filters=filters,
            )
            sections["revenue"] = {"metrics_returned": revenue_used, "rows": revenue_rows}
            if revenue_dropped:
                sections["revenue"]["unavailable_metrics"] = revenue_dropped
        except ExecutionError as err:
            sections["revenue"] = {
                "unavailable": err.message,
                "likely_causes": [
                    "The channel is not in the YouTube Partner Programme.",
                    "The monetary Analytics scope was not granted -- re-run "
                    "'python execution/utils/youtube_auth.py --authorize --revenue'.",
                    "The date range predates monetization.",
                ],
                "fallback": "Ask for Studio > Analytics > Revenue: RPM and estimated revenue "
                            "for the same range.",
            }

    report["sections"] = sections
    if unavailable:
        report["unavailable_metrics"] = sorted(set(unavailable))
        report["unavailable_note"] = (
            "These metrics were refused for this channel, video type or date range. "
            "Everything else in this report is complete."
        )
    return report


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main():
    install_excepthook()
    parser = argparse.ArgumentParser(
        description="Fetch private YouTube Analytics for a channel you own (OAuth). "
                    "Outputs JSON on stdout.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Own channel only. Competitor retention, CTR and revenue are not obtainable\n"
            "through any official API -- do not promise them.\n\n"
            "First-time setup: python execution/utils/youtube_auth.py --authorize"
        ),
    )
    parser.add_argument("video_ids", nargs="*",
                        help="Video IDs to report on. Omit for channel-level totals.")
    parser.add_argument("--days", type=int, default=28,
                        help="Look back this many days, ending yesterday (default: 28).")
    parser.add_argument("--start", help="Range start, YYYY-MM-DD (use with --end).")
    parser.add_argument("--end", help="Range end, YYYY-MM-DD (use with --start).")
    parser.add_argument("--daily", action="store_true",
                        help="Add a day-by-day breakdown for trend reading.")
    parser.add_argument("--geography", action="store_true",
                        help="Add a per-country breakdown (drives localization decisions).")
    parser.add_argument("--revenue", action="store_true",
                        help="Add revenue metrics. Needs the monetary scope and a monetized channel.")
    parser.add_argument("--no-traffic-sources", dest="traffic_sources", action="store_false",
                        help="Skip the traffic-source breakdown (included by default).")
    parser.set_defaults(traffic_sources=True)
    args = parser.parse_args()

    try:
        start, end = resolve_range(args)

        try:
            service, creds = build_analytics_client(include_revenue=args.revenue)
        except ExecutionError as err:
            # No OAuth, no dependency, no consent -- all the same to the workflow:
            # the analysis continues from Studio numbers instead.
            die(err, extra={"fallback": STUDIO_FALLBACK})

        channel_id, channel_title = resolve_owned_channel_id(creds)
        report = build_report(service, channel_id, args.video_ids, start, end, args)

        emit({
            "ok": True,
            "channel": {"channel_id": channel_id, "title": channel_title},
            "date_range": {"start": start, "end": end},
            "video_ids": args.video_ids or None,
            "report": report,
            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "note": "Private analytics for the authenticated owner only. "
                    "Competitor equivalents are not obtainable.",
        })

    except InputInvalid as err:
        die(err)
    except ExecutionError as err:
        die(err, extra={"fallback": STUDIO_FALLBACK})


if __name__ == "__main__":
    main()
