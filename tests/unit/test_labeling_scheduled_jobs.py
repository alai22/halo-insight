"""Scheduled Process and Remove-duplicates runs: X-Report-Secret gets in, but only a safe run."""

import pytest
from flask import Flask

from backend.api.routes import labeling_routes as routes
from backend.services.auth_service import AuthService


@pytest.fixture(autouse=True)
def _config(monkeypatch):
    monkeypatch.setattr(routes.Config, "ADMIN_PASSWORD", "admin-pw")
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SECRET", "s3cret")
    monkeypatch.setattr(routes, "_is_process_busy", lambda: False)
    monkeypatch.setattr(routes, "_gmail_writing_staging", lambda: False)
    monkeypatch.setattr(routes, "_set_process_state", lambda **kw: kw)
    monkeypatch.setattr(routes, "_merge_process_state", lambda: {"running": True})
    monkeypatch.setattr(routes, "_cache_mark_stale", lambda: None)


def _client():
    app = Flask(__name__)
    app.secret_key = "test"
    app.register_blueprint(routes.labeling_bp)
    return app.test_client()


@pytest.fixture
def calls(monkeypatch):
    """Record what each job was asked to do; background workers run inline, with no S3."""
    seen = _Calls()

    class _Service:
        pending = {"pending": [], "unresolved": []}

        def pending_forwards(self):
            return self.pending

        def promote_forwards(self, message_ids):
            seen.append(("promote", tuple(message_ids)))
            return {"promoted": list(message_ids), "errors": []}

        def process_staging(self, dry_run, clear_output, on_progress):
            seen.append(("process", clear_output))
            return {"copied": 0}

        def compact_staging(self, dry_run, on_progress):
            seen.append(("compact", dry_run))
            return {}

    class _Thread:
        def __init__(self, target, daemon=None, **kw):
            self._target = target

        def start(self):
            seen.append(("background", None))
            self._target()

    monkeypatch.setattr(routes, "LabelingIngestService", _Service)
    monkeypatch.setattr(routes.threading, "Thread", _Thread)
    seen.service = _Service
    return seen


class _Calls(list):
    service = None


@pytest.mark.parametrize("path", ["/api/labeling/process", "/api/labeling/compact"])
def test_wrong_or_missing_secret_is_refused(path, calls):
    client = _client()
    assert client.post(path, json={}).status_code == 401
    assert client.post(path, json={}, headers={"X-Report-Secret": "wrong"}).status_code == 401
    assert calls == []


@pytest.mark.parametrize("path", ["/api/labeling/process", "/api/labeling/compact"])
def test_unset_secret_lets_nobody_in(path, monkeypatch, calls):
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SECRET", "")
    assert _client().post(path, json={}, headers={"X-Report-Secret": ""}).status_code == 401
    assert calls == []


def test_scheduled_process_never_wipes_and_runs_in_the_background(calls):
    response = _client().post(
        "/api/labeling/process",
        json={"clear_output": True, "async": False},
        headers={"X-Report-Secret": "s3cret"},
    )
    assert response.status_code == 200
    assert response.get_json()["async"] is True
    assert calls == [("background", None), ("process", False)]


def test_scheduled_compact_runs_in_the_background(calls):
    response = _client().post(
        "/api/labeling/compact",
        json={"async": False, "dry_run": True},
        headers={"X-Report-Secret": "s3cret"},
    )
    assert response.status_code == 200
    assert calls == [("background", None), ("compact", True)]


def test_admin_can_still_rebuild_inline(calls):
    headers = {"X-Admin-Token": AuthService.issue_admin_token()}
    response = _client().post(
        "/api/labeling/process", json={"async": False, "clear_output": True}, headers=headers
    )
    assert response.status_code == 200
    assert calls == [("process", True)]


@pytest.fixture
def notices(monkeypatch):
    sent = []
    monkeypatch.setattr(routes, "_notify_scheduled_job", lambda job, ok, detail: sent.append((job, ok, detail)))
    return sent


def test_scheduled_process_posts_success(calls, notices):
    _client().post("/api/labeling/process", json={}, headers={"X-Report-Secret": "s3cret"})
    assert [(job, ok) for job, ok, _ in notices] == [("Process staging", True)]
    assert "copied 0 files" in notices[0][2]


def test_scheduled_process_posts_failure(calls, notices, monkeypatch):
    class _Broken:
        def pending_forwards(self):
            return {"pending": [], "unresolved": []}

        def process_staging(self, **kw):
            raise RuntimeError("S3 is down")

    monkeypatch.setattr(routes, "LabelingIngestService", _Broken)
    _client().post("/api/labeling/process", json={}, headers={"X-Report-Secret": "s3cret"})
    assert notices == [("Process staging", False, "S3 is down")]


def test_scheduled_compact_posts_its_result(calls, notices):
    _client().post("/api/labeling/compact", json={}, headers={"X-Report-Secret": "s3cret"})
    assert [(job, ok) for job, ok, _ in notices] == [("Remove duplicate copies", True)]


def test_an_admin_run_posts_nothing(calls, notices):
    headers = {"X-Admin-Token": AuthService.issue_admin_token()}
    _client().post("/api/labeling/process", json={}, headers=headers)
    _client().post("/api/labeling/compact", json={}, headers=headers)
    assert notices == []


def test_notice_goes_to_the_first_channel_and_never_raises(monkeypatch):
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_WEBHOOK_URL", None)
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_CHANNEL", "C1:data-labeling,C2:other")
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SLACK_TOKEN", "xoxb-test")
    monkeypatch.setattr(routes.Config, "APP_BASE_URL", "https://insight.example.com/")
    posted = []
    monkeypatch.setattr(routes, "post_to_slack", lambda token, channel, text: posted.append((channel, text)))
    routes._notify_scheduled_job("Process staging", False, "S3 is down")
    assert posted == [(
        "C1",
        ":x: Scheduled *Process staging* failed. S3 is down"
        "\n<https://insight.example.com|Open the dashboard>",
    )]

    def _boom(*a):
        raise RuntimeError("channel_not_found")

    monkeypatch.setattr(routes, "post_to_slack", _boom)
    routes._notify_scheduled_job("Process staging", True, "Done")  # logged, not raised


def test_scheduled_process_promotes_known_forwards_first(calls, notices):
    calls.service.pending = {
        "pending": [{"message_id": "m1"}, {"message_id": "m2"}],
        "unresolved": [{"message_id": "m3"}],
    }
    _client().post("/api/labeling/process", json={}, headers={"X-Report-Secret": "s3cret"})
    assert calls == [("background", None), ("promote", ("m1", "m2")), ("process", False)]
    detail = notices[0][2]
    assert "Promoted 2 forwarded batch(es) first." in detail
    assert "1 forwarded batch(es) need a labeler" in detail


def test_an_admin_process_does_not_promote(calls, notices):
    calls.service.pending = {"pending": [{"message_id": "m1"}], "unresolved": []}
    headers = {"X-Admin-Token": AuthService.issue_admin_token()}
    _client().post("/api/labeling/process", json={}, headers=headers)
    assert ("promote", ("m1",)) not in calls


def test_a_failed_promote_still_processes_and_is_reported(calls, notices):
    def _boom(self, message_ids):
        raise RuntimeError("S3 copy failed")

    calls.service.pending = {"pending": [{"message_id": "m1"}], "unresolved": []}
    calls.service.promote_forwards = _boom
    _client().post(
        "/api/labeling/process", json={"quiet": True}, headers={"X-Report-Secret": "s3cret"}
    )
    assert ("process", False) in calls
    assert [(job, ok) for job, ok, _ in notices] == [("Process staging", False)]
    assert "Promoting forwards failed: S3 copy failed." in notices[0][2]


def test_a_quiet_run_posts_only_failures(calls, notices, monkeypatch):
    _client().post(
        "/api/labeling/process", json={"quiet": True}, headers={"X-Report-Secret": "s3cret"}
    )
    assert notices == []

    class _Broken:
        def pending_forwards(self):
            return {"pending": [], "unresolved": []}

        def process_staging(self, **kw):
            raise RuntimeError("S3 is down")

    monkeypatch.setattr(routes, "LabelingIngestService", _Broken)
    _client().post(
        "/api/labeling/process", json={"quiet": True}, headers={"X-Report-Secret": "s3cret"}
    )
    assert notices == [("Process staging", False, "S3 is down")]


def test_a_quiet_run_with_collar_sync_posts_nothing_on_success(calls, notices, monkeypatch):
    monkeypatch.setattr(routes, "_should_sync_collar_after_process", lambda *a: True)
    monkeypatch.setattr(routes, "_owner_collar_sns", lambda: [])
    monkeypatch.setattr(routes, "sync_done_message", lambda report, dry: "Synced.")

    class _Sync:
        def sync(self, **kw):
            return {}

    monkeypatch.setattr(routes, "LabelingCollarSyncService", _Sync)
    _client().post(
        "/api/labeling/process", json={"quiet": True}, headers={"X-Report-Secret": "s3cret"}
    )
    assert notices == []
    _client().post("/api/labeling/process", json={}, headers={"X-Report-Secret": "s3cret"})
    assert [(job, ok) for job, ok, _ in notices] == [("Process staging", True)]
