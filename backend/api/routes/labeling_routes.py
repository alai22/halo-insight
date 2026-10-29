"""
API routes for Halo AI labeling: staging process + summaries.
"""

from __future__ import annotations

import json
import threading
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import boto3
from flask import Blueprint, jsonify, request

from backend.api.middleware.auth import require_admin_auth
from backend.services.labeling_data_analyzer import LabelingDataAnalyzer, format_ui_summary
from backend.services.labeling_collar_sync_service import (
    LabelingCollarSyncService,
    azure_configured,
    redact_secrets,
)
from backend.services.labeling_ingest_service import LabelingIngestService
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
_STALE_RUNNING_SEC = 2 * 60 * 60  # allow restart if marked running > 2h
_PROCESS_STATUS_KEY = "labeling-jobs/process_status.json"
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


def _attach_collar_coverage(data: Dict[str, Any], raw: Dict[str, Any]) -> Dict[str, Any]:
    """Join mirrored collar-raw/ AI dumps onto the UI summary."""
    try:
        coverage = LabelingCollarSyncService().build_coverage(summary=raw)
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
    analyzer = LabelingDataAnalyzer()
    raw = analyzer.analyze(include_content=True)
    data = _attach_collar_coverage(format_ui_summary(raw), raw)
    entry = _cache_set_memory(_SUMMARY_CACHE_MEM_KEY, data, ttl_sec)
    _persist_summary_cache(data, entry["generated_at"], ttl_sec)
    return entry


def _maybe_start_background_refresh(ttl_sec: int) -> bool:
    """Start one summary scan off the request thread. False when a job is busy."""
    global _BG_REFRESH_RUNNING
    if _is_process_busy():
        logger.info("Deferring labeling summary refresh until the current job finishes")
        return False
    with _BG_REFRESH_LOCK:
        if _BG_REFRESH_RUNNING:
            return True
        _BG_REFRESH_RUNNING = True

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
    # If S3 says running but started long ago, treat as stale
    if persisted.get("running") and persisted.get("started_at"):
        try:
            started = datetime.strptime(
                persisted["started_at"], "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=timezone.utc)
            age = (datetime.now(timezone.utc) - started).total_seconds()
            if age > _STALE_RUNNING_SEC:
                persisted = {
                    **persisted,
                    "running": False,
                    "last_error": persisted.get("last_error")
                    or "Process marked stale (exceeded 2h); you can start again.",
                    "message": "Stale job cleared",
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
            "last_error": persisted.get("last_error"),
            "last_report": persisted.get("last_report"),
            "message": persisted.get("message"),
            "progress": _progress_value(persisted.get("progress")),
        }
    )


def _set_process_state(**kwargs: Any) -> Dict[str, Any]:
    with _PROCESS_LOCK:
        _PROCESS_STATE.update(kwargs)
        snap = _process_fields()
    _persist_process_state(snap)
    return _annotate_runtime(snap)


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


def _is_process_busy() -> bool:
    state = _merge_process_state()
    return bool(state.get("running"))


@labeling_bp.route("/status", methods=["GET"])
@require_admin_auth
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
        return jsonify({"success": True, "data": status})
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to get labeling status")
        return jsonify({"success": False, "error": str(exc)}), 500


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
            "Listing Azure collar ai/ dumps for labeled collars…"
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
                    )
                    _cache_clear()
                    matched = ((report.get("coverage") or {}).get("totals") or {}).get(
                        "matched", 0
                    )
                    missing = ((report.get("coverage") or {}).get("totals") or {}).get(
                        "missing", 0
                    )
                    clone = report.get("clone") or {}
                    if inventory_only:
                        done_message = (
                            f"Azure check done — {clone.get('azure_files', report.get('listed', 0))} "
                            f"files in Azure, {clone.get('not_cloned', 0)} not in S3"
                        )
                    else:
                        done_message = (
                            f"Collar sync done — copied {report.get('copied', 0)} files, "
                            f"{matched} sessions matched, {missing} missing"
                        )
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
            )
            _cache_clear()
            clone = report.get("clone") or {}
            if inventory_only:
                done_message = (
                    f"Azure check done — {clone.get('azure_files', report.get('listed', 0))} "
                    f"files in Azure, {clone.get('not_cloned', 0)} not in S3"
                )
            else:
                done_message = f"Done — copied {report.get('copied', 0)} files"
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



@labeling_bp.route("/process", methods=["POST"])
@require_admin_auth
def labeling_process():
    """
    Process staging/ → extracted-txt/<email>/<collar-sn>/.

    JSON body (optional):
      dry_run: bool (default false)
      clear_output: bool (default false) — wipe extracted-txt before copy
      async: bool (default true) — run in background; poll GET /status
    """
    try:
        body = request.get_json(silent=True) or {}
        dry_run = bool(body.get("dry_run", False))
        clear_output = bool(body.get("clear_output", False))
        # Default async so browser tabs are not held open for long S3 copies
        run_async = bool(body.get("async", True))

        if _is_process_busy():
            state = _merge_process_state()
            return jsonify({
                "success": False,
                "error": "A labeling process job is already running",
                "data": state,
            }), 409

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


@labeling_bp.route("/summary", methods=["GET"])
@require_admin_auth
def labeling_summary():
    """
    Summarize processed labeling exports under extracted-txt/.

    Serves the last computed summary immediately when available (memory, then S3).
    A cold cache or refresh=1 starts a background rescan and returns pending.
    The scan never runs on this request, so a health check can still get through.

    Query params:
      refresh=1  — start a background rescan (last summary is still returned)
      ttl=900    — freshness window seconds (stale after this; 0 = always stale)
    """
    try:
        refresh = request.args.get("refresh", "").lower() in ("1", "true", "yes")
        try:
            ttl = int(request.args.get("ttl", _DEFAULT_CACHE_TTL_SEC))
        except ValueError:
            ttl = _DEFAULT_CACHE_TTL_SEC

        ttl_sec = ttl if ttl > 0 else _DEFAULT_CACHE_TTL_SEC
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
                    "data": entry["data"],
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
                "data": entry["data"] if entry else None,
                "message": message,
            }
        )
    except ValueError as exc:
        logger.warning("Labeling summary misconfigured: %s", exc)
        return jsonify({"success": False, "error": str(exc)}), 400
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to build labeling summary")
        return jsonify({"success": False, "error": str(exc)}), 500
