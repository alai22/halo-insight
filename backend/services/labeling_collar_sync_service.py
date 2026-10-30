"""
Mirror Azure collar AI dumps into S3 and join them to labeled sessions.

Azure layout (device-centric):
  <collar-sn>/ai/ai_log_model_*_YYYY-MM-DD_HH-MM-SS_*.log      # posture (binary)
  <collar-sn>/ai/ai_gps_log_model_*_YYYY-MM-DD_HH-MM-SS.log    # GPS (binary)

S3 mirror:
  collar-raw/<collar-sn>/ai/<filename>

Join key: collar SN + timestamp in the AI log name vs activity/gps session
filename timestamp, with a pad around the labeled duration window.

v1 does not parse the binary dumps — coverage is presence + bytes + time overlap.
"""

from __future__ import annotations

import json
import re
import tempfile
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

import boto3

from ..utils.config import Config
from ..utils.logging import get_logger
from .labeling_data_analyzer import UNKNOWN_COLLAR_SN, in_date_window, sanitize_collar_sn

logger = get_logger("labeling_collar_sync")

AI_LOG_TS_RE = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2})_(?P<h>\d{2})-(?P<m>\d{2})-(?P<s>\d{2})")
INDEX_KEY_SUFFIX = "labeling-jobs/session_collar_index_v1.json"
DEFAULT_WINDOW_DURATION_SEC = 15 * 60
UNMATCHED_SAMPLE_LIMIT = 25
ERROR_SAMPLE_LIMIT = 3
ERROR_SAMPLE_CHARS = 300
QUERY_REDACT_RE = re.compile(r"\?[^ \n]+")


def resolve_azure_container_url(
    sas_url: Optional[str] = None,
    blob_url: Optional[str] = None,
    sas_token: Optional[str] = None,
) -> Optional[str]:
    """Build a container SAS URL from env-style pieces. Never log the result."""
    combined = (sas_url if sas_url is not None else Config.LABELING_AZURE_SAS_URL) or ""
    combined = combined.strip()
    if combined:
        return combined
    url = (blob_url if blob_url is not None else Config.LABELING_AZURE_BLOB_URL) or ""
    token = (sas_token if sas_token is not None else Config.LABELING_AZURE_SAS_TOKEN) or ""
    url = url.strip().rstrip("?")
    token = token.strip().lstrip("?")
    if url and token:
        return f"{url}?{token}"
    return None


def azure_configured() -> bool:
    return bool(resolve_azure_container_url())


# Ordered: the first matching kind wins.
_AZURE_ERROR_KINDS = (
    (
        "address",
        (
            "nodename nor servname",
            "name or service not known",
            "failed to resolve",
            "getaddrinfo",
            "temporary failure in name resolution",
        ),
    ),
    ("container", ("containernotfound", "resourcenotfound", "does not exist")),
    (
        "access",
        (
            "authenticationfailed",
            "authorizationfailure",
            "authorizationpermissionmismatch",
            "signature",
            "not authorized",
            "expired",
            "403",
        ),
    ),
)


def classify_azure_error(text: str) -> str:
    """
    Bucket an Azure error message so the UI can say what to fix.

    address: the account URL does not resolve (often a template placeholder).
    container: the container in the URL does not exist.
    access: the SAS was refused (expired, missing List/Read, wrong container).
    other: anything else.
    """
    lowered = (text or "").lower()
    for kind, needles in _AZURE_ERROR_KINDS:
        if any(needle in lowered for needle in needles):
            return kind
    return "other"


def redact_secrets(text: str, extra: Optional[str] = None) -> str:
    """Strip SAS query strings from error text before returning to clients/logs."""
    if not text:
        return text
    out = QUERY_REDACT_RE.sub("?***", str(text))
    secret = extra or Config.LABELING_AZURE_SAS_TOKEN or ""
    if secret and secret in out:
        out = out.replace(secret, "***")
    combined = Config.LABELING_AZURE_SAS_URL or ""
    if combined and combined in out:
        out = out.replace(combined, "***")
    return out


def parse_ai_log_filename(filename: str) -> Optional[Dict[str, Any]]:
    """
    Parse collar AI dump names.

    ai_log_model_50f_8c_2026-07-02_21-13-44_v3.log → activity, 2026-07-02T21:13:44
    ai_gps_log_model_gps_04_2025-12-11_14-45-40.log → gps
    ai_log_model_8c_80f_v2_2025-12-11_14-36-23_v2.log → activity
    """
    if not filename or not isinstance(filename, str):
        return None
    base = filename.rsplit("/", 1)[-1]
    lowered = base.lower()
    if "ai_gps_log" in lowered:
        family = "gps"
    elif "ai_log_model" in lowered:
        family = "activity"
    else:
        return None
    match = AI_LOG_TS_RE.search(base)
    if not match:
        return None
    ts = (
        f"{match.group('date')}T{match.group('h')}:{match.group('m')}:{match.group('s')}"
    )
    try:
        when = datetime.fromisoformat(ts)
    except ValueError:
        return None
    return {"family": family, "timestamp": ts, "when": when, "filename": base}


def parse_session_timestamp(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


@dataclass
class CollarAiFile:
    key: str
    collar_sn: str
    filename: str
    family: str
    timestamp: str
    when: datetime
    size: int = 0


@dataclass
class SyncReport:
    bucket: str
    collar_prefix: str
    dry_run: bool
    inventory_only: bool = False
    azure_configured: bool = False
    sns: List[str] = field(default_factory=list)
    listed: int = 0
    copied: int = 0
    skipped_unchanged: int = 0
    bytes_copied: int = 0
    errors: List[Dict[str, str]] = field(default_factory=list)
    coverage: Dict[str, Any] = field(default_factory=dict)
    clone: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bucket": self.bucket,
            "collar_prefix": self.collar_prefix,
            "dry_run": self.dry_run,
            "inventory_only": self.inventory_only,
            "azure_configured": self.azure_configured,
            "sns": self.sns,
            "sns_count": len(self.sns),
            "listed": self.listed,
            "copied": self.copied,
            "skipped_unchanged": self.skipped_unchanged,
            "bytes_copied": self.bytes_copied,
            "errors": self.errors,
            "coverage": self.coverage,
            "clone": self.clone,
        }


def sessions_from_analyze(summary: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Flatten posture + GPS session rows from LabelingDataAnalyzer.analyze()."""
    rows: List[Dict[str, Any]] = []
    for item in summary.get("sessions") or []:
        rows.append({**item, "family": item.get("family") or "activity"})
    for item in (summary.get("gps") or {}).get("sessions") or []:
        rows.append({**item, "family": item.get("family") or "gps"})
    return rows


def _nearest(when: datetime, items: Iterable[Tuple[datetime, Any]]) -> Optional[Tuple[float, Any]]:
    """Closest item to ``when`` as (signed seconds item minus when, item)."""
    best: Optional[Tuple[float, Any]] = None
    for at, item in items:
        delta = (at - when).total_seconds()
        if best is None or abs(delta) < abs(best[0]):
            best = (delta, item)
    return best


def match_coverage(
    sessions: Iterable[Dict[str, Any]],
    ai_files: Iterable[CollarAiFile],
    pad_sec: int = 300,
    window: Optional[Tuple[str, str]] = None,
) -> Dict[str, Any]:
    """
    Join labeled sessions to mirrored AI dumps by SN + time window.

    window: inclusive (start, end) YYYY-MM-DD. Sessions should already be limited to it.
    Every file can still match a session near the edge, but only files on window days
    are counted or listed.
    """
    pad = timedelta(seconds=max(0, int(pad_sec)))
    by_sn_family: Dict[Tuple[str, str], List[CollarAiFile]] = defaultdict(list)
    files_list = list(ai_files)
    for blob in files_list:
        by_sn_family[(blob.collar_sn, blob.family)].append(blob)

    totals = {
        "sessions": 0,
        "matched": 0,
        "missing": 0,
        "unknown_sn": 0,
        "matched_seconds": 0.0,
        "missing_seconds": 0.0,
    }
    by_user: Dict[str, Dict[str, Any]] = {}
    by_sn: Dict[str, Dict[str, Any]] = {}
    missing_reasons = {
        "no_blobs_for_sn": 0,
        "time_gap": 0,
        "unknown_sn": 0,
        "bad_timestamp": 0,
    }
    unmatched: List[Dict[str, Any]] = []
    by_date: Dict[str, Dict[str, int]] = defaultdict(
        lambda: {"matched": 0, "app_only": 0, "collar_only": 0}
    )
    used_files = set()
    sessions_by_file: Dict[int, List[Dict[str, Any]]] = defaultdict(list)
    # Every unmatched session and its closest log on the same collar, for debugging on the dashboard.
    # nearest_log_delta_sec is log time minus session start, so a clock offset shows one sign.
    mismatched_sessions: List[Dict[str, Any]] = []
    sessions_by_sn: Dict[str, List[Tuple[datetime, Dict[str, Any]]]] = defaultdict(list)
    labelers_by_sn: Dict[str, set] = defaultdict(set)

    def _mismatch(row: Dict[str, Any], start: Optional[datetime], sn: str, family: str) -> None:
        if start is not None and sn != UNKNOWN_COLLAR_SN:
            same = [(b.when, b) for b in by_sn_family.get((sn, family)) or []]
            nearest = _nearest(start, same) or _nearest(
                start, ((b.when, b) for b in files_list if b.collar_sn == sn)
            )
            if nearest is not None:
                row["nearest_log_delta_sec"] = round(nearest[0], 1)
                row["nearest_log"] = nearest[1].filename
        mismatched_sessions.append(row)

    def _touch_sn(sn: str) -> Dict[str, Any]:
        return by_sn.setdefault(
            sn,
            {
                "collar_sn": sn,
                "sessions": 0,
                "matched": 0,
                "missing": 0,
                "s3_files": 0,
                "no_blobs_for_sn": 0,
                "time_gap": 0,
                "unknown_sn": 0,
                "bad_timestamp": 0,
            },
        )

    for session in sessions:
        totals["sessions"] += 1
        email = session.get("user") or session.get("email") or ""
        raw_sn = session.get("collar_sn")
        # Keep the sentinel. sanitize_collar_sn strips the leading underscore.
        if not raw_sn or raw_sn == UNKNOWN_COLLAR_SN:
            sn = UNKNOWN_COLLAR_SN
        else:
            sn = sanitize_collar_sn(raw_sn)
        family = session.get("family") or "activity"
        duration = float(session.get("duration_seconds") or 0.0)
        user = by_user.setdefault(
            email,
            {
                "email": email,
                "sessions": 0,
                "matched_sessions": 0,
                "missing_sessions": 0,
                "unknown_sn_sessions": 0,
                "matched_seconds": 0.0,
                "missing_seconds": 0.0,
            },
        )
        user["sessions"] += 1
        sn_row = _touch_sn(sn or UNKNOWN_COLLAR_SN)
        sn_row["sessions"] += 1

        if not sn or sn == UNKNOWN_COLLAR_SN:
            unknown_start = parse_session_timestamp(session.get("timestamp") or "")
            if unknown_start is not None:
                by_date[unknown_start.date().isoformat()]["app_only"] += 1
            totals["unknown_sn"] += 1
            totals["missing"] += 1
            totals["missing_seconds"] += duration
            missing_reasons["unknown_sn"] += 1
            sn_row["missing"] += 1
            sn_row["unknown_sn"] += 1
            user["unknown_sn_sessions"] += 1
            user["missing_sessions"] += 1
            user["missing_seconds"] += duration
            _mismatch(
                {
                    "email": email,
                    "family": family,
                    "timestamp": session.get("timestamp"),
                    "collar_sn": UNKNOWN_COLLAR_SN,
                    "duration_seconds": round(duration, 3),
                    "reason": "unknown_sn",
                },
                None,
                UNKNOWN_COLLAR_SN,
                family,
            )
            if len(unmatched) < UNMATCHED_SAMPLE_LIMIT:
                unmatched.append(
                    {
                        "email": email,
                        "family": family,
                        "timestamp": session.get("timestamp"),
                        "collar_sn": sn or UNKNOWN_COLLAR_SN,
                        "duration_seconds": round(duration, 3),
                        "reason": "unknown_sn",
                    }
                )
            continue

        start = parse_session_timestamp(session.get("timestamp") or "")
        if start is None:
            totals["missing"] += 1
            totals["missing_seconds"] += duration
            missing_reasons["bad_timestamp"] += 1
            sn_row["missing"] += 1
            sn_row["bad_timestamp"] += 1
            user["missing_sessions"] += 1
            user["missing_seconds"] += duration
            _mismatch(
                {
                    "email": email,
                    "family": family,
                    "timestamp": session.get("timestamp"),
                    "collar_sn": sn,
                    "duration_seconds": round(duration, 3),
                    "reason": "bad_timestamp",
                },
                None,
                sn,
                family,
            )
            if len(unmatched) < UNMATCHED_SAMPLE_LIMIT:
                unmatched.append(
                    {
                        "email": email,
                        "family": family,
                        "timestamp": session.get("timestamp"),
                        "collar_sn": sn,
                        "duration_seconds": round(duration, 3),
                        "reason": "bad_timestamp",
                    }
                )
            continue

        sessions_by_sn[sn].append((start, {"email": email, "family": family}))
        labelers_by_sn[sn].add(email)
        window_dur = duration if duration > 0 else float(DEFAULT_WINDOW_DURATION_SEC)
        window_start = start - pad
        window_end = start + timedelta(seconds=window_dur) + pad
        candidates = by_sn_family.get((sn, family)) or []
        hits = [b for b in candidates if window_start <= b.when <= window_end]
        day = by_date[start.date().isoformat()]
        if hits:
            used_files.update(id(b) for b in hits)
            for blob in hits:
                sessions_by_file[id(blob)].append(
                    {"email": email, "timestamp": session.get("timestamp"), "family": family}
                )
            day["matched"] += 1
            totals["matched"] += 1
            totals["matched_seconds"] += duration
            sn_row["matched"] += 1
            user["matched_sessions"] += 1
            user["matched_seconds"] += duration
        else:
            day["app_only"] += 1
            reason = "no_blobs_for_sn" if not candidates else "time_gap"
            # candidates empty for family could still have other family files
            other = any(b.collar_sn == sn for b in files_list)
            if not other:
                reason = "no_blobs_for_sn"
            totals["missing"] += 1
            totals["missing_seconds"] += duration
            missing_reasons[reason] += 1
            sn_row["missing"] += 1
            sn_row[reason] += 1
            user["missing_sessions"] += 1
            user["missing_seconds"] += duration
            _mismatch(
                {
                    "email": email,
                    "family": family,
                    "timestamp": session.get("timestamp"),
                    "collar_sn": sn,
                    "duration_seconds": round(duration, 3),
                    "reason": reason,
                },
                start,
                sn,
                family,
            )
            if len(unmatched) < UNMATCHED_SAMPLE_LIMIT:
                unmatched.append(
                    {
                        "email": email,
                        "family": family,
                        "timestamp": session.get("timestamp"),
                        "collar_sn": sn,
                        "duration_seconds": round(duration, 3),
                        "reason": reason,
                    }
                )

    users_out = sorted(
        (
            {
                **stats,
                "matched_seconds": round(float(stats["matched_seconds"]), 3),
                "missing_seconds": round(float(stats["missing_seconds"]), 3),
            }
            for stats in by_user.values()
        ),
        key=lambda u: (-u["matched_seconds"], u["email"]),
    )
    counted_files = [b for b in files_list if in_date_window(b.timestamp, window)]
    collar_only_logs: List[Dict[str, Any]] = []
    for blob in counted_files:
        _touch_sn(blob.collar_sn)["s3_files"] += 1
        if id(blob) not in used_files:
            by_date[blob.when.date().isoformat()]["collar_only"] += 1
            on_sn = sessions_by_sn.get(blob.collar_sn) or []
            nearest = _nearest(
                blob.when, [(at, item) for at, item in on_sn if item["family"] == blob.family]
            ) or _nearest(blob.when, on_sn)
            collar_only_logs.append(
                {
                    "collar_sn": blob.collar_sn,
                    "filename": blob.filename,
                    "family": blob.family,
                    "timestamp": blob.timestamp,
                    "size": blob.size,
                    "labelers": sorted(labelers_by_sn.get(blob.collar_sn) or []),
                    # Log time minus closest session start, same sign as nearest_log_delta_sec.
                    "nearest_session_delta_sec": round(-nearest[0], 1) if nearest else None,
                    "nearest_session_email": nearest[1]["email"] if nearest else None,
                }
            )
    by_sn_out = sorted(
        by_sn.values(),
        key=lambda row: (-row["missing"], -row["sessions"], row["collar_sn"]),
    )
    return {
        "totals": {
            "sessions": totals["sessions"],
            "matched": totals["matched"],
            "missing": totals["missing"],
            "unknown_sn": totals["unknown_sn"],
            "matched_seconds": round(totals["matched_seconds"], 3),
            "missing_seconds": round(totals["missing_seconds"], 3),
            "ai_files": len(counted_files),
            "ai_bytes": int(sum(b.size for b in counted_files)),
            "sns": len({b.collar_sn for b in counted_files}),
        },
        "missing_reasons": missing_reasons,
        "by_user": users_out,
        "by_sn": by_sn_out,
        # Matched and app_only count sessions; collar_only counts AI files no session used.
        "by_date": [{"date": d, **by_date[d]} for d in sorted(by_date)],
        "mismatched_sessions": mismatched_sessions,
        "collar_only_logs": collar_only_logs,
        # Every mirrored file with the sessions it matched, for browsing collar-raw/ per collar.
        "collar_files": [
            {
                "collar_sn": blob.collar_sn,
                "filename": blob.filename,
                "family": blob.family,
                "timestamp": blob.timestamp,
                "size": blob.size,
                "sessions": sessions_by_file.get(id(blob), []),
            }
            for blob in sorted(counted_files, key=lambda b: (b.collar_sn, b.when))
        ],
        "unmatched_samples": unmatched,
    }


def empty_clone_row(sn: str) -> Dict[str, Any]:
    return {
        "collar_sn": sn,
        "azure_files": 0,
        "s3_files": 0,
        "copied": 0,
        "skipped": 0,
        "errors": 0,
        "list_errors": 0,
    }


def classify_blob_presence(existing_size: Optional[int], azure_size: int) -> str:
    """Return skipped when S3 already has the same bytes, else copied (needs clone)."""
    if existing_size is not None and int(existing_size) == int(azure_size):
        return "skipped"
    return "copied"


def build_clone_snapshot(
    rows: Iterable[Dict[str, Any]],
    *,
    inventory_only: bool,
    generated_at: Optional[str] = None,
    error_rows: Optional[Iterable[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    """
    Summarize an Azure listing against S3.

    Per row: collar_sn, azure_files, s3_files, copied, skipped, errors, list_errors.
    On an inventory check, copied means "not in S3 or a different size".
    After a copy, copied means "just written", so not_cloned is the error count.
    list_errors marks collars whose Azure folder could not be listed at all.
    error_rows: report errors; a few redacted samples and their kind are kept
    so the dashboard can show why Azure could not be read.
    """
    normalized: List[Dict[str, Any]] = []
    for row in rows:
        normalized.append(
            {
                "collar_sn": row.get("collar_sn") or UNKNOWN_COLLAR_SN,
                "azure_files": int(row.get("azure_files") or 0),
                "s3_files": int(row.get("s3_files") or 0),
                "copied": int(row.get("copied") or 0),
                "skipped": int(row.get("skipped") or 0),
                "errors": int(row.get("errors") or 0),
                "list_errors": int(row.get("list_errors") or 0),
            }
        )
    normalized.sort(key=lambda row: row["collar_sn"])
    azure_files = sum(row["azure_files"] for row in normalized)
    s3_files = sum(row["s3_files"] for row in normalized)
    copied = sum(row["copied"] for row in normalized)
    skipped = sum(row["skipped"] for row in normalized)
    errors = sum(row["errors"] for row in normalized)
    not_cloned = (copied + errors) if inventory_only else errors
    unreadable = sum(1 for row in normalized if row["list_errors"] > 0)
    samples: List[Dict[str, str]] = []
    kinds: Dict[str, int] = defaultdict(int)
    for item in error_rows or []:
        text = str(item.get("error") or "")
        kinds[classify_azure_error(text)] += 1
        if len(samples) < ERROR_SAMPLE_LIMIT:
            sample = {"error": text[:ERROR_SAMPLE_CHARS]}
            if item.get("sn"):
                sample["sn"] = item["sn"]
            if item.get("key"):
                sample["key"] = item["key"]
            samples.append(sample)
    error_kind = max(kinds, key=kinds.get) if kinds else None
    return {
        "generated_at": generated_at
        or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "inventory_only": bool(inventory_only),
        "azure_files": azure_files,
        "s3_files": s3_files,
        "copied": copied,
        "skipped_unchanged": skipped,
        "errors": errors,
        "not_cloned": not_cloned,
        "collars": len(normalized),
        "collars_unreadable": unreadable,
        "error_kind": error_kind,
        "error_samples": samples,
        "by_sn": normalized,
    }


def sync_done_message(report: Dict[str, Any], inventory_only: bool) -> str:
    """One-line status for a finished sync or Azure check."""
    clone = report.get("clone") or {}
    totals = (report.get("coverage") or {}).get("totals") or {}
    collars = int(clone.get("collars") or report.get("sns_count") or 0)
    unreadable = int(clone.get("collars_unreadable") or 0)
    if collars and unreadable == collars:
        return (
            f"Could not read Azure for any of the {collars} labeled collars — "
            "nothing was copied. See the Azure error on the page."
        )
    unreadable_note = (
        f" Azure could not be read for {unreadable} of {collars} collars." if unreadable else ""
    )
    if inventory_only:
        return (
            f"Azure check done — {clone.get('azure_files', report.get('listed', 0))} "
            f"files in Azure, {clone.get('not_cloned', 0)} not in S3.{unreadable_note}"
        )
    return (
        f"Collar sync done — copied {report.get('copied', 0)} files, "
        f"{totals.get('matched', 0)} sessions matched, {totals.get('missing', 0)} missing."
        f"{unreadable_note}"
    )


class LabelingCollarSyncService:
    """Copy <sn>/ai/* from Azure into S3 and report session coverage."""

    def __init__(
        self,
        bucket_name: Optional[str] = None,
        extracted_prefix: Optional[str] = None,
        collar_prefix: Optional[str] = None,
        region: Optional[str] = None,
        s3_client=None,
        azure_client=None,
        pad_sec: Optional[int] = None,
    ):
        self.bucket_name = bucket_name or Config.LABELING_S3_BUCKET_NAME
        self.extracted_prefix = (
            extracted_prefix or Config.LABELING_S3_PREFIX or "extracted-txt/"
        ).rstrip("/") + "/"
        self.collar_prefix = (
            collar_prefix or Config.LABELING_COLLAR_S3_PREFIX or "collar-raw/"
        ).rstrip("/") + "/"
        self.region = region or Config.S3_REGION or "us-east-1"
        self.s3_client = s3_client or boto3.client("s3", region_name=self.region)
        self._azure_client = azure_client
        self.pad_sec = (
            int(pad_sec)
            if pad_sec is not None
            else int(getattr(Config, "LABELING_COLLAR_MATCH_PAD_SEC", 300) or 300)
        )
        if not self.bucket_name:
            raise ValueError("LABELING_S3_BUCKET_NAME is not configured")

    def azure_client(self):
        if self._azure_client is not None:
            return self._azure_client
        url = resolve_azure_container_url()
        if not url:
            raise ValueError(
                "Azure collar blob is not configured. Set LABELING_AZURE_SAS_URL "
                "or LABELING_AZURE_BLOB_URL + LABELING_AZURE_SAS_TOKEN in .env"
            )
        from azure.storage.blob import ContainerClient

        self._azure_client = ContainerClient.from_container_url(url)
        return self._azure_client

    def labeled_collar_sns(self, files=None) -> List[str]:
        from .labeling_data_analyzer import LabelingDataAnalyzer

        if files is None:
            files = LabelingDataAnalyzer(
                bucket_name=self.bucket_name,
                prefix=self.extracted_prefix,
                region=self.region,
                s3_client=self.s3_client,
            ).list_session_files()
        sns = {
            sanitize_collar_sn(f.collar_sn)
            for f in files
            if getattr(f, "collar_sn", None)
        }
        sns.discard(UNKNOWN_COLLAR_SN)
        sns.discard("")
        return sorted(sns)

    def list_collar_ai_files(self) -> List[CollarAiFile]:
        """List mirrored AI dumps already in S3 under collar-raw/."""
        out: List[CollarAiFile] = []
        paginator = self.s3_client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket_name, Prefix=self.collar_prefix):
            for obj in page.get("Contents", []) or []:
                key = obj["Key"]
                if key.endswith("/"):
                    continue
                rel = key[len(self.collar_prefix) :] if key.startswith(self.collar_prefix) else key
                parts = [p for p in rel.split("/") if p]
                if len(parts) < 3 or parts[1] != "ai":
                    continue
                sn = sanitize_collar_sn(parts[0])
                parsed = parse_ai_log_filename(parts[-1])
                if not parsed:
                    continue
                out.append(
                    CollarAiFile(
                        key=key,
                        collar_sn=sn,
                        filename=parsed["filename"],
                        family=parsed["family"],
                        timestamp=parsed["timestamp"],
                        when=parsed["when"],
                        size=int(obj.get("Size") or 0),
                    )
                )
        return out

    def build_coverage(
        self,
        summary: Optional[Dict[str, Any]] = None,
        window: Optional[Tuple[str, str]] = None,
    ) -> Dict[str, Any]:
        if summary is None:
            from .labeling_data_analyzer import LabelingDataAnalyzer

            summary = LabelingDataAnalyzer(
                bucket_name=self.bucket_name,
                prefix=self.extracted_prefix,
                region=self.region,
                s3_client=self.s3_client,
            ).analyze(include_content=True, window=window)
        coverage = match_coverage(
            sessions_from_analyze(summary),
            self.list_collar_ai_files(),
            pad_sec=self.pad_sec,
            window=window,
        )
        coverage["azure_configured"] = azure_configured() or self._azure_client is not None
        coverage["collar_prefix"] = self.collar_prefix
        coverage["pad_sec"] = self.pad_sec
        return coverage

    def persist_index(
        self, coverage: Dict[str, Any], clone: Optional[Dict[str, Any]] = None
    ) -> None:
        if clone is None:
            existing = self.load_index() or {}
            clone = existing.get("clone")
        payload = {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "coverage": coverage,
            "clone": clone,
        }
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=INDEX_KEY_SUFFIX,
                Body=json.dumps(payload).encode("utf-8"),
                ContentType="application/json",
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to persist collar coverage index: %s", redact_secrets(str(exc)))

    def load_index(self) -> Optional[Dict[str, Any]]:
        try:
            raw = self.s3_client.get_object(Bucket=self.bucket_name, Key=INDEX_KEY_SUFFIX)[
                "Body"
            ].read()
            body = json.loads(raw.decode("utf-8"))
            if isinstance(body, dict):
                return body
        except Exception:  # noqa: BLE001
            return None
        return None

    def _s3_size(self, key: str) -> Optional[int]:
        try:
            head = self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            return int(head.get("ContentLength") or head.get("content_length") or 0)
        except Exception:  # noqa: BLE001
            return None

    def _copy_blob(self, blob_name: str, dest_key: str, size: int, dry_run: bool) -> str:
        existing = self._s3_size(dest_key)
        if existing is not None and existing == size:
            return "skipped"
        if dry_run:
            return "copied"
        client = self.azure_client()
        downloader = client.get_blob_client(blob_name).download_blob()
        # Spill to disk after 8 MiB so parallel copies cannot pin whole logs in RAM.
        with tempfile.SpooledTemporaryFile(max_size=8 * 1024 * 1024) as tmp:
            downloader.readinto(tmp)
            tmp.seek(0)
            self.s3_client.upload_fileobj(
                tmp,
                self.bucket_name,
                dest_key,
                ExtraArgs={"ContentType": "application/octet-stream"},
            )
        return "copied"

    def sync(
        self,
        dry_run: bool = False,
        inventory_only: bool = False,
        sns: Optional[List[str]] = None,
        workers: Optional[int] = None,
        summary: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Copy Azure <sn>/ai/* for labeled collar SNs into collar-raw/, then join.

        inventory_only: list Azure blobs, do not write S3.
        """
        from .labeling_data_analyzer import LabelingDataAnalyzer

        report = SyncReport(
            bucket=self.bucket_name,
            collar_prefix=self.collar_prefix,
            dry_run=dry_run,
            inventory_only=inventory_only,
            azure_configured=azure_configured() or self._azure_client is not None,
        )
        analyzer = LabelingDataAnalyzer(
            bucket_name=self.bucket_name,
            prefix=self.extracted_prefix,
            region=self.region,
            s3_client=self.s3_client,
        )
        if summary is None:
            summary = analyzer.analyze(include_content=True)
        if sns:
            report.sns = [sanitize_collar_sn(s) for s in sns if sanitize_collar_sn(s) != UNKNOWN_COLLAR_SN]
        else:
            report.sns = self.labeled_collar_sns(files=analyzer.list_session_files())

        stats: Dict[str, Dict[str, Any]] = {
            sn: empty_clone_row(sn) for sn in report.sns
        }

        if not report.sns:
            logger.info("No labeled collar SNs in extracted-txt; skipping Azure copy")
            report.coverage = self.build_coverage(summary=summary)
            if inventory_only and not dry_run:
                report.clone = build_clone_snapshot([], inventory_only=True)
                self.persist_index(report.coverage, report.clone)
            elif not dry_run:
                self.persist_index(report.coverage)
            return report.to_dict()

        azure = self.azure_client()
        # sn, blob_name, dest_key, size
        planned: List[Tuple[str, str, str, int]] = []
        for sn in report.sns:
            prefix = f"{sn}/ai/"
            try:
                blobs = list(azure.list_blobs(name_starts_with=prefix))
            except Exception as exc:  # noqa: BLE001
                stats[sn]["errors"] += 1
                stats[sn]["list_errors"] += 1
                report.errors.append({"sn": sn, "error": redact_secrets(str(exc))})
                logger.warning("Failed listing Azure %s: %s", prefix, redact_secrets(str(exc)))
                continue
            for blob in blobs:
                name = getattr(blob, "name", "") or ""
                if not name or name.endswith("/"):
                    continue
                rel = name.split("/", 1)[-1] if name.startswith(sn + "/") else name
                if not rel.startswith("ai/"):
                    continue
                dest_key = f"{self.collar_prefix}{sn}/{rel}"
                size = int(getattr(blob, "size", 0) or 0)
                stats[sn]["azure_files"] += 1
                planned.append((sn, name, dest_key, size))

        report.listed = len(planned)

        def _note(sn: str, action: str) -> None:
            row = stats.setdefault(sn, empty_clone_row(sn))
            if action == "skipped":
                row["skipped"] += 1
            elif action == "copied":
                row["copied"] += 1
            else:
                row["errors"] += 1

        if inventory_only:
            for sn, _blob_name, dest_key, size in planned:
                action = classify_blob_presence(self._s3_size(dest_key), size)
                _note(sn, action)
                if action == "skipped":
                    report.skipped_unchanged += 1
        else:
            if workers is None:
                from ..utils.runtime_stats import env_int

                workers = env_int("LABELING_SYNC_WORKERS", 4)
            workers = max(1, int(workers or 1))

            def _one(item: Tuple[str, str, str, int]) -> Tuple[str, str, str, int, Optional[str]]:
                sn, blob_name, dest_key, size = item
                try:
                    action = self._copy_blob(blob_name, dest_key, size, dry_run=dry_run)
                    return action, sn, dest_key, size, None
                except Exception as exc:  # noqa: BLE001
                    return "error", sn, dest_key, size, redact_secrets(str(exc))

            if planned:
                with ThreadPoolExecutor(max_workers=workers) as pool:
                    futures = [pool.submit(_one, item) for item in planned]
                    done = 0
                    for fut in as_completed(futures):
                        action, sn, dest_key, size, err = fut.result()
                        done += 1
                        _note(sn, action)
                        if action == "copied":
                            report.copied += 1
                            report.bytes_copied += size
                        elif action == "skipped":
                            report.skipped_unchanged += 1
                        else:
                            report.errors.append({"key": dest_key, "error": err or "copy failed"})
                        if done % 50 == 0 or done == len(futures):
                            logger.info(
                                "Collar sync copy %s/%s (copied=%s skipped=%s errors=%s)",
                                done,
                                len(futures),
                                report.copied,
                                report.skipped_unchanged,
                                len(report.errors),
                            )

        report.coverage = self.build_coverage(summary=summary)
        for row in report.coverage.get("by_sn") or []:
            sn = row.get("collar_sn")
            if not sn:
                continue
            stats.setdefault(sn, empty_clone_row(sn))["s3_files"] = int(row.get("s3_files") or 0)
        report.clone = build_clone_snapshot(
            stats.values(), inventory_only=inventory_only, error_rows=report.errors
        )
        if not dry_run:
            self.persist_index(report.coverage, report.clone)
        return report.to_dict()
