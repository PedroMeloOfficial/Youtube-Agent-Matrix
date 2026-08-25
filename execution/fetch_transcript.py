"""
Fetch a video's captions as timed segments.

A transcript is the cheapest high-value input the matrix has: it feeds retention
analysis, repurposing, competitor teardowns and chapter generation without costing
a single quota unit on the public path.

Three methods are tried in order, cheapest and least privileged first:

  1. **Public caption track** -- read the video's player response over HTTPS and
     download the caption track it advertises. No credentials, no quota.
  2. **External extractor** -- if a caption extractor such as ``yt-dlp`` happens to
     be on PATH, use it. Optional; never installed or required by this plugin.
  3. **Owner captions via OAuth** -- ``--owned`` downloads the caption track through
     the Data API for a video on the creator's own channel. This is the only method
     that works when captions are owner-restricted, and it costs quota.

When every method fails, the output says *why* -- captions absent, disabled,
restricted, or the requested language missing -- and names the manual fallback:
open the video, use the transcript panel under the description, paste it in. A
missing transcript slows a workflow down; it never stops one.

Usage:
    python execution/fetch_transcript.py VIDEO_ID
    python execution/fetch_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
    python execution/fetch_transcript.py VIDEO_ID --lang pt --format text
    python execution/fetch_transcript.py VIDEO_ID --list-languages
    python execution/fetch_transcript.py VIDEO_ID --owned          # own channel, OAuth

Exit 0 with ``{"ok": true, ...}``; exit 1 with ``{"ok": false, "error": {...}}``.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import quota_tracker  # noqa: E402
from utils.youtube_auth import (  # noqa: E402
    ApiCallFailed,
    ExecutionError,
    InputInvalid,
    build_data_client_oauth,
    die,
    emit,
    explain_api_error,
    install_excepthook,
    load_oauth_credentials,
)

VIDEO_ID_RE = re.compile(r"^[\w-]{11}$")
URL_ID_RE = re.compile(
    r"(?:youtube\.com/(?:watch\?(?:.*&)?v=|shorts/|embed/|live/)|youtu\.be/)([\w-]{11})"
)
PLAYER_RESPONSE_RE = re.compile(r"ytInitialPlayerResponse\s*=\s*(\{.+?\})\s*;\s*(?:var|</script>)", re.S)

USER_AGENT = "Mozilla/5.0 (compatible; youtube-agent-matrix/1.0)"
HTTP_TIMEOUT = 20
EXTRACTOR_TIMEOUT = 45

MANUAL_FALLBACK = [
    "Open the video, click '...more' under the description, then 'Show transcript'.",
    "Copy the transcript panel and paste it into the conversation.",
    "For the creator's own video: Studio > Subtitles > the language > Edit as text.",
]


# --------------------------------------------------------------------------- #
# Input
# --------------------------------------------------------------------------- #

def parse_video_id(raw):
    value = (raw or "").strip()
    if not value:
        raise InputInvalid("No video given.", fix=["Pass a video ID or a YouTube URL."])
    if VIDEO_ID_RE.match(value):
        return value
    match = URL_ID_RE.search(value)
    if match:
        return match.group(1)
    raise InputInvalid(
        f"Could not read an 11-character video ID out of '{value}'.",
        fix=["Pass the ID itself, or a URL of the form youtube.com/watch?v=... or youtu.be/..."],
    )


# --------------------------------------------------------------------------- #
# Method 1 -- public caption track
# --------------------------------------------------------------------------- #

def _http_get(url, headers=None):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9", **(headers or {})},
    )
    with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as response:  # noqa: S310
        return response.read().decode("utf-8", "replace")


def list_public_tracks(video_id):
    """Return the caption tracks the watch page advertises, or raise a typed error."""
    url = f"https://www.youtube.com/watch?v={video_id}&hl=en"
    try:
        html = _http_get(url)
    except urllib.error.HTTPError as exc:
        raise ApiCallFailed(
            f"YouTube returned HTTP {exc.code} for that video page.",
            fix=["Check the video ID and that the video is public.", *MANUAL_FALLBACK],
        )
    except Exception as exc:  # noqa: BLE001 -- offline, blocked, DNS, TLS
        raise ApiCallFailed(
            f"Could not reach the video page: {exc}",
            fix=["Check network access.", *MANUAL_FALLBACK],
        )

    match = PLAYER_RESPONSE_RE.search(html)
    if not match:
        raise ApiCallFailed(
            "The video page did not include a readable player response.",
            fix=["YouTube may be serving a consent or bot-check page from this network.",
                 *MANUAL_FALLBACK],
        )

    try:
        player = json.loads(match.group(1))
    except json.JSONDecodeError:
        raise ApiCallFailed(
            "The player response could not be parsed.",
            fix=MANUAL_FALLBACK,
        )

    status = player.get("playabilityStatus", {}).get("status")
    if status and status not in ("OK", "LIVE_STREAM_OFFLINE"):
        reason = player.get("playabilityStatus", {}).get("reason", "")
        raise ApiCallFailed(
            f"The video is not publicly playable ({status}). {reason}".strip(),
            fix=["If it is the creator's own video, retry with --owned.", *MANUAL_FALLBACK],
        )

    tracks = (
        player.get("captions", {})
        .get("playerCaptionsTracklistRenderer", {})
        .get("captionTracks", [])
    )
    return [
        {
            "language_code": track.get("languageCode"),
            "name": (track.get("name", {}).get("simpleText")
                     or track.get("name", {}).get("runs", [{}])[0].get("text")),
            "auto_generated": track.get("kind") == "asr",
            "is_translatable": bool(track.get("isTranslatable")),
            "base_url": track.get("baseUrl"),
        }
        for track in tracks
        if track.get("baseUrl")
    ]


def pick_track(tracks, lang):
    """Prefer an exact language match, then a prefix match, then a human track, then anything."""
    if not tracks:
        return None
    if lang:
        exact = [t for t in tracks if (t["language_code"] or "").lower() == lang.lower()]
        prefix = [t for t in tracks if (t["language_code"] or "").lower().startswith(lang.lower()[:2])]
        for pool in (exact, prefix):
            if pool:
                manual = [t for t in pool if not t["auto_generated"]]
                return (manual or pool)[0]
        return None
    manual = [t for t in tracks if not t["auto_generated"]]
    return (manual or tracks)[0]


def download_track(track):
    """Download a caption track as json3 and parse it into timed segments."""
    separator = "&" if "?" in track["base_url"] else "?"
    url = f"{track['base_url']}{separator}fmt=json3"
    try:
        body = _http_get(url)
    except Exception as exc:  # noqa: BLE001
        raise ApiCallFailed(
            f"The caption track could not be downloaded: {exc}",
            fix=MANUAL_FALLBACK,
        )
    return parse_json3(body)


def parse_json3(body):
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return parse_timedtext_xml(body)

    segments = []
    for event in data.get("events", []):
        pieces = event.get("segs") or []
        text = "".join(piece.get("utf8", "") for piece in pieces).strip()
        if not text:
            continue
        start = (event.get("tStartMs") or 0) / 1000.0
        duration = (event.get("dDurationMs") or 0) / 1000.0
        segments.append(make_segment(start, duration, text))
    return segments


def parse_timedtext_xml(body):
    segments = []
    for match in re.finditer(
        r'<text start="([\d.]+)"(?: dur="([\d.]+)")?[^>]*>(.*?)</text>', body, re.S
    ):
        start = float(match.group(1))
        duration = float(match.group(2) or 0)
        text = unescape_caption(match.group(3))
        if text:
            segments.append(make_segment(start, duration, text))
    return segments


# --------------------------------------------------------------------------- #
# Method 2 -- optional external extractor
# --------------------------------------------------------------------------- #

def fetch_via_extractor(video_id, lang):
    """Use yt-dlp if it is already installed. Returns (segments, error_message)."""
    binary = shutil.which("yt-dlp")
    if not binary:
        return None, "yt-dlp is not installed (optional)"

    url = f"https://www.youtube.com/watch?v={video_id}"
    with tempfile.TemporaryDirectory() as tmp:
        command = [
            binary, "--skip-download", "--write-subs", "--write-auto-subs",
            "--sub-langs", f"{lang}.*,{lang}", "--sub-format", "vtt/srt",
            "--output", str(Path(tmp) / "captions"), url,
        ]
        try:
            completed = subprocess.run(  # noqa: S603 -- fixed binary, no shell
                command, capture_output=True, text=True, timeout=EXTRACTOR_TIMEOUT
            )
        except subprocess.TimeoutExpired:
            return None, f"yt-dlp timed out after {EXTRACTOR_TIMEOUT}s"
        except OSError as exc:
            return None, f"yt-dlp could not be run: {exc}"

        for path in sorted(Path(tmp).glob("*.vtt")):
            return parse_vtt(path.read_text(encoding="utf-8", errors="replace")), None
        for path in sorted(Path(tmp).glob("*.srt")):
            return parse_srt(path.read_text(encoding="utf-8", errors="replace")), None

        detail = (completed.stderr or "").strip().splitlines()
        return None, detail[-1][:200] if detail else "yt-dlp produced no subtitle file"


# --------------------------------------------------------------------------- #
# Method 3 -- owner captions via OAuth
# --------------------------------------------------------------------------- #

def fetch_via_oauth(video_id, lang):
    """Download a caption track for a video on the authenticated user's own channel."""
    creds = load_oauth_credentials(include_revenue=False, allow_browser=True)
    service = build_data_client_oauth(creds)

    try:
        listed = service.captions().list(part="snippet", videoId=video_id).execute()
    except Exception as exc:  # noqa: BLE001
        raise explain_api_error(exc)
    quota_tracker.record("captions.list")

    items = listed.get("items", [])
    if not items:
        raise ApiCallFailed(
            "The Data API reports no caption tracks on that video.",
            fix=["Confirm the video belongs to the authorised channel.",
                 "Upload or auto-generate captions in Studio > Subtitles.", *MANUAL_FALLBACK],
        )

    def score(item):
        snippet = item.get("snippet", {})
        code = (snippet.get("language") or "").lower()
        return (
            0 if lang and code == lang.lower() else 1 if lang and code.startswith(lang[:2].lower()) else 2,
            0 if snippet.get("trackKind") != "ASR" else 1,
        )

    chosen = sorted(items, key=score)[0]
    budget = quota_tracker.can_afford("captions.download")
    if not budget["allowed"]:
        raise ApiCallFailed(budget["error"], fix=MANUAL_FALLBACK, details={"quota": budget})

    try:
        body = service.captions().download(id=chosen["id"], tfmt="srt").execute()
    except Exception as exc:  # noqa: BLE001
        raise explain_api_error(exc)
    quota_tracker.record("captions.download")

    text = body.decode("utf-8", "replace") if isinstance(body, bytes) else str(body)
    return parse_srt(text), chosen.get("snippet", {})


# --------------------------------------------------------------------------- #
# Caption parsing helpers
# --------------------------------------------------------------------------- #

def unescape_caption(raw):
    text = re.sub(r"<[^>]+>", "", raw)
    replacements = {
        "&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"',
        "&#39;": "'", "&apos;": "'", "&nbsp;": " ",
    }
    # YouTube's timedtext XML double-escapes entities (&amp;#39; for an apostrophe),
    # so run the substitution twice.
    for _ in range(2):
        for needle, replacement in replacements.items():
            text = text.replace(needle, replacement)
    return re.sub(r"\s+", " ", text).strip()


def timestamp(seconds):
    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes}:{secs:02d}"


def make_segment(start, duration, text):
    return {
        "start": round(start, 2),
        "duration": round(duration, 2),
        "timestamp": timestamp(start),
        "text": text,
    }


def _clock_to_seconds(clock):
    clock = clock.replace(",", ".")
    parts = clock.split(":")
    seconds = 0.0
    for part in parts:
        seconds = seconds * 60 + float(part)
    return seconds


def _parse_cue_blocks(content, pattern):
    segments = []
    for block in re.split(r"\n\s*\n", content.strip()):
        lines = [line for line in block.strip().splitlines() if line.strip()]
        if not lines:
            continue
        cue_index = next((i for i, line in enumerate(lines) if pattern.search(line)), None)
        if cue_index is None:
            continue
        match = pattern.search(lines[cue_index])
        start = _clock_to_seconds(match.group(1))
        end = _clock_to_seconds(match.group(2))
        text = unescape_caption(" ".join(lines[cue_index + 1:]))
        if text:
            segments.append(make_segment(start, max(end - start, 0), text))
    return dedupe(segments)


VTT_CUE = re.compile(r"((?:\d+:)?\d{2}:\d{2}[.,]\d{3})\s*-->\s*((?:\d+:)?\d{2}:\d{2}[.,]\d{3})")


def parse_vtt(content):
    return _parse_cue_blocks(content, VTT_CUE)


def parse_srt(content):
    return _parse_cue_blocks(content, VTT_CUE)


def dedupe(segments):
    """Auto-generated captions repeat the rolling line; collapse consecutive duplicates."""
    result = []
    for segment in segments:
        if result and result[-1]["text"] == segment["text"]:
            continue
        result.append(segment)
    return result


def to_plain_text(segments):
    return " ".join(segment["text"] for segment in segments).strip()


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main():
    install_excepthook()
    parser = argparse.ArgumentParser(
        description="Fetch a video's captions as timed segments. Outputs JSON on stdout.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "The public path costs no quota and needs no credentials.\n"
            "When captions are absent or restricted, the JSON error names the manual fallback."
        ),
    )
    parser.add_argument("video", help="Video ID or YouTube URL.")
    parser.add_argument("--lang", default="en",
                        help="Preferred caption language code (default: en). Use --lang '' for any.")
    parser.add_argument("--format", choices=["segments", "text", "both"], default="both",
                        help="What to include in the output (default: both).")
    parser.add_argument("--list-languages", action="store_true",
                        help="List the available caption tracks and exit.")
    parser.add_argument("--owned", action="store_true",
                        help="Use OAuth to download captions from your own channel (costs quota).")
    parser.add_argument("--no-extractor", action="store_true",
                        help="Skip the optional external extractor step.")
    args = parser.parse_args()

    try:
        video_id = parse_video_id(args.video)
        lang = args.lang.strip()
        attempts = []

        if args.list_languages:
            tracks = list_public_tracks(video_id)
            emit({
                "ok": True,
                "video_id": video_id,
                "tracks": [{k: v for k, v in t.items() if k != "base_url"} for t in tracks],
                "track_count": len(tracks),
            })

        # Method 1 -- public track, no credentials, no quota.
        tracks = []
        try:
            tracks = list_public_tracks(video_id)
            if tracks:
                track = pick_track(tracks, lang)
                if track is None:
                    available = ", ".join(sorted({t["language_code"] for t in tracks if t["language_code"]}))
                    attempts.append({"method": "public-captions",
                                     "error": f"No '{lang}' track. Available: {available}"})
                else:
                    segments = download_track(track)
                    if segments:
                        result = {
                            "ok": True,
                            "video_id": video_id,
                            "source": "public-captions",
                            "language": track["language_code"],
                            "track_name": track["name"],
                            "auto_generated": track["auto_generated"],
                            "segment_count": len(segments),
                            "duration_seconds": round(
                                segments[-1]["start"] + segments[-1]["duration"], 1),
                            "available_languages": sorted(
                                {t["language_code"] for t in tracks if t["language_code"]}),
                            "quota_units_used": 0,
                            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                        }
                        if args.format in ("segments", "both"):
                            result["segments"] = segments
                        if args.format in ("text", "both"):
                            result["text"] = to_plain_text(segments)
                        emit(result)
                    attempts.append({"method": "public-captions", "error": "Track downloaded but empty."})
            else:
                attempts.append({"method": "public-captions",
                                 "error": "The video advertises no caption tracks."})
        except ExecutionError as err:
            attempts.append({"method": "public-captions", "error": err.message})

        # Method 2 -- optional local extractor.
        if not args.no_extractor:
            segments, error = fetch_via_extractor(video_id, lang or "en")
            if segments:
                result = {
                    "ok": True,
                    "video_id": video_id,
                    "source": "yt-dlp",
                    "language": lang or "unknown",
                    "auto_generated": None,
                    "segment_count": len(segments),
                    "quota_units_used": 0,
                    "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                }
                if args.format in ("segments", "both"):
                    result["segments"] = segments
                if args.format in ("text", "both"):
                    result["text"] = to_plain_text(segments)
                emit(result)
            attempts.append({"method": "yt-dlp", "error": error})

        # Method 3 -- owner captions via OAuth, only when asked for.
        if args.owned:
            try:
                segments, snippet = fetch_via_oauth(video_id, lang)
                if segments:
                    result = {
                        "ok": True,
                        "video_id": video_id,
                        "source": "data-api-oauth",
                        "language": snippet.get("language"),
                        "track_name": snippet.get("name"),
                        "auto_generated": snippet.get("trackKind") == "ASR",
                        "segment_count": len(segments),
                        "quota_units_used": quota_tracker.cost_of("captions.list")
                        + quota_tracker.cost_of("captions.download"),
                        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    }
                    if args.format in ("segments", "both"):
                        result["segments"] = segments
                    if args.format in ("text", "both"):
                        result["text"] = to_plain_text(segments)
                    emit(result)
                attempts.append({"method": "data-api-oauth", "error": "Downloaded track was empty."})
            except ExecutionError as err:
                attempts.append({"method": "data-api-oauth", "error": err.message})

        available = sorted({t["language_code"] for t in tracks if t.get("language_code")})
        die(ApiCallFailed(
            f"No transcript could be retrieved for {video_id}"
            + (f" in '{lang}'." if lang else "."),
            fix=[
                *( [f"Available caption languages: {', '.join(available)} -- retry with --lang."]
                   if available else
                   ["This video has no captions: none uploaded, none auto-generated, or captions "
                    "are disabled by the owner."] ),
                *MANUAL_FALLBACK,
                "For the creator's own video, retry with --owned to use the Data API.",
            ],
            details={"video_id": video_id, "attempts": attempts},
        ))

    except ExecutionError as err:
        die(err)


if __name__ == "__main__":
    main()
