"""Process liveness numbers for /health and the labeling dashboard.

Reads RSS from /proc so a health check does not touch S3, Azure, or Claude.
"""

from __future__ import annotations

import calendar
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


def build_info() -> Dict[str, Optional[str]]:
    """The deployed commit, set by deploy.sh; None when run outside a deploy."""
    return {
        "commit": os.environ.get("APP_COMMIT") or None,
        "subject": os.environ.get("APP_COMMIT_SUBJECT") or None,
        "deployed_at": os.environ.get("APP_DEPLOYED_AT") or None,
    }


def build_liveness(job: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Cheap JSON body for load-balancer and Docker health checks."""
    body: Dict[str, Any] = {"status": "ok", **snapshot(), "build": build_info()}
    job = job or {}
    body["job_running"] = bool(job.get("running"))
    body["job"] = job.get("job")
    body["job_message"] = job.get("message")
    return body


def _human_duration(seconds: float) -> str:
    seconds = max(0, int(seconds))
    days, rest = divmod(seconds, 86400)
    hours, rest = divmod(rest, 3600)
    minutes = rest // 60
    if days:
        return f"{days}d {hours}h"
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def _since(iso: Optional[str], now: float) -> str:
    """'2026-11-01 03:33 UTC (14h 34m ago)' for a UTC timestamp, or 'unknown'."""
    if not iso:
        return "unknown"
    try:
        then = calendar.timegm(time.strptime(iso, "%Y-%m-%dT%H:%M:%SZ"))
    except ValueError:
        return iso
    return f"{iso[:10]} {iso[11:16]} UTC ({_human_duration(now - then)} ago)"


def render_liveness_html(body: Dict[str, Any], now: Optional[float] = None) -> str:
    """The /health JSON as a small page for people. Probes and scripts keep getting JSON."""
    from html import escape

    now = time.time() if now is None else now
    ok = body.get("status") == "ok"
    build = body.get("build") or {}
    rss = body.get("rss_mb")
    peak = body.get("peak_rss_mb")
    memory = (
        f"{rss:,.0f} MB now · peak {peak:,.0f} MB"
        + (" · high, nearing the container limit" if rss and rss >= _WARN_RSS_MB else "")
        if rss is not None
        else "unknown"
    )
    if body.get("job_running"):
        job = f"Running {escape(str(body.get('job') or 'a job'))}"
        if body.get("job_message"):
            job += f": {escape(str(body['job_message']))}"
    else:
        job = "Idle"
    commit = escape(build.get("commit") or "not recorded")
    subject = escape(build.get("subject") or "")
    uptime = _human_duration(body.get("uptime_sec") or 0)
    started_iso = body.get("started_at") or ""
    started = f"{started_iso[:10]} {started_iso[11:16]} UTC" if started_iso else "unknown"
    subject_html = f"<div class='sub'>{subject}</div>" if subject else ""
    rows = [
        ("Running build", f"<code>{commit}</code>{subject_html}"),
        ("Deployed", escape(_since(build.get("deployed_at"), now))),
        ("Up for", escape(f"{uptime} (since {started})")),
        ("Memory", escape(memory)),
        ("Labeling job", job),
    ]
    table = "".join(f"<tr><th>{label}</th><td>{value}</td></tr>" for label, value in rows)
    pill_bg, pill_fg = ("#d1fae5", "#065f46") if ok else ("#fee2e2", "#991b1b")
    status_label = "OK" if ok else escape(str(body.get("status") or "unknown")).upper()
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="30">
<title>Halo Insight · Server health</title>
<style>
  body {{ font: 15px/1.5 -apple-system, system-ui, sans-serif; background: #f9fafb;
          color: #111827; margin: 0; }}
  main {{ max-width: 640px; margin: 48px auto; padding: 0 16px; }}
  h1 {{ font-size: 20px; margin: 0 0 4px; }}
  .pill {{ display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: 13px;
          font-weight: 600; background: {pill_bg}; color: {pill_fg}; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: #fff;
           border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; }}
  th, td {{ text-align: left; padding: 10px 14px; border-top: 1px solid #f3f4f6;
            vertical-align: top; }}
  tr:first-child th, tr:first-child td {{ border-top: 0; }}
  th {{ width: 140px; color: #6b7280; font-weight: 500; }}
  code {{ font: 13px ui-monospace, Menlo, monospace; }}
  .sub {{ color: #6b7280; font-size: 13px; }}
  footer {{ margin-top: 16px; color: #9ca3af; font-size: 13px; }}
  a {{ color: #2563eb; }}
</style></head>
<body><main>
  <h1>Halo Insight server <span class="pill">{status_label}</span></h1>
  <div class="sub">Refreshes every 30 seconds.</div>
  <table>{table}</table>
  <footer>Raw data: <a href="?format=json">/health?format=json</a>.
  Health checks and scripts get JSON automatically.</footer>
</main></body></html>"""
