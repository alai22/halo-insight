"""Liveness, non-blocking summary, and bounded copy workers."""

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
