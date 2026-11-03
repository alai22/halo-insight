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
    seen = []

    class _Service:
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
    return seen


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
