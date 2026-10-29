"""Process liveness numbers for /health and the labeling dashboard.

Reads RSS from /proc so a health check does not touch S3, Azure, or Claude.
"""

from __future__ import annotations

import os
import threading
import time
from typing import Any, Dict, Optional

_LOCK = threading.Lock()
_PEAK_RSS_KB = 0
_STARTED_AT = time.time()
_STARTED_AT_ISO = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(_STARTED_AT))

# t3.medium is 4 GiB. Warn in logs before the container cap (default 2800m) is hit.
_WARN_RSS_MB = 2200


def env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or not str(raw).strip():
        return default
    try:
        return max(1, int(raw))
    except ValueError:
        return default


def rss_kb() -> Optional[int]:
    try:
        with open("/proc/self/status", "r", encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("VmRSS:"):
                    kb = int(line.split()[1])
                    global _PEAK_RSS_KB
                    with _LOCK:
                        if kb > _PEAK_RSS_KB:
                            _PEAK_RSS_KB = kb
                    return kb
    except Exception:  # noqa: BLE001
        return None
    return None


def snapshot() -> Dict[str, Any]:
    kb = rss_kb()
    with _LOCK:
        peak = _PEAK_RSS_KB
    return {
        "rss_mb": round(kb / 1024, 1) if kb is not None else None,
        "peak_rss_mb": round(peak / 1024, 1) if peak else None,
        "started_at": _STARTED_AT_ISO,
        "uptime_sec": int(time.time() - _STARTED_AT),
    }


def log_rss(logger: Any, label: str) -> Dict[str, Any]:
    snap = snapshot()
    rss = snap.get("rss_mb")
    message = "%s rss_mb=%s peak_rss_mb=%s uptime_sec=%s"
    args = (label, rss, snap.get("peak_rss_mb"), snap.get("uptime_sec"))
    if isinstance(rss, (int, float)) and rss >= _WARN_RSS_MB:
        logger.warning(
            message + " — memory is high; the container cap should restart the app before the instance dies",
            *args,
        )
    else:
        logger.info(message, *args)
    return snap


def build_liveness(job: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Cheap JSON body for load-balancer and Docker health checks."""
    body: Dict[str, Any] = {"status": "ok", **snapshot()}
    job = job or {}
    body["job_running"] = bool(job.get("running"))
    body["job"] = job.get("job")
    body["job_message"] = job.get("message")
    return body
