"""
YouTube Data API v3 quota ledger.

The Data API grants a fixed number of units per day and refuses every call once
they are gone. One careless loop of ``search.list`` burns the whole day. This
module keeps a small ledger so a script can answer three questions before it
spends anything:

    Can I afford this call?  How much is left?  Should I warn the creator first?

Headline quota figures (10,000 units/day, midnight-Pacific reset, search.list at
100 units, most reads at 1-5) are stated in ``references/benchmarks.md`` §10 --
that file is the single source of truth for numbers the matrix *cites*. The table
below is the operational cost list the code *spends against*; it mirrors Google's
published per-call costs and is the one place such constants live in code.

The ledger is a single JSON file in the user's config directory -- never in the
plugin folder. It holds no credentials: a date, a running total, per-operation
counts, and up to a week of history.

    $XDG_CONFIG_HOME/youtube-agent-matrix/quota-ledger.json

Usage:
    python execution/utils/quota_tracker.py --check
    python execution/utils/quota_tracker.py --can-afford search.list
    python execution/utils/quota_tracker.py --can-afford videos.list --count 4
    python execution/utils/quota_tracker.py --record playlistItems.list --count 3
    python execution/utils/quota_tracker.py --costs
    python execution/utils/quota_tracker.py --reset

Exit code is 0 when the requested operation fits in the remaining budget, 1 when
it does not. Output is JSON on stdout in both cases.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

DAILY_QUOTA_UNITS = 10000
WARN_AT_FRACTION = 0.80          # warn once this share of the day's budget is gone
EXPENSIVE_CALL_UNITS = 100       # a single call at or above this deserves a warning
HISTORY_DAYS = 7

LEDGER_FILENAME = "quota-ledger.json"
CONFIG_HOME_ENV = "YOUTUBE_AGENT_MATRIX_HOME"
CONFIG_DIR_NAME = "youtube-agent-matrix"

# Published per-call unit costs for the Data API v3 operations this plugin uses.
OPERATION_COSTS = {
    "search.list": 100,
    "captions.download": 200,
    "captions.list": 50,
    "channels.list": 1,
    "playlistItems.list": 1,
    "playlists.list": 1,
    "videos.list": 1,
    "commentThreads.list": 1,
    "comments.list": 1,
    "videoCategories.list": 1,
    "channelSections.list": 1,
    "i18nLanguages.list": 1,
    "i18nRegions.list": 1,
}

DEFAULT_UNKNOWN_COST = 1

CHEAPER_ALTERNATIVE = {
    "search.list": (
        "To list one channel's videos, use fetch_channel_data.py instead -- the "
        "uploads-playlist path (channels.list + playlistItems.list + videos.list) "
        "returns the same data for a handful of units."
    ),
}


# --------------------------------------------------------------------------- #
# Paths and clock
# --------------------------------------------------------------------------- #

def _config_dir():
    override = os.environ.get(CONFIG_HOME_ENV, "").strip()
    if override:
        return Path(override).expanduser()
    xdg = os.environ.get("XDG_CONFIG_HOME", "").strip()
    base = Path(xdg).expanduser() if xdg else Path.home() / ".config"
    return base / CONFIG_DIR_NAME


def ledger_path():
    return _config_dir() / LEDGER_FILENAME


def pacific_date():
    """Today's date in US/Pacific -- the day boundary the quota resets on."""
    try:
        from zoneinfo import ZoneInfo  # noqa: WPS433 -- stdlib, 3.9+

        now = datetime.now(ZoneInfo("America/Los_Angeles"))
    except Exception:  # noqa: BLE001 -- no tz database: fall back to a fixed offset
        now = datetime.now(timezone.utc) - timedelta(hours=8)
    return now.strftime("%Y-%m-%d")


def seconds_until_reset():
    """Seconds until the next midnight-Pacific reset."""
    try:
        from zoneinfo import ZoneInfo  # noqa: WPS433

        tz = ZoneInfo("America/Los_Angeles")
        now = datetime.now(tz)
    except Exception:  # noqa: BLE001
        tz = timezone(timedelta(hours=-8))
        now = datetime.now(timezone.utc).astimezone(tz)
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    return int((midnight - now).total_seconds())


def _hours_minutes(seconds):
    return f"{seconds // 3600}h {(seconds % 3600) // 60}m"


# --------------------------------------------------------------------------- #
# Ledger I/O
# --------------------------------------------------------------------------- #

def _blank(date):
    return {"date": date, "consumed": 0, "operations": {}}


def _load():
    """Load the ledger, rolling it over when the Pacific date has changed."""
    today = pacific_date()
    path = ledger_path()
    if not path.exists():
        return {"current": _blank(today), "history": []}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 -- a corrupt ledger must never break a fetch
        return {"current": _blank(today), "history": []}

    current = data.get("current") or _blank(today)
    history = data.get("history") or []

    if current.get("date") != today:
        if current.get("consumed"):
            history.insert(0, current)
        history = history[:HISTORY_DAYS]
        current = _blank(today)

    current.setdefault("operations", {})
    current.setdefault("consumed", 0)
    return {"current": current, "history": history}


def _save(data):
    path = ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp.replace(path)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def cost_of(operation, count=1):
    """Unit cost of running `operation` `count` times."""
    return OPERATION_COSTS.get(operation, DEFAULT_UNKNOWN_COST) * max(int(count), 0)


def remaining():
    """Units left in today's budget."""
    return max(DAILY_QUOTA_UNITS - _load()["current"]["consumed"], 0)


def snapshot():
    """Current quota state, with a warning field once the budget runs low."""
    data = _load()["current"]
    consumed = data["consumed"]
    left = max(DAILY_QUOTA_UNITS - consumed, 0)
    used_fraction = consumed / DAILY_QUOTA_UNITS if DAILY_QUOTA_UNITS else 1.0

    result = {
        "date_pacific": data["date"],
        "daily_quota": DAILY_QUOTA_UNITS,
        "consumed": consumed,
        "remaining": left,
        "used_percent": round(used_fraction * 100, 1),
        "resets_in": _hours_minutes(seconds_until_reset()),
        "operations": dict(sorted(data["operations"].items())),
        "ledger": str(ledger_path()),
    }
    if used_fraction >= WARN_AT_FRACTION:
        result["warning"] = (
            f"{result['used_percent']}% of today's quota is gone -- {left} units left, "
            f"resetting in {result['resets_in']}. Prefer the manual fallbacks in "
            "references/data-sources.md until then."
        )
    return result


def can_afford(operation, count=1):
    """
    Decide whether an operation fits in the remaining budget.

    Returns a dict with `allowed`, `cost`, `remaining`, and -- when the call is
    expensive or the budget is low -- a human-readable `warning`.
    """
    state = snapshot()
    cost = cost_of(operation, count)
    left = state["remaining"]

    result = {
        "operation": operation,
        "count": count,
        "cost": cost,
        "remaining": left,
        "remaining_after": max(left - cost, 0),
        "daily_quota": DAILY_QUOTA_UNITS,
        "used_percent": state["used_percent"],
        "resets_in": state["resets_in"],
        "allowed": cost <= left,
    }

    if operation not in OPERATION_COSTS:
        result["note"] = (
            f"Unknown operation '{operation}'; assuming {DEFAULT_UNKNOWN_COST} unit per call."
        )

    warnings = []
    if cost >= EXPENSIVE_CALL_UNITS:
        share = round(cost / DAILY_QUOTA_UNITS * 100, 1)
        warnings.append(
            f"EXPENSIVE: {operation} x{count} costs {cost} units -- {share}% of the entire day."
        )
        if operation in CHEAPER_ALTERNATIVE:
            warnings.append(CHEAPER_ALTERNATIVE[operation])
    if state.get("warning"):
        warnings.append(state["warning"])
    if warnings:
        result["warning"] = " ".join(warnings)

    if not result["allowed"]:
        result["error"] = (
            f"{operation} x{count} needs {cost} units but only {left} remain today. "
            f"Quota resets in {state['resets_in']}."
        )
        result["fallback"] = "references/data-sources.md §2 -- ask the creator for the numbers instead."

    return result


def record(operation, count=1):
    """Record consumption after a call succeeded. Returns the updated state."""
    cost = cost_of(operation, count)
    data = _load()
    current = data["current"]
    current["consumed"] += cost
    current["operations"][operation] = current["operations"].get(operation, 0) + int(count)
    try:
        _save(data)
    except OSError as exc:
        # A ledger that cannot be written is a bookkeeping problem, not a fetch problem.
        return {
            "operation": operation,
            "count": count,
            "units_consumed": cost,
            "warning": f"Quota ledger could not be written ({exc}). Tracking is degraded this run.",
        }

    state = snapshot()
    result = {
        "operation": operation,
        "count": count,
        "units_consumed": cost,
        "consumed_today": state["consumed"],
        "remaining": state["remaining"],
        "used_percent": state["used_percent"],
    }
    if state.get("warning"):
        result["warning"] = state["warning"]
    return result


def reset():
    """Clear today's counter. Testing and recovery only."""
    data = _load()
    data["current"] = _blank(pacific_date())
    _save(data)
    return {"reset": True, "date_pacific": data["current"]["date"], "remaining": DAILY_QUOTA_UNITS}


def costs_table():
    return {
        "daily_quota": DAILY_QUOTA_UNITS,
        "expensive_threshold": EXPENSIVE_CALL_UNITS,
        "warn_at_percent": int(WARN_AT_FRACTION * 100),
        "operation_costs": dict(sorted(OPERATION_COSTS.items(), key=lambda kv: (-kv[1], kv[0]))),
        "unknown_operation_cost": DEFAULT_UNKNOWN_COST,
        "note": "Headline quota figures are cited from references/benchmarks.md §10.",
    }


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser(
        description="Track YouTube Data API v3 quota against the daily unit budget. "
                    "Outputs JSON on stdout.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exit 0 when the checked operation fits in the remaining budget, 1 when it does not.\n"
            "The ledger lives in the user config directory, never in the plugin folder."
        ),
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--check", action="store_true", help="Show today's quota state.")
    group.add_argument("--can-afford", metavar="OPERATION",
                       help="Check whether an operation fits in the remaining budget.")
    group.add_argument("--record", metavar="OPERATION",
                       help="Record units consumed by an operation that already ran.")
    group.add_argument("--costs", action="store_true", help="Print the per-operation cost table.")
    group.add_argument("--reset", action="store_true", help="Clear today's counter (testing only).")
    parser.add_argument("--count", type=int, default=1, help="Number of calls (default: 1).")
    args = parser.parse_args()

    if args.count < 0:
        print(json.dumps({"ok": False, "error": {
            "code": "input_invalid", "message": "--count must be zero or greater."}}, indent=2))
        sys.exit(1)

    exit_code = 0
    if args.reset:
        payload = reset()
    elif args.costs:
        payload = costs_table()
    elif args.can_afford:
        payload = can_afford(args.can_afford, args.count)
        exit_code = 0 if payload["allowed"] else 1
    elif args.record:
        payload = record(args.record, args.count)
    elif args.check:
        payload = snapshot()
    else:
        parser.print_help()
        return

    payload.setdefault("ok", exit_code == 0)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
