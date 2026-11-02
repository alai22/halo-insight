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
# Medals for the top three shout-outs by minutes labeled.
PODIUM = (":first_place_medal:", ":second_place_medal:", ":third_place_medal:")


def report_day(tz_name: Optional[str], now: Optional[datetime] = None) -> str:
    """Yesterday as YYYY-MM-DD in the report's time zone (Pacific if unset or unknown)."""
    try:
        from zoneinfo import ZoneInfo

        tz = ZoneInfo(tz_name or "America/Los_Angeles")
    except Exception:  # noqa: BLE001 - no tz database in the image
        tz = timezone(timedelta(hours=-8))
    current = (now or datetime.now(timezone.utc)).astimezone(tz)
    return (current.date() - timedelta(days=1)).isoformat()


def _report_tz(tz_name: Optional[str]):
    try:
        from zoneinfo import ZoneInfo

        return ZoneInfo(tz_name or "America/Los_Angeles")
    except Exception:  # noqa: BLE001 - no tz database in the image
        return timezone(timedelta(hours=-8), "UTC-8")


def period_footnote(start: date, end: date, tz_name: Optional[str]) -> str:
    """
    The exact period the recap counts. Session times are recorded without a time zone,
    so days follow each session's own timestamp; "yesterday" is chosen in the report zone.
    """
    tz = _report_tz(tz_name)
    # The zone's abbreviation on the last day (PST or PDT), plus its name.
    abbrev = datetime(end.year, end.month, end.day, 12, tzinfo=tz).tzname()
    zone = tz_name or "America/Los_Angeles"
    span = (
        f"{start.strftime('%a %b %-d')} 12:00 AM – {end.strftime('%a %b %-d, %Y')} 11:59 PM"
    )
    return (
        f"_Period: {span}. Sessions count on the date in their own timestamp, which is "
        f"recorded without a time zone. The report day is chosen in {zone} ({abbrev})._"
    )


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


def _add_labels(into: Dict[str, float], rows: Any) -> None:
    """Add activity rows ({label, seconds}) to a label -> seconds map."""
    for row in rows or []:
        label = row.get("label")
        if label:
            into[label] = into.get(label, 0.0) + float(row.get("seconds") or 0)


def _merge_labelers(day_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Posture and GPS labelers combined by email, with sessions and seconds per collar."""
    merged: Dict[str, Dict[str, Any]] = {}
    for users in (day_data.get("users") or [], (day_data.get("gps") or {}).get("users") or []):
        for user in users:
            email = user.get("email") or ""
            row = merged.setdefault(
                email, {"email": email, "sessions": 0, "seconds": 0.0, "collars": {}, "labels": {}}
            )
            row["sessions"] += int(user.get("sessions") or 0)
            row["seconds"] += float(user.get("total_duration_seconds") or 0)
            _add_labels(row["labels"], user.get("activities"))
            for collar in user.get("collars") or []:
                stats = row["collars"].setdefault(
                    collar.get("collar_sn"), {"sessions": 0, "seconds": 0.0, "labels": {}}
                )
                stats["sessions"] += int(collar.get("sessions") or 0)
                stats["seconds"] += float(collar.get("total_duration_seconds") or 0)
                _add_labels(stats["labels"], collar.get("activities"))
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
                "labels": dict(stats.get("labels") or {}),
            })
    return _sort_labelers(out)


# Who a labeler is to Halo. Saved per person in the dashboard; @halocollar.com means employee.
LABELER_TYPES = ("employee", "pack_member", "partner")
EMPLOYEE_DOMAIN = "@halocollar.com"


def _people(
    data: Dict[str, Any],
    owner_names: Optional[Dict[str, str]],
    group_senders: Optional[set],
    owner_emails: Optional[Dict[str, str]],
    names_by_email: Optional[Dict[str, str]],
    labeler_types: Optional[Dict[str, str]],
) -> List[Dict[str, Any]]:
    """Labelers merged into one row per person, with their emails and labeler type."""
    owner_names = owner_names or {}
    owner_emails = owner_emails or {}

    def emails_of(labeler: Dict[str, Any]) -> List[str]:
        if "group_collar" in labeler:
            email = owner_emails.get(serial_key(labeler["group_collar"]))
            return [email.lower()] if email else []
        return [labeler["email"].lower()] if labeler.get("email") else []

    people = _merge_same_person(
        _split_group_senders(_merge_labelers(data), group_senders),
        lambda labeler: labeler_name(labeler, owner_names, owner_emails, names_by_email),
        emails_of,
    )
    for person in people:
        person["labeler_type"] = labeler_type(person["person"], person["emails"], labeler_types)
    return people


def labeler_type(person: str, emails: List[str], labeler_types: Optional[Dict[str, str]]) -> Optional[str]:
    """The saved type for this person, else employee for a Halo email, else unknown (None)."""
    saved = (labeler_types or {}).get(person.lower())
    if saved in LABELER_TYPES:
        return saved
    if any(email.endswith(EMPLOYEE_DOMAIN) for email in emails):
        return "employee"
    return None


def _merge_same_person(labelers: List[Dict[str, Any]], name_of, emails_of=None) -> List[Dict[str, Any]]:
    """
    One row per name. Someone who sends from their own email and also through a shared
    inbox (for their collar) would otherwise be thanked twice.
    """
    merged: Dict[str, Dict[str, Any]] = {}
    for labeler in labelers:
        person = name_of(labeler)
        emails = emails_of(labeler) if emails_of else []
        row = merged.get(person.lower())
        if row is None:
            merged[person.lower()] = {
                **labeler,
                "person": person,
                "emails": list(emails),
                "collars": dict(labeler["collars"]),
                "labels": dict(labeler.get("labels") or {}),
            }
            continue
        row["emails"] += [e for e in emails if e not in row["emails"]]
        row["sessions"] += labeler["sessions"]
        row["seconds"] += labeler["seconds"]
        for label, seconds in (labeler.get("labels") or {}).items():
            row["labels"][label] = row["labels"].get(label, 0.0) + seconds
        for sn, stats in labeler["collars"].items():
            mine = row["collars"].get(sn) or {"sessions": 0, "seconds": 0.0}
            row["collars"][sn] = {
                "sessions": mine["sessions"] + stats["sessions"],
                "seconds": mine["seconds"] + stats["seconds"],
            }
    return _sort_labelers(list(merged.values()))


def labeler_name(
    labeler: Dict[str, Any],
    owner_names: Dict[str, str],
    owner_emails: Optional[Dict[str, str]] = None,
    names_by_email: Optional[Dict[str, str]] = None,
    labeler_types: Optional[Dict[str, str]] = None,
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


def _dog_leaderboard(
    labelers: List[Dict[str, Any]], dogs_by_collar: Dict[str, str]
) -> List[Dict[str, Any]]:
    """
    One row per dog with its people, ranked by labeled time. Collars without a dog name
    in the app are left out; the people list covers those.
    """
    dogs: Dict[str, Dict[str, Any]] = {}
    for labeler in labelers:
        for sn, stats in labeler["collars"].items():
            name = dogs_by_collar.get(serial_key(sn))
            if not name:
                continue
            row = dogs.setdefault(
                name.lower(), {"dog": name, "people": {}, "sessions": 0, "seconds": 0.0}
            )
            row["sessions"] += int(stats.get("sessions") or 0)
            row["seconds"] += float(stats.get("seconds") or 0)
            person = labeler["person"]
            row["people"][person] = row["people"].get(person, 0.0) + float(stats.get("seconds") or 0)
    ranked = sorted(dogs.values(), key=lambda r: (-r["seconds"], -r["sessions"], r["dog"]))
    return [
        {
            "dog": row["dog"],
            "people": [p for p, _ in sorted(row["people"].items(), key=lambda item: -item[1])],
            "sessions": row["sessions"],
            "seconds": round(row["seconds"], 1),
            "medal": PODIUM[index] if len(ranked) > 1 and index < len(PODIUM) else None,
        }
        for index, row in enumerate(ranked)
    ]


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


def recap_data(
    end: str,
    day_data: Dict[str, Any],
    all_data: Dict[str, Any],
    start: Optional[str] = None,
    owner_names: Optional[Dict[str, str]] = None,
    group_senders: Optional[set] = None,
    owner_emails: Optional[Dict[str, str]] = None,
    names_by_email: Optional[Dict[str, str]] = None,
    labeler_types: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    The recap as data, for the period start..end (inclusive; start None = all time).
    day_data is the summary limited to that period. Shared by Slack and the dashboard.
    """
    owner_names = owner_names or {}
    period = _totals(day_data)
    overall = _totals(all_data)
    sessions = period["activity_sessions"] + period["gps_sessions"]
    seconds = period["activity_seconds"] + period["gps_seconds"]
    all_sessions = overall["activity_sessions"] + overall["gps_sessions"]
    all_seconds = overall["activity_seconds"] + overall["gps_seconds"]
    labelers = _people(day_data, owner_names, group_senders, owner_emails, names_by_email, labeler_types)
    dogs_by_collar = _dogs_by_collar(day_data)
    leaderboard = []
    for index, labeler in enumerate(labelers):
        leaderboard.append({
            "person": labeler["person"],
            "emails": labeler["emails"],
            "labeler_type": labeler["labeler_type"],
            "dogs": labeler_dogs(labeler, dogs_by_collar),
            "sessions": labeler["sessions"],
            "seconds": round(labeler["seconds"], 1),
            "medal": PODIUM[index] if len(labelers) > 1 and index < len(PODIUM) else None,
        })
    dog_board = _dog_leaderboard(labelers, dogs_by_collar)
    # Milestones are what this period pushed the all-time totals past.
    period_bound = start is not None
    return {
        "start": start,
        "end": end,
        "sessions": sessions,
        "seconds": round(seconds, 1),
        "activity": {
            "sessions": period["activity_sessions"],
            "seconds": period["activity_seconds"],
        },
        "gps": {"sessions": period["gps_sessions"], "seconds": period["gps_seconds"]},
        "all_sessions": all_sessions,
        "all_seconds": round(all_seconds, 1),
        "labelers": len(labelers),
        "dogs": _dog_names(day_data),
        "leaderboard": leaderboard,
        "dog_leaderboard": dog_board,
        "streak": _streak(all_data, end),
        "session_milestone": (
            _crossed(all_sessions - sessions, all_sessions, SESSION_MILESTONE_STEP)
            if period_bound
            else None
        ),
        "hours_milestone": (
            _crossed((all_seconds - seconds) / 3600, all_seconds / 3600, HOURS_MILESTONE_STEP)
            if period_bound
            else None
        ),
    }


# A 5-button remote goes to anyone with REMOTE_MIN_SECONDS in each of REMOTE_MIN_LABELS
# different labels (postures and environments both count).
REMOTE_MIN_SECONDS = 120
REMOTE_MIN_LABELS = 9


def remote_eligibility(
    data: Dict[str, Any],
    owner_names: Optional[Dict[str, str]] = None,
    group_senders: Optional[set] = None,
    owner_emails: Optional[Dict[str, str]] = None,
    names_by_email: Optional[Dict[str, str]] = None,
    labeler_types: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Who has earned a remote, and how close everyone else is, from a summary."""
    owner_names = owner_names or {}
    labelers = _people(data, owner_names, group_senders, owner_emails, names_by_email, labeler_types)
    dogs_by_collar = _dogs_by_collar(data)
    people = []
    for labeler in labelers:
        labels = sorted(labeler.get("labels", {}).items(), key=lambda item: -item[1])
        qualified = [{"label": k, "seconds": round(v, 1)} for k, v in labels if v >= REMOTE_MIN_SECONDS]
        close = [
            {"label": k, "seconds": round(v, 1)} for k, v in labels if 0 < v < REMOTE_MIN_SECONDS
        ]
        people.append({
            "person": labeler["person"],
            "emails": labeler["emails"],
            "labeler_type": labeler["labeler_type"],
            "dogs": labeler_dogs(labeler, dogs_by_collar),
            "sessions": labeler["sessions"],
            "seconds": round(labeler["seconds"], 1),
            "qualified": qualified,
            "close": close,
            "eligible": len(qualified) >= REMOTE_MIN_LABELS,
        })
    people.sort(key=lambda p: (not p["eligible"], -len(p["qualified"]), -p["seconds"]))
    return {
        "min_seconds": REMOTE_MIN_SECONDS,
        "min_labels": REMOTE_MIN_LABELS,
        "eligible": sum(1 for p in people if p["eligible"]),
        "people": people,
    }


def _day_rows(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(data.get("by_date") or []) + list((data.get("gps") or {}).get("by_date") or [])


def period_change(all_data: Dict[str, Any], start: str, end: str) -> Dict[str, Any]:
    """
    Sessions, minutes and labelers in start..end and in the same-length period just before,
    from the all-time summary's per-day rows.
    """
    span = (date.fromisoformat(end) - date.fromisoformat(start)).days + 1
    prev_end = date.fromisoformat(start) - timedelta(days=1)
    prev_start = prev_end - timedelta(days=span - 1)

    def _sum(lo: str, hi: str) -> Dict[str, Any]:
        sessions, seconds, people = 0, 0.0, set()
        for row in _day_rows(all_data):
            if lo <= str(row.get("date") or "") <= hi:
                sessions += int(row.get("sessions") or 0)
                seconds += float(row.get("duration_seconds") or 0)
                people.update(u.get("user") for u in row.get("by_user") or [] if u.get("user"))
        return {"sessions": sessions, "seconds": round(seconds, 1), "labelers": len(people)}

    return {
        "current": _sum(start, end),
        "previous": _sum(prev_start.isoformat(), prev_end.isoformat()),
        "previous_start": prev_start.isoformat(),
        "previous_end": prev_end.isoformat(),
    }


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
    labeler_types: Optional[Dict[str, str]] = None,
    timezone_name: Optional[str] = None,
) -> str:
    """
    Slack mrkdwn for the days-long period ending on day (one day by default).
    day_data is the summary limited to that period.
    """
    end = date.fromisoformat(day)
    footnote = "\n" + period_footnote(
        date.fromisoformat(period_start(day, days)), end, timezone_name
    )
    if days > 1:
        start = date.fromisoformat(period_start(day, days))
        pretty_day = f"{start.strftime('%b %-d')} – {end.strftime('%b %-d')} ({days} days)"
        quiet = "A quiet stretch"
    else:
        pretty_day = end.strftime("%A, %b %-d")
        quiet = "A quiet day"
    recap = recap_data(
        day,
        day_data,
        all_data,
        start=period_start(day, days),
        owner_names=owner_names,
        group_senders=group_senders,
        owner_emails=owner_emails,
        names_by_email=names_by_email,
        labeler_types=labeler_types,
    )
    sessions = recap["sessions"]
    link = f"\n<{dashboard_url.rstrip('/')}|Open the labeling dashboard>" if dashboard_url else ""

    if sessions == 0:
        return (
            f":sunrise: *Labeling recap for {pretty_day}*\n"
            f"{quiet}, with no new labeled sessions. "
            f"So far the team has labeled *{recap['all_sessions']:,} sessions* and "
            f"*{format_minutes(recap['all_seconds'])}* of data. Thank you! :sparkles:{link}"
            f"{footnote}"
        )

    labelers, dogs = recap["labelers"], recap["dogs"]
    lines = [
        f":tada: *Labeling recap for {pretty_day}*",
        f"*{sessions} session{'s' if sessions != 1 else ''}* and "
        f"*{format_minutes(recap['seconds'])}* "
        f"of labeled data from *{labelers} labeler{'s' if labelers != 1 else ''}*"
        + (f" and *{len(dogs)} dog{'s' if len(dogs) != 1 else ''}*" if dogs else "")
        + ".",
    ]
    if recap["activity"]["sessions"]:
        lines.append(
            f"• :dog2: Activity: {recap['activity']['sessions']} sessions · "
            f"{format_minutes(recap['activity']['seconds'])}"
        )
    if recap["gps"]["sessions"]:
        lines.append(
            f"• :house_with_garden: Indoor/outdoor: {recap['gps']['sessions']} sessions · "
            f"{format_minutes(recap['gps']['seconds'])}"
        )

    lines.append("")
    # Each line thanks the dogs first, with their people in brackets.
    lines.append(":raised_hands: *Shout-outs to the good dogs and their people*")
    for row in recap["leaderboard"][:SHOUT_OUT_LIMIT]:
        shown = ", ".join(row["dogs"][:DOGS_PER_LINE])
        if len(row["dogs"]) > DOGS_PER_LINE:
            shown += f" +{len(row['dogs']) - DOGS_PER_LINE}"
        who = f":dog: {shown} ({row['person']})" if row["dogs"] else row["person"]
        medal = f" {row['medal']}" if row["medal"] else ""
        lines.append(
            f"• {who}: {row['sessions']} sessions · {format_minutes(row['seconds'])}{medal}"
        )
    if labelers > SHOUT_OUT_LIMIT:
        lines.append(f"• …and {labelers - SHOUT_OUT_LIMIT} more. Thank you all!")

    if recap["streak"] >= STREAK_MIN_DAYS:
        lines.append(f":fire: {recap['streak']} days in a row with new labeled data!")
    if recap["session_milestone"]:
        lines.append(
            f":trophy: Milestone: we passed *{recap['session_milestone']:,} labeled sessions*!"
        )
    if recap["hours_milestone"]:
        lines.append(
            f":stopwatch: Milestone: over *{recap['hours_milestone']:,} hours* of labeled data!"
        )

    return "\n".join(lines) + link + footnote


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
