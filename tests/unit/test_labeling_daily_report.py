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
        "collars": [
            {"collar_sn": c[0], "sessions": c[1], "total_duration_seconds": c[2] if len(c) > 2 else 0}
            for c in collars
        ],
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
            dogs=[{"name": "Mochi", "collar_sn": "26h5364782rt"}],
        ),
        "gps": _family(
            2,
            600,
            users=[_user("lindsey@x.com", 2, 600, [("24h4290093rt", 2)])],
            dogs=[{"name": "Rocky", "collar_sn": "24h4290093rt"}],
        ),
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
    # Each line thanks the dogs, with their person in brackets; the top labeler gets the trophy.
    assert "• :dog: Mochi (Brandon Rivera): 3 sessions · 30m :first_place_medal:" in text
    assert "• :dog: Rocky (lindsey@x.com): 2 sessions · 10m :second_place_medal:" in text
    assert "Good dogs on the job" not in text
    assert "3 days in a row" in text
    assert "we passed *500 labeled sessions*" in text
    # The dashboard link, then the period footnote last.
    assert text.splitlines()[-2] == "<https://insight.example.com|Open the labeling dashboard>"
    assert text.splitlines()[-1].startswith("_Period: Fri Oct 30 12:00 AM")


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


def test_group_sender_is_split_per_collar_with_a_name_fallback_chain():
    day = {
        **_family(
            20,
            2520,
            users=[
                _user(
                    "ai_logs@halocollar.com",
                    20,
                    2520,
                    [
                        ("26h5230414rt", 12, 1314),  # no owner row: collar serial
                        ("25h5425925vm", 2, 708),  # owner email only
                        ("26h5220121th", 4, 390),  # owner name
                        ("_unknown", 2, 108),  # no serial: shared inbox
                    ],
                )
            ],
        ),
        "gps": _family(0, 0),
    }
    text = build_daily_report(
        "2026-10-30",
        day,
        {**_family(100, 0), "gps": _family(0, 0)},
        owner_names={"26h5220121th": "Jenny & Adrian"},
        days=7,
        group_senders={"ai_logs@halocollar.com"},
        owner_emails={"25h5425925vm": "someone@yahoo.com"},
    )
    # Medals go to the top three by minutes; the fourth line gets none.
    assert "• collar 26h5230414rt: 12 sessions · 22m :first_place_medal:" in text
    assert "• someone@yahoo.com: 2 sessions · 12m :second_place_medal:" in text
    assert "• Jenny & Adrian: 4 sessions · 6m :third_place_medal:" in text
    assert "• ai_logs@ shared inbox: 2 sessions · 2m\n" in text or text.endswith(
        "• ai_logs@ shared inbox: 2 sessions · 2m"
    )


def test_direct_labeler_prefers_the_name_on_their_email():
    day = {
        **_family(3, 600, users=[_user("victor@vmo3.com", 3, 600, [("24h4290375rt", 3, 600)])]),
        "gps": _family(0, 0),
    }
    text = build_daily_report(
        "2026-10-30",
        day,
        {**_family(10, 0), "gps": _family(0, 0)},
        owner_names={"24h4290375rt": "Someone Else"},
        names_by_email={"victor@vmo3.com": "Victor O"},
    )
    assert "• Victor O: 3 sessions · 10m" in text


def test_shout_out_without_known_dogs_names_just_the_person():
    day = {**_family(4, 600, users=[_user("a@x.com", 4, 600, [("sn9", 4)])]), "gps": _family(0, 0)}
    text = build_daily_report("2026-10-30", day, {**_family(10, 0), "gps": _family(0, 0)})
    assert "• a@x.com: 4 sessions · 10m" in text


def test_several_dogs_on_one_line_are_capped():
    collars = [(f"sn{i}", 5 - i) for i in range(5)]
    dogs = [{"name": f"Dog{i}", "collar_sn": f"sn{i}"} for i in range(5)]
    day = {**_family(15, 900, users=[_user("a@x.com", 15, 900, collars)], dogs=dogs), "gps": _family(0, 0)}
    text = build_daily_report("2026-10-30", day, {**_family(20, 0), "gps": _family(0, 0)})
    assert "• :dog: Dog0, Dog1, Dog2 +2 (a@x.com): 15 sessions · 15m" in text


def test_recap_data_gives_the_dashboard_the_same_leaderboard_as_slack():
    from backend.services.labeling_daily_report import recap_data

    day = {
        **_family(
            5,
            1800,
            users=[
                _user("b@x.com", 3, 1200, [("sn1", 3, 1200)]),
                _user("c@x.com", 2, 600, [("sn2", 2, 600)]),
            ],
            dogs=[{"name": "Mochi", "collar_sn": "sn1"}],
        ),
        "gps": _family(0, 0),
    }
    recap = recap_data(
        "2026-10-30",
        day,
        {**_family(497, 0), "gps": _family(7, 0)},  # 504 all-time, 499 before this week
        start="2026-10-24",
        owner_names={"sn1": "Brandon Rivera"},
    )
    assert recap["sessions"] == 5 and recap["labelers"] == 2
    assert recap["leaderboard"][0] == {
        "person": "Brandon Rivera",
        "emails": ["b@x.com"],
        "labeler_type": None,
        "dogs": ["Mochi"],
        "sessions": 3,
        "seconds": 1200.0,
        "medal": ":first_place_medal:",
    }
    assert recap["leaderboard"][1]["medal"] == ":second_place_medal:"
    assert recap["session_milestone"] == 500
    # All time has no period to have pushed past a milestone.
    assert recap_data("2026-10-30", day, day)["session_milestone"] is None


def test_same_person_via_own_email_and_shared_inbox_is_one_row():
    from backend.services.labeling_daily_report import recap_data

    day = {
        **_family(
            9,
            900,
            users=[
                _user("brandon@x.com", 5, 600, [("sn1", 5, 600)]),
                _user("ai_logs@halocollar.com", 4, 300, [("sn1", 3, 200), ("sn2", 1, 100)]),
            ],
            dogs=[{"name": "Dixon", "collar_sn": "sn1"}, {"name": "Rex", "collar_sn": "sn2"}],
        ),
        "gps": _family(0, 0),
    }
    recap = recap_data(
        "2026-10-30",
        day,
        day,
        start="2026-10-30",
        owner_names={"sn1": "Brandon Rivera", "sn2": "Ken E"},
        group_senders={"ai_logs@halocollar.com"},
    )
    assert recap["labelers"] == 2
    assert [(r["person"], r["dogs"], r["sessions"], r["seconds"]) for r in recap["leaderboard"]] == [
        ("Brandon Rivera", ["Dixon"], 8, 800.0),
        ("Ken E", ["Rex"], 1, 100.0),
    ]


def _labeled(email, collar, labels):
    seconds = sum(labels.values())
    acts = [{"label": k, "seconds": v} for k, v in labels.items()]
    return {
        "email": email,
        "sessions": len(labels),
        "total_duration_seconds": seconds,
        "activities": acts,
        "collars": [
            {"collar_sn": collar, "sessions": len(labels), "total_duration_seconds": seconds, "activities": acts}
        ],
    }


def test_remote_needs_two_minutes_in_nine_labels_across_both_models():
    from backend.services.labeling_daily_report import remote_eligibility

    postures = {f"Posture{i}": 120 for i in range(6)}
    data = {
        **_family(0, 0, users=[
            _labeled("a@x.com", "sn1", postures),
            _labeled("b@x.com", "sn2", {**{f"Posture{i}": 300 for i in range(8)}, "Potty": 119}),
        ]),
        # a@ also labels three environments through the shared inbox on their collar.
        "gps": _family(0, 0, users=[
            _labeled("ai_logs@halocollar.com", "sn1", {"Indoor": 200, "Outdoor": 130, "Door": 125}),
        ]),
    }
    result = remote_eligibility(
        data,
        owner_names={"sn1": "Ana", "sn2": "Ben"},
        group_senders={"ai_logs@halocollar.com"},
    )
    assert result["eligible"] == 1
    ana, ben = result["people"]
    assert (ana["person"], ana["eligible"], len(ana["qualified"])) == ("Ana", True, 9)
    # Eight labels at 2 minutes or more; Potty is a second short.
    assert (ben["person"], ben["eligible"], len(ben["qualified"])) == ("Ben", False, 8)
    assert ben["close"] == [{"label": "Potty", "seconds": 119}]


def test_dog_leaderboard_ranks_dogs_with_their_people():
    from backend.services.labeling_daily_report import recap_data

    day = {
        **_family(
            10,
            1000,
            users=[
                _user("ken@x.com", 6, 500, [("sn1", 4, 300), ("sn2", 2, 200)]),
                _user("amy@x.com", 4, 500, [("sn1", 1, 100), ("sn3", 3, 400)]),
            ],
            dogs=[
                {"name": "Reese", "collar_sn": "sn1"},
                {"name": "Reese", "collar_sn": "sn2"},  # same dog, second collar
                {"name": "Bear", "collar_sn": "sn3"},
            ],
        ),
        "gps": _family(0, 0),
    }
    recap = recap_data("2026-10-30", day, day, start="2026-10-30")
    assert recap["dog_leaderboard"] == [
        {"dog": "Reese", "people": ["ken@x.com", "amy@x.com"], "sessions": 7, "seconds": 600.0,
         "medal": ":first_place_medal:"},
        {"dog": "Bear", "people": ["amy@x.com"], "sessions": 3, "seconds": 400.0,
         "medal": ":second_place_medal:"},
    ]


def test_labeler_type_defaults_halo_emails_to_employee_and_saved_types_win():
    from backend.services.labeling_daily_report import recap_data

    day = {
        **_family(
            6,
            600,
            users=[
                _user("amy@halocollar.com", 2, 200, [("sn1", 2, 200)]),
                _user("ken@x.com", 2, 200, [("sn2", 2, 200)]),
                _user("bo@x.com", 2, 200, [("sn3", 2, 200)]),
            ],
        ),
        "gps": _family(0, 0),
    }
    recap = recap_data(
        "2026-10-30", day, day, start="2026-10-30",
        names_by_email={"ken@x.com": "Ken E"},
        labeler_types={"ken e": "partner"},
    )
    types = {r["person"]: r["labeler_type"] for r in recap["leaderboard"]}
    assert types == {"amy@halocollar.com": "employee", "Ken E": "partner", "bo@x.com": None}
    assert recap["leaderboard"][0]["emails"] == ["amy@halocollar.com"]


def test_recap_ends_with_the_exact_period_and_time_zone():
    from datetime import date

    from backend.services.labeling_daily_report import build_daily_report, period_footnote

    note = period_footnote(date(2026, 10, 26), date(2026, 11, 1), "America/Los_Angeles")
    assert "Mon Oct 26 12:00 AM – Sun Nov 1, 2026 11:59 PM" in note
    assert "America/Los_Angeles (PST)" in note
    assert "PDT" in period_footnote(date(2026, 7, 4), date(2026, 7, 4), "America/Los_Angeles")

    empty = {"totals": {"sessions": 0, "duration_seconds": 0}, "users": [], "dogs": [], "by_date": []}
    text = build_daily_report("2026-11-01", empty, empty, days=7, timezone_name="America/Los_Angeles")
    assert text.splitlines()[-1].startswith("_Period: Mon Oct 26 12:00 AM")
