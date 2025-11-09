from fastapi.testclient import TestClient
from src import app as app_module
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure clean start: remove if already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup should succeed
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail with 400
    r2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert r2.status_code == 400

    # Remove the participant
    r3 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert r3.status_code == 200
    assert email not in activities[activity]["participants"]

    # Removing again should return 404
    r4 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert r4.status_code == 404


def test_nonexistent_activity_errors():
    r = client.post("/activities/NoSuchActivity/signup?email=foo@example.com")
    assert r.status_code == 404

    r2 = client.delete("/activities/NoSuchActivity/participants?email=foo@example.com")
    assert r2.status_code == 404
