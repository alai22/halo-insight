"""Per-labeler session log: built with the summary, served by /api/labeling/sessions."""

import pytest
from flask import Flask

from backend.api.routes import labeling_routes as routes
from backend.services.auth_service import AuthService
from backend.services.labeling_data_analyzer import (
    LabelingDataAnalyzer,
    SessionFileRef,
    format_ui_summary,
)

DURATIONS = {
    "2026-10-27T10:00:00": b'{"Walking (1)": "00:01:30", "Lying (8)": "00:00:30", "Barking (14)": "00:00:00"}',
    "2026-10-28T10:00:00": b'{"Sniffing (6)": "00:00:45"}',
}


def _summary():
    def ref(user, ts, kind):
        return SessionFileRef(
            key=f"x/{user}/sn1/{ts}_{kind}.txt", user=user, filename=f"{ts}_{kind}.txt",
            timestamp=ts, index=0, kind=kind, size=11, collar_sn="25h5425925vm",
        )

    files = [
        ref("ana@halocollar.com", "2026-10-27T10:00:00", "durations"),
        ref("ana@halocollar.com", "2026-10-27T10:00:00", "user_reported"),
        ref("ana@halocollar.com", "2026-10-28T10:00:00", "durations"),
        ref("ben@halocollar.com", "2026-10-28T10:00:00", "durations"),
    ]

    class _S3:
        def get_object(self, Bucket, Key):  # noqa: N803
            ts = Key.split("/")[-1][:19]
            body = DURATIONS[ts] if Key.endswith("durations.txt") else b""

            class _B:
                def read(self):
                    return body

            return {"Body": _B()}

    analyzer = LabelingDataAnalyzer(bucket_name="log-test", prefix="x/", s3_client=_S3())
    return format_ui_summary(analyzer.analyze(include_content=True, files=files))


def test_session_log_has_one_row_per_session_with_activities():
    log = _summary()["session_log"]
    ana = [r for r in log if r["email"] == "ana@halocollar.com"]
    assert len(ana) == 2
    first = next(r for r in ana if r["timestamp"] == "2026-10-27T10:00:00")
    assert first["duration_seconds"] == 120
    assert first["files"] == 2
    assert first["kinds"] == ["durations", "user_reported"]
    # Zero-second activities are left out, largest first.
    assert list(first["activities"].values()) == [90, 30]
    assert first["collar_sn"] == "25h5425925vm"


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(routes.Config, "ADMIN_PASSWORD", "admin-pw")
    data = _summary()
    monkeypatch.setattr(routes, "_cache_get_memory", lambda _key: {"data": data, "stale": False})
    monkeypatch.setattr(routes, "_maybe_start_background_refresh", lambda _ttl: True)
    app = Flask(__name__)
    app.secret_key = "test"
    app.register_blueprint(routes.labeling_bp)
    test_client = app.test_client()
    test_client.environ_base["HTTP_X_ADMIN_TOKEN"] = AuthService.issue_admin_token()
    return test_client


def test_sessions_endpoint_returns_one_labeler_newest_first(client):
    body = client.get("/api/labeling/sessions?user=ANA@halocollar.com").get_json()
    assert body["success"] is True
    assert [r["timestamp"] for r in body["sessions"]] == ["2026-10-28T10:00:00", "2026-10-27T10:00:00"]
    assert {r["email"] for r in body["sessions"]} == {"ana@halocollar.com"}


def test_sessions_endpoint_reads_the_range_cache(client):
    with routes._WINDOW_CACHE_LOCK:
        routes._WINDOW_CACHE.clear()
    body = client.get("/api/labeling/sessions?user=ana@halocollar.com&start=2026-10-28").get_json()
    assert body["pending"] is True and body["sessions"] == []
    with routes._WINDOW_CACHE_LOCK:
        routes._WINDOW_CACHE[f"2026-10-28..{routes._OPEN_END}"] = {
            "payload": {"session_log": [{"email": "ana@halocollar.com", "timestamp": "2026-10-28T10:00:00"}]},
            "generated_at": 0,
        }
    body = client.get("/api/labeling/sessions?user=ana@halocollar.com&start=2026-10-28").get_json()
    assert len(body["sessions"]) == 1
    with routes._WINDOW_CACHE_LOCK:
        routes._WINDOW_CACHE.clear()


def test_sessions_endpoint_asks_for_a_refresh_on_an_old_summary(client, monkeypatch):
    monkeypatch.setattr(routes, "_cache_get_memory", lambda _key: {"data": {"totals": {}}, "stale": False})
    body = client.get("/api/labeling/sessions?user=ana@halocollar.com").get_json()
    assert body["needs_refresh"] is True


def test_sessions_endpoint_validates_input(client):
    assert client.get("/api/labeling/sessions").status_code == 400
    assert client.get("/api/labeling/sessions?user=a@b.com&family=nope").status_code == 400


def test_summary_response_leaves_session_logs_out(client):
    data = client.get("/api/labeling/summary").get_json()["data"]
    assert "session_log" not in data
    assert "session_log" not in data["gps"]
    assert data["totals"]["sessions"] == 3


def test_sessions_endpoint_needs_login():
    app = Flask(__name__)
    app.secret_key = "test"
    app.register_blueprint(routes.labeling_bp)
    assert app.test_client().get("/api/labeling/sessions?user=a@b.com").status_code == 401
