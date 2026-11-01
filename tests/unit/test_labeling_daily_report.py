"""Daily Slack recap text, report day, and the send endpoint's guards. No Slack or S3."""

from datetime import datetime, timezone

from flask import Flask

from backend.api.routes import labeling_routes as routes
from backend.services.auth_service import AuthService
from backend.services.labeling_daily_report import build_daily_report, format_minutes, report_day


def _family(sessions, seconds, users=(), dogs=(), by_date=()):
    return {
        "totals": {"sessions": sessions, "duration_seconds": seconds},
        "users": list(users),
        "dogs": list(dogs),
        "by_date": list(by_date),
    }


def _user(email, sessions, seconds, collars=()):
    return {
        "email": email,
        "sessions": sessions,
        "total_duration_seconds": seconds,
        "collars": [{"collar_sn": sn, "sessions": n} for sn, n in collars],
    }


def test_report_day_is_yesterday_in_pacific_time():
    # 06:00 UTC on Oct 31 is still Oct 30 in Los Angeles, so "yesterday" is Oct 29.
    now = datetime(2026, 10, 31, 6, 0, tzinfo=timezone.utc)
    assert report_day("America/Los_Angeles", now) == "2026-10-29"
    assert report_day("America/Los_Angeles", datetime(2026, 10, 31, 18, 0, tzinfo=timezone.utc)) == "2026-10-30"


def test_format_minutes():
    assert format_minutes(59) == "1m"
    assert format_minutes(3 * 3600 + 12 * 60) == "3h 12m"


def test_report_celebrates_labelers_by_owner_name_and_counts_both_models():
    day = {
        **_family(
            3,
            1800,
            users=[_user("ai_logs@halocollar.com", 3, 1800, [("26-H5364782-RT", 3)])],
            dogs=[{"name": "Mochi"}],
        ),
        "gps": _family(2, 600, users=[_user("lindsey@x.com", 2, 600)], dogs=[{"name": "Rocky"}]),
    }
    all_time = {
        **_family(498, 0, by_date=[{"date": "2026-10-28", "sessions": 4}, {"date": "2026-10-29", "sessions": 1}, {"date": "2026-10-30", "sessions": 3}]),
        "gps": _family(2, 0),
    }
    text = build_daily_report(
        "2026-10-30",
        day,
        all_time,
        owner_names={"26h5364782rt": "Brandon Rivera"},
        dashboard_url="https://insight.example.com/",
    )
    assert text.startswith(":tada: *Labeling recap for Friday, Oct 30*")
    assert "*5 sessions* and *40m* of labeled data from *2 labelers* and *2 dogs*." in text
    assert "Activity: 3 sessions · 30m" in text
    assert "Indoor/outdoor: 2 sessions · 10m" in text
    # The shared account is credited to the collar's owner; the top labeler gets the trophy.
    assert "• Brandon Rivera: 3 sessions · 30m :trophy:" in text
    assert "• lindsey: 2 sessions · 10m" in text
    assert "Good dogs on the job: Mochi, Rocky" in text
    assert "3 days in a row" in text
    assert "we passed *500 labeled sessions*" in text
    assert text.endswith("<https://insight.example.com|Open the labeling dashboard>")


def test_quiet_day_is_still_friendly():
    text = build_daily_report("2026-10-30", {"gps": {}}, {**_family(40, 7200), "gps": _family(0, 0)})
    assert "A quiet day" in text
    assert "*40 sessions*" in text
    assert "2h 00m" in text


def _client():
    app = Flask(__name__)
    app.secret_key = "test"
    app.register_blueprint(routes.labeling_bp)
    return app.test_client()


def test_send_requires_the_report_secret_not_just_any_admin_header(monkeypatch):
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SECRET", "s3cret")
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_CHANNEL", "C123")
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_TOKEN", "xoxb-test")
    client = _client()
    assert client.post("/api/labeling/daily-report", headers={"X-Admin-Token": "anything"}).status_code == 401
    assert client.post("/api/labeling/daily-report", headers={"X-Report-Secret": "wrong"}).status_code == 401


def test_send_skips_a_day_already_posted_and_starts_otherwise(monkeypatch):
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SECRET", "s3cret")
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_CHANNEL", "C123")
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_TOKEN", "xoxb-test")
    monkeypatch.setattr(routes, "_report_state", lambda: {"last_posted_day": "2026-10-30"})
    sent = []
    monkeypatch.setattr(
        routes, "_send_daily_report", lambda day, refresh, days, channels: sent.append((day, refresh, days))
    )
    monkeypatch.setattr(routes, "_report_summary_entry", lambda: None)

    class _Thread:
        def __init__(self, target, args, daemon):
            self._target, self._args = target, args

        def start(self):
            self._target(*self._args)

    monkeypatch.setattr(routes.threading, "Thread", _Thread)
    headers = {"X-Report-Secret": "s3cret"}
    client = _client()

    body = client.post("/api/labeling/daily-report", json={"date": "2026-10-30"}, headers=headers).get_json()
    assert body["started"] is False and sent == []

    response = client.post("/api/labeling/daily-report", json={"date": "2026-10-31"}, headers=headers)
    assert response.status_code == 202
    # The scheduled call refreshes first and says so when the summary is old.
    assert response.get_json()["refresh_needed"] is True
    assert sent == [("2026-10-31", True, 1)]
    routes._REPORT_RUNNING.update({"day": None, "stage": None, "started_at": None})

    # The dashboard posts what it previewed, without a refresh.
    body = client.post(
        "/api/labeling/daily-report",
        json={"date": "2026-11-01", "refresh": False},
        headers=headers,
    ).get_json()
    assert body["refresh_needed"] is False
    assert sent[-1] == ("2026-11-01", False, 1)
    routes._REPORT_RUNNING.update({"day": None, "stage": None, "started_at": None})


def test_status_reports_the_stage_of_a_send_in_progress(monkeypatch):
    monkeypatch.setattr(routes.Config, "ADMIN_PASSWORD", "admin-pw")
    admin = {"X-Admin-Token": AuthService.issue_admin_token()}
    monkeypatch.setattr(routes, "_report_state", lambda: {"last_posted_day": "2026-10-30", "last_error": None})
    routes._REPORT_RUNNING.update({"day": "2026-10-31", "stage": "refreshing", "started_at": "2026-11-01T16:00:00Z"})
    body = _client().get("/api/labeling/daily-report/status", headers=admin).get_json()
    assert body["data"]["running"]["stage"] == "refreshing"
    assert body["data"]["running"]["day"] == "2026-10-31"
    assert body["data"]["last_posted_day"] == "2026-10-30"
    routes._REPORT_RUNNING.update({"day": None, "stage": None, "started_at": None})
    body = _client().get("/api/labeling/daily-report/status", headers=admin).get_json()
    assert body["data"]["running"] is None


def test_send_without_refresh_never_scans(monkeypatch):
    calls = []
    monkeypatch.setattr(routes, "_report_state", lambda: {})
    monkeypatch.setattr(routes, "_save_report_state", lambda state: calls.append(("saved", state.get("last_posted_day"))))
    monkeypatch.setattr(
        routes,
        "_build_report_text",
        lambda day, allow_scan, days: calls.append(("build", allow_scan)) or "hi",
    )
    monkeypatch.setattr(
        routes, "_post_report", lambda text, ids: calls.append(("post", text)) or (["C1"], [])
    )
    routes._send_daily_report("2026-10-31", refresh=False)
    assert calls == [("build", False), ("post", "hi"), ("saved", "2026-10-31")]
    assert routes._REPORT_RUNNING["day"] is None


def test_webhook_is_used_when_set_and_its_url_never_appears_in_errors(monkeypatch):
    from backend.services import labeling_daily_report as report

    posted = []

    class _Resp:
        status_code = 200
        text = "ok"

    monkeypatch.setattr(report.requests, "post", lambda url, json, timeout: posted.append((url, json)) or _Resp())
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_WEBHOOK_URL", "https://hooks.slack.com/services/T/B/secret")
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_CHANNEL", None)
    assert routes._report_configured() is True
    routes._post_report("hello", [])
    assert posted == [("https://hooks.slack.com/services/T/B/secret", {"text": "hello", "unfurl_links": False})]

    def _boom(url, json, timeout):
        raise report.requests.ConnectionError(f"cannot reach {url}")

    monkeypatch.setattr(report.requests, "post", _boom)
    try:
        routes._post_report("hello", [])
    except RuntimeError as exc:
        assert "secret" not in str(exc)
    else:
        raise AssertionError("expected a failure")


def test_week_recap_covers_seven_days_ending_on_the_day():
    from backend.services.labeling_daily_report import period_start

    assert period_start("2026-10-30", 7) == "2026-10-24"
    assert period_start("2026-10-30", 1) == "2026-10-30"
    day = {**_family(4, 600, users=[_user("a@x.com", 4, 600)]), "gps": _family(0, 0)}
    text = build_daily_report("2026-10-30", day, {**_family(10, 0), "gps": _family(0, 0)}, days=7)
    assert text.startswith(":tada: *Labeling recap for Oct 24 – Oct 30 (7 days)*")
    quiet = build_daily_report("2026-10-30", {"gps": {}}, {**_family(10, 0), "gps": _family(0, 0)}, days=7)
    assert "A quiet stretch" in quiet


def test_week_send_uses_its_own_repeat_guard_and_window(monkeypatch):
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SECRET", "s3cret")
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_CHANNEL", "C123")
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_TOKEN", "xoxb-test")
    # The daily recap for 10-30 was posted, but not the week ending 10-30.
    monkeypatch.setattr(routes, "_report_state", lambda: {"last_posted_day": "2026-10-30"})
    monkeypatch.setattr(routes, "_report_summary_entry", lambda: None)
    sent = []
    monkeypatch.setattr(
        routes, "_send_daily_report", lambda day, refresh, days, channels: sent.append((day, refresh, days))
    )

    class _Thread:
        def __init__(self, target, args, daemon):
            self._target, self._args = target, args

        def start(self):
            self._target(*self._args)

    monkeypatch.setattr(routes.threading, "Thread", _Thread)
    response = _client().post(
        "/api/labeling/daily-report",
        json={"date": "2026-10-30", "days": 7, "refresh": False},
        headers={"X-Report-Secret": "s3cret"},
    )
    assert response.status_code == 202
    assert sent == [("2026-10-30", False, 7)]
    routes._REPORT_RUNNING.update({"day": None, "days": None, "stage": None, "started_at": None})

    bad = _client().post(
        "/api/labeling/daily-report", json={"days": 90}, headers={"X-Report-Secret": "s3cret"}
    )
    assert bad.status_code == 400


def test_weekly_post_does_not_count_as_the_daily_post(monkeypatch):
    saved = {}
    monkeypatch.setattr(routes, "_report_state", lambda: {"last_posted_day": "2026-10-29"})
    monkeypatch.setattr(routes, "_save_report_state", lambda state: saved.update(state))
    monkeypatch.setattr(routes, "_build_report_text", lambda day, allow_scan, days: "hi")
    monkeypatch.setattr(routes, "_post_report", lambda text, ids: (ids, []))
    routes._send_daily_report("2026-10-30", refresh=False, days=7, channel_ids=["C1"])
    assert saved["last_posted_period"] == "2026-10-24..2026-10-30"
    assert saved["last_posted_day"] == "2026-10-29"


def test_channels_parse_ids_and_names_with_the_first_as_default(monkeypatch):
    monkeypatch.setattr(
        routes.Config,
        "LABELING_REPORT_SLACK_CHANNEL",
        " C0BK8F2BHMZ:data-labeling , C09PY36MHQV:#activity-ai-labeling,C0PLAIN",
    )
    assert routes._report_channels() == [
        {"id": "C0BK8F2BHMZ", "name": "data-labeling"},
        {"id": "C09PY36MHQV", "name": "activity-ai-labeling"},
        {"id": "C0PLAIN", "name": "C0PLAIN"},
    ]


def test_send_only_to_configured_channels_with_a_per_channel_repeat_guard(monkeypatch):
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SECRET", "s3cret")
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_WEBHOOK_URL", None)
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_CHANNEL", "C1:data-labeling,C2:activity")
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_TOKEN", "xoxb-test")
    monkeypatch.setattr(
        routes, "_report_state", lambda: {"last_posted_day": "2026-10-30", "last_posted_day_channels": ["C1"]}
    )
    monkeypatch.setattr(routes, "_report_summary_entry", lambda: None)
    sent = []
    monkeypatch.setattr(
        routes,
        "_send_daily_report",
        lambda day, refresh, days, channels: sent.append(channels),
    )

    class _Thread:
        def __init__(self, target, args, daemon):
            self._target, self._args = target, args

        def start(self):
            self._target(*self._args)

    monkeypatch.setattr(routes.threading, "Thread", _Thread)
    headers = {"X-Report-Secret": "s3cret"}
    client = _client()

    bad = client.post("/api/labeling/daily-report", json={"channels": ["C9"]}, headers=headers)
    assert bad.status_code == 400

    # Already posted to C1 for that day...
    body = client.post(
        "/api/labeling/daily-report", json={"date": "2026-10-30", "channels": ["C1"]}, headers=headers
    ).get_json()
    assert body["started"] is False
    # ...but not to C2, so that goes ahead.
    response = client.post(
        "/api/labeling/daily-report", json={"date": "2026-10-30", "channels": ["C2"]}, headers=headers
    )
    assert response.status_code == 202
    assert sent == [["C2"]]
    routes._REPORT_RUNNING.update({"day": None, "days": None, "stage": None, "started_at": None})


def test_one_failing_channel_does_not_stop_the_others(monkeypatch):
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_WEBHOOK_URL", None)
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_CHANNEL", "C1:data-labeling,C2:activity")
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_TOKEN", "xoxb-test")

    def _post(token, channel, text):
        if channel == "C2":
            raise RuntimeError("Slack chat.postMessage failed: not_in_channel")

    monkeypatch.setattr(routes, "post_to_slack", _post)
    posted, errors = routes._post_report("hi", ["C1", "C2"])
    assert posted == ["C1"]
    assert errors == ["#activity: Slack chat.postMessage failed: not_in_channel"]

    saved = {}
    monkeypatch.setattr(routes, "_report_state", lambda: {})
    monkeypatch.setattr(routes, "_save_report_state", lambda state: saved.update(state))
    monkeypatch.setattr(routes, "_build_report_text", lambda day, allow_scan, days: "hi")
    routes._send_daily_report("2026-10-30", refresh=False, days=1, channel_ids=["C1", "C2"])
    assert saved["last_posted_day_channels"] == ["C1"]
    assert "not_in_channel" in saved["last_error"]
