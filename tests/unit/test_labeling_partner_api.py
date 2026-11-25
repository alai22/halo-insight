"""Partner API: Treat Therapeutics sees its own participants and nobody else's labeling."""

import pytest
from flask import Flask

from backend.api.middleware.auth import restrict_labeling_viewers
from backend.api.routes import labeling_partner_routes as routes
from backend.api.routes import labeling_routes as lr
from backend.api.routes.auth_routes import auth_bp
from backend.services import labeling_partner_service as svc


def _session(email, ts, labels, dog="Rex", sid=None):
    return {
        "email": email,
        "session_id": sid or f"{ts}_0",
        "timestamp": ts,
        "collar_sn": "sn1",
        "dog": dog,
        "duration_seconds": sum(labels.values()),
        "files": 3,
        "kinds": ["durations"],
        "activities": labels,
    }


SUMMARY = {
    "session_log": [
        _session("ana@treat.example", "2026-11-10T09:00:00", {"Lying": 120, "Potty1": 50}),
        _session("ana@treat.example", "2026-11-12T09:00:00", {"Lying": 90, "PottyTwo": 20}),
        _session("halo.labeler@gmail.com", "2026-11-12T10:00:00", {"Lying": 999}, dog="Secret"),
    ],
    "gps": {
        "session_log": [
            _session("ana@treat.example", "2026-11-12T11:00:00", {"OutdoorOpenSky": 30}),
            _session("halo.labeler@gmail.com", "2026-11-12T12:00:00", {"Door": 500}),
        ]
    },
}


@pytest.fixture(autouse=True)
def store(monkeypatch):
    saved = {}

    def _save(config):
        config = svc.normalize_config(config)
        saved["config"] = config
        return config

    config = svc.normalize_config({
        "orgs": {"treat": {
            "participants": ["ana@treat.example", "new.recruit@treat.example"],
            "logins": ["coordinator@treat.example"],
        }}
    })
    key, record = svc.new_api_key("treat", "test")
    config["orgs"]["treat"]["keys"].append(record)
    saved["config"] = config
    monkeypatch.setattr(svc, "load_config", lambda force=False: saved["config"])
    monkeypatch.setattr(svc, "save_config", _save)
    monkeypatch.setattr(lr, "_cache_get_memory", lambda key: {"data": SUMMARY, "generated_at_iso": "2026-11-25T00:00:00Z"})
    monkeypatch.setattr(routes, "_names_by_email", lambda: {"ana@treat.example": "Ana"})
    monkeypatch.setattr(lr.Config, "ADMIN_PASSWORD", "admin-pw")
    saved["key"] = key
    return saved


def _client():
    app = Flask(__name__)
    app.secret_key = "test"
    app.before_request(restrict_labeling_viewers)
    app.register_blueprint(routes.partner_bp)
    app.register_blueprint(routes.partner_admin_bp)
    app.register_blueprint(lr.labeling_bp)
    app.register_blueprint(auth_bp)
    return app.test_client()


def _get(client, path, key):
    return client.get(path, headers={"Authorization": f"Bearer {key}"})


def test_participants_lists_only_treats_people_with_label_progress(store):
    body = _get(_client(), "/api/partner/v1/participants", store["key"]).get_json()
    assert body["organization"] == "Treat Therapeutics"
    assert [p["email"] for p in body["participants"]] == ["ana@treat.example", "new.recruit@treat.example"]
    ana, recruit = body["participants"]
    assert ana["name"] == "Ana" and ana["sessions"] == 3 and ana["dogs"] == ["Rex"]
    assert ana["labels"]["Lying"] == {"minutes": 3.5, "remaining_minutes": 0.0, "done": True}
    # Potty1 and PottyTwo count as Potty.
    assert ana["labels"]["Potty"]["minutes"] == 1.17
    assert ana["labels"]["OutdoorOpenSky"]["minutes"] == 0.5
    assert ana["labels_done"] == 1 and ana["first_contribution"] == "2026-11-10"
    assert recruit["sessions"] == 0 and recruit["labels_done"] == 0
    assert "halo.labeler" not in str(body) and "Secret" not in str(body)


def test_date_range_and_daily_and_sessions(store):
    c = _client()
    body = _get(c, "/api/partner/v1/participants?start=2026-11-12&end=2026-11-12", store["key"]).get_json()
    assert body["participants"][0]["sessions"] == 2
    daily = _get(c, "/api/partner/v1/participants/ana@treat.example/daily", store["key"]).get_json()
    assert [(d["date"], d["sessions"]) for d in daily["days"]] == [("2026-11-10", 1), ("2026-11-12", 2)]
    assert daily["days"][1]["labels"] == {"Lying": 1.5, "OutdoorOpenSky": 0.5, "Potty": 0.33}
    sessions = _get(c, "/api/partner/v1/participants/ana@treat.example/sessions", store["key"]).get_json()
    assert sessions["sessions"][0]["model"] == "indoor_outdoor"
    assert len(sessions["sessions"]) == 3


def test_someone_elses_labeler_looks_unknown(store):
    c = _client()
    for path in ("daily", "sessions"):
        r = _get(c, f"/api/partner/v1/participants/halo.labeler@gmail.com/{path}", store["key"])
        assert r.status_code == 404


@pytest.mark.parametrize("key", ["", "hlp_treat_wrong", "hlp_other_x", "nonsense"])
def test_bad_keys_are_refused(store, key):
    r = _client().get("/api/partner/v1/participants", headers={"X-API-Key": key} if key else {})
    assert r.status_code == 401


def test_revoked_key_stops_working(store):
    c = _client()
    record_id = store["config"]["orgs"]["treat"]["keys"][0]["id"]
    with c.session_transaction() as s:
        s["admin_authenticated"] = True
    assert c.delete(f"/api/labeling/partners/treat/keys/{record_id}").status_code == 200
    with c.session_transaction() as s:
        s.clear()
    assert _get(c, "/api/partner/v1/participants", store["key"]).status_code == 401


def test_bad_dates_are_rejected(store):
    r = _get(_client(), "/api/partner/v1/participants?start=11/12/2026", store["key"])
    assert r.status_code == 400


def _partner_session(c, email="coordinator@treat.example"):
    with c.session_transaction() as s:
        s.update(authenticated=True, email=email, role="labeling_partner", partner_org="treat")


def test_partner_login_sees_its_participants_and_nothing_else(store):
    c = _client()
    _partner_session(c)
    assert c.get("/api/partner/v1/participants").status_code == 200
    # No admin preview of other orgs, no labeling dashboard, no writes.
    assert c.get("/api/labeling/summary").status_code == 403
    assert c.get("/api/labeling/partners").status_code == 403
    assert c.put("/api/labeling/partners/treat", json={"participants": ["x@y.com"]}).status_code == 403


def test_removed_login_loses_access_at_once(store):
    c = _client()
    _partner_session(c)
    store["config"]["orgs"]["treat"]["logins"] = []
    assert c.get("/api/partner/v1/participants").status_code == 401


def test_admin_can_preview_and_edit(store):
    c = _client()
    with c.session_transaction() as s:
        s["admin_authenticated"] = True
    assert c.get("/api/partner/v1/participants").status_code == 401
    assert c.get("/api/partner/v1/participants?org=treat").status_code == 200
    r = c.put("/api/labeling/partners/treat", json={"participants": ["B@Treat.example ", "b@treat.example"]})
    assert r.get_json()["orgs"]["treat"]["participants"] == ["b@treat.example"]
    assert c.put("/api/labeling/partners/treat", json={"participants": ["not an email"]}).status_code == 400
    created = c.post("/api/labeling/partners/treat/keys", json={"label": "prod"}).get_json()
    assert created["key"].startswith("hlp_treat_")
    assert "sha256" not in str(created["orgs"])


def test_admin_endpoints_need_admin(store):
    c = _client()
    assert c.get("/api/labeling/partners").status_code == 401
    assert c.post("/api/labeling/partners/treat/keys").status_code == 401


def test_partner_staff_can_request_a_login_link(store):
    from backend.services.auth_service import AuthService

    assert AuthService.can_request_login("coordinator@treat.example")
    assert not AuthService.can_request_login("ana@treat.example")
