"""Daily Slack recap text, report day, and the send endpoint's guards. No Slack or S3."""

from datetime import datetime, timezone

from flask import Flask

from backend.api.routes import labeling_routes as routes
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
    monkeypatch.setattr(routes, "_send_daily_report", lambda day, refresh: sent.append((day, refresh)))
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
    assert sent == [("2026-10-31", True)]
    routes._REPORT_RUNNING.update({"day": None, "stage": None, "started_at": None})

    # The dashboard posts what it previewed, without a refresh.
    body = client.post(
        "/api/labeling/daily-report",
        json={"date": "2026-11-01", "refresh": False},
        headers=headers,
    ).get_json()
    assert body["refresh_needed"] is False
    assert sent[-1] == ("2026-11-01", False)
    routes._REPORT_RUNNING.update({"day": None, "stage": None, "started_at": None})


def test_status_reports_the_stage_of_a_send_in_progress(monkeypatch):
    monkeypatch.setattr(routes, "_report_state", lambda: {"last_posted_day": "2026-10-30", "last_error": None})
    routes._REPORT_RUNNING.update({"day": "2026-10-31", "stage": "refreshing", "started_at": "2026-11-01T16:00:00Z"})
    body = _client().get("/api/labeling/daily-report/status", headers={"X-Admin-Token": "t"}).get_json()
    assert body["data"]["running"] == {"day": "2026-10-31", "stage": "refreshing", "started_at": "2026-11-01T16:00:00Z"}
    assert body["data"]["last_posted_day"] == "2026-10-30"
    routes._REPORT_RUNNING.update({"day": None, "stage": None, "started_at": None})
    body = _client().get("/api/labeling/daily-report/status", headers={"X-Admin-Token": "t"}).get_json()
    assert body["data"]["running"] is None


def test_send_without_refresh_never_scans(monkeypatch):
    calls = []
    monkeypatch.setattr(routes, "_report_state", lambda: {})
    monkeypatch.setattr(routes, "_save_report_state", lambda state: calls.append(("saved", state.get("last_posted_day"))))
    monkeypatch.setattr(routes, "_build_report_text", lambda day, allow_scan: calls.append(("build", allow_scan)) or "hi")
    monkeypatch.setattr(routes, "_post_report", lambda text: calls.append(("post", text)))
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
    routes._post_report("hello")
    assert posted == [("https://hooks.slack.com/services/T/B/secret", {"text": "hello", "unfurl_links": False})]

    def _boom(url, json, timeout):
        raise report.requests.ConnectionError(f"cannot reach {url}")

    monkeypatch.setattr(report.requests, "post", _boom)
    try:
        routes._post_report("hello")
    except RuntimeError as exc:
        assert "secret" not in str(exc)
    else:
        raise AssertionError("expected a failure")
