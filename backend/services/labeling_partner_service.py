"""
Partner organizations (e.g. Treat Therapeutics) that recruit and manage labelers for Halo.

A partner sees its own participants and nobody else: Halo admins list each participant's
email, and every partner response is built only from sessions sent from those emails.
A partner reaches the data with an API key or by logging in with a listed staff email.

The config lives in one S3 file:
    {"orgs": {"treat": {"participants": [...], "logins": [...],
                        "keys": [{"id", "sha256", "last4", "label", "created_at"}]}}}
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import secrets
import threading
import time
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional, Tuple

import boto3

from ..utils.config import Config
from ..utils.logging import get_logger
from .labeling_daily_report import PROGRESS_LABELS, PROGRESS_TARGET_SECONDS

logger = get_logger("labeling_partner")

# Partners Halo works with. Adding one is a code change, so nobody can invent an org.
PARTNER_ORGS: Dict[str, str] = {"treat": "Treat Therapeutics"}

PARTNERS_KEY = "labeling-jobs/partners.json"
KEY_PREFIX = "hlp"
_CACHE_TTL_SEC = 60
_EMAIL_RE = re.compile(r"^[^@\s,;]+@[^@\s,;]+\.[^@\s,;]+$")

_cache_lock = threading.Lock()
_cache: Dict[str, Any] = {"config": None, "loaded_at": 0.0}


# --- config store --------------------------------------------------------------------------


def _s3():
    return boto3.client("s3", region_name=Config.S3_REGION or "us-east-1")


def _empty_org() -> Dict[str, Any]:
    return {"participants": [], "logins": [], "keys": []}


def normalize_config(raw: Any) -> Dict[str, Any]:
    """Known orgs only, each with clean, de-duplicated, lowercase email lists."""
    orgs_in = (raw or {}).get("orgs") if isinstance(raw, dict) else None
    orgs: Dict[str, Any] = {}
    for org in PARTNER_ORGS:
        src = (orgs_in or {}).get(org) or {}
        out = _empty_org()
        out["participants"] = clean_emails(src.get("participants") or [])
        out["logins"] = clean_emails(src.get("logins") or [])
        out["keys"] = [k for k in src.get("keys") or [] if isinstance(k, dict) and k.get("sha256")]
        orgs[org] = out
    return {"orgs": orgs, "updated_at": (raw or {}).get("updated_at") if isinstance(raw, dict) else None}


def clean_emails(values: Iterable[Any]) -> List[str]:
    seen: List[str] = []
    for value in values:
        email = str(value or "").strip().lower()
        if email and _EMAIL_RE.match(email) and email not in seen:
            seen.append(email)
    return seen


def invalid_emails(values: Iterable[Any]) -> List[str]:
    return [str(v).strip() for v in values if str(v or "").strip() and not _EMAIL_RE.match(str(v).strip())]


def load_config(force: bool = False) -> Dict[str, Any]:
    """The partners file, cached for a minute (saves here refresh it at once)."""
    with _cache_lock:
        if not force and _cache["config"] is not None and time.time() - _cache["loaded_at"] < _CACHE_TTL_SEC:
            return _cache["config"]
    raw: Any = {}
    bucket = Config.LABELING_S3_BUCKET_NAME
    if bucket:
        try:
            raw = json.loads(_s3().get_object(Bucket=bucket, Key=PARTNERS_KEY)["Body"].read())
        except Exception as exc:  # noqa: BLE001
            if "NoSuchKey" not in str(exc) and "Not Found" not in str(exc):
                logger.warning("Partners config load failed: %s", exc)
                # Keep serving the last good copy rather than locking everyone out.
                with _cache_lock:
                    if _cache["config"] is not None:
                        return _cache["config"]
    config = normalize_config(raw)
    with _cache_lock:
        _cache["config"] = config
        _cache["loaded_at"] = time.time()
    return config


def save_config(config: Dict[str, Any]) -> Dict[str, Any]:
    config = normalize_config(config)
    config["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _s3().put_object(
        Bucket=Config.LABELING_S3_BUCKET_NAME,
        Key=PARTNERS_KEY,
        Body=json.dumps(config).encode("utf-8"),
        ContentType="application/json",
    )
    with _cache_lock:
        _cache["config"] = config
        _cache["loaded_at"] = time.time()
    return config


def public_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """The config for the admin page: key hashes stay on the server."""
    return {
        "orgs": {
            org: {
                "name": PARTNER_ORGS[org],
                "participants": cfg["participants"],
                "logins": cfg["logins"],
                "keys": [
                    {k: key.get(k) for k in ("id", "last4", "label", "created_at")}
                    for key in cfg["keys"]
                ],
            }
            for org, cfg in config["orgs"].items()
        },
        "updated_at": config.get("updated_at"),
    }


# --- API keys --------------------------------------------------------------------------------


def _hash(key: str) -> str:
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def new_api_key(org: str, label: str = "") -> Tuple[str, Dict[str, Any]]:
    """A fresh key (shown once) and the record that stores only its hash."""
    key = f"{KEY_PREFIX}_{org}_{secrets.token_urlsafe(32)}"
    record = {
        "id": secrets.token_hex(6),
        "sha256": _hash(key),
        "last4": key[-4:],
        "label": str(label or "").strip()[:80],
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    return key, record


def org_for_api_key(key: Optional[str], config: Optional[Dict[str, Any]] = None) -> Optional[str]:
    """The org a key belongs to, or None. Keys name their org, so only its hashes are checked."""
    key = (key or "").strip()
    parts = key.split("_", 2)
    if len(parts) != 3 or parts[0] != KEY_PREFIX or parts[1] not in PARTNER_ORGS:
        return None
    org = parts[1]
    digest = _hash(key)
    records = (config or load_config())["orgs"].get(org, {}).get("keys") or []
    matched = False
    for record in records:
        matched |= hmac.compare_digest(str(record.get("sha256") or ""), digest)
    return org if matched else None


def org_for_login(email: Optional[str], config: Optional[Dict[str, Any]] = None) -> Optional[str]:
    email = (email or "").strip().lower()
    if not email:
        return None
    for org, cfg in (config or load_config())["orgs"].items():
        if email in cfg["logins"]:
            return org
    return None


# --- reports (built only from the org's participants' sessions) --------------------------------

_ALIAS_TO_KEY = {alias: spec["key"] for spec in PROGRESS_LABELS for alias in spec["aliases"]}


def _label_key(label: str) -> str:
    return _ALIAS_TO_KEY.get(label, label)


def _minutes(seconds: float) -> float:
    return round(float(seconds) / 60.0, 2)


def _in_range(day: str, start: Optional[str], end: Optional[str]) -> bool:
    return (not start or day >= start) and (not end or day <= end)


def participant_sessions(
    data: Dict[str, Any], emails: Iterable[str], start: Optional[str] = None, end: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Sessions from these emails only, both models, oldest first."""
    wanted = {e.lower() for e in emails}
    rows = []
    for model, source in (("activity", data or {}), ("indoor_outdoor", (data or {}).get("gps") or {})):
        for row in source.get("session_log") or []:
            email = str(row.get("email") or "").lower()
            if email not in wanted:
                continue
            day = str(row.get("timestamp") or "")[:10]
            if not _in_range(day, start, end):
                continue
            labels: Dict[str, float] = defaultdict(float)
            for label, sec in (row.get("activities") or {}).items():
                if float(sec or 0) > 0:
                    labels[_label_key(label)] += float(sec)
            rows.append({
                "email": email,
                "session_id": row.get("session_id"),
                "started_at": row.get("timestamp") or None,
                "date": day or None,
                "model": model,
                "dog": row.get("dog"),
                "collar_sn": row.get("collar_sn"),
                "seconds": float(row.get("duration_seconds") or 0),
                "label_seconds": dict(labels),
            })
    rows.sort(key=lambda r: (r["started_at"] or "", r["session_id"] or ""))
    return rows


def _session_out(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "session_id": row["session_id"],
        "started_at": row["started_at"],
        "date": row["date"],
        "model": row["model"],
        "dog": row["dog"],
        "collar_sn": row["collar_sn"],
        "minutes": _minutes(row["seconds"]),
        "labels": {k: _minutes(v) for k, v in sorted(row["label_seconds"].items(), key=lambda kv: -kv[1])},
    }


def _label_progress(label_seconds: Dict[str, float]) -> Tuple[Dict[str, Any], Dict[str, float], int]:
    progress, done = {}, 0
    for spec in PROGRESS_LABELS:
        have = label_seconds.get(spec["key"], 0.0)
        reached = have >= PROGRESS_TARGET_SECONDS
        done += reached
        progress[spec["key"]] = {
            "minutes": _minutes(have),
            "remaining_minutes": _minutes(max(0.0, PROGRESS_TARGET_SECONDS - have)),
            "done": reached,
        }
    known = {spec["key"] for spec in PROGRESS_LABELS}
    other = {k: _minutes(v) for k, v in sorted(label_seconds.items()) if k not in known and v > 0}
    return progress, other, done


def participants_report(
    data: Dict[str, Any],
    participants: List[str],
    start: Optional[str] = None,
    end: Optional[str] = None,
    names_by_email: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """One row per listed participant, including people who have not sent anything yet."""
    names_by_email = names_by_email or {}
    sessions = participant_sessions(data, participants, start, end)
    by_email: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in sessions:
        by_email[row["email"]].append(row)
    out = []
    for email in participants:
        rows = by_email.get(email, [])
        label_seconds: Dict[str, float] = defaultdict(float)
        for row in rows:
            for key, sec in row["label_seconds"].items():
                label_seconds[key] += sec
        progress, other, done = _label_progress(label_seconds)
        days = sorted({r["date"] for r in rows if r["date"]})
        out.append({
            "email": email,
            "name": names_by_email.get(email),
            "dogs": sorted({r["dog"] for r in rows if r["dog"]}),
            "sessions": len(rows),
            "minutes": _minutes(sum(r["seconds"] for r in rows)),
            "days_active": len(days),
            "first_contribution": days[0] if days else None,
            "last_contribution": days[-1] if days else None,
            "labels_done": done,
            "labels_total": len(PROGRESS_LABELS),
            "labels": progress,
            "other_labels": other,
        })
    return out


def participant_daily(
    data: Dict[str, Any], email: str, start: Optional[str] = None, end: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Each day the participant sent sessions, with minutes per label."""
    days: Dict[str, Dict[str, Any]] = {}
    for row in participant_sessions(data, [email], start, end):
        day = days.setdefault(row["date"] or "unknown", {"seconds": 0.0, "sessions": 0, "labels": defaultdict(float)})
        day["seconds"] += row["seconds"]
        day["sessions"] += 1
        for key, sec in row["label_seconds"].items():
            day["labels"][key] += sec
    return [
        {
            "date": d,
            "minutes": _minutes(v["seconds"]),
            "sessions": v["sessions"],
            "labels": {k: _minutes(s) for k, s in sorted(v["labels"].items(), key=lambda kv: -kv[1])},
        }
        for d, v in sorted(days.items())
    ]


def participant_session_list(
    data: Dict[str, Any], email: str, start: Optional[str] = None, end: Optional[str] = None
) -> List[Dict[str, Any]]:
    return [_session_out(r) for r in reversed(participant_sessions(data, [email], start, end))]


def label_catalog() -> List[Dict[str, str]]:
    return [{k: spec[k] for k in ("key", "name", "group")} for spec in PROGRESS_LABELS]
