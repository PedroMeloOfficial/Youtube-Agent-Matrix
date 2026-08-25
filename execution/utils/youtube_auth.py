"""
Credential resolution for the YouTube Agent Matrix execution layer.

Two auth paths, and nothing else:

  1. **API key** -> YouTube Data API v3. Public data only: channel statistics,
     uploads playlists, video metadata, public counts, search. Read from the
     ``YOUTUBE_API_KEY`` environment variable.

  2. **OAuth 2.0** -> YouTube Analytics API v2. Private metrics for a channel the
     creator owns. The client-secret file path comes from
     ``YOUTUBE_OAUTH_CLIENT_SECRET`` (or a default under the user config dir), and
     the refreshable token is cached in the user's own config directory.

Credential rules this module enforces, from ``references/data-sources.md`` §10:

  * No credential is ever read from, or written to, the plugin folder.
  * No credential is ever printed -- not in full, not masked, not in an error.
    ``--check`` reports *whether* something is configured, never *what* it is.
  * Cached tokens are written with owner-only permissions.

Every failure raises a typed error (``CredentialsMissing`` / ``DependencyMissing``
/ ``ApiCallFailed``) that carries an actionable fix, so calling scripts can print a
JSON error object instead of a stack trace.

Config directory (override with ``YOUTUBE_AGENT_MATRIX_HOME``):

    $XDG_CONFIG_HOME/youtube-agent-matrix/   (default ~/.config/youtube-agent-matrix/)
        oauth-client-secret.json    # you put this here (or point the env var at it)
        analytics-token.json        # written by the OAuth flow, chmod 600
        quota-ledger.json           # written by quota_tracker.py

Usage:
    python execution/utils/youtube_auth.py --check api-key
    python execution/utils/youtube_auth.py --check oauth
    python execution/utils/youtube_auth.py --check all
    python execution/utils/youtube_auth.py --authorize          # run the consent flow
    python execution/utils/youtube_auth.py --authorize --revenue

Exit code is 0 when everything checked is configured, 1 otherwise. Output is JSON
on stdout in both cases.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

API_KEY_ENV = "YOUTUBE_API_KEY"
CLIENT_SECRET_ENV = "YOUTUBE_OAUTH_CLIENT_SECRET"
CONFIG_HOME_ENV = "YOUTUBE_AGENT_MATRIX_HOME"

CONFIG_DIR_NAME = "youtube-agent-matrix"
CLIENT_SECRET_FILENAME = "oauth-client-secret.json"
TOKEN_FILENAME = "analytics-token.json"
TOKEN_FILENAME_MONETARY = "analytics-token-monetary.json"

ANALYTICS_SCOPE = "https://www.googleapis.com/auth/yt-analytics.readonly"
MONETARY_SCOPE = "https://www.googleapis.com/auth/yt-analytics-monetary.readonly"
YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"

BASE_SCOPES = [ANALYTICS_SCOPE, YOUTUBE_READONLY_SCOPE]

INSTALL_HINT = "pip install google-api-python-client google-auth-oauthlib"
CLOUD_CONSOLE = "https://console.cloud.google.com/apis/credentials"


# --------------------------------------------------------------------------- #
# Typed errors
# --------------------------------------------------------------------------- #

class ExecutionError(Exception):
    """Base error carrying a machine-readable code and an actionable fix."""

    code = "execution_error"

    def __init__(self, message, fix=None, docs=None, details=None):
        super().__init__(message)
        self.message = message
        if fix is None:
            self.fix = []
        elif isinstance(fix, str):
            self.fix = [fix]
        else:
            self.fix = list(fix)
        self.docs = docs
        self.details = details or {}

    def to_dict(self):
        error = {"code": self.code, "message": self.message}
        if self.fix:
            error["fix"] = self.fix
        if self.docs:
            error["docs"] = self.docs
        if self.details:
            error["details"] = self.details
        return {"ok": False, "error": error}


class CredentialsMissing(ExecutionError):
    """A required credential is not configured. Never a stack trace."""

    code = "credentials_missing"


class DependencyMissing(ExecutionError):
    """A required Python package is not installed."""

    code = "dependency_missing"


class ApiCallFailed(ExecutionError):
    """The API was reachable but refused or failed the call."""

    code = "api_call_failed"


class InputInvalid(ExecutionError):
    """The caller passed something this script cannot work with."""

    code = "input_invalid"


# --------------------------------------------------------------------------- #
# JSON output helpers -- shared by every script in execution/
# --------------------------------------------------------------------------- #

def emit(payload, exit_code=0):
    """Print a JSON payload on stdout and exit."""
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    sys.exit(exit_code)


def die(err, extra=None):
    """Print a JSON error object on stdout and exit non-zero."""
    if isinstance(err, ExecutionError):
        payload = err.to_dict()
    else:
        payload = {"ok": False, "error": {"code": "unexpected_error", "message": str(err)}}
    if extra:
        payload["error"].update(extra)
    emit(payload, exit_code=1)


def install_excepthook():
    """Turn any uncaught exception into a JSON error object instead of a traceback."""

    def _hook(exc_type, exc, _tb):
        if isinstance(exc, ExecutionError):
            payload = exc.to_dict()
        elif isinstance(exc, KeyboardInterrupt):
            payload = {"ok": False, "error": {"code": "interrupted", "message": "Interrupted."}}
        else:
            payload = {
                "ok": False,
                "error": {
                    "code": "unexpected_error",
                    "message": f"{exc_type.__name__}: {exc}",
                    "fix": ["Re-run with the same arguments; if it persists, report the message above."],
                },
            }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        sys.exit(1)

    sys.excepthook = _hook


# --------------------------------------------------------------------------- #
# Paths -- always outside the plugin folder
# --------------------------------------------------------------------------- #

def config_dir():
    """Return the user config directory. Never inside the plugin folder."""
    override = os.environ.get(CONFIG_HOME_ENV, "").strip()
    if override:
        return Path(override).expanduser()
    xdg = os.environ.get("XDG_CONFIG_HOME", "").strip()
    base = Path(xdg).expanduser() if xdg else Path.home() / ".config"
    return base / CONFIG_DIR_NAME


def ensure_config_dir():
    path = config_dir()
    path.mkdir(parents=True, exist_ok=True)
    try:
        path.chmod(0o700)
    except OSError:
        pass
    return path


def token_path(include_revenue=False):
    name = TOKEN_FILENAME_MONETARY if include_revenue else TOKEN_FILENAME
    return config_dir() / name


def client_secret_path():
    """Where the OAuth client secret lives. Env var wins, then the config dir."""
    override = os.environ.get(CLIENT_SECRET_ENV, "").strip()
    if override:
        return Path(override).expanduser()
    return config_dir() / CLIENT_SECRET_FILENAME


def scopes_for(include_revenue=False):
    return list(BASE_SCOPES) + ([MONETARY_SCOPE] if include_revenue else [])


# --------------------------------------------------------------------------- #
# Data API v3 -- API key
# --------------------------------------------------------------------------- #

def require_api_key():
    """Return the Data API key, or raise CredentialsMissing with setup steps."""
    key = os.environ.get(API_KEY_ENV, "").strip()
    if key:
        return key
    raise CredentialsMissing(
        f"No YouTube Data API key found: the {API_KEY_ENV} environment variable is not set.",
        fix=[
            f"Create a project at {CLOUD_CONSOLE} and enable 'YouTube Data API v3'.",
            "Create an API key under Credentials and restrict it to that API.",
            f'Export it in your shell profile: export {API_KEY_ENV}="your-key-here"',
            "Then open a new shell so the variable is present, and re-run this script.",
            "No key today? Skip the script entirely: ask the creator for the channel URL, "
            "subscriber count, and the last 10 video titles with view counts and publish dates.",
        ],
        docs="references/data-sources.md §2",
    )


def _import_build():
    try:
        from googleapiclient.discovery import build  # noqa: WPS433
    except ImportError:
        raise DependencyMissing(
            "The google-api-python-client package is not installed.",
            fix=[
                INSTALL_HINT,
                "Or skip the API entirely and use the manual fallbacks in references/data-sources.md §2.",
            ],
        )
    return build


def build_data_client(api_key=None):
    """Build a YouTube Data API v3 client from an API key."""
    key = api_key or require_api_key()   # credential first: it is the likelier gap
    build = _import_build()
    try:
        return build("youtube", "v3", developerKey=key, cache_discovery=False)
    except Exception as exc:  # noqa: BLE001 -- surfaced as JSON, never a traceback
        raise ApiCallFailed(
            f"Could not build the YouTube Data API client: {exc}",
            fix=["Check network access, then confirm the key is valid and the API is enabled."],
        )


# --------------------------------------------------------------------------- #
# Analytics API v2 -- OAuth
# --------------------------------------------------------------------------- #

def _import_oauth():
    try:
        from google.auth.transport.requests import Request  # noqa: WPS433
        from google.oauth2.credentials import Credentials  # noqa: WPS433
        from google_auth_oauthlib.flow import InstalledAppFlow  # noqa: WPS433
    except ImportError:
        raise DependencyMissing(
            "OAuth dependencies are not installed (google-auth-oauthlib).",
            fix=[
                INSTALL_HINT,
                "Or use the YouTube Studio fallback in references/data-sources.md §3 -- "
                "the matrix is designed to run without OAuth.",
            ],
        )
    return Request, Credentials, InstalledAppFlow


def _write_token(creds, path):
    ensure_config_dir()
    path.write_text(creds.to_json(), encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass


def oauth_status(include_revenue=False):
    """Report configuration state without touching the network or printing secrets."""
    return {
        "client_secret_configured": client_secret_path().exists(),
        "client_secret_path": str(client_secret_path()),
        "token_cached": token_path(include_revenue).exists(),
        "token_path": str(token_path(include_revenue)),
        "scopes": scopes_for(include_revenue),
    }


def _oauth_not_configured():
    """The single, actionable 'OAuth is not set up' error used everywhere."""
    secret = client_secret_path()
    return CredentialsMissing(
        "YouTube Analytics OAuth is not configured: no cached token and no client-secret file.",
        fix=[
            f"In the same Google Cloud project, enable 'YouTube Analytics API' at {CLOUD_CONSOLE}.",
            "Create an OAuth 2.0 Client ID of type 'Desktop app' and download the JSON.",
            f"Save it to {secret} (outside the plugin folder), or point "
            f"{CLIENT_SECRET_ENV} at wherever you keep it.",
            "Run: python execution/utils/youtube_auth.py --authorize "
            "(add --revenue only if you need revenue metrics).",
            "Not setting this up? Skip it -- ask the creator for the Studio numbers instead.",
        ],
        docs="references/data-sources.md §3",
    )


def load_oauth_credentials(include_revenue=False, allow_browser=True):
    """
    Return refreshable OAuth credentials, running the consent flow if needed.

    Raises CredentialsMissing (never a traceback) when neither a cached token nor a
    client-secret file is available.
    """
    scopes = scopes_for(include_revenue)
    path = token_path(include_revenue)

    # Credential state first: a missing setup is the likelier gap, and its message
    # is far more useful than "package not installed".
    if not path.exists() and not client_secret_path().exists():
        raise _oauth_not_configured()

    Request, Credentials, InstalledAppFlow = _import_oauth()
    creds = None

    if path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(path), scopes)
        except Exception:  # noqa: BLE001 -- a corrupt cache is not fatal
            creds = None

    if creds and not creds.valid and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            _write_token(creds, path)
        except Exception:  # noqa: BLE001 -- expired refresh token: re-consent below
            creds = None

    if creds and creds.valid:
        return creds

    secret = client_secret_path()
    if not secret.exists():
        raise _oauth_not_configured()

    if not allow_browser:
        raise CredentialsMissing(
            "OAuth consent is required but this run cannot open a browser.",
            fix=["Run: python execution/utils/youtube_auth.py --authorize, then re-run this script."],
        )

    try:
        flow = InstalledAppFlow.from_client_secrets_file(str(secret), scopes)
        creds = flow.run_local_server(port=0, open_browser=True)
    except Exception as exc:  # noqa: BLE001
        raise CredentialsMissing(
            f"The OAuth consent flow did not complete: {exc}",
            fix=[
                "Add your Google account as a test user on the project's OAuth consent screen.",
                "Confirm the client type is 'Desktop app'.",
                "Confirm the browser can reach a localhost callback port.",
            ],
            docs="references/data-sources.md §9",
        )

    _write_token(creds, path)
    return creds


def build_analytics_client(include_revenue=False, allow_browser=True, creds=None):
    """Build a YouTube Analytics API v2 client. Returns (service, credentials)."""
    creds = creds or load_oauth_credentials(include_revenue, allow_browser)
    build = _import_build()
    try:
        service = build("youtubeAnalytics", "v2", credentials=creds, cache_discovery=False)
    except Exception as exc:  # noqa: BLE001
        raise ApiCallFailed(f"Could not build the YouTube Analytics client: {exc}")
    return service, creds


def build_data_client_oauth(creds):
    """Data API client authorised as the signed-in user (needed for mine=true)."""
    build = _import_build()
    try:
        return build("youtube", "v3", credentials=creds, cache_discovery=False)
    except Exception as exc:  # noqa: BLE001
        raise ApiCallFailed(f"Could not build the authorised Data API client: {exc}")


def resolve_owned_channel_id(creds):
    """Return the channel ID of the authenticated account."""
    service = build_data_client_oauth(creds)
    try:
        response = service.channels().list(part="id,snippet", mine=True).execute()
    except Exception as exc:  # noqa: BLE001
        raise explain_api_error(exc)
    items = response.get("items", [])
    if not items:
        raise ApiCallFailed(
            "The authenticated Google account has no YouTube channel.",
            fix=["Re-authorise with the account that owns the channel: "
                 "python execution/utils/youtube_auth.py --authorize"],
        )
    return items[0]["id"], items[0].get("snippet", {}).get("title")


# --------------------------------------------------------------------------- #
# API error translation
# --------------------------------------------------------------------------- #

def explain_api_error(exc):
    """Turn a googleapiclient HttpError into a typed, actionable ExecutionError."""
    status = getattr(getattr(exc, "resp", None), "status", None)
    raw = ""
    content = getattr(exc, "content", None)
    if content:
        try:
            raw = content.decode("utf-8", "replace") if isinstance(content, bytes) else str(content)
        except Exception:  # noqa: BLE001
            raw = ""

    reason = ""
    message = ""
    try:
        parsed = json.loads(raw).get("error", {})
        message = parsed.get("message", "")
        errors = parsed.get("errors") or []
        if errors:
            reason = errors[0].get("reason", "")
    except Exception:  # noqa: BLE001
        message = raw[:300]

    if reason == "quotaExceeded" or "quota" in message.lower():
        return ApiCallFailed(
            "The YouTube Data API daily quota is exhausted.",
            fix=[
                "Quota resets at midnight Pacific. Use the manual fallbacks until then.",
                "Check what drained it: python execution/utils/quota_tracker.py --check",
                "If search.list ran in a loop, switch to fetch_channel_data.py "
                "(uploads-playlist path, a fraction of the cost).",
            ],
            docs="references/data-sources.md §9",
            details={"reason": reason or "quotaExceeded"},
        )

    if reason == "accessNotConfigured":
        return ApiCallFailed(
            "The API is not enabled on this Google Cloud project.",
            fix=[f"Enable the API for the project that issued the key at {CLOUD_CONSOLE}."],
            details={"reason": reason},
        )

    if status == 403:
        return ApiCallFailed(
            f"Access denied by the API (403). {message or 'No detail returned.'}",
            fix=[
                "If using an API key: check its API and referrer restrictions, and that it was not rotated.",
                "If using OAuth: confirm the token belongs to the account that owns the channel, "
                "and that the required scope was granted.",
            ],
            docs="references/data-sources.md §9",
            details={"reason": reason or "forbidden", "http_status": status},
        )

    if status == 404:
        return ApiCallFailed(
            f"Not found (404). {message or 'The requested resource does not exist.'}",
            fix=["Check the channel, playlist or video identifier and try again."],
            details={"http_status": status},
        )

    if status == 400:
        return ApiCallFailed(
            f"The API rejected the request (400). {message or 'No detail returned.'}",
            fix=["Check the arguments -- an unsupported metric, dimension or filter is the usual cause."],
            details={"reason": reason, "http_status": status},
        )

    return ApiCallFailed(
        f"API call failed{f' ({status})' if status else ''}. {message or exc}",
        fix=["Retry once. If it persists, fall back to the manual path in references/data-sources.md."],
        details={"http_status": status} if status else None,
    )


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def check(kind, include_revenue=False):
    """Report configuration state. Never returns or prints a credential value."""
    result = {"config_dir": str(config_dir())}

    if kind in ("api-key", "all"):
        configured = bool(os.environ.get(API_KEY_ENV, "").strip())
        entry = {"configured": configured, "source": f"${API_KEY_ENV}"}
        if not configured:
            entry["fix"] = (
                f'export {API_KEY_ENV}="your-key-here" -- get one at {CLOUD_CONSOLE} '
                "with YouTube Data API v3 enabled."
            )
            entry["fallback"] = "references/data-sources.md §2 -- ask the creator for the numbers instead."
        result["data_api"] = entry

    if kind in ("oauth", "all"):
        state = oauth_status(include_revenue)
        ready = state["token_cached"] or state["client_secret_configured"]
        state["configured"] = ready
        if not state["token_cached"] and state["client_secret_configured"]:
            state["next_step"] = "python execution/utils/youtube_auth.py --authorize"
        if not ready:
            state["fix"] = (
                f"Save an OAuth 'Desktop app' client secret to {state['client_secret_path']}, "
                f"or point ${CLIENT_SECRET_ENV} at it, then run --authorize."
            )
            state["fallback"] = "references/data-sources.md §3 -- ask for the YouTube Studio numbers."
        result["analytics_api"] = state

    checked = [v for k, v in result.items() if isinstance(v, dict) and "configured" in v]
    result["ok"] = all(v["configured"] for v in checked) if checked else False
    result["note"] = "Credential values are never printed by this tool."
    return result


def main():
    install_excepthook()
    parser = argparse.ArgumentParser(
        description="Resolve and verify YouTube API credentials. Outputs JSON on stdout.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Credentials are read from the environment and the user config directory only.\n"
            "Nothing is ever read from or written to the plugin folder."
        ),
    )
    parser.add_argument(
        "--check",
        choices=["api-key", "oauth", "all"],
        help="Report whether a credential is configured (never prints its value).",
    )
    parser.add_argument(
        "--authorize",
        action="store_true",
        help="Run the OAuth consent flow and cache the token in the user config directory.",
    )
    parser.add_argument(
        "--revenue",
        action="store_true",
        help="Include the monetary Analytics scope (revenue metrics). Ask for it only when needed.",
    )
    args = parser.parse_args()

    if args.authorize:
        try:
            creds = load_oauth_credentials(include_revenue=args.revenue, allow_browser=True)
            channel_id, channel_title = resolve_owned_channel_id(creds)
        except ExecutionError as err:
            die(err)
        emit({
            "ok": True,
            "authorized": True,
            "channel_id": channel_id,
            "channel_title": channel_title,
            "scopes": scopes_for(args.revenue),
            "token_path": str(token_path(args.revenue)),
            "note": "Token cached with owner-only permissions. Never commit this file.",
        })

    if args.check:
        result = check(args.check, include_revenue=args.revenue)
        emit(result, exit_code=0 if result["ok"] else 1)

    parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
