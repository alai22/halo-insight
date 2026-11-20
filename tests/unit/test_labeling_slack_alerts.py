"""Slack alerts: Gmail ingest failing, giving up on an email or stalling, and forwards
nobody can place in the daily Process post."""

import pytest
from flask import Flask

from backend.api.routes import labeling_routes as routes
from backend.services import labeling_gmail_ingest_service as gsvc


@pytest.fixture(autouse=True)
def _reset(monkeypatch):
    monkeypatch.setattr(routes.Config, "LABELING_REPORT_SECRET", "s3cret")
    monkeypatch.setattr(routes.Config, "LABELING_GMAIL_INGEST_MODE", "live")
    routes._GMAIL_ALERT.update(failed_runs=0, failing=False, stalled=False)
    routes._GMAIL_STATE.update(running=False, last_error=None, last_compare_at=0.0)
    yield
    routes._GMAIL_ALERT.update(failed_runs=0, failing=False, stalled=False)


@pytest.fixture
def posted(monkeypatch):
    sent = []
    monkeypatch.setattr(routes, "_notify_recap_channel", lambda text, what: sent.append(text))
    return sent


def _report(**kw):
    return {"ingested": 0, "quarantined": 0, "errors": [], "warnings": [], "batches": [], **kw}


def _gmail(monkeypatch, outcomes):
    """Each run takes the next outcome: an exception to raise, or a report to return."""

    class _Service:
        mode = "live"

        def run(self, **kw):
            outcome = outcomes.pop(0)
            if isinstance(outcome, Exception):
                raise outcome
            return outcome

    monkeypatch.setattr(gsvc, "LabelingGmailIngestService", _Service)


def _run(kind="poll", dry_run=False):
    try:
        routes.run_gmail_ingest(kind, dry_run=dry_run)
    except RuntimeError:
        pass


def test_failing_ingest_posts_once_after_three_runs_then_recovery(monkeypatch, posted):
    boom = RuntimeError("invalid_grant")
    _gmail(monkeypatch, [boom, boom, boom, boom, _report(ingested=2)])
    _run()
    _run()
    assert posted == []
    _run()
    assert len(posted) == 1 and "Gmail ingest* is failing" in posted[0]
    assert "invalid_grant" in posted[0]
    _run()
    assert len(posted) == 1
    _run()
    assert len(posted) == 2 and "working again" in posted[1] and "2 email(s)" in posted[1]


def test_one_failure_then_success_stays_quiet(monkeypatch, posted):
    _gmail(monkeypatch, [RuntimeError("blip"), _report(), RuntimeError("blip"), RuntimeError("blip")])
    for _ in range(4):
        _run()
    assert posted == []


def test_dry_runs_never_alert(monkeypatch, posted):
    _gmail(monkeypatch, [RuntimeError("x")] * 4)
    for _ in range(4):
        _run(dry_run=True)
    assert posted == []


def test_email_given_up_on_is_posted(monkeypatch, posted):
    errors = [
        {"message_id": "m1", "error": "bad zip", "attempts": gsvc.MAX_ATTEMPTS},
        {"message_id": "m2", "error": "timeout", "attempts": 1},
    ]
    _gmail(monkeypatch, [_report(errors=errors)])
    _run()
    assert len(posted) == 1
    assert "gave up on 1 email(s)" in posted[0] and "`m1`" in posted[0] and "m2" not in posted[0]


def test_stall_posts_once_and_again_when_it_resumes(monkeypatch, posted):
    status = {"enabled": True, "stalled": True, "last_run": {"finished_at": "2026-11-20T08:00:00Z"}}
    monkeypatch.setattr(routes, "_gmail_ingest_status", lambda: status)
    routes._gmail_alert_check_stalled()
    routes._gmail_alert_check_stalled()
    assert len(posted) == 1 and "stopped checking" in posted[0] and "2026-11-20T08:00:00Z" in posted[0]
    status["stalled"] = False
    routes._gmail_alert_check_stalled()
    assert len(posted) == 2 and "checking the inbox again" in posted[1]


def test_stall_check_ignores_a_disabled_ingester(monkeypatch, posted):
    monkeypatch.setattr(routes, "_gmail_ingest_status", lambda: {"enabled": False, "stalled": True})
    routes._gmail_alert_check_stalled()
    assert posted == []


# --- scheduled Process: stall watchdog and forwards nobody can place ---------------------


def _client():
    app = Flask(__name__)
    app.secret_key = "test"
    app.register_blueprint(routes.labeling_bp)
    return app.test_client()


@pytest.fixture
def process(monkeypatch):
    notices, checks = [], []
    monkeypatch.setattr(routes.Config, "ADMIN_PASSWORD", "admin-pw")
    monkeypatch.setattr(routes, "_is_process_busy", lambda: False)
    monkeypatch.setattr(routes, "_gmail_writing_staging", lambda: False)
    monkeypatch.setattr(routes, "_set_process_state", lambda **kw: kw)
    monkeypatch.setattr(routes, "_merge_process_state", lambda: {"running": True})
    monkeypatch.setattr(routes, "_refresh_summary_after_process", lambda *a: None)
    monkeypatch.setattr(routes, "_gmail_alert_check_stalled", lambda: checks.append(True))
    monkeypatch.setattr(
        routes, "_notify_scheduled_job", lambda job, ok, detail: notices.append((ok, detail))
    )

    class _Service:
        def pending_forwards(self):
            return {"pending": [], "unresolved": [{"message_id": "fw1"}, {"message_id": "fw2"}]}

        def process_staging(self, **kw):
            return {"copied": 0}

    class _Thread:
        def __init__(self, target, daemon=None, **kw):
            self._target = target

        def start(self):
            self._target()

    monkeypatch.setattr(routes, "LabelingIngestService", _Service)
    monkeypatch.setattr(routes.threading, "Thread", _Thread)
    return notices, checks


def test_daily_post_lists_forwards_nobody_can_place(process):
    notices, checks = process
    _client().post("/api/labeling/process", json={}, headers={"X-Report-Secret": "s3cret"})
    assert checks == [True]
    ok, detail = notices[0]
    assert ok is True
    assert "\n:warning: 2 forwarded email(s) don't say who first sent them" in detail
    assert "`fw1`, `fw2`" in detail


def test_quiet_run_still_checks_for_a_stall_but_posts_nothing(process):
    notices, checks = process
    _client().post(
        "/api/labeling/process", json={"quiet": True}, headers={"X-Report-Secret": "s3cret"}
    )
    assert checks == [True]
    assert notices == []
