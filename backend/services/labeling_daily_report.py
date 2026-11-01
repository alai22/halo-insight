"""
Daily labeling recap for Slack.

Celebrates yesterday's labeling: sessions and minutes per model, shout-outs to the
people who labeled, the dogs involved, streaks and milestones. Mismatches stay on the
dashboard; this message is for the team.
"""

from __future__ import annotations

import re
from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests

from ..utils.logging import get_logger

logger = get_logger(__name__)

SLACK_API_POST_MESSAGE = "https://slack.com/api/chat.postMessage"
SESSION_MILESTONE_STEP = 500
HOURS_MILESTONE_STEP = 10
STREAK_MIN_DAYS = 3
SHOUT_OUT_LIMIT = 5
DOGS_PER_LINE = 3


def report_day(tz_name: Optional[str], now: Optional[datetime] = None) -> str:
    """Yesterday as YYYY-MM-DD in the report's time zone (Pacific if unset or unknown)."""
    try:
        from zoneinfo import ZoneInfo

        tz = ZoneInfo(tz_name or "America/Los_Angeles")
    except Exception:  # noqa: BLE001 - no tz database in the image
        tz = timezone(timedelta(hours=-8))
    current = (now or datetime.now(timezone.utc)).astimezone(tz)
    return (current.date() - timedelta(days=1)).isoformat()


def serial_key(sn: Any) -> str:
    return re.sub(r"[^a-z0-9]", "", str(sn or "").lower())


def format_minutes(seconds: float) -> str:
    minutes = int(round(float(seconds or 0) / 60))
    if minutes < 60:
        return f"{minutes}m"
    return f"{minutes // 60}h {minutes % 60:02d}m"


def _sort_labelers(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(rows, key=lambda r: (-r["seconds"], -r["sessions"], r["email"]))


def _busiest_first(collars: Dict[str, Dict[str, float]]) -> List[str]:
    return [sn for sn, _ in sorted(collars.items(), key=lambda item: -item[1]["sessions"])]


def _merge_labelers(day_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Posture and GPS labelers combined by email, with sessions and seconds per collar."""
    merged: Dict[str, Dict[str, Any]] = {}
    for users in (day_data.get("users") or [], (day_data.get("gps") or {}).get("users") or []):
        for user in users:
            email = user.get("email") or ""
            row = merged.setdefault(
                email, {"email": email, "sessions": 0, "seconds": 0.0, "collars": {}}
            )
            row["sessions"] += int(user.get("sessions") or 0)
            row["seconds"] += float(user.get("total_duration_seconds") or 0)
            for collar in user.get("collars") or []:
                stats = row["collars"].setdefault(
                    collar.get("collar_sn"), {"sessions": 0, "seconds": 0.0}
                )
                stats["sessions"] += int(collar.get("sessions") or 0)
                stats["seconds"] += float(collar.get("total_duration_seconds") or 0)
    return _sort_labelers(list(merged.values()))


def _split_group_senders(
    labelers: List[Dict[str, Any]], group_senders: Optional[set]
) -> List[Dict[str, Any]]:
    """A group sender is several people, so it gets one row per collar instead of one row."""
    if not group_senders:
        return labelers
    out: List[Dict[str, Any]] = []
    for labeler in labelers:
        if (labeler["email"] or "").lower() not in group_senders or not labeler["collars"]:
            out.append(labeler)
            continue
        for sn, stats in labeler["collars"].items():
            out.append({
                "email": labeler["email"],
                "group_collar": sn,
                "sessions": stats["sessions"],
                "seconds": stats["seconds"],
                "collars": {sn: stats},
            })
    return _sort_labelers(out)


def labeler_name(
    labeler: Dict[str, Any],
    owner_names: Dict[str, str],
    owner_emails: Optional[Dict[str, str]] = None,
    names_by_email: Optional[Dict[str, str]] = None,
) -> str:
    """
    The friendliest name we have, falling back to more technical ones:
    owner name, then email, then collar serial, then the shared inbox.
    """
    email = labeler["email"] or ""
    if "group_collar" in labeler:
        sn = labeler["group_collar"]
        if sn and sn != "_unknown":
            key = serial_key(sn)
            return owner_names.get(key) or (owner_emails or {}).get(key) or f"collar {sn}"
        return f"{email.split('@', 1)[0]}@ shared inbox"
    name = (names_by_email or {}).get(email.lower())
    if name:
        return name
    for sn in _busiest_first(labeler["collars"]):
        name = owner_names.get(serial_key(sn))
        if name:
            return name
    return email or "someone"


def _dog_names(day_data: Dict[str, Any]) -> List[str]:
    names: List[str] = []
    for dogs in (day_data.get("dogs") or [], (day_data.get("gps") or {}).get("dogs") or []):
        for dog in dogs:
            name = (dog.get("name") or "").strip()
            if name and name.lower() != "unnamed" and name not in names:
                names.append(name)
    return names


def _dogs_by_collar(day_data: Dict[str, Any]) -> Dict[str, str]:
    """Dog name per collar serial key, from the app data."""
    out: Dict[str, str] = {}
    for dogs in (day_data.get("dogs") or [], (day_data.get("gps") or {}).get("dogs") or []):
        for dog in dogs:
            name = (dog.get("name") or "").strip()
            key = serial_key(dog.get("collar_sn"))
            if key and name and name.lower() != "unnamed":
                out.setdefault(key, name)
    return out


def labeler_dogs(labeler: Dict[str, Any], dogs_by_collar: Dict[str, str]) -> List[str]:
    """Dogs on the labeler's collars, busiest collar first."""
    names: List[str] = []
    for sn in _busiest_first(labeler["collars"]):
        name = dogs_by_collar.get(serial_key(sn))
        if name and name not in names:
            names.append(name)
    return names


def _streak(all_data: Dict[str, Any], day: str) -> int:
    """Days in a row, ending on day, that had at least one labeled session."""
    active = {
        row.get("date")
        for rows in (
            all_data.get("by_date") or [],
            (all_data.get("gps") or {}).get("by_date") or [],
        )
        for row in rows
        if int(row.get("sessions") or 0) > 0
    }
    streak = 0
    current = date.fromisoformat(day)
    while current.isoformat() in active:
        streak += 1
        current -= timedelta(days=1)
    return streak


def _crossed(before: float, after: float, step: float) -> Optional[int]:
    """The highest multiple of step passed when going from before to after, if any."""
    if step <= 0 or after <= before:
        return None
    mark = int(after // step) * step
    return int(mark) if mark > before and mark > 0 else None


def _totals(data: Dict[str, Any]) -> Dict[str, float]:
    posture = data.get("totals") or {}
    gps = (data.get("gps") or {}).get("totals") or {}
    return {
        "activity_sessions": int(posture.get("sessions") or 0),
        "gps_sessions": int(gps.get("sessions") or 0),
        "activity_seconds": float(posture.get("duration_seconds") or 0),
        "gps_seconds": float(gps.get("duration_seconds") or 0),
    }


def period_start(day: str, days: int) -> str:
    """First day of the days-long period that ends on day (inclusive)."""
    return (date.fromisoformat(day) - timedelta(days=max(1, days) - 1)).isoformat()


def build_daily_report(
    day: str,
    day_data: Dict[str, Any],
    all_data: Dict[str, Any],
    owner_names: Optional[Dict[str, str]] = None,
    dashboard_url: Optional[str] = None,
    days: int = 1,
    group_senders: Optional[set] = None,
    owner_emails: Optional[Dict[str, str]] = None,
    names_by_email: Optional[Dict[str, str]] = None,
) -> str:
    """
    Slack mrkdwn for the days-long period ending on day (one day by default).
    day_data is the summary limited to that period.
    """
    owner_names = owner_names or {}
    end = date.fromisoformat(day)
    if days > 1:
        start = date.fromisoformat(period_start(day, days))
        pretty_day = f"{start.strftime('%b %-d')} – {end.strftime('%b %-d')} ({days} days)"
        quiet = "A quiet stretch"
    else:
        pretty_day = end.strftime("%A, %b %-d")
        quiet = "A quiet day"
    today = _totals(day_data)
    overall = _totals(all_data)
    sessions = today["activity_sessions"] + today["gps_sessions"]
    seconds = today["activity_seconds"] + today["gps_seconds"]
    all_sessions = overall["activity_sessions"] + overall["gps_sessions"]
    all_seconds = overall["activity_seconds"] + overall["gps_seconds"]
    link = f"\n<{dashboard_url.rstrip('/')}|Open the labeling dashboard>" if dashboard_url else ""

    if sessions == 0:
        return (
            f":sunrise: *Labeling recap for {pretty_day}*\n"
            f"{quiet}, with no new labeled sessions. "
            f"So far the team has labeled *{all_sessions:,} sessions* and "
            f"*{format_minutes(all_seconds)}* of data. Thank you! :sparkles:{link}"
        )

    labelers = _split_group_senders(_merge_labelers(day_data), group_senders)
    dogs = _dog_names(day_data)
    lines = [
        f":tada: *Labeling recap for {pretty_day}*",
        f"*{sessions} session{'s' if sessions != 1 else ''}* and *{format_minutes(seconds)}* "
        f"of labeled data from *{len(labelers)} labeler{'s' if len(labelers) != 1 else ''}*"
        + (f" and *{len(dogs)} dog{'s' if len(dogs) != 1 else ''}*" if dogs else "")
        + ".",
    ]
    if today["activity_sessions"]:
        lines.append(
            f"• :dog2: Activity: {today['activity_sessions']} sessions · "
            f"{format_minutes(today['activity_seconds'])}"
        )
    if today["gps_sessions"]:
        lines.append(
            f"• :house_with_garden: Indoor/outdoor: {today['gps_sessions']} sessions · "
            f"{format_minutes(today['gps_seconds'])}"
        )

    lines.append("")
    # Each line thanks the dogs first, with their people in brackets.
    lines.append(":raised_hands: *Shout-outs to the good dogs and their people*")
    dogs_by_collar = _dogs_by_collar(day_data)
    for index, labeler in enumerate(labelers[:SHOUT_OUT_LIMIT]):
        trophy = " :trophy:" if index == 0 and len(labelers) > 1 else ""
        person = labeler_name(labeler, owner_names, owner_emails, names_by_email)
        their_dogs = labeler_dogs(labeler, dogs_by_collar)
        shown = ", ".join(their_dogs[:DOGS_PER_LINE])
        if len(their_dogs) > DOGS_PER_LINE:
            shown += f" +{len(their_dogs) - DOGS_PER_LINE}"
        who = f":dog: {shown} ({person})" if their_dogs else person
        lines.append(
            f"• {who}: {labeler['sessions']} sessions · "
            f"{format_minutes(labeler['seconds'])}{trophy}"
        )
    if len(labelers) > SHOUT_OUT_LIMIT:
        lines.append(f"• …and {len(labelers) - SHOUT_OUT_LIMIT} more. Thank you all!")

    streak = _streak(all_data, day)
    if streak >= STREAK_MIN_DAYS:
        lines.append(f":fire: {streak} days in a row with new labeled data!")
    session_mark = _crossed(all_sessions - sessions, all_sessions, SESSION_MILESTONE_STEP)
    if session_mark:
        lines.append(f":trophy: Milestone: we passed *{session_mark:,} labeled sessions*!")
    hours_mark = _crossed((all_seconds - seconds) / 3600, all_seconds / 3600, HOURS_MILESTONE_STEP)
    if hours_mark:
        lines.append(f":stopwatch: Milestone: over *{hours_mark:,} hours* of labeled data!")

    return "\n".join(lines) + link


def post_to_slack_webhook(url: str, text: str) -> None:
    """Post one message to an incoming webhook. Errors never include the URL, a secret."""
    try:
        resp = requests.post(url, json={"text": text, "unfurl_links": False}, timeout=15)
    except requests.RequestException as exc:
        raise RuntimeError(f"Slack webhook request failed: {type(exc).__name__}") from None
    if resp.status_code != 200:
        raise RuntimeError(f"Slack webhook returned {resp.status_code}: {resp.text[:100]}")
    logger.info("Labeling daily report posted via webhook chars=%s", len(text))


def post_to_slack(token: str, channel: str, text: str) -> Dict[str, Any]:
    """Post one message; returns Slack's response. Raises on transport or API errors."""
    resp = requests.post(
        SLACK_API_POST_MESSAGE,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        json={"channel": channel, "text": text, "unfurl_links": False},
        timeout=15,
    )
    data = resp.json() if resp.content else {}
    if not data.get("ok"):
        raise RuntimeError(f"Slack chat.postMessage failed: {data.get('error', resp.status_code)}")
    logger.info("Labeling daily report posted channel=%s chars=%s", channel, len(text))
    return data
