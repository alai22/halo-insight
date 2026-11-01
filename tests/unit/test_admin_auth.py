"""X-Admin-Token must be a token the server issued, not just any header value."""

import pytest
from flask import Flask, jsonify

from backend.api.middleware.auth import require_admin_auth
from backend.api.routes.auth_routes import auth_bp
from backend.services import auth_service
from backend.services.auth_service import AuthService


@pytest.fixture(autouse=True)
def _admin_password(monkeypatch):
    monkeypatch.setattr(auth_service.Config, "ADMIN_PASSWORD", "admin-pw")


def _app():
    app = Flask(__name__)
    app.secret_key = "test"
    app.register_blueprint(auth_bp)

    @app.route("/admin-only")
    @require_admin_auth
    def admin_only():
        return jsonify({"ok": True})

    return app


@pytest.mark.parametrize("header", ["x", "t", "anything", "123.abc", "9999999999.deadbeef"])
def test_arbitrary_header_is_rejected(header):
    client = _app().test_client()
    assert client.get("/admin-only", headers={"X-Admin-Token": header}).status_code == 401
    status = client.get("/api/auth/admin-status", headers={"X-Admin-Token": header})
    assert status.get_json()["admin_authenticated"] is False


def test_no_credentials_is_rejected():
    assert _app().test_client().get("/admin-only").status_code == 401


def test_issued_token_is_accepted():
    client = _app().test_client()
    headers = {"X-Admin-Token": AuthService.issue_admin_token()}
    assert client.get("/admin-only", headers=headers).status_code == 200
    assert client.get("/api/auth/admin-status", headers=headers).get_json()["admin_authenticated"] is True


def test_tampered_expiry_is_rejected():
    expires_at, signature = AuthService.issue_admin_token().split(".")
    forged = f"{int(expires_at) + 3600}.{signature}"
    assert _app().test_client().get("/admin-only", headers={"X-Admin-Token": forged}).status_code == 401


def test_expired_token_is_rejected(monkeypatch):
    monkeypatch.setattr(AuthService, "ADMIN_TOKEN_TTL_SECONDS", -1)
    token = AuthService.issue_admin_token()
    assert _app().test_client().get("/admin-only", headers={"X-Admin-Token": token}).status_code == 401


def test_changing_admin_password_revokes_tokens(monkeypatch):
    token = AuthService.issue_admin_token()
    monkeypatch.setattr(auth_service.Config, "ADMIN_PASSWORD", "rotated")
    assert _app().test_client().get("/admin-only", headers={"X-Admin-Token": token}).status_code == 401


def test_no_tokens_without_admin_password(monkeypatch):
    token = AuthService.issue_admin_token()
    monkeypatch.setattr(auth_service.Config, "ADMIN_PASSWORD", "")
    assert AuthService.issue_admin_token() is None
    assert _app().test_client().get("/admin-only", headers={"X-Admin-Token": token}).status_code == 401


def test_admin_session_is_accepted():
    client = _app().test_client()
    with client.session_transaction() as sess:
        sess["admin_authenticated"] = True
    assert client.get("/admin-only").status_code == 200


def test_admin_login_sets_session_and_returns_working_token():
    client = _app().test_client()
    response = client.post("/api/auth/admin-login", json={"password": "admin-pw"})
    assert response.status_code == 200
    token = response.get_json()["admin_token"]
    assert client.get("/admin-only").status_code == 200

    # Header alone (no session cookie) still works.
    cookieless = _app().test_client()
    assert cookieless.get("/admin-only").status_code == 401
    assert cookieless.get("/admin-only", headers={"X-Admin-Token": token}).status_code == 200


def test_admin_login_rejects_wrong_password():
    response = _app().test_client().post("/api/auth/admin-login", json={"password": "nope"})
    assert response.status_code == 401
    assert "admin_token" not in response.get_json()
