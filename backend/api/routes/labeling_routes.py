"""
API routes for Halo AI labeling: staging process + summaries.
"""

from __future__ import annotations

import gzip
import hmac
import json
from functools import wraps
import re
import threading
import time
from datetime import date, datetime, timedelta, timezone
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Tuple

import boto3
from flask import Blueprint, jsonify, request, session

from backend.api.middleware.auth import (
    is_labeling_viewer,
    require_admin_auth,
    require_labeling_read,
)
from backend.services.labeling_data_analyzer import (
    LabelingDataAnalyzer,
    file_snapshot_payload,
    files_from_snapshot,
    format_ui_summary,
    serial_key,
)
from backend.services.labeling_collar_sync_service import (
    LabelingCollarSyncService,
    azure_configured,
    redact_secrets,
    sync_done_message,
)
from backend.services.labeling_daily_report import (
    build_daily_report,
    period_change,
    period_start,
    recap_data,
    remote_eligibility,
    LABELER_TYPES,
    post_to_slack,
    post_to_slack_webhook,
    report_day,
)
from backend.services.labeling_ingest_service import LabelingIngestService
from backend.services.ml_processed_inventory import MlProcessedInventory, ml_object_key_allowed
from backend.utils.config import Config
from backend.utils.logging import get_logger
from backend.utils.runtime_stats import log_rss, snapshot as runtime_snapshot

logger = get_logger("labeling_routes")

labeling_bp = Blueprint("labeling", __name__, url_prefix="/api/labeling")

_CACHE_LOCK = threading.Lock()
# payload: ui summary dict; generated_at: unix ts; fresh_until: unix ts
_CACHE: Dict[str, Any] = {
    "key": None,
    "payload": None,
    "generated_at": 0.0,
    "fresh_until": 0.0,
}
_DEFAULT_CACHE_TTL_SEC = 15 * 60  # treat as fresh for 15 minutes
_SUMMARY_CACHE_KEY = "labeling-jobs/summary_cache_v4.json"
_SUMMARY_CACHE_MEM_KEY = "summary:v4"
_BG_REFRESH_LOCK = threading.Lock()
_BG_REFRESH_RUNNING = False
_BG_REFRESH_STARTED_AT: Optional[str] = None

_PROCESS_LOCK = threading.Lock()
_PROCESS_STATE: Dict[str, Any] = {
    "running": False,
    "job": None,  # "process" | "promote-forwards" | "compact-staging" | "sync-collar"
    "started_at": None,
    "finished_at": None,
    "last_report": None,
    "last_error": None,
    "message": None,
    "progress": None,
}
# A running job re-saves its state every minute. One that has not for 5 minutes died
# (usually a deploy restarted the container) and no longer blocks other work.
_HEARTBEAT_SEC = 60
_STALE_HEARTBEAT_SEC = 5 * 60
_PROCESS_STATUS_KEY = "labeling-jobs/process_status.json"
# Who each collar belongs to, edited on the dashboard. Kept in S3, not the repo.
_COLLAR_OWNERS_KEY = "labeling-jobs/collar_owners.json"
# Employee, pack member or partner, per labeler name (lowercase).
_LABELER_TYPES_KEY = "labeling-jobs/labeler_types.json"
_COLLAR_OWNER_FIELD_MAX = 120
# Status polls every few seconds. Re-listing the whole staging tree that often
# competes with the job that is copying those same objects.
_INVENTORY_LOCK = threading.Lock()
_INVENTORY_CACHE: Dict[str, Any] = {"at": 0.0, "data": None}
_INVENTORY_TTL_SEC = 15


def _s3_client():
    return boto3.client("s3", region_name=Config.S3_REGION or "us-east-1")


def _cache_entry(
    payload: Dict[str, Any], generated_at: float, fresh_until: float
) -> Dict[str, Any]:
    return {
        "data": payload,
        "generated_at": generated_at,
        "generated_at_iso": time.strftime(
            "%Y-%m-%dT%H:%M:%SZ", time.gmtime(generated_at)
        ),
        "fresh_until": fresh_until,
        "stale": time.time() >= fresh_until,
    }


def _cache_get_memory(key: str) -> Optional[Dict[str, Any]]:
    """Return last summary even if past TTL (stale-while-revalidate)."""
    with _CACHE_LOCK:
        if _CACHE["key"] != key or _CACHE["payload"] is None:
            return None
        return _cache_entry(
            _CACHE["payload"],
            float(_CACHE["generated_at"] or 0),
            float(_CACHE["fresh_until"] or 0),
        )


def _cache_set_memory(
    key: str, payload: Dict[str, Any], ttl_sec: int, generated_at: Optional[float] = None
) -> Dict[str, Any]:
    now = time.time()
    gen = float(generated_at if generated_at is not None else now)
    fresh_until = gen + max(0, ttl_sec)
    with _CACHE_LOCK:
        _CACHE["key"] = key
        _CACHE["payload"] = payload
        _CACHE["generated_at"] = gen
        _CACHE["fresh_until"] = fresh_until
    return _cache_entry(payload, gen, fresh_until)


def _persist_summary_cache(payload: Dict[str, Any], generated_at: float, ttl_sec: int) -> None:
    bucket = Config.LABELING_S3_BUCKET_NAME
    if not bucket:
        return
    try:
        body = {
            "generated_at": generated_at,
            "generated_at_iso": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime(generated_at)
            ),
            "ttl_sec": ttl_sec,
            "data": payload,
        }
        _s3_client().put_object(
            Bucket=bucket,
            Key=_SUMMARY_CACHE_KEY,
            Body=json.dumps(body).encode("utf-8"),
            ContentType="application/json",
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to persist labeling summary cache: %s", exc)


def _load_summary_cache_s3(ttl_sec: int) -> Optional[Dict[str, Any]]:
    bucket = Config.LABELING_S3_BUCKET_NAME
    if not bucket:
        return None
    try:
        raw = _s3_client().get_object(Bucket=bucket, Key=_SUMMARY_CACHE_KEY)["Body"].read()
        body = json.loads(raw.decode("utf-8"))
        if not isinstance(body, dict) or not isinstance(body.get("data"), dict):
            return None
        generated_at = float(body.get("generated_at") or 0)
        if generated_at <= 0 and body.get("generated_at_iso"):
            try:
                generated_at = datetime.strptime(
                    body["generated_at_iso"], "%Y-%m-%dT%H:%M:%SZ"
                ).replace(tzinfo=timezone.utc).timestamp()
            except Exception:  # noqa: BLE001
                generated_at = time.time()
        # Hydrate memory so subsequent requests skip S3
        return _cache_set_memory(
            _SUMMARY_CACHE_MEM_KEY, body["data"], ttl_sec, generated_at=generated_at
        )
    except Exception:  # noqa: BLE001
        return None


def _cache_clear() -> None:
    _window_cache_clear()
    with _CACHE_LOCK:
        _CACHE["key"] = None
        _CACHE["payload"] = None
        _CACHE["generated_at"] = 0.0
        _CACHE["fresh_until"] = 0.0
    bucket = Config.LABELING_S3_BUCKET_NAME
    if not bucket:
        return
    try:
        _s3_client().delete_object(Bucket=bucket, Key=_SUMMARY_CACHE_KEY)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to clear labeling summary cache: %s", exc)


def _cache_mark_stale() -> None:
    """Keep the last summary so the page can paint, and mark it ready to refresh."""
    _window_cache_clear()
    with _CACHE_LOCK:
        payload = _CACHE["payload"] if _CACHE["key"] == _SUMMARY_CACHE_MEM_KEY else None
    if payload is None:
        loaded = _load_summary_cache_s3(_DEFAULT_CACHE_TTL_SEC)
        payload = loaded["data"] if loaded else None
    if not payload:
        return
    generated_at = time.time() - _DEFAULT_CACHE_TTL_SEC - 1
    _cache_set_memory(
        _SUMMARY_CACHE_MEM_KEY, payload, _DEFAULT_CACHE_TTL_SEC, generated_at=generated_at
    )
    _persist_summary_cache(payload, generated_at, _DEFAULT_CACHE_TTL_SEC)


def _refresh_summary_after_process(report: Dict[str, Any], clear_output: bool, dry_run: bool) -> None:
    """Drop a blocking rescan when the process did not change extracted-txt."""
    if dry_run:
        return
    if clear_output or int(report.get("copied") or 0) > 0:
        _cache_mark_stale()


def _attach_collar_coverage(
    data: Dict[str, Any], raw: Dict[str, Any], window: Optional[Tuple[str, str]] = None
) -> Dict[str, Any]:
    """Join mirrored collar-raw/ AI dumps onto the UI summary."""
    try:
        coverage = LabelingCollarSyncService().build_coverage(summary=raw, window=window)
        data["collar_coverage"] = coverage
    except Exception as exc:  # noqa: BLE001
        logger.warning("Collar coverage attach failed: %s", redact_secrets(str(exc)))
        data["collar_coverage"] = {
            "azure_configured": azure_configured(),
            "error": redact_secrets(str(exc)),
            "totals": {},
            "by_user": [],
            "unmatched_samples": [],
        }
    return data


def _compute_summary(ttl_sec: int) -> Dict[str, Any]:
    analyzer = _configure_analyzer(LabelingDataAnalyzer())
    raw = analyzer.analyze(include_content=True)
    data = _attach_collar_coverage(format_ui_summary(raw), raw)
    _attach_overview(data, data)
    entry = _cache_set_memory(_SUMMARY_CACHE_MEM_KEY, data, ttl_sec)
    _persist_summary_cache(data, entry["generated_at"], ttl_sec)
    _persist_file_snapshot(file_snapshot_payload(analyzer), entry["generated_at"])
    # Ranges were cut from the previous snapshot; rebuild them from this one.
    _window_cache_clear()
    return entry


# The file listing and texts behind the last full summary. A date range is built from
# this instead of downloading every labeling file again, so it takes seconds and gives
# exactly the all-time numbers cut to the range.
_FILE_SNAPSHOT_KEY = "labeling-jobs/summary_files_v1.json.gz"
_SNAPSHOT_LOCK = threading.Lock()
_SNAPSHOT_MEMO: Dict[str, Any] = {"payload": None}


def _persist_file_snapshot(payload: Dict[str, Any], generated_at: float) -> None:
    payload = {**payload, "generated_at": generated_at}
    with _SNAPSHOT_LOCK:
        _SNAPSHOT_MEMO["payload"] = payload
    bucket = Config.LABELING_S3_BUCKET_NAME
    if not bucket:
        return
    try:
        _s3_client().put_object(
            Bucket=bucket,
            Key=_FILE_SNAPSHOT_KEY,
            Body=gzip.compress(json.dumps(payload).encode("utf-8")),
            ContentType="application/json",
            ContentEncoding="gzip",
        )
        log_rss(logger, f"labeling file snapshot saved ({len(payload.get('files') or [])} files)")
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to persist labeling file snapshot: %s", exc)


def _load_file_snapshot() -> Optional[Dict[str, Any]]:
    with _SNAPSHOT_LOCK:
        if _SNAPSHOT_MEMO["payload"] is not None:
            return _SNAPSHOT_MEMO["payload"]
    bucket = Config.LABELING_S3_BUCKET_NAME
    if not bucket:
        return None
    try:
        body = _s3_client().get_object(Bucket=bucket, Key=_FILE_SNAPSHOT_KEY)["Body"].read()
        payload = json.loads(gzip.decompress(body).decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        if "NoSuchKey" not in str(exc):
            logger.warning("Failed to load labeling file snapshot: %s", exc)
        return None
    with _SNAPSHOT_LOCK:
        _SNAPSHOT_MEMO["payload"] = payload
    return payload


# Date-range summaries, newest last. They come from the same files as the full summary,
# so they are dropped whenever that one is cleared or marked stale.
_WINDOW_CACHE_LOCK = threading.Lock()
_WINDOW_CACHE: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()
_WINDOW_RUNNING: set = set()
_WINDOW_ERRORS: Dict[str, str] = {}
_WINDOW_CACHE_MAX = 4
_OPEN_START = "0000-01-01"
_OPEN_END = "9999-12-31"


def _parse_window(args: Any) -> Optional[Tuple[str, str]]:
    """start/end query params (YYYY-MM-DD, either may be empty) as an inclusive day window."""
    start = (args.get("start") or "").strip()
    end = (args.get("end") or "").strip()
    if not start and not end:
        return None
    for value in (start, end):
        if value:
            datetime.strptime(value, "%Y-%m-%d")
    window = (start or _OPEN_START, end or _OPEN_END)
    if window[0] > window[1]:
        raise ValueError("start date is after end date")
    return window


def _window_label(window: Tuple[str, str]) -> Dict[str, Optional[str]]:
    return {
        "start": None if window[0] == _OPEN_START else window[0],
        "end": None if window[1] == _OPEN_END else window[1],
    }


def _window_cache_clear() -> None:
    with _WINDOW_CACHE_LOCK:
        _WINDOW_CACHE.clear()
        _WINDOW_ERRORS.clear()


def _compute_window_summary(window: Tuple[str, str]) -> None:
    snapshot = _load_file_snapshot()
    if snapshot is None:
        # No snapshot yet (first range since this was deployed). One full scan writes it,
        # and refreshes the all-time summary on the way.
        _compute_summary(_DEFAULT_CACHE_TTL_SEC)
        snapshot = _load_file_snapshot() or {}
    analyzer = _configure_analyzer(LabelingDataAnalyzer())
    analyzer.text_overrides = snapshot.get("texts") or {}
    raw = analyzer.analyze(
        include_content=True,
        window=window,
        files=files_from_snapshot(snapshot) if snapshot.get("files") is not None else None,
    )
    data = _attach_collar_coverage(format_ui_summary(raw), raw, window)
    data["window"] = _window_label(window)
    # Streaks, milestones and the change compare against the all-time summary.
    full = _cache_get_memory(_SUMMARY_CACHE_MEM_KEY) or _load_summary_cache_s3(
        _DEFAULT_CACHE_TTL_SEC
    )
    _attach_overview(data, full["data"] if full else data, window)
    key = f"{window[0]}..{window[1]}"
    with _WINDOW_CACHE_LOCK:
        _WINDOW_CACHE.pop(key, None)
        _WINDOW_CACHE[key] = {"payload": data, "generated_at": time.time()}
        while len(_WINDOW_CACHE) > _WINDOW_CACHE_MAX:
            _WINDOW_CACHE.popitem(last=False)


def _maybe_start_window_refresh(window: Tuple[str, str]) -> bool:
    """Start one date-range scan off the request thread. False when a job is busy."""
    if _is_process_busy():
        return False
    key = f"{window[0]}..{window[1]}"
    with _WINDOW_CACHE_LOCK:
        if key in _WINDOW_RUNNING:
            return True
        _WINDOW_RUNNING.add(key)

    def _worker():
        try:
            log_rss(logger, f"labeling window summary {key} start")
            _compute_window_summary(window)
            log_rss(logger, f"labeling window summary {key} finish")
        except Exception as exc:  # noqa: BLE001
            logger.exception("Labeling window summary %s failed", key)
            with _WINDOW_CACHE_LOCK:
                _WINDOW_ERRORS[key] = str(exc) or exc.__class__.__name__
        finally:
            with _WINDOW_CACHE_LOCK:
                _WINDOW_RUNNING.discard(key)

    threading.Thread(target=_worker, daemon=True).start()
    return True


def _client_summary(data: Dict[str, Any]) -> Dict[str, Any]:
    """The summary as the dashboard gets it: per-session logs stay on the server."""
    if not isinstance(data, dict):
        return data
    out = {k: v for k, v in data.items() if k != "session_log"}
    if isinstance(out.get("gps"), dict):
        out["gps"] = {k: v for k, v in out["gps"].items() if k != "session_log"}
    return out


def _window_summary_response(window: Tuple[str, str], refresh: bool, ttl_sec: int):
    key = f"{window[0]}..{window[1]}"
    with _WINDOW_CACHE_LOCK:
        entry = _WINDOW_CACHE.get(key)
        running = key in _WINDOW_RUNNING
        if refresh:
            _WINDOW_ERRORS.pop(key, None)
        error = _WINDOW_ERRORS.get(key)
    if error and entry is None and not running:
        # Report the failure instead of starting the same failing build on every poll.
        return jsonify({
            "success": True,
            "pending": False,
            "cached": False,
            "stale": False,
            "generated_at": None,
            "data": None,
            "error": f"Could not build stats for this date range: {error}",
        })
    generated_iso = (
        time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(entry["generated_at"])) if entry else None
    )
    # Refresh means new files: rescan everything, then cut the range from the new
    # snapshot (the rescan clears the range cache when it finishes).
    if refresh:
        _maybe_start_background_refresh(ttl_sec)
    full_refresh = _summary_refresh_job()
    if entry is not None and (not refresh or full_refresh):
        stale = time.time() - entry["generated_at"] > ttl_sec or full_refresh is not None
        if stale and full_refresh is None:
            _maybe_start_window_refresh(window)
        return jsonify({
            "success": True,
            "pending": False,
            "cached": True,
            "stale": stale,
            "generated_at": generated_iso,
            "data": _client_summary(entry["payload"]),
            "blocked_by": full_refresh,
        })
    if full_refresh is not None:
        return jsonify({
            "success": True,
            "pending": True,
            "cached": False,
            "stale": True,
            "generated_at": None,
            "data": None,
            "blocked_by": full_refresh,
            "message": "Stats for this range follow the full refresh.",
        })
    started = _maybe_start_window_refresh(window)
    blocked_by = None if started else _blocking_job()
    if not started:
        logger.info(
            "Deferring labeling range %s until %s finishes", key, (blocked_by or {}).get("job")
        )
    return jsonify({
        "success": True,
        "pending": True,
        "cached": entry is not None,
        "stale": True,
        "generated_at": generated_iso,
        "data": _client_summary(entry["payload"]) if entry else None,
        "blocked_by": blocked_by,
        "message": (
            "Building stats for this date range in the background."
            if started
            else "Date-range stats wait until the current labeling job finishes."
        ),
    })


def _summary_refresh_job() -> Optional[Dict[str, Any]]:
    """The full summary rescan, when one is running, shaped like _blocking_job."""
    with _BG_REFRESH_LOCK:
        if not _BG_REFRESH_RUNNING:
            return None
        started_at = _BG_REFRESH_STARTED_AT
    return {
        "job": "summary-refresh",
        "started_at": started_at,
        "updated_at": None,
        "message": "Rescanning every labeling file",
        "progress": None,
    }


def _maybe_start_background_refresh(ttl_sec: int) -> bool:
    """Start one summary scan off the request thread. False when a job is busy."""
    global _BG_REFRESH_RUNNING
    if _is_process_busy():
        logger.info("Deferring labeling summary refresh until the current job finishes")
        return False
    global _BG_REFRESH_STARTED_AT
    with _BG_REFRESH_LOCK:
        if _BG_REFRESH_RUNNING:
            return True
        _BG_REFRESH_RUNNING = True
        _BG_REFRESH_STARTED_AT = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def _worker():
        global _BG_REFRESH_RUNNING
        try:
            log_rss(logger, "labeling summary refresh start")
            _compute_summary(ttl_sec)
            log_rss(logger, "labeling summary refresh finish")
        except Exception:  # noqa: BLE001
            log_rss(logger, "labeling summary refresh failed")
            logger.exception("Background labeling summary refresh failed")
        finally:
            with _BG_REFRESH_LOCK:
                _BG_REFRESH_RUNNING = False

    threading.Thread(target=_worker, daemon=True).start()
    return True


def _annotate_runtime(snap: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(snap)
    out["runtime"] = runtime_snapshot()
    return out


def _progress_value(value: Any) -> Optional[Dict[str, Any]]:
    return value if isinstance(value, dict) else None


def _process_fields() -> Dict[str, Any]:
    return {
        "running": bool(_PROCESS_STATE["running"]),
        "job": _PROCESS_STATE.get("job"),
        "started_at": _PROCESS_STATE["started_at"],
        "finished_at": _PROCESS_STATE["finished_at"],
        "last_error": _PROCESS_STATE["last_error"],
        "last_report": _PROCESS_STATE["last_report"],
        "message": _PROCESS_STATE["message"],
        "progress": _progress_value(_PROCESS_STATE.get("progress")),
    }


def process_liveness() -> Dict[str, Any]:
    """In-memory job flag for /health. Does not read S3."""
    with _PROCESS_LOCK:
        return {
            "running": bool(_PROCESS_STATE["running"]),
            "job": _PROCESS_STATE.get("job"),
            "message": _PROCESS_STATE["message"],
        }


def _process_snapshot() -> Dict[str, Any]:
    with _PROCESS_LOCK:
        snap = _process_fields()
    return _annotate_runtime(snap)


def _persist_process_state(state: Dict[str, Any]) -> None:
    """Write job state to S3 so status survives tab close / other workers."""
    bucket = Config.LABELING_S3_BUCKET_NAME
    if not bucket:
        return
    try:
        payload = {
            **state,
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        _s3_client().put_object(
            Bucket=bucket,
            Key=_PROCESS_STATUS_KEY,
            Body=json.dumps(payload).encode("utf-8"),
            ContentType="application/json",
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to persist labeling process status: %s", exc)


def _load_persisted_process_state() -> Optional[Dict[str, Any]]:
    bucket = Config.LABELING_S3_BUCKET_NAME
    if not bucket:
        return None
    try:
        body = _s3_client().get_object(Bucket=bucket, Key=_PROCESS_STATUS_KEY)["Body"].read()
        data = json.loads(body.decode("utf-8"))
        if not isinstance(data, dict):
            return None
        return data
    except Exception:  # noqa: BLE001
        return None


def _merge_process_state() -> Dict[str, Any]:
    """Prefer in-memory if this worker is running; else S3 (for other workers / reloads)."""
    mem = _process_snapshot()
    if mem.get("running"):
        return mem
    persisted = _load_persisted_process_state()
    if not persisted:
        return mem
    # S3 says running but this process is not: trust it only while it keeps beating.
    beat = persisted.get("updated_at") or persisted.get("started_at")
    if persisted.get("running") and beat:
        try:
            last = datetime.strptime(beat, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            silent = (datetime.now(timezone.utc) - last).total_seconds()
            if silent > _STALE_HEARTBEAT_SEC:
                logger.warning(
                    "Labeling job %s stopped reporting %ds ago; treating it as not running",
                    persisted.get("job"),
                    int(silent),
                )
                persisted = {
                    **persisted,
                    "running": False,
                    "last_error": persisted.get("last_error")
                    or "Job stopped reporting (likely interrupted by a restart); you can start again.",
                    "message": "Interrupted job cleared",
                }
        except Exception:  # noqa: BLE001
            pass
    # Keep last_report from whichever is newer
    if not persisted.get("last_report") and mem.get("last_report"):
        persisted["last_report"] = mem["last_report"]
    return _annotate_runtime(
        {
            "running": bool(persisted.get("running")),
            "job": persisted.get("job"),
            "started_at": persisted.get("started_at"),
            "finished_at": persisted.get("finished_at"),
            "updated_at": persisted.get("updated_at"),
            "last_error": persisted.get("last_error"),
            "last_report": persisted.get("last_report"),
            "message": persisted.get("message"),
            "progress": _progress_value(persisted.get("progress")),
        }
    )


_HEARTBEAT_THREAD: Optional[threading.Thread] = None


def _heartbeat_loop() -> None:
    while True:
        time.sleep(_HEARTBEAT_SEC)
        with _PROCESS_LOCK:
            if not _PROCESS_STATE["running"]:
                return
            snap = _process_fields()
        _persist_process_state(snap)


def _ensure_heartbeat() -> None:
    """Keep the S3 state fresh while a job runs, even through long silent phases."""
    global _HEARTBEAT_THREAD
    with _PROCESS_LOCK:
        if _HEARTBEAT_THREAD is not None and _HEARTBEAT_THREAD.is_alive():
            return
        _HEARTBEAT_THREAD = threading.Thread(target=_heartbeat_loop, daemon=True)
        _HEARTBEAT_THREAD.start()


def _set_process_state(**kwargs: Any) -> Dict[str, Any]:
    with _PROCESS_LOCK:
        _PROCESS_STATE.update(kwargs)
        snap = _process_fields()
    _persist_process_state(snap)
    if snap["running"]:
        _ensure_heartbeat()
    return _annotate_runtime(snap)


def _blocking_job() -> Optional[Dict[str, Any]]:
    """The job a deferred summary is waiting on, for the dashboard to name."""
    state = _merge_process_state()
    if not state.get("running"):
        return None
    return {
        "job": state.get("job"),
        "started_at": state.get("started_at"),
        "updated_at": state.get("updated_at"),
        "message": state.get("message"),
        "progress": state.get("progress"),
    }


def _progress_callback(job: str):
    def _on_progress(payload: Dict[str, Any]) -> None:
        _set_process_state(
            running=True,
            job=job,
            message=payload.get("message"),
            progress={
                "phase": payload.get("phase"),
                "done": int(payload.get("done") or 0),
                "total": int(payload.get("total") or 0),
            },
        )

    return _on_progress


def _process_done_message(report: Dict[str, Any]) -> str:
    health = report.get("health") or {}
    unique = health.get("unique_files_after_dedupe")
    incomplete = int(report.get("incomplete_sessions") or 0)
    unique_bit = (
        f" About {unique} unique files after dedupe." if unique is not None else ""
    )
    incomplete_bit = (
        f" {incomplete} incomplete sessions were kept as-is." if incomplete else ""
    )
    skipped = int(report.get("skipped_unchanged") or 0)
    skipped_bit = f" Skipped {skipped} already in output." if skipped else ""
    return (
        f"Done — copied {report.get('copied', 0)} files across "
        f"{report.get('sessions', 0)} sessions.{skipped_bit}{unique_bit}{incomplete_bit} "
        "Charts match that deduped set."
    )


def _compact_done_message(report: Dict[str, Any]) -> str:
    if report.get("dry_run"):
        return (
            f"Dry run — would remove {report.get('extracted_duplicates_planned', 0)} "
            f"duplicate extracted files and {report.get('raw_objects_planned', 0)} raw objects."
        )
    extracted = int(report.get("extracted_duplicates_removed") or 0)
    raw = int(report.get("raw_objects_removed") or 0)
    kept = int(report.get("unique_filenames") or 0)
    mismatch = int(report.get("size_mismatch_copies_kept") or 0)
    raw_bit = (
        f" and {raw} raw objects from batches that added nothing new" if raw else ""
    )
    mismatch_bit = (
        f" {mismatch} size-mismatch copies were left in place." if mismatch else ""
    )
    return (
        f"Removed {extracted} duplicate extracted files{raw_bit}. "
        f"{kept} filenames kept.{mismatch_bit} "
        "Charts stay unchanged until you Process staging."
    )


def _progress_callback(job: str):
    def _on_progress(payload: Dict[str, Any]) -> None:
        _set_process_state(
            running=True,
            job=job,
            message=payload.get("message"),
            progress={
                "phase": payload.get("phase"),
                "done": int(payload.get("done") or 0),
                "total": int(payload.get("total") or 0),
            },
        )

    return _on_progress


def _process_done_message(report: Dict[str, Any]) -> str:
    health = report.get("health") or {}
    unique = health.get("unique_files_after_dedupe")
    incomplete = int(report.get("incomplete_sessions") or 0)
    unique_bit = (
        f" About {unique} unique files after dedupe." if unique is not None else ""
    )
    incomplete_bit = (
        f" {incomplete} incomplete sessions were kept as-is." if incomplete else ""
    )
    return (
        f"Done — copied {report.get('copied', 0)} files across "
        f"{report.get('sessions', 0)} sessions.{unique_bit}{incomplete_bit} "
        "Charts match that deduped set."
    )


def _compact_done_message(report: Dict[str, Any]) -> str:
    if report.get("dry_run"):
        return (
            f"Dry run — would remove {report.get('extracted_duplicates_planned', 0)} "
            f"duplicate extracted files and {report.get('raw_objects_planned', 0)} raw objects."
        )
    extracted = int(report.get("extracted_duplicates_removed") or 0)
    raw = int(report.get("raw_objects_removed") or 0)
    kept = int(report.get("unique_filenames") or 0)
    mismatch = int(report.get("size_mismatch_copies_kept") or 0)
    raw_bit = (
        f" and {raw} raw objects from batches that added nothing new" if raw else ""
    )
    mismatch_bit = (
        f" {mismatch} size-mismatch copies were left in place." if mismatch else ""
    )
    return (
        f"Removed {extracted} duplicate extracted files{raw_bit}. "
        f"{kept} filenames kept.{mismatch_bit} "
        "Charts stay unchanged until you Process staging."
    )


def _is_process_busy() -> bool:
    state = _merge_process_state()
    return bool(state.get("running"))


def _staging_inventory() -> Dict[str, Any]:
    now = time.time()
    with _INVENTORY_LOCK:
        cached = _INVENTORY_CACHE["data"]
        if isinstance(cached, dict) and (now - float(_INVENTORY_CACHE["at"])) < _INVENTORY_TTL_SEC:
            return dict(cached)
    fresh = LabelingIngestService().staging_status()
    with _INVENTORY_LOCK:
        _INVENTORY_CACHE["data"] = fresh
        _INVENTORY_CACHE["at"] = time.time()
    return dict(fresh)


@labeling_bp.route("/status", methods=["GET"])
@require_labeling_read
def labeling_status():
    """Staging vs processed output inventory + process job state."""
    try:
        status = _staging_inventory()
        status["process"] = _merge_process_state()
        collar: Dict[str, Any] = {
            "azure_configured": azure_configured(),
            "s3_prefix": (Config.LABELING_COLLAR_S3_PREFIX or "collar-raw/").rstrip("/")
            + "/",
        }
        try:
            index = LabelingCollarSyncService().load_index()
            if index:
                collar["last_index_at"] = index.get("generated_at")
                totals = (index.get("coverage") or {}).get("totals") or {}
                collar["last_matched"] = totals.get("matched")
                collar["last_missing"] = totals.get("missing")
                collar["last_ai_files"] = totals.get("ai_files")
                clone = index.get("clone")
                if isinstance(clone, dict) and clone.get("generated_at"):
                    collar["clone"] = clone
        except Exception as exc:  # noqa: BLE001
            logger.warning("Collar sync status failed: %s", redact_secrets(str(exc)))
        status["collar_sync"] = collar
        try:
            status["gmail_ingest"] = _gmail_ingest_status()
        except Exception as exc:  # noqa: BLE001
            logger.warning("Gmail ingest status failed: %s", redact_secrets(str(exc)))
        return jsonify({"success": True, "data": status})
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to get labeling status")
        return jsonify({"success": False, "error": str(exc)}), 500


collar_serial_key = serial_key


def _clean_owner_rows(rows: Any) -> list:
    """Keep rows with a serial and an owner, model or email; last row wins per serial."""
    if not isinstance(rows, list):
        raise ValueError("owners must be a list")
    by_key: Dict[str, Dict[str, str]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        key = collar_serial_key(row.get("collar_sn"))
        owner = str(row.get("owner") or "").strip()[:_COLLAR_OWNER_FIELD_MAX]
        model = str(row.get("model") or "").strip()[:_COLLAR_OWNER_FIELD_MAX]
        email = str(row.get("email") or "").strip().lower()[:_COLLAR_OWNER_FIELD_MAX]
        if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            raise ValueError(f"Not an email address for {key}: {email}")
        if key and (owner or model or email):
            by_key[key] = {"collar_sn": key, "owner": owner, "model": model, "email": email}
    return sorted(by_key.values(), key=lambda r: r["collar_sn"])


def _load_collar_owners() -> Dict[str, Any]:
    try:
        return json.loads(
            _s3_client()
            .get_object(Bucket=Config.LABELING_S3_BUCKET_NAME, Key=_COLLAR_OWNERS_KEY)["Body"]
            .read()
        )
    except Exception as exc:  # noqa: BLE001
        if "NoSuchKey" not in str(exc) and "Not Found" not in str(exc):
            logger.warning("Collar owners load failed: %s", exc)
        return {}


def _owner_collar_sns() -> list:
    """Serials on the owner list, so collar sync covers collars with no app labels yet."""
    return [r["collar_sn"] for r in _load_collar_owners().get("owners") or [] if r.get("collar_sn")]


def _load_labeler_types() -> Dict[str, str]:
    try:
        body = json.loads(
            _s3_client()
            .get_object(Bucket=Config.LABELING_S3_BUCKET_NAME, Key=_LABELER_TYPES_KEY)["Body"]
            .read()
        )
        return body.get("types") or {}
    except Exception as exc:  # noqa: BLE001
        if "NoSuchKey" not in str(exc) and "Not Found" not in str(exc):
            logger.warning("Labeler types load failed: %s", exc)
        return {}


def _configure_analyzer(analyzer: LabelingDataAnalyzer) -> LabelingDataAnalyzer:
    """Credit sessions sent through a group address to the collar owner's email."""
    analyzer.group_senders = {
        s.strip().lower() for s in (Config.LABELING_GROUP_SENDERS or "").split(",") if s.strip()
    }
    analyzer.owner_emails = {
        row["collar_sn"]: row["email"]
        for row in _load_collar_owners().get("owners") or []
        if row.get("email")
    }
    analyzer.labeler_aliases = {
        src.strip().lower(): dst.strip().lower()
        for src, sep, dst in (
            pair.partition("=") for pair in (Config.LABELING_LABELER_ALIASES or "").split(",")
        )
        if sep and src.strip() and dst.strip()
    }
    return analyzer


def _recap_lookups() -> Dict[str, Any]:
    """Owner names, owner emails, names by email and group senders, for naming labelers."""
    owner_rows = _load_collar_owners().get("owners") or []
    names_by_email: Dict[str, str] = {}
    for row in owner_rows:
        if row.get("email") and row.get("owner"):
            names_by_email.setdefault(row["email"].lower(), row["owner"])
    return {
        "owner_names": {r["collar_sn"]: r["owner"] for r in owner_rows if r.get("owner")},
        "owner_emails": {r["collar_sn"]: r["email"] for r in owner_rows if r.get("email")},
        "names_by_email": names_by_email,
        "labeler_types": _load_labeler_types(),
        "group_senders": {
            s.strip().lower()
            for s in (Config.LABELING_GROUP_SENDERS or "").split(",")
            if s.strip()
        },
    }


def _attach_overview(
    data: Dict[str, Any],
    all_data: Dict[str, Any],
    window: Optional[Tuple[str, str]] = None,
) -> None:
    """
    The dashboard Overview: the recap for the summary's period, plus the change from the
    same-length period before (the last 7 days vs the 7 before, for all time).
    """
    try:
        today = (
            date.fromisoformat(report_day(Config.LABELING_REPORT_TIMEZONE)) + timedelta(days=1)
        ).isoformat()
        start = window[0] if window and window[0] != _OPEN_START else None
        end = window[1] if window and window[1] != _OPEN_END else today
        lookups = _recap_lookups()
        recap = recap_data(end, data, all_data, start=start, **lookups)
        change_start = start or (date.fromisoformat(end) - timedelta(days=6)).isoformat()
        data["overview"] = {
            "recap": recap,
            "change": period_change(all_data, change_start, end),
            "change_is_last_7_days": start is None,
            "compensation": remote_eligibility(data, **lookups),
        }
    except Exception as exc:  # noqa: BLE001 - the rest of the summary still works
        logger.warning("Labeling overview failed: %s", exc)


def _rebuild_summary_from_snapshot() -> None:
    """Re-aggregate the all-time summary from the file snapshot, without reading S3 files."""
    snapshot = _load_file_snapshot()
    if not snapshot or snapshot.get("files") is None:
        _cache_mark_stale()
        return
    analyzer = _configure_analyzer(LabelingDataAnalyzer())
    analyzer.text_overrides = snapshot.get("texts") or {}
    raw = analyzer.analyze(include_content=True, files=files_from_snapshot(snapshot))
    data = _attach_collar_coverage(format_ui_summary(raw), raw)
    _attach_overview(data, data)
    entry = _cache_set_memory(_SUMMARY_CACHE_MEM_KEY, data, _DEFAULT_CACHE_TTL_SEC)
    _persist_summary_cache(data, entry["generated_at"], _DEFAULT_CACHE_TTL_SEC)
    _window_cache_clear()


def _rebuild_summary_in_background() -> None:
    def _worker():
        try:
            _rebuild_summary_from_snapshot()
        except Exception:  # noqa: BLE001
            logger.exception("Labeling summary rebuild after owner change failed")

    threading.Thread(target=_worker, daemon=True).start()


@labeling_bp.route("/collar-owners", methods=["GET"])
@require_labeling_read
def labeling_collar_owners():
    """The collar → owner list. Empty until someone saves one."""
    body = _load_collar_owners()
    return jsonify({
        "success": True,
        "data": {
            "owners": body.get("owners") or [],
            "updated_at": body.get("updated_at"),
        },
    })


@labeling_bp.route("/collar-owners", methods=["PUT"])
@require_admin_auth
def labeling_save_collar_owners():
    """
    Replace the collar → owner list. Body: {"owners": [{collar_sn, owner, model, email}]}.
    Owner emails change who group-sender sessions are credited to, so the summary is rebuilt.
    """
    try:
        rows = _clean_owner_rows((request.get_json(silent=True) or {}).get("owners"))
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    payload = {
        "owners": rows,
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    try:
        _s3_client().put_object(
            Bucket=Config.LABELING_S3_BUCKET_NAME,
            Key=_COLLAR_OWNERS_KEY,
            Body=json.dumps(payload).encode("utf-8"),
            ContentType="application/json",
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Collar owners save failed")
        return jsonify({"success": False, "error": str(exc)}), 500
    _rebuild_summary_in_background()
    return jsonify({"success": True, "data": payload})


@labeling_bp.route("/labeler-types", methods=["PUT"])
@require_admin_auth
def labeling_save_labeler_types():
    """
    Change saved labeler types. Body: {"types": {"<labeler name>": "employee" |
    "pack_member" | "partner" | null}}. Only the names sent change, so people outside
    the dashboard's date range keep theirs; null clears one back to the default
    (employee for a Halo email, otherwise not set).
    """
    raw = (request.get_json(silent=True) or {}).get("types")
    if not isinstance(raw, dict):
        return jsonify({"success": False, "error": "types must be an object"}), 400
    types = _load_labeler_types()
    for name, kind in raw.items():
        key = str(name or "").strip().lower()[:_COLLAR_OWNER_FIELD_MAX]
        if not key:
            continue
        if kind in (None, ""):
            types.pop(key, None)
        elif kind in LABELER_TYPES:
            types[key] = kind
        else:
            return jsonify({"success": False, "error": f"Unknown labeler type: {kind}"}), 400
    payload = {"types": types, "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    try:
        _s3_client().put_object(
            Bucket=Config.LABELING_S3_BUCKET_NAME,
            Key=_LABELER_TYPES_KEY,
            Body=json.dumps(payload).encode("utf-8"),
            ContentType="application/json",
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Labeler types save failed")
        return jsonify({"success": False, "error": str(exc)}), 500
    _rebuild_summary_in_background()
    return jsonify({"success": True, "data": payload})


# ---- Daily Slack recap ----

_REPORT_STATE_KEY = "labeling-jobs/daily_report_state.json"
# Refresh the all-time summary first when it is older than this.
_REPORT_MAX_SUMMARY_AGE_SEC = 6 * 3600
_REPORT_LOCK = threading.Lock()
# The send in progress: day, stage (refreshing, building, posting) and when it started.
_REPORT_RUNNING: Dict[str, Any] = {"day": None, "days": None, "stage": None, "started_at": None}


def _report_token() -> Optional[str]:
    return Config.LABELING_REPORT_SLACK_TOKEN or Config.SLACK_BOT_TOKEN


def _report_channels() -> List[Dict[str, str]]:
    """
    Channels the recap may post to, from LABELING_REPORT_SLACK_CHANNEL as "ID[:name]" items
    separated by commas. The first is the default, used by the scheduled run.
    """
    channels = []
    for item in (Config.LABELING_REPORT_SLACK_CHANNEL or "").split(","):
        channel_id, _, name = item.strip().partition(":")
        if channel_id.strip():
            channel_id = channel_id.strip()
            channels.append({"id": channel_id, "name": name.strip().lstrip("#") or channel_id})
    return channels


def _report_configured() -> bool:
    """A webhook URL, or at least one channel plus a bot token."""
    return bool(
        Config.LABELING_REPORT_SLACK_WEBHOOK_URL or (_report_channels() and _report_token())
    )


def _post_report(text: str, channel_ids: List[str]) -> Tuple[List[str], List[str]]:
    """Post to each channel (or the webhook). Returns the ids posted and per-channel errors."""
    if Config.LABELING_REPORT_SLACK_WEBHOOK_URL:
        post_to_slack_webhook(Config.LABELING_REPORT_SLACK_WEBHOOK_URL, text)
        return ["webhook"], []
    names = {c["id"]: c["name"] for c in _report_channels()}
    posted, errors = [], []
    for channel_id in channel_ids:
        try:
            post_to_slack(_report_token(), channel_id, text)
            posted.append(channel_id)
        except Exception as exc:  # noqa: BLE001 - keep posting to the other channels
            errors.append(f"#{names.get(channel_id, channel_id)}: {exc}")
    return posted, errors


def _report_state() -> Dict[str, Any]:
    try:
        return json.loads(
            _s3_client()
            .get_object(Bucket=Config.LABELING_S3_BUCKET_NAME, Key=_REPORT_STATE_KEY)["Body"]
            .read()
        )
    except Exception:  # noqa: BLE001
        return {}


def _save_report_state(state: Dict[str, Any]) -> None:
    try:
        _s3_client().put_object(
            Bucket=Config.LABELING_S3_BUCKET_NAME,
            Key=_REPORT_STATE_KEY,
            Body=json.dumps(state).encode("utf-8"),
            ContentType="application/json",
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to save daily report state: %s", exc)


def _report_summary_entry() -> Optional[Dict[str, Any]]:
    return _cache_get_memory(_SUMMARY_CACHE_MEM_KEY) or _load_summary_cache_s3(
        _DEFAULT_CACHE_TTL_SEC
    )


def _report_summary_stale(entry: Optional[Dict[str, Any]]) -> bool:
    return entry is None or time.time() - float(entry["generated_at"]) > _REPORT_MAX_SUMMARY_AGE_SEC


def _set_report_stage(stage: str) -> None:
    with _REPORT_LOCK:
        _REPORT_RUNNING["stage"] = stage


_REPORT_MAX_DAYS = 31


def _report_days(value: Any) -> int:
    """How many days the recap covers, ending on its day: 1 (default) up to a month."""
    try:
        days = int(value or 1)
    except (TypeError, ValueError):
        raise ValueError("days must be a whole number") from None
    if not 1 <= days <= _REPORT_MAX_DAYS:
        raise ValueError(f"days must be between 1 and {_REPORT_MAX_DAYS}")
    return days


def _build_report_text(day: str, allow_scan: bool, days: int = 1) -> str:
    """
    The recap for the days ending on day. Without allow_scan, only data already
    computed is used.
    """
    entry = _report_summary_entry()
    if entry is None and _load_file_snapshot() is not None:
        # The summary was dropped but its files are saved: re-aggregate (seconds, no scan).
        _set_report_stage("building")
        _rebuild_summary_from_snapshot()
        entry = _report_summary_entry()
    if allow_scan and _report_summary_stale(entry):
        _set_report_stage("refreshing")
        entry = _compute_summary(_DEFAULT_CACHE_TTL_SEC)
    if entry is None or (not allow_scan and _load_file_snapshot() is None):
        raise RuntimeError(
            "The labeling summary has not been built yet. Choose All time on the dashboard "
            "and click Refresh, then try again in a few minutes."
            if entry is None
            else "The saved file snapshot is missing. Choose All time on the dashboard and "
            "click Refresh, then try again in a few minutes."
        )
    window = (period_start(day, days), day)
    key = f"{window[0]}..{window[1]}"
    with _WINDOW_CACHE_LOCK:
        cached = _WINDOW_CACHE.get(key)
    if cached is None or cached["generated_at"] < float(entry["generated_at"]):
        _set_report_stage("building")
        _compute_window_summary(window)
        with _WINDOW_CACHE_LOCK:
            cached = _WINDOW_CACHE.get(key)
    return build_daily_report(
        day,
        cached["payload"],
        entry["data"],
        dashboard_url=Config.APP_BASE_URL,
        days=days,
        timezone_name=Config.LABELING_REPORT_TIMEZONE,
        **_recap_lookups(),
    )


def _send_daily_report(
    day: str, refresh: bool = True, days: int = 1, channel_ids: Optional[List[str]] = None
) -> None:
    """Build and post the recap. Without refresh it posts from data already computed."""
    state = _report_state()
    channel_ids = channel_ids or [c["id"] for c in _report_channels()[:1]]
    try:
        text = _build_report_text(day, allow_scan=refresh, days=days)
        _set_report_stage("posting")
        posted, errors = _post_report(text, channel_ids)
        if posted:
            state.update({
                "last_posted_period": f"{period_start(day, days)}..{day}",
                "last_posted_period_channels": posted,
                "last_posted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            })
            # Only a one-day recap counts as that day's daily post for the scheduled run.
            if days == 1:
                state["last_posted_day"] = day
                state["last_posted_day_channels"] = posted
        state["last_error"] = f"{day}: " + "; ".join(errors) if errors else None
    except Exception as exc:  # noqa: BLE001
        logger.exception("Labeling daily report for %s failed", day)
        state.update({"last_error": f"{day}: {redact_secrets(str(exc))}"})
    finally:
        _save_report_state(state)
        with _REPORT_LOCK:
            _REPORT_RUNNING.update({"day": None, "days": None, "stage": None, "started_at": None})


def _report_request_authorized() -> bool:
    """The scheduled job sends X-Report-Secret; a person needs an admin session."""
    secret = Config.LABELING_REPORT_SECRET
    sent = request.headers.get("X-Report-Secret") or ""
    if secret and sent and hmac.compare_digest(sent.encode(), secret.encode()):
        return True
    try:
        return bool(session.get("admin_authenticated"))
    except RuntimeError:
        return False


@labeling_bp.route("/daily-report/preview", methods=["GET"])
@require_admin_auth
def labeling_daily_report_preview():
    """The recap text for a day (default yesterday) from data already computed. Posts nothing."""
    day = (request.args.get("date") or "").strip() or report_day(Config.LABELING_REPORT_TIMEZONE)
    try:
        datetime.strptime(day, "%Y-%m-%d")
        days = _report_days(request.args.get("days"))
    except ValueError as exc:
        message = str(exc) if "days" in str(exc) else "date must be YYYY-MM-DD"
        return jsonify({"success": False, "error": message}), 400
    try:
        text = _build_report_text(day, allow_scan=False, days=days)
    except RuntimeError as exc:
        return jsonify({"success": False, "error": str(exc)}), 409
    state = _report_state()
    return jsonify({
        "success": True,
        "data": {
            "day": day,
            "days": days,
            "start": period_start(day, days),
            "text": text,
            "configured": _report_configured(),
            "last_posted_day": state.get("last_posted_day"),
            "last_posted_day_channels": state.get("last_posted_day_channels"),
            "last_posted_period": state.get("last_posted_period"),
            "last_posted_period_channels": state.get("last_posted_period_channels"),
            "last_posted_at": state.get("last_posted_at"),
            "last_error": state.get("last_error"),
            "channels": _report_channels(),
            "webhook": bool(Config.LABELING_REPORT_SLACK_WEBHOOK_URL),
        },
    })


@labeling_bp.route("/daily-report", methods=["POST"])
def labeling_send_daily_report():
    """
    Post the recap to Slack in the background.

    Body (optional): date (YYYY-MM-DD, default yesterday), days (1 by default; 7 = the week
    ending on date), channels (ids from LABELING_REPORT_SLACK_CHANNEL; default the first),
    force (re-post a period already sent to those channels),
    refresh (default true: refresh the summary first if it is over 6 hours old, which can
    take minutes; the dashboard sends false to post the preview it shows right away).
    Called daily by .github/workflows/labeling-daily-report.yml with X-Report-Secret.
    """
    if not _report_request_authorized():
        return jsonify({"success": False, "error": "Not authorized"}), 401
    if not _report_configured():
        return jsonify({
            "success": False,
            "error": "Set LABELING_REPORT_SLACK_WEBHOOK_URL on the server.",
        }), 400
    body = request.get_json(silent=True) or {}
    day = str(body.get("date") or "").strip() or report_day(Config.LABELING_REPORT_TIMEZONE)
    try:
        datetime.strptime(day, "%Y-%m-%d")
        days = _report_days(body.get("days"))
    except ValueError as exc:
        message = str(exc) if "days" in str(exc) else "date must be YYYY-MM-DD"
        return jsonify({"success": False, "error": message}), 400
    allowed = [c["id"] for c in _report_channels()]
    channel_ids = body.get("channels") or allowed[:1]
    if not isinstance(channel_ids, list) or any(c not in allowed for c in channel_ids):
        if not Config.LABELING_REPORT_SLACK_WEBHOOK_URL:
            return jsonify({"success": False, "error": "Unknown channel"}), 400
    state = _report_state()
    # Channels the same period already went to; older state without them meant the default.
    if days == 1:
        same = state.get("last_posted_day") == day
        sent_to = state.get("last_posted_day_channels") or allowed[:1]
    else:
        same = state.get("last_posted_period") == f"{period_start(day, days)}..{day}"
        sent_to = state.get("last_posted_period_channels") or allowed[:1]
    already = same and set(channel_ids) <= set(sent_to)
    if not body.get("force") and already:
        return jsonify({
            "success": True,
            "started": False,
            "day": day,
            "message": "Already posted for this day.",
        })
    with _REPORT_LOCK:
        if _REPORT_RUNNING["day"]:
            return jsonify({
                "success": True,
                "started": False,
                "day": _REPORT_RUNNING["day"],
                "message": "A report is already being sent.",
            })
        _REPORT_RUNNING.update({
            "day": day,
            "days": days,
            "stage": "starting",
            "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        })
    refresh = bool(body.get("refresh", True))
    threading.Thread(
        target=_send_daily_report, args=(day, refresh, days, channel_ids), daemon=True
    ).start()
    return jsonify({
        "success": True,
        "started": True,
        "day": day,
        "refresh_needed": refresh and _report_summary_stale(_report_summary_entry()),
    }), 202


@labeling_bp.route("/daily-report/status", methods=["GET"])
@require_admin_auth
def labeling_daily_report_status():
    """The send in progress, if any, and the last result. Cheap enough to poll."""
    with _REPORT_LOCK:
        running = dict(_REPORT_RUNNING) if _REPORT_RUNNING["day"] else None
    state = _report_state()
    return jsonify({
        "success": True,
        "data": {
            "running": running,
            "last_posted_day": state.get("last_posted_day"),
            "last_posted_at": state.get("last_posted_at"),
            "last_error": state.get("last_error"),
        },
    })


@labeling_bp.route("/promote-forwards", methods=["POST"])
@require_admin_auth
def labeling_promote_forwards():
    """
    Promote staging/_forwards/<id>/ → staging/<labeler>/<id>/.

    JSON body (optional):
      async: bool (default true)
      dry_run: bool (default false)
      message_ids: list[str] (optional subset)
    """
    try:
        body = request.get_json(silent=True) or {}
        dry_run = bool(body.get("dry_run", False))
        run_async = bool(body.get("async", True))
        message_ids = body.get("message_ids")
        if message_ids is not None and not isinstance(message_ids, list):
            return jsonify({"success": False, "error": "message_ids must be a list"}), 400

        if _is_process_busy():
            state = _merge_process_state()
            return jsonify({
                "success": False,
                "error": "A labeling job is already running",
                "data": state,
            }), 409
        if _gmail_writing_staging():
            return jsonify({"success": False, "error": _GMAIL_BUSY_ERROR}), 409

        def _run():
            return LabelingIngestService().promote_forwards(
                dry_run=dry_run,
                message_ids=message_ids,
            )

        if run_async:
            _set_process_state(
                running=True,
                job="promote-forwards",
                started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                finished_at=None,
                last_error=None,
                last_report=None,
                message="Promoting forwarded quarantine batches into staging…",
            )

            def _worker():
                log_rss(logger, "labeling promote start")
                try:
                    report = _run()
                    promoted = len(report.get("promoted") or [])
                    skipped = len(report.get("skipped") or [])
                    _set_process_state(
                        running=False,
                        job="promote-forwards",
                        finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        last_report=report,
                        last_error=None,
                        message=(
                            f"Promote done — {promoted} batch(es), {skipped} skipped. "
                            "Run Process staging to refresh charts."
                        ),
                    )
                except Exception as exc:  # noqa: BLE001
                    logger.exception("Async promote-forwards failed")
                    _set_process_state(
                        running=False,
                        job="promote-forwards",
                        finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        last_error=str(exc),
                        message="Promote forwards failed",
                    )
                finally:
                    log_rss(logger, "labeling promote end")

            threading.Thread(target=_worker, daemon=True).start()
            return jsonify({
                "success": True,
                "async": True,
                "message": "Promote started in background. Safe to leave this page.",
                "data": _merge_process_state(),
            })

        _set_process_state(
            running=True,
            job="promote-forwards",
            started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            finished_at=None,
            last_error=None,
            message="Promoting forwarded quarantine batches into staging…",
        )
        try:
            report = _run()
            promoted = len(report.get("promoted") or [])
            state = _set_process_state(
                running=False,
                job="promote-forwards",
                finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                last_report=report,
                last_error=None,
                message=f"Promote done — {promoted} batch(es)",
            )
            return jsonify({
                "success": True,
                "async": False,
                "data": report,
                "process": state,
            })
        except Exception as exc:  # noqa: BLE001
            _set_process_state(
                running=False,
                job="promote-forwards",
                finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                last_error=str(exc),
                message="Promote forwards failed",
            )
            raise
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to promote labeling forwards")
        return jsonify({"success": False, "error": str(exc)}), 500


@labeling_bp.route("/sync-collar", methods=["POST"])
@require_admin_auth
def labeling_sync_collar():
    """
    Copy Azure <sn>/ai/* for labeled collar SNs into collar-raw/, then join.

    JSON body (optional):
      dry_run: bool (default false)
      inventory_only: bool (default false)
      async: bool (default true)
    """
    try:
        if not azure_configured():
            return jsonify({
                "success": False,
                "error": (
                    "Azure collar blob is not configured. Set LABELING_AZURE_SAS_URL "
                    "or LABELING_AZURE_BLOB_URL + LABELING_AZURE_SAS_TOKEN on the server."
                ),
            }), 400

        body = request.get_json(silent=True) or {}
        dry_run = bool(body.get("dry_run", False))
        inventory_only = bool(body.get("inventory_only", False))
        run_async = bool(body.get("async", True))

        if _is_process_busy():
            state = _merge_process_state()
            return jsonify({
                "success": False,
                "error": "A labeling process job is already running",
                "data": state,
            }), 409

        start_message = (
            "Listing Azure collar ai/ dumps for labeled and owner-listed collars…"
            if inventory_only
            else "Syncing Azure collar ai/ dumps into collar-raw/…"
        )
        if run_async:
            _set_process_state(
                running=True,
                job="sync-collar",
                started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                finished_at=None,
                last_error=None,
                last_report=None,
                message=start_message,
            )

            def _worker():
                log_rss(logger, "labeling collar sync start")
                try:
                    report = LabelingCollarSyncService().sync(
                        dry_run=dry_run,
                        inventory_only=inventory_only,
                        extra_sns=_owner_collar_sns(),
                    )
                    # Only collar coverage changed: re-join it from the snapshot (seconds)
                    # and keep serving the last summary meanwhile.
                    _rebuild_summary_in_background()
                    done_message = sync_done_message(report, inventory_only)
                    _set_process_state(
                        running=False,
                        job="sync-collar",
                        finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        last_report=report,
                        last_error=None,
                        message=done_message,
                    )
                except Exception as exc:  # noqa: BLE001
                    logger.exception("Async collar sync failed")
                    _set_process_state(
                        running=False,
                        job="sync-collar",
                        finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        last_error=redact_secrets(str(exc)),
                        message="Collar sync failed",
                    )
                finally:
                    log_rss(logger, "labeling collar sync end")

            threading.Thread(target=_worker, daemon=True).start()
            return jsonify({
                "success": True,
                "async": True,
                "message": "Collar sync started in background. Safe to leave this page.",
                "data": _merge_process_state(),
            })

        _set_process_state(
            running=True,
            job="sync-collar",
            started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            finished_at=None,
            last_error=None,
            message=start_message,
        )
        try:
            report = LabelingCollarSyncService().sync(
                dry_run=dry_run,
                inventory_only=inventory_only,
                extra_sns=_owner_collar_sns(),
            )
            _rebuild_summary_in_background()
            done_message = sync_done_message(report, inventory_only)
            state = _set_process_state(
                running=False,
                job="sync-collar",
                finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                last_report=report,
                last_error=None,
                message=done_message,
            )
            return jsonify({
                "success": True,
                "async": False,
                "data": report,
                "process": state,
            })
        except Exception as exc:  # noqa: BLE001
            _set_process_state(
                running=False,
                job="sync-collar",
                finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                last_error=redact_secrets(str(exc)),
                message="Collar sync failed",
            )
            raise
    except ValueError as exc:
        return jsonify({"success": False, "error": redact_secrets(str(exc))}), 400
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to sync labeling collar data")
        return jsonify({"success": False, "error": redact_secrets(str(exc))}), 500



@labeling_bp.route("/compact", methods=["POST"])
@require_admin_auth
def labeling_compact():
    """
    Delete duplicate extracted copies under staging/<email>/<message-id>/.

    Keeps the latest message_id when file sizes match. Leaves size mismatches.
    Also deletes raw zips from batches that kept no extracted file.

    JSON body (optional):
      dry_run: bool (default false)
      async: bool (default true)
    """
    try:
        body = request.get_json(silent=True) or {}
        dry_run = bool(body.get("dry_run", False))
        run_async = bool(body.get("async", True))

        if _is_process_busy():
            state = _merge_process_state()
            return jsonify({
                "success": False,
                "error": "A labeling job is already running",
                "data": state,
            }), 409
        if _gmail_writing_staging():
            return jsonify({"success": False, "error": _GMAIL_BUSY_ERROR}), 409

        def _run():
            return LabelingIngestService().compact_staging(
                dry_run=dry_run,
                on_progress=_progress_callback("compact-staging"),
            )

        if run_async:
            _set_process_state(
                running=True,
                job="compact-staging",
                started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                finished_at=None,
                last_error=None,
                last_report=None,
                progress={"phase": "listing", "done": 0, "total": 0},
                message="Listing staging files…",
            )

            def _worker():
                try:
                    report = _run()
                    _set_process_state(
                        running=False,
                        job="compact-staging",
                        finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        last_report=report,
                        last_error=None,
                        progress=None,
                        message=_compact_done_message(report),
                    )
                except Exception as exc:  # noqa: BLE001
                    logger.exception("Async labeling compact failed")
                    _set_process_state(
                        running=False,
                        job="compact-staging",
                        finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        last_error=str(exc),
                        progress=None,
                        message="Removing duplicate copies failed",
                    )

            threading.Thread(target=_worker, daemon=True).start()
            return jsonify({
                "success": True,
                "async": True,
                "message": "Removing duplicate copies in the background.",
                "data": _merge_process_state(),
            })

        _set_process_state(
            running=True,
            job="compact-staging",
            started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            finished_at=None,
            last_error=None,
            progress={"phase": "listing", "done": 0, "total": 0},
            message="Listing staging files…",
        )
        try:
            report = _run()
            state = _set_process_state(
                running=False,
                job="compact-staging",
                finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                last_report=report,
                last_error=None,
                progress=None,
                message=_compact_done_message(report),
            )
            return jsonify({
                "success": True,
                "async": False,
                "data": report,
                "process": state,
            })
        except Exception as exc:  # noqa: BLE001
            _set_process_state(
                running=False,
                job="compact-staging",
                finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                last_error=str(exc),
                progress=None,
                message="Removing duplicate copies failed",
            )
            raise
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to compact labeling staging")
        return jsonify({"success": False, "error": str(exc)}), 500



def _should_sync_collar_after_process(
    report: Dict[str, Any], clear_output: bool, dry_run: bool, requested: bool
) -> bool:
    """New extracted files can bring new sessions and new collars, which only a sync lists."""
    if dry_run or not requested or not azure_configured():
        return False
    return clear_output or int(report.get("copied") or 0) > 0


def _sync_collar_after_process(process_message: str) -> None:
    """Run a collar sync as the tail of a process job; keeps the job running until it ends."""
    _set_process_state(
        running=True,
        job="sync-collar",
        progress=None,
        message=f"{process_message} Syncing collar logs from Azure for labeled and owner-listed collars…",
    )
    log_rss(logger, "labeling collar sync after process start")
    try:
        report = LabelingCollarSyncService().sync(
            dry_run=False, inventory_only=False, extra_sns=_owner_collar_sns()
        )
        # Process just added files, so the snapshot is behind: keep the last summary
        # but mark it for a full rescan.
        _cache_mark_stale()
        _set_process_state(
            running=False,
            job="sync-collar",
            finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            last_report=report,
            last_error=None,
            message=f"{process_message} {sync_done_message(report, False)}",
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Collar sync after process failed")
        _set_process_state(
            running=False,
            job="sync-collar",
            finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            last_error=(
                "Processing finished, but the collar sync after it failed: "
                + redact_secrets(str(exc))
            ),
            message="Collar sync after processing failed",
        )
    finally:
        log_rss(logger, "labeling collar sync after process end")


@labeling_bp.route("/process", methods=["POST"])
@require_admin_auth
def labeling_process():
    """
    Process staging/ → extracted-txt/<email>/<collar-sn>/.

    JSON body (optional):
      dry_run: bool (default false)
      clear_output: bool (default false) — wipe extracted-txt before copy
      async: bool (default true) — run in background; poll GET /status
      sync_collar: bool (default true) — async only: when new files were copied,
        sync Azure collar logs afterwards so new sessions and collars can match
    """
    try:
        body = request.get_json(silent=True) or {}
        dry_run = bool(body.get("dry_run", False))
        clear_output = bool(body.get("clear_output", False))
        sync_collar = bool(body.get("sync_collar", True))
        # Default async so browser tabs are not held open for long S3 copies
        run_async = bool(body.get("async", True))

        if _is_process_busy():
            state = _merge_process_state()
            return jsonify({
                "success": False,
                "error": "A labeling process job is already running",
                "data": state,
            }), 409
        if _gmail_writing_staging():
            return jsonify({"success": False, "error": _GMAIL_BUSY_ERROR}), 409

        if run_async:
            _set_process_state(
                running=True,
                job="process",
                started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                finished_at=None,
                last_error=None,
                last_report=None,
                progress={"phase": "listing", "done": 0, "total": 0},
                message=(
                    "Rebuilding extracted-txt from staging…"
                    if clear_output
                    else "Adding new staging files into extracted-txt…"
                ),
            )

            def _worker():
                log_rss(logger, "labeling process start")
                try:
                    report = LabelingIngestService().process_staging(
                        dry_run=dry_run,
                        clear_output=clear_output,
                        on_progress=_progress_callback("process"),
                    )
                    _refresh_summary_after_process(report, clear_output, dry_run)
                    if _should_sync_collar_after_process(
                        report, clear_output, dry_run, sync_collar
                    ):
                        _set_process_state(last_report=report)
                        _sync_collar_after_process(_process_done_message(report))
                        return
                    _set_process_state(
                        running=False,
                        job="process",
                        finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        last_report=report,
                        last_error=None,
                        progress=None,
                        message=_process_done_message(report),
                    )
                except Exception as exc:  # noqa: BLE001
                    logger.exception("Async labeling process failed")
                    _set_process_state(
                        running=False,
                        job="process",
                        finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        last_error=str(exc),
                        progress=None,
                        message="Process failed",
                    )
                finally:
                    log_rss(logger, "labeling process end")

            threading.Thread(target=_worker, daemon=True).start()
            return jsonify({
                "success": True,
                "async": True,
                "message": "Processing started in background. Safe to leave this page.",
                "data": _merge_process_state(),
            })

        _set_process_state(
            running=True,
            job="process",
            started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            finished_at=None,
            last_error=None,
            progress={"phase": "listing", "done": 0, "total": 0},
            message=(
                "Rebuilding extracted-txt from staging…"
                if clear_output
                else "Adding new staging files into extracted-txt…"
            ),
        )
        try:
            report = LabelingIngestService().process_staging(
                dry_run=dry_run,
                clear_output=clear_output,
                on_progress=_progress_callback("process"),
            )
            _refresh_summary_after_process(report, clear_output, dry_run)
            state = _set_process_state(
                running=False,
                job="process",
                finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                last_report=report,
                last_error=None,
                progress=None,
                message=_process_done_message(report),
            )
            return jsonify({"success": True, "async": False, "data": report, "process": state})
        except Exception as exc:  # noqa: BLE001
            _set_process_state(
                running=False,
                job="process",
                finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                last_error=str(exc),
                progress=None,
                message="Process failed",
            )
            raise
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to process labeling staging")
        return jsonify({"success": False, "error": str(exc)}), 500


def _without_pay_for_viewers(f):
    """Labeling viewers (outside contractors) never receive labeler pay eligibility."""

    @wraps(f)
    def decorated(*args, **kwargs):
        result = f(*args, **kwargs)
        if not is_labeling_viewer():
            return result
        response, status = (result if isinstance(result, tuple) else (result, None))
        body = response.get_json(silent=True)
        overview = ((body or {}).get("data") or {}).get("overview")
        if isinstance(overview, dict) and "compensation" in overview:
            overview.pop("compensation")
            response.set_data(json.dumps(body))
        return (response, status) if status is not None else response

    return decorated


@labeling_bp.route("/summary", methods=["GET"])
@require_labeling_read
@_without_pay_for_viewers
def labeling_summary():
    """
    Summarize processed labeling exports under extracted-txt/.

    Serves the last computed summary immediately when available (memory, then S3).
    A cold cache or refresh=1 starts a background rescan and returns pending.
    The scan never runs on this request, so a health check can still get through.

    Query params:
      refresh=1  — start a background rescan (last summary is still returned)
      ttl=900    — freshness window seconds (stale after this; 0 = always stale)
      start, end — optional YYYY-MM-DD; only sessions and collar logs on those days
                   (inclusive) are counted. Built and cached apart from the full summary.
    """
    try:
        # Viewers read what is there; only admins start a rescan.
        refresh = (
            request.args.get("refresh", "").lower() in ("1", "true", "yes")
            and not is_labeling_viewer()
        )
        try:
            ttl = int(request.args.get("ttl", _DEFAULT_CACHE_TTL_SEC))
        except ValueError:
            ttl = _DEFAULT_CACHE_TTL_SEC

        # A tiny ttl would make every poll start a rescan; viewers get the default.
        ttl_sec = ttl if ttl > 0 and not is_labeling_viewer() else _DEFAULT_CACHE_TTL_SEC
        window = _parse_window(request.args)
        if window is not None:
            return _window_summary_response(window, refresh, ttl_sec)
        entry = _cache_get_memory(_SUMMARY_CACHE_MEM_KEY)
        if entry is None:
            entry = _load_summary_cache_s3(ttl_sec)
        if entry is not None and not refresh:
            if entry.get("stale"):
                _maybe_start_background_refresh(ttl_sec)
            return jsonify(
                {
                    "success": True,
                    "pending": False,
                    "cached": True,
                    "stale": bool(entry.get("stale")),
                    "generated_at": entry.get("generated_at_iso"),
                    "data": _client_summary(entry["data"]),
                }
            )

        # A full scan downloads every labeling file. Doing that inside the
        # request is what stalls health checks. Always scan in the background.
        started = _maybe_start_background_refresh(ttl_sec)
        if not started:
            message = "Summary refresh waits until the current labeling job finishes."
        elif entry is not None:
            message = "Refreshing the summary in the background."
        else:
            message = "Building the summary in the background."
        return jsonify(
            {
                "success": True,
                "pending": True,
                "cached": entry is not None,
                "stale": True,
                "generated_at": entry.get("generated_at_iso") if entry else None,
                "data": _client_summary(entry["data"]) if entry else None,
                "blocked_by": None if started else _blocking_job(),
                "message": message,
            }
        )
    except ValueError as exc:
        logger.warning("Labeling summary misconfigured: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to build labeling summary")
        return jsonify({"success": False, "error": str(exc)}), 500


@labeling_bp.route("/sessions", methods=["GET"])
@require_labeling_read
def labeling_sessions():
    """
    One labeler's sessions, newest first, from the summary already computed
    (all time, or the start/end range). Never scans.

    Query params:
      user         — labeler email (required)
      family       — activity (default) | gps
      start, end   — optional YYYY-MM-DD, same as /summary
    """
    user = (request.args.get("user") or "").strip().lower()
    if not user:
        return jsonify({"success": False, "error": "user is required"}), 400
    family = request.args.get("family") or "activity"
    if family not in ("activity", "gps"):
        return jsonify({"success": False, "error": "family must be activity or gps"}), 400
    try:
        window = _parse_window(request.args)
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400

    if window is not None:
        with _WINDOW_CACHE_LOCK:
            cached = _WINDOW_CACHE.get(f"{window[0]}..{window[1]}")
        data = cached["payload"] if cached else None
    else:
        entry = _cache_get_memory(_SUMMARY_CACHE_MEM_KEY) or _load_summary_cache_s3(
            _DEFAULT_CACHE_TTL_SEC
        )
        data = entry["data"] if entry else None
    if data is None:
        return jsonify({
            "success": True,
            "pending": True,
            "sessions": [],
            "message": "Stats for this range are not built yet.",
        })
    source = (data.get("gps") or {}) if family == "gps" else data
    log = source.get("session_log")
    if log is None:
        # Summary built before session logs existed.
        return jsonify({
            "success": True,
            "pending": False,
            "needs_refresh": True,
            "sessions": [],
            "message": "Session logs appear after the next summary refresh.",
        })
    rows = [row for row in log if (row.get("email") or "").lower() == user]
    rows.sort(key=lambda r: (r.get("timestamp") or "", r.get("session_id") or ""), reverse=True)
    return jsonify({"success": True, "pending": False, "sessions": rows})


_ML_CACHE_LOCK = threading.Lock()
_ML_CACHE: Dict[str, Any] = {
    "payload": None,
    "generated_at": 0.0,
    "fresh_until": 0.0,
}
_ML_INDEX_KEY = "labeling-jobs/ml_processed_index_v1.json"
_ML_BG_LOCK = threading.Lock()
_ML_BG_RUNNING = False


def _ml_cache_get() -> Optional[Dict[str, Any]]:
    with _ML_CACHE_LOCK:
        if _ML_CACHE["payload"] is None:
            return None
        return _cache_entry(
            _ML_CACHE["payload"],
            float(_ML_CACHE["generated_at"] or 0),
            float(_ML_CACHE["fresh_until"] or 0),
        )


def _ml_cache_set(
    payload: Dict[str, Any], ttl_sec: int, generated_at: Optional[float] = None
) -> Dict[str, Any]:
    now = time.time()
    gen = float(generated_at if generated_at is not None else now)
    fresh_until = gen + max(0, ttl_sec)
    with _ML_CACHE_LOCK:
        _ML_CACHE["payload"] = payload
        _ML_CACHE["generated_at"] = gen
        _ML_CACHE["fresh_until"] = fresh_until
    return _cache_entry(payload, gen, fresh_until)


def _persist_ml_index(payload: Dict[str, Any], generated_at: float, ttl_sec: int) -> None:
    bucket = Config.LABELING_S3_BUCKET_NAME
    if not bucket:
        return
    try:
        body = {
            "generated_at": generated_at,
            "generated_at_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(generated_at)),
            "ttl_sec": ttl_sec,
            "data": payload,
        }
        _s3_client().put_object(
            Bucket=bucket,
            Key=_ML_INDEX_KEY,
            Body=json.dumps(body).encode("utf-8"),
            ContentType="application/json",
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to persist collar-log index: %s", exc)


def _load_ml_index(ttl_sec: int) -> Optional[Dict[str, Any]]:
    bucket = Config.LABELING_S3_BUCKET_NAME
    if not bucket:
        return None
    try:
        raw = _s3_client().get_object(Bucket=bucket, Key=_ML_INDEX_KEY)["Body"].read()
        body = json.loads(raw.decode("utf-8"))
        if not isinstance(body, dict) or not isinstance(body.get("data"), dict):
            return None
        generated_at = float(body.get("generated_at") or 0)
        if generated_at <= 0 and body.get("generated_at_iso"):
            try:
                generated_at = datetime.strptime(
                    body["generated_at_iso"], "%Y-%m-%dT%H:%M:%SZ"
                ).replace(tzinfo=timezone.utc).timestamp()
            except Exception:  # noqa: BLE001
                generated_at = time.time()
        return _ml_cache_set(body["data"], ttl_sec, generated_at=generated_at)
    except Exception:  # noqa: BLE001
        return None


def _compute_ml_index(ttl_sec: int) -> Dict[str, Any]:
    data = MlProcessedInventory().build()
    entry = _ml_cache_set(data, ttl_sec)
    _persist_ml_index(data, entry["generated_at"], ttl_sec)
    logger.info(
        "Collar-log index built: %s sessions, %s collars",
        (data.get("totals") or {}).get("sessions"),
        (data.get("totals") or {}).get("collars"),
    )
    return entry


def _maybe_refresh_ml_index(ttl_sec: int) -> None:
    global _ML_BG_RUNNING
    with _ML_BG_LOCK:
        if _ML_BG_RUNNING:
            return
        _ML_BG_RUNNING = True

    def _worker():
        global _ML_BG_RUNNING
        try:
            logger.info("Background collar-log index refresh started")
            _compute_ml_index(ttl_sec)
            logger.info("Background collar-log index refresh finished")
        except Exception:  # noqa: BLE001
            logger.exception("Background collar-log index refresh failed")
        finally:
            with _ML_BG_LOCK:
                _ML_BG_RUNNING = False

    threading.Thread(target=_worker, daemon=True).start()


@labeling_bp.route("/ml-processed", methods=["GET"])
@require_admin_auth
def labeling_ml_processed():
    """
    Inventory collar logs under ml-processed/.

    Serves the last index immediately when one exists (memory, then S3).
    A stale index is returned while a background rescan runs. A synchronous
    rescan happens when no cache exists or refresh=1.

    Query params:
      refresh=1  — force synchronous rescan
      ttl=900    — freshness window seconds
    """
    try:
        refresh = request.args.get("refresh", "").lower() in ("1", "true", "yes")
        try:
            ttl = int(request.args.get("ttl", _DEFAULT_CACHE_TTL_SEC))
        except ValueError:
            ttl = _DEFAULT_CACHE_TTL_SEC
        ttl = ttl if ttl > 0 else _DEFAULT_CACHE_TTL_SEC

        if not refresh:
            entry = _ml_cache_get()
            if entry is None:
                entry = _load_ml_index(ttl)
            if entry is not None:
                if entry.get("stale"):
                    _maybe_refresh_ml_index(ttl)
                return jsonify(
                    {
                        "success": True,
                        "cached": True,
                        "stale": bool(entry.get("stale")),
                        "generated_at": entry.get("generated_at_iso"),
                        "data": entry["data"],
                    }
                )

        entry = _compute_ml_index(ttl)
        return jsonify(
            {
                "success": True,
                "cached": False,
                "stale": False,
                "generated_at": entry.get("generated_at_iso"),
                "data": entry["data"],
            }
        )
    except ValueError as exc:
        logger.warning("Collar-log index misconfigured: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to build collar-log index")
        return jsonify({"success": False, "error": str(exc)}), 500


@labeling_bp.route("/ml-processed/download", methods=["GET"])
@require_admin_auth
def labeling_ml_download():
    """Return a short-lived URL for one object under the collar-log prefix."""
    key = (request.args.get("key") or "").strip()
    prefix = Config.LABELING_S3_ML_PREFIX or "ml-processed/"
    if not ml_object_key_allowed(key, prefix):
        return jsonify({"success": False, "error": "Key is outside the collar-log prefix"}), 400
    bucket = Config.LABELING_S3_BUCKET_NAME
    if not bucket:
        return jsonify({"success": False, "error": "LABELING_S3_BUCKET_NAME is not configured"}), 400
    try:
        url = _s3_client().generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=300,
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to sign collar-log download")
        return jsonify({"success": False, "error": str(exc)}), 500
    return jsonify({"success": True, "url": url, "key": key})


# ---------------------------------------------------------------------------
# Gmail ingester: reads the inbox the ai_logs group delivers to and writes
# staging batches (docs/LABELING_GMAIL_INGEST.md). Runs beside Make.com: in
# shadow mode it writes to its own prefix, in live mode into staging/.

_GMAIL_LOCK = threading.Lock()  # held for the whole of one run
_GMAIL_STATE: Dict[str, Any] = {
    "running": False,
    "kind": None,  # "poll" | "backfill" | "run"
    "started_at": None,
    "finished_at": None,
    "message": None,
    "last_error": None,
    "last_report": None,
    "poller_started_at": None,
    "last_compare_at": 0.0,
}
_GMAIL_POLLER: Optional[threading.Thread] = None
_GMAIL_FIRST_POLL_DELAY_SEC = 30
_GMAIL_COMPARE_EVERY_SEC = 60 * 60
_GMAIL_STATUS_CACHE: Dict[str, Any] = {"at": 0.0, "data": None}
# Jobs that read or rewrite staging/ wait while a live run is writing into it.
_GMAIL_BUSY_ERROR = "The Gmail ingester is writing new uploads into staging; try again in a minute"


def _gmail_writing_staging() -> bool:
    with _PROCESS_LOCK:
        running = bool(_GMAIL_STATE["running"])
    return running and (Config.LABELING_GMAIL_INGEST_MODE or "shadow").lower() == "live"


def _gmail_report_summary(report: Dict[str, Any]) -> Dict[str, Any]:
    out = {k: v for k, v in report.items() if k not in ("batches", "warnings", "errors")}
    out["errors"] = report.get("errors", [])[:20]
    out["warnings"] = report.get("warnings", [])[:20]
    out["batches"] = report.get("batches", [])[:50]
    return out


def run_gmail_ingest(
    kind: str,
    since: Optional[datetime] = None,
    until: Optional[datetime] = None,
    dry_run: bool = False,
) -> Optional[Dict[str, Any]]:
    """One ingest run. Returns None when another run holds the lock."""
    from backend.services.labeling_gmail_ingest_service import LabelingGmailIngestService

    if not _GMAIL_LOCK.acquire(blocking=False):
        return None
    try:
        with _PROCESS_LOCK:
            _GMAIL_STATE.update(
                running=True,
                kind=kind,
                started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                finished_at=None,
                message="Checking the inbox…",
            )
        service = LabelingGmailIngestService()

        def _on_progress(message: str) -> None:
            with _PROCESS_LOCK:
                _GMAIL_STATE["message"] = message

        report = service.run(since=since, until=until, dry_run=dry_run, on_progress=_on_progress)
        if service.mode == "live" and not dry_run and (report["ingested"] or report["quarantined"]):
            with _INVENTORY_LOCK:
                _INVENTORY_CACHE["at"] = 0.0
        compare_due = time.time() - float(_GMAIL_STATE["last_compare_at"]) > _GMAIL_COMPARE_EVERY_SEC
        if service.mode == "shadow" and not dry_run and (kind != "poll" or compare_due or report["ingested"]):
            try:
                service.save_compare(service.compare_with_make())
                _GMAIL_STATE["last_compare_at"] = time.time()
            except Exception as exc:  # noqa: BLE001
                logger.warning("Gmail vs Make comparison failed: %s", exc)
        with _PROCESS_LOCK:
            _GMAIL_STATE.update(
                last_report=_gmail_report_summary(report),
                last_error=None,
                message=(
                    f"Ingested {report['ingested']} email(s)"
                    + (f", {report['quarantined']} to forwards" if report["quarantined"] else "")
                    + (f", {len(report['errors'])} error(s)" if report["errors"] else "")
                    + (" (dry run)" if dry_run else "")
                ),
            )
        _GMAIL_STATUS_CACHE["at"] = 0.0
        return report
    except Exception as exc:  # noqa: BLE001
        logger.exception("Gmail ingest run failed")
        with _PROCESS_LOCK:
            _GMAIL_STATE.update(last_error=redact_secrets(str(exc)), message="Gmail ingest failed")
        _GMAIL_STATUS_CACHE["at"] = 0.0
        raise
    finally:
        with _PROCESS_LOCK:
            _GMAIL_STATE.update(
                running=False,
                finished_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            )
        _GMAIL_LOCK.release()


def _gmail_poll_once() -> None:
    live = (Config.LABELING_GMAIL_INGEST_MODE or "shadow").lower() == "live"
    if live and _is_process_busy():
        logger.info("Gmail ingest poll skipped: a labeling job is running")
        return
    try:
        run_gmail_ingest("poll")
    except Exception:  # noqa: BLE001
        pass  # logged and kept in _GMAIL_STATE; the next poll tries again


def _gmail_poll_loop() -> None:
    time.sleep(_GMAIL_FIRST_POLL_DELAY_SEC)
    while True:
        _gmail_poll_once()
        time.sleep(max(60, int(Config.LABELING_GMAIL_INGEST_POLL_SEC or 300)))


def start_gmail_ingest_poller() -> bool:
    """Start the background poll once per process, when enabled."""
    global _GMAIL_POLLER
    if not Config.LABELING_GMAIL_INGEST_ENABLED:
        return False
    with _PROCESS_LOCK:
        if _GMAIL_POLLER is not None and _GMAIL_POLLER.is_alive():
            return False
        _GMAIL_POLLER = threading.Thread(target=_gmail_poll_loop, name="gmail-ingest", daemon=True)
        _GMAIL_POLLER.start()
        _GMAIL_STATE["poller_started_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    logger.info(
        "Gmail ingest poller started (%s mode, every %ss)",
        Config.LABELING_GMAIL_INGEST_MODE,
        Config.LABELING_GMAIL_INGEST_POLL_SEC,
    )
    return True


def _gmail_ingest_status() -> Dict[str, Any]:
    """The `gmail_ingest` block of /status: last run, counts, errors, Make comparison."""
    mode = (Config.LABELING_GMAIL_INGEST_MODE or "shadow").lower()
    poll_sec = int(Config.LABELING_GMAIL_INGEST_POLL_SEC or 300)
    with _PROCESS_LOCK:
        live = {
            k: _GMAIL_STATE[k]
            for k in ("running", "kind", "started_at", "finished_at", "message", "last_error", "poller_started_at")
        }
        last_report = _GMAIL_STATE["last_report"]
    out: Dict[str, Any] = {
        "enabled": bool(Config.LABELING_GMAIL_INGEST_ENABLED),
        "configured": bool(Config.LABELING_GMAIL_SERVICE_ACCOUNT_JSON),
        "mode": mode,
        "mailbox": Config.LABELING_GMAIL_INGEST_MAILBOX,
        "target_prefix": (
            Config.LABELING_S3_STAGING_PREFIX
            if mode == "live"
            else Config.LABELING_GMAIL_SHADOW_PREFIX
        ),
        "poll_sec": poll_sec,
        **live,
    }
    if last_report and last_report.get("dry_run"):
        out["last_dry_run"] = last_report
    now = time.time()
    cached = _GMAIL_STATUS_CACHE["data"]
    if not (isinstance(cached, dict) and now - float(_GMAIL_STATUS_CACHE["at"]) < _INVENTORY_TTL_SEC):
        cached = {}
        try:
            from backend.services.labeling_gmail_ingest_service import LabelingGmailIngestService

            service = LabelingGmailIngestService()
            state = service.load_state()
            cached = {
                "last_run": state.get("last_run"),
                "last_ingest_at": state.get("last_ingest_at"),
                "first_run_at": state.get("first_run_at"),
                "totals": state.get("totals"),
                "recent_errors": (state.get("recent_errors") or [])[-5:],
                "retrying": len(state.get("failures") or {}),
                "compare": service.load_compare(),
            }
        except Exception as exc:  # noqa: BLE001
            cached = {"state_error": redact_secrets(str(exc))}
        _GMAIL_STATUS_CACHE.update(at=now, data=cached)
    out.update(cached)
    # Stalled: enabled, but no finished run for three poll intervals.
    finished = (out.get("last_run") or {}).get("finished_at")
    stalled = False
    if out["enabled"] and out.get("poller_started_at"):
        try:
            ref = finished or out["poller_started_at"]
            last = datetime.strptime(ref, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            age = (datetime.now(timezone.utc) - last).total_seconds()
            stalled = age > 3 * poll_sec + _GMAIL_FIRST_POLL_DELAY_SEC
        except Exception:  # noqa: BLE001
            stalled = False
    out["stalled"] = stalled
    return out


@labeling_bp.route("/gmail-ingest/run", methods=["POST"])
@require_admin_auth
def labeling_gmail_ingest_run():
    """
    Run the Gmail ingester now, or backfill from a date.

    JSON body (optional):
      since: "YYYY-MM-DD" — backfill from this date (UTC) instead of the cursor
      until: "YYYY-MM-DD" — stop before this date
      dry_run: bool (default false) — list and parse only; write nothing
    """
    from backend.services.labeling_gmail_ingest_service import parse_since

    body = request.get_json(silent=True) or {}
    try:
        since = parse_since(body["since"]) if body.get("since") else None
        until = parse_since(body["until"]) if body.get("until") else None
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    if not Config.LABELING_GMAIL_SERVICE_ACCOUNT_JSON:
        return jsonify({
            "success": False,
            "error": "LABELING_GMAIL_SERVICE_ACCOUNT_JSON is not configured on the server",
        }), 400
    dry_run = bool(body.get("dry_run", False))
    live = (Config.LABELING_GMAIL_INGEST_MODE or "shadow").lower() == "live"
    if live and not dry_run and _is_process_busy():
        return jsonify({
            "success": False,
            "error": "A labeling job is running; backfill once it finishes",
            "data": _merge_process_state(),
        }), 409
    if _GMAIL_LOCK.locked():
        return jsonify({
            "success": False,
            "error": "A Gmail ingest run is already in progress",
            "data": _gmail_ingest_status(),
        }), 409

    def _worker():
        try:
            run_gmail_ingest("backfill" if since else "run", since=since, until=until, dry_run=dry_run)
        except Exception:  # noqa: BLE001
            pass  # kept in _GMAIL_STATE["last_error"]

    threading.Thread(target=_worker, daemon=True).start()
    return jsonify({
        "success": True,
        "async": True,
        "message": (
            f"Gmail backfill from {body['since']} started." if since else "Gmail ingest started."
        ),
        "data": _gmail_ingest_status(),
    })


@labeling_bp.route("/gmail-ingest/compare", methods=["POST"])
@require_admin_auth
def labeling_gmail_ingest_compare():
    """Compare Gmail shadow batches with Make's staging/ now. Body: {since?: "YYYY-MM-DD"}."""
    from backend.services.labeling_gmail_ingest_service import (
        LabelingGmailIngestService,
        parse_since,
    )

    body = request.get_json(silent=True) or {}
    try:
        since = parse_since(body["since"]) if body.get("since") else None
        service = LabelingGmailIngestService(mode="shadow")
        result = service.compare_with_make(since=since)
        service.save_compare(result)
        _GMAIL_STATUS_CACHE["at"] = 0.0
        return jsonify({"success": True, "data": result})
    except ValueError as exc:
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception as exc:  # noqa: BLE001
        logger.exception("Gmail vs Make comparison failed")
        return jsonify({"success": False, "error": redact_secrets(str(exc))}), 500
