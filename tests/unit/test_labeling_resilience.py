"""Liveness, non-blocking summary, and bounded copy workers."""

import pytest
from flask import Flask

from backend.api.routes import labeling_routes as routes
from backend.utils.runtime_stats import build_liveness, env_int, snapshot


def test_snapshot_reads_rss_on_linux():
    snap = snapshot()
    assert snap["rss_mb"] is None or snap["rss_mb"] > 0
    assert snap["started_at"].endswith("Z")
    assert snap["uptime_sec"] >= 0


def test_build_liveness_includes_job_flag():
    body = build_liveness({"running": True, "job": "process", "message": "copying"})
    assert body["status"] == "ok"
    assert body["job_running"] is True
    assert body["job"] == "process"
    assert body["job_message"] == "copying"
    assert "rss_mb" in body


def test_env_int_defaults_and_rejects_junk(monkeypatch):
    monkeypatch.delenv("LABELING_SYNC_WORKERS", raising=False)
    assert env_int("LABELING_SYNC_WORKERS", 4) == 4
    monkeypatch.setenv("LABELING_SYNC_WORKERS", "2")
    assert env_int("LABELING_SYNC_WORKERS", 4) == 2
    monkeypatch.setenv("LABELING_SYNC_WORKERS", "nope")
    assert env_int("LABELING_SYNC_WORKERS", 4) == 4
    monkeypatch.setenv("LABELING_SYNC_WORKERS", "0")
    assert env_int("LABELING_SYNC_WORKERS", 4) == 1


def _client():
    app = Flask(__name__)
    app.secret_key = "test"
    app.register_blueprint(routes.labeling_bp)
    return app.test_client()


def test_summary_never_scans_on_the_request(monkeypatch):
    called = {"compute": 0, "bg": 0}

    def _compute(_ttl):
        called["compute"] += 1
        raise AssertionError("summary scan ran on the request")

    def _bg(_ttl):
        called["bg"] += 1
        return True

    monkeypatch.setattr(routes, "_compute_summary", _compute)
    monkeypatch.setattr(routes, "_maybe_start_background_refresh", _bg)
    monkeypatch.setattr(routes, "_cache_get_memory", lambda _key: None)
    monkeypatch.setattr(routes, "_load_summary_cache_s3", lambda _ttl: None)

    response = _client().get("/api/labeling/summary", headers={"X-Admin-Token": "t"})
    assert response.status_code == 200
    body = response.get_json()
    assert body["success"] is True
    assert body["pending"] is True
    assert body["data"] is None
    assert called["compute"] == 0
    assert called["bg"] == 1


def test_summary_refresh_returns_last_payload_without_scanning(monkeypatch):
    called = {"compute": 0}

    monkeypatch.setattr(
        routes,
        "_compute_summary",
        lambda _ttl: called.__setitem__("compute", called["compute"] + 1),
    )
    monkeypatch.setattr(routes, "_maybe_start_background_refresh", lambda _ttl: True)
    monkeypatch.setattr(
        routes,
        "_cache_get_memory",
        lambda _key: {"data": {"totals": {"files": 3}}, "generated_at_iso": "2026-01-01T00:00:00Z", "stale": False},
    )
    monkeypatch.setattr(routes, "_load_summary_cache_s3", lambda _ttl: None)

    response = _client().get(
        "/api/labeling/summary?refresh=1", headers={"X-Admin-Token": "t"}
    )
    body = response.get_json()
    assert body["pending"] is True
    assert body["data"]["totals"]["files"] == 3
    assert called["compute"] == 0


def test_summary_waits_while_a_job_is_running(monkeypatch):
    monkeypatch.setattr(routes, "_compute_summary", lambda _ttl: None)
    monkeypatch.setattr(routes, "_is_process_busy", lambda: True)
    monkeypatch.setattr(routes, "_cache_get_memory", lambda _key: None)
    monkeypatch.setattr(routes, "_load_summary_cache_s3", lambda _ttl: None)

    response = _client().get("/api/labeling/summary", headers={"X-Admin-Token": "t"})
    body = response.get_json()
    assert body["pending"] is True
    assert "waits" in body["message"]


def test_status_route_returns_azure_configured_flag(monkeypatch):
    """The page hides collar sync when this flag is missing from the response."""
    monkeypatch.setattr(
        routes,
        "_staging_inventory",
        lambda: {"staging_extracted_files": 4, "output_files": 9},
    )
    monkeypatch.setattr(routes, "_merge_process_state", lambda: {"running": False, "job": None})
    monkeypatch.setattr(routes, "azure_configured", lambda: True)

    class _Index:
        def load_index(self):
            return None

    monkeypatch.setattr(routes, "LabelingCollarSyncService", _Index)

    response = _client().get("/api/labeling/status", headers={"X-Admin-Token": "t"})
    assert response.status_code == 200
    body = response.get_json()
    assert body["success"] is True
    assert body["data"]["staging_extracted_files"] == 4
    assert body["data"]["collar_sync"]["azure_configured"] is True


def test_root_health_returns_rss_without_service_container():
    import serve

    client = serve.app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    body = response.get_json()
    assert body["status"] == "ok"
    assert "rss_mb" in body
    assert "job_running" in body
    assert response.headers["Content-Type"].startswith("application/json")


def test_collar_sync_runs_after_process_only_when_files_changed(monkeypatch):
    monkeypatch.setattr(routes, "azure_configured", lambda: True)
    should = routes._should_sync_collar_after_process
    assert should({"copied": 3}, clear_output=False, dry_run=False, requested=True)
    assert should({"copied": 0}, clear_output=True, dry_run=False, requested=True)
    assert not should({"copied": 0}, clear_output=False, dry_run=False, requested=True)
    assert not should({"copied": 3}, clear_output=False, dry_run=True, requested=True)
    assert not should({"copied": 3}, clear_output=False, dry_run=False, requested=False)
    monkeypatch.setattr(routes, "azure_configured", lambda: False)
    assert not should({"copied": 3}, clear_output=False, dry_run=False, requested=True)


def test_collar_sync_after_process_keeps_both_messages(monkeypatch):
    states = []
    monkeypatch.setattr(routes, "_set_process_state", lambda **kw: states.append(kw) or kw)
    monkeypatch.setattr(routes, "_cache_clear", lambda: None)

    class _Service:
        def sync(self, dry_run, inventory_only):
            assert (dry_run, inventory_only) == (False, False)
            return {"copied": 4}

    monkeypatch.setattr(routes, "LabelingCollarSyncService", _Service)
    monkeypatch.setattr(routes, "sync_done_message", lambda report, _inv: "Synced 4.")
    routes._sync_collar_after_process("Processed 10.")

    assert states[0]["running"] is True and states[0]["job"] == "sync-collar"
    assert states[-1]["running"] is False
    assert states[-1]["message"] == "Processed 10. Synced 4."
    assert states[-1]["last_report"] == {"copied": 4}


def test_collar_sync_after_process_reports_failure(monkeypatch):
    states = []
    monkeypatch.setattr(routes, "_set_process_state", lambda **kw: states.append(kw) or kw)

    class _Service:
        def sync(self, dry_run, inventory_only):
            raise RuntimeError("azure down")

    monkeypatch.setattr(routes, "LabelingCollarSyncService", _Service)
    routes._sync_collar_after_process("Processed 10.")

    assert states[-1]["running"] is False
    assert states[-1]["job"] == "sync-collar"
    assert "Processing finished" in states[-1]["last_error"]
    assert "azure down" in states[-1]["last_error"]


def test_parse_window_accepts_open_ends_and_rejects_bad_ranges():
    assert routes._parse_window({}) is None
    assert routes._parse_window({"start": "2026-08-01"}) == ("2026-08-01", "9999-12-31")
    assert routes._parse_window({"end": "2026-10-30"}) == ("0000-01-01", "2026-10-30")
    with pytest.raises(ValueError):
        routes._parse_window({"start": "2026-10-30", "end": "2026-08-01"})
    with pytest.raises(ValueError):
        routes._parse_window({"start": "08/01/2026"})


def test_summary_with_dates_builds_window_in_background(monkeypatch):
    started = []
    monkeypatch.setattr(routes, "_maybe_start_window_refresh", lambda w: started.append(w) or True)
    monkeypatch.setattr(routes, "_compute_summary", lambda _ttl: (_ for _ in ()).throw(AssertionError))
    routes._window_cache_clear()

    response = _client().get(
        "/api/labeling/summary?start=2026-08-01&end=2026-10-30", headers={"X-Admin-Token": "t"}
    )
    body = response.get_json()
    assert body["pending"] is True
    assert body["data"] is None
    assert started == [("2026-08-01", "2026-10-30")]

    with routes._WINDOW_CACHE_LOCK:
        routes._WINDOW_CACHE["2026-08-01..2026-10-30"] = {
            "payload": {"window": {"start": "2026-08-01", "end": "2026-10-30"}},
            "generated_at": routes.time.time(),
        }
    body = _client().get(
        "/api/labeling/summary?start=2026-08-01&end=2026-10-30", headers={"X-Admin-Token": "t"}
    ).get_json()
    assert body["pending"] is False
    assert body["data"]["window"]["start"] == "2026-08-01"
    routes._window_cache_clear()
