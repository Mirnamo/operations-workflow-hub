from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_filter_work_items():
    response = client.get("/api/work-items", params={"status": "blocked"})
    assert response.status_code == 200
    assert all(item["status"] == "blocked" for item in response.json())


def test_create_and_audit():
    response = client.post("/api/work-items", headers={"X-User": "test-user"}, json={"title": "Prepare weekly report", "owner": "Analyst", "priority": "high"})
    assert response.status_code == 201
    item_id = response.json()["id"]
    events = client.get("/api/audit-events").json()
    assert any(event["item_id"] == item_id and event["actor"] == "test-user" for event in events)
