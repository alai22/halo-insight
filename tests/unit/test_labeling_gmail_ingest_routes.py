"""Gmail ingester on /status, and it never overlaps a staging job."""

import pytest
from flask import Flask

from backend.api.routes import labeling_routes as routes
from backend.services import labeling_gmail_ingest_service as gsvc
from backend.services.auth_service import AuthService


@pytest.fixture(autouse=True)
def _config(monkeypatch):
    monkeypatch.setattr(routes.Config, "ADMIN_PASSWORD", "admin-pw")
    monkeypatch.setattr(routes.Config, "LABELING_GMAIL_INGEST_ENABLED", True)
    monkeypatch.setattr(routes.Config, "LABELING_GMAIL_SERVICE_ACCOUNT_JSON", None)
    monkeypatch.setattr(routes.Config, "LABELING_GMAIL_OAUTH_REFRESH_TOKEN", "1//tok")
    monkeypatch.setattr(routes.Config, "LABELING_GMAIL_INGEST_MODE", "live")
    routes._GMAIL_STATUS_CACHE.update(at=0.0, data=None)
    routes._GMAIL_STATE.update(running=False, last_error=None, poller_started_at=None)
    yield
    routes._GMAIL_STATUS_CACHE.update(at=0.0, data=None)


def _client():
    app = Flask(__name__)
    app.secret_key = "test"
    app.register_blueprint(routes.labeling_bp)
    return app.test_client()


def _headers():
    return {"X-Admin-Token": AuthService.issue_admin_token()}


class _FakeService:
    def __init__(self, *a, **kw):
        pass

    def load_state(self):
        return {
            "last_run": {"finished_at": "2026-11-02T10:00:00Z", "ingested": 3, "errors": 0},
            "totals": {"ingested": 12, "quarantined": 1, "errors": 0},
            "recent_errors": [],
            "failures": {},
        }

    def load_compare(self):
        return {"agrees": True, "both": 5}


def test_status_reports_gmail_ingest_block(monkeypatch):
    monkeypatch.setattr(routes, "_staging_inventory", lambda: {"uploads": {"stalled": []}})
    monkeypatch.setattr(routes, "_merge_process_state", lambda: {"running": False})
    monkeypatch.setattr(routes, "azure_configured", lambda: False)
    monkeypatch.setattr(routes, "LabelingCollarSyncService", lambda: type("I", (), {"load_index": lambda s: None})())
    monkeypatch.setattr(gsvc, "LabelingGmailIngestService", _FakeService)

    body = _client().get("/api/labeling/status", headers=_headers()).get_json()
    block = body["data"]["gmail_ingest"]
    assert "uploads" in body["data"]
    assert block["enabled"] and block["mode"] == "live"
    assert block["configured"] and block["auth"] == "oauth"
    assert block["last_run"]["ingested"] == 3
    assert block["totals"]["ingested"] == 12
    assert block["compare"]["agrees"] is True
    assert block["stalled"] is False


def test_stalled_when_no_run_finishes(monkeypatch):
    monkeypatch.setattr(gsvc, "LabelingGmailIngestService", _FakeService)
    routes._GMAIL_STATE["poller_started_at"] = "2026-11-01T00:00:00Z"
    assert routes._gmail_ingest_status()["stalled"] is True


def test_process_refused_while_live_ingest_writes(monkeypatch):
    monkeypatch.setattr(routes, "_is_process_busy", lambda: False)
    routes._GMAIL_STATE["running"] = True
    try:
        resp = _client().post("/api/labeling/process", json={}, headers=_headers())
    finally:
        routes._GMAIL_STATE["running"] = False
    assert resp.status_code == 409
    assert "Gmail" in resp.get_json()["error"]


def test_poll_skips_while_process_runs_in_live_mode(monkeypatch):
    monkeypatch.setattr(routes, "_is_process_busy", lambda: True)
    called = []
    monkeypatch.setattr(routes, "run_gmail_ingest", lambda kind: called.append(kind))
    routes._gmail_poll_once()
    assert called == []


def test_second_run_does_not_overlap(monkeypatch):
    assert routes._GMAIL_LOCK.acquire(blocking=False)
    try:
        assert routes.run_gmail_ingest("poll") is None
    finally:
        routes._GMAIL_LOCK.release()


def test_backfill_endpoint_validates_date():
    resp = _client().post("/api/labeling/gmail-ingest/run", json={"since": "Nov 1"}, headers=_headers())
    assert resp.status_code == 400


def test_backfill_endpoint_requires_admin():
    resp = _client().post("/api/labeling/gmail-ingest/run", json={"since": "2026-11-01"})
    assert resp.status_code in (401, 403)


def test_poller_off_unless_enabled(monkeypatch):
    monkeypatch.setattr(routes.Config, "LABELING_GMAIL_INGEST_ENABLED", False)
    assert routes.start_gmail_ingest_poller() is False
