"""Outside labeling viewers: email-link login, read-only labeling stats, nothing else."""

import pytest
from flask import Flask, jsonify

from backend.api.middleware.auth import require_auth, restrict_labeling_viewers
from backend.api.routes import labeling_routes as routes
from backend.api.routes.auth_routes import auth_bp
from backend.services import auth_service
from backend.services.auth_service import AuthService

VIEWER = "ashvin@edgeimpulse.com"


@pytest.fixture(autouse=True)
def _config(monkeypatch):
    monkeypatch.setattr(auth_service.Config, "LABELING_VIEWER_EMAILS", f"{VIEWER}, other@example.com")
    monkeypatch.setattr(auth_service.Config, "ALLOWED_EMAIL_DOMAINS", "halocollar.com")
    monkeypatch.setattr(auth_service.Config, "AUTH_PASSWORD", "user-pw")
    monkeypatch.setattr(auth_service.Config, "ADMIN_PASSWORD", "admin-pw")
    monkeypatch.setattr(routes, "_staging_inventory", lambda: {"files": 1})
    monkeypatch.setattr(routes, "_merge_process_state", lambda: {"running": False})
    monkeypatch.setattr(routes, "_load_collar_owners", lambda: ({}, None), raising=False)
    entry = {
        "generated_at_iso": "2026-11-01T00:00:00Z",
        "data": {"totals": {"sessions": 3}, "overview": {"recap": {}, "compensation": {"people": [1]}}},
    }
    monkeypatch.setattr(routes, "_cache_get_memory", lambda _key: entry)
    starts = []
    monkeypatch.setattr(routes, "_maybe_start_background_refresh", lambda ttl: starts.append(ttl) or True)
    return starts


def _app():
    app = Flask(__name__)
    app.secret_key = "test"
    app.before_request(restrict_labeling_viewers)
    app.register_blueprint(auth_bp)
    app.register_blueprint(routes.labeling_bp)

    @app.route("/api/interviews/list")
    @require_auth
    def interviews():
        return jsonify({"ok": True})

    @app.route("/api/conversations/summary")
    def unprotected():
        return jsonify({"ok": True})

    return app


def _viewer_client():
    client = _app().test_client()
    with client.session_transaction() as sess:
        sess["authenticated"] = True
        sess["email"] = VIEWER
        sess["role"] = "labeling_viewer"
    return client


def test_viewer_email_can_request_a_login_link():
    assert AuthService.can_request_login(VIEWER)
    assert AuthService.can_request_login("ASHVIN@edgeimpulse.com ")
    assert not AuthService.can_request_login("someone@edgeimpulse.com")
    assert AuthService.can_request_login("staff@halocollar.com")


def test_email_link_gives_a_viewer_session_without_admin():
    client = _app().test_client()
    with client.session_transaction() as sess:
        sess["admin_authenticated"] = True  # left over from someone else in this browser
    token = AuthService.generate_token(VIEWER)
    client.get(f"/api/auth/verify?token={token}")
    status = client.get("/api/auth/status").get_json()
    assert status["authenticated"] is True
    assert status["role"] == "labeling_viewer"
    assert client.get("/api/auth/admin-status").get_json()["admin_authenticated"] is False


def test_staff_email_link_has_no_viewer_role():
    client = _app().test_client()
    client.get(f"/api/auth/verify?token={AuthService.generate_token('staff@halocollar.com')}")
    assert client.get("/api/auth/status").get_json()["role"] is None


def test_viewer_reads_labeling_stats_without_pay():
    client = _viewer_client()
    assert client.get("/api/labeling/status").status_code == 200
    body = client.get("/api/labeling/summary").get_json()
    assert body["data"]["totals"]["sessions"] == 3
    assert "compensation" not in body["data"]["overview"]


def test_admin_still_sees_pay():
    client = _app().test_client()
    with client.session_transaction() as sess:
        sess["admin_authenticated"] = True
    body = client.get("/api/labeling/summary").get_json()
    assert body["data"]["overview"]["compensation"] == {"people": [1]}


def test_viewer_refresh_and_tiny_ttl_do_not_start_a_rescan(_config):
    client = _viewer_client()
    client.get("/api/labeling/summary?refresh=1&ttl=1")
    assert _config == []


@pytest.mark.parametrize(
    "method,path",
    [
        ("POST", "/api/labeling/process"),
        ("POST", "/api/labeling/sync-collar"),
        ("POST", "/api/labeling/promote-forwards"),
        ("POST", "/api/labeling/compact"),
        ("PUT", "/api/labeling/collar-owners"),
        ("PUT", "/api/labeling/labeler-types"),
        ("POST", "/api/labeling/daily-report"),
        ("GET", "/api/labeling/daily-report/preview"),
        ("GET", "/api/labeling/ml-processed"),
        ("GET", "/api/interviews/list"),
        ("GET", "/api/conversations/summary"),
        ("POST", "/api/auth/admin-login"),
    ],
)
def test_viewer_is_blocked_everywhere_else(method, path):
    response = _viewer_client().open(path, method=method, json={})
    assert response.status_code == 403


def test_viewer_cannot_use_an_admin_token_to_escape():
    # A viewer who somehow holds an admin token still only reaches the allowlist.
    client = _viewer_client()
    headers = {"X-Admin-Token": AuthService.issue_admin_token()}
    assert client.post("/api/labeling/process", json={}, headers=headers).status_code == 403


def test_signed_auth_token_required_for_header_login():
    client = _app().test_client()
    assert client.get("/api/interviews/list", headers={"X-Auth-Token": "x"}).status_code == 401
    assert client.get("/api/auth/status", headers={"X-Auth-Token": "x"}).get_json()["authenticated"] is False
    token = client.post("/api/auth/password-login", json={"password": "user-pw"}).get_json()["auth_token"]
    fresh = _app().test_client()
    assert fresh.get("/api/interviews/list", headers={"X-Auth-Token": token}).status_code == 200


def test_admin_and_auth_tokens_are_not_interchangeable():
    client = _app().test_client()
    assert client.get("/api/labeling/status", headers={"X-Admin-Token": AuthService.issue_auth_token()}).status_code == 401
