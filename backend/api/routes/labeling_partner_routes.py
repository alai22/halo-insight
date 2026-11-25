"""
Partner API: a partner organization (Treat Therapeutics) sees labeling progress for its
own participants only. Also the admin endpoints that list participants, staff logins and
API keys.

Partner auth, checked on every call:
  - an API key: `Authorization: Bearer hlp_treat_...` or `X-API-Key: hlp_treat_...`
  - a partner staff login session (magic link to an email on the org's login list)
  - a Halo admin previewing an org with ?org=treat
"""

import re
from functools import wraps
from typing import Optional

from flask import Blueprint, g, jsonify, request, session

from ...services import labeling_partner_service as partners
from ...services.auth_service import AuthService
from ...utils.logging import get_logger
from ..middleware.auth import LABELING_PARTNER_ROLE, require_admin_auth

logger = get_logger("labeling_partner_routes")

partner_bp = Blueprint("labeling_partner", __name__, url_prefix="/api/partner/v1")
partner_admin_bp = Blueprint("labeling_partner_admin", __name__, url_prefix="/api/labeling/partners")

_DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _error(status: int, message: str):
    return jsonify({"success": False, "error": message}), status


def _api_key_from_request() -> Optional[str]:
    header = request.headers.get("Authorization") or ""
    if header.lower().startswith("bearer "):
        return header[7:].strip()
    return (request.headers.get("X-API-Key") or "").strip() or None


def _is_admin() -> bool:
    try:
        if session.get("admin_authenticated"):
            return True
    except RuntimeError:
        pass
    return AuthService.verify_admin_token(request.headers.get("X-Admin-Token"))


def _partner_org() -> Optional[str]:
    """The org this request may see, or None."""
    key = _api_key_from_request()
    if key:
        # A key that doesn't match is a refusal, never a fallback to the session.
        return partners.org_for_api_key(key)
    try:
        if session.get("role") == LABELING_PARTNER_ROLE:
            org = session.get("partner_org")
            # Taking someone off the login list ends their access on the next call.
            return org if org and partners.org_for_login(session.get("email")) == org else None
    except RuntimeError:
        pass
    if _is_admin():
        org = (request.args.get("org") or "").strip().lower()
        return org if org in partners.PARTNER_ORGS else None
    return None


def require_partner(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        org = _partner_org()
        if not org:
            return _error(401, "A valid partner API key or login is required.")
        g.partner_org = org
        return f(*args, **kwargs)

    return wrapper


def _range():
    start = (request.args.get("start") or "").strip() or None
    end = (request.args.get("end") or "").strip() or None
    for value in (start, end):
        if value and not _DAY_RE.match(value):
            raise ValueError("start and end must be YYYY-MM-DD")
    if start and end and start > end:
        raise ValueError("start must be on or before end")
    return start, end


def _summary():
    """The all-time labeling summary the dashboard uses, or None while it loads."""
    from . import labeling_routes as lr

    return lr._cache_get_memory(lr._SUMMARY_CACHE_MEM_KEY) or lr._load_summary_cache_s3(
        lr._DEFAULT_CACHE_TTL_SEC
    )


def _names_by_email():
    from . import labeling_routes as lr

    try:
        return lr._recap_lookups().get("names_by_email") or {}
    except Exception as exc:  # noqa: BLE001 - names are a nicety
        logger.warning("Partner names lookup failed: %s", exc)
        return {}


def _participants(org: str):
    return partners.load_config()["orgs"][org]["participants"]


def _base(org: str, entry, start, end):
    return {
        "success": True,
        "organization": partners.PARTNER_ORGS[org],
        "start": start,
        "end": end,
        "data_as_of": entry.get("generated_at_iso"),
    }


def _with_data(handler):
    """Range, summary and org checks shared by every partner read."""

    @wraps(handler)
    def wrapper(*args, **kwargs):
        try:
            start, end = _range()
        except ValueError as exc:
            return _error(400, str(exc))
        entry = _summary()
        if not entry:
            return _error(503, "Labeling stats are loading. Try again in a minute.")
        return handler(g.partner_org, entry, start, end, *args, **kwargs)

    return wrapper


@partner_bp.route("/participants", methods=["GET"])
@require_partner
@_with_data
def list_participants(org, entry, start, end):
    """Every participant with total minutes and minutes per label against the target."""
    rows = partners.participants_report(
        entry["data"], _participants(org), start, end, _names_by_email()
    )
    return jsonify({
        **_base(org, entry, start, end),
        "target_minutes_per_label": partners.PROGRESS_TARGET_SECONDS / 60,
        "labels": partners.label_catalog(),
        "participants": rows,
    })


def _participant_or_404(org: str, email: str) -> Optional[str]:
    email = (email or "").strip().lower()
    # Anyone not on this org's list looks exactly like an unknown email.
    return email if email in _participants(org) else None


@partner_bp.route("/participants/<path:email>/daily", methods=["GET"])
@require_partner
@_with_data
def participant_daily(org, entry, start, end, email):
    """Minutes per label for each day the participant sent sessions."""
    email = _participant_or_404(org, email)
    if not email:
        return _error(404, "No such participant.")
    return jsonify({
        **_base(org, entry, start, end),
        "email": email,
        "days": partners.participant_daily(entry["data"], email, start, end),
    })


@partner_bp.route("/participants/<path:email>/sessions", methods=["GET"])
@require_partner
@_with_data
def participant_sessions(org, entry, start, end, email):
    """Each session, newest first: when, model, dog, collar and minutes per label."""
    email = _participant_or_404(org, email)
    if not email:
        return _error(404, "No such participant.")
    return jsonify({
        **_base(org, entry, start, end),
        "email": email,
        "sessions": partners.participant_session_list(entry["data"], email, start, end),
    })


@partner_bp.route("/me", methods=["GET"])
@require_partner
def whoami():
    org = g.partner_org
    return jsonify({
        "success": True,
        "org": org,
        "organization": partners.PARTNER_ORGS[org],
        "participants": len(_participants(org)),
    })


# --- admin: participants, staff logins and API keys -----------------------------------------


def _org_or_404(org: str) -> Optional[str]:
    org = (org or "").strip().lower()
    return org if org in partners.PARTNER_ORGS else None


@partner_admin_bp.route("", methods=["GET"])
@require_admin_auth
def get_partners():
    return jsonify({"success": True, **partners.public_config(partners.load_config(force=True))})


@partner_admin_bp.route("/<org>", methods=["PUT"])
@require_admin_auth
def save_partner(org):
    """Body: {"participants": [emails], "logins": [emails]}; either may be left out."""
    org = _org_or_404(org)
    if not org:
        return _error(404, "Unknown partner.")
    body = request.get_json(silent=True) or {}
    config = partners.load_config(force=True)
    for field in ("participants", "logins"):
        if field not in body:
            continue
        values = body[field]
        if not isinstance(values, list):
            return _error(400, f"{field} must be a list of emails")
        bad = partners.invalid_emails(values)
        if bad:
            return _error(400, f"Not an email: {', '.join(bad[:5])}")
        config["orgs"][org][field] = partners.clean_emails(values)
    try:
        config = partners.save_config(config)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Partners save failed")
        return _error(500, str(exc))
    return jsonify({"success": True, **partners.public_config(config)})


@partner_admin_bp.route("/<org>/keys", methods=["POST"])
@require_admin_auth
def create_partner_key(org):
    """A new API key. The key itself is in this response only; Halo keeps its hash."""
    org = _org_or_404(org)
    if not org:
        return _error(404, "Unknown partner.")
    label = (request.get_json(silent=True) or {}).get("label") or ""
    key, record = partners.new_api_key(org, label)
    config = partners.load_config(force=True)
    config["orgs"][org]["keys"].append(record)
    try:
        config = partners.save_config(config)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Partner key save failed")
        return _error(500, str(exc))
    logger.info("Created partner API key %s for %s", record["id"], org)
    return jsonify({"success": True, "key": key, **partners.public_config(config)})


@partner_admin_bp.route("/<org>/keys/<key_id>", methods=["DELETE"])
@require_admin_auth
def revoke_partner_key(org, key_id):
    org = _org_or_404(org)
    if not org:
        return _error(404, "Unknown partner.")
    config = partners.load_config(force=True)
    keys = config["orgs"][org]["keys"]
    remaining = [k for k in keys if k.get("id") != key_id]
    if len(remaining) == len(keys):
        return _error(404, "No such key.")
    config["orgs"][org]["keys"] = remaining
    try:
        config = partners.save_config(config)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Partner key revoke failed")
        return _error(500, str(exc))
    logger.info("Revoked partner API key %s for %s", key_id, org)
    return jsonify({"success": True, **partners.public_config(config)})
