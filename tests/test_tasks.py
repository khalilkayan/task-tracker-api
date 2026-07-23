from fastapi.testclient import TestClient

def test_create_task_valid_returns_201_with_full_body(client: TestClient):
    r = client.post("/tasks", json={"title": "Buy milk"})
    assert r.status_code == 201
    body = r.json()
    assert body["title"] == "Buy milk"
    assert body["status"] == "ToDo"
    assert body["priority"] == "Medium"
    assert body["description"] == ""
    assert body["assignee"] is None
    assert "id" in body and len(body["id"]) > 0
    assert "created_at" in body
    assert "updated_at" in body

def test_create_task_missing_title_returns_422(client: TestClient):
    r = client.post("/tasks", json={})
    assert r.status_code == 422

def test_create_task_blank_title_returns_422(client: TestClient):
    r = client.post("/tasks", json={"title": "   "})
    assert r.status_code == 422

def test_create_task_title_over_200_chars_returns_422(client: TestClient):
    r = client.post("/tasks", json={"title": "x" * 201})
    assert r.status_code == 422

def test_create_task_extra_field_returns_422(client: TestClient):
    r = client.post("/tasks", json={"title": "Test", "unknown": "bad"})
    assert r.status_code == 422

def test_create_task_invalid_status_returns_422(client: TestClient):
    r = client.post("/tasks", json={"title": "Test", "status": "Bogus"})
    assert r.status_code == 422

def test_list_tasks_empty_returns_200_and_empty_list(client: TestClient):
    r = client.get("/tasks")
    assert r.status_code == 200
    assert r.json() == []

def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client: TestClient, created_task):
    r = client.get("/tasks?status=Done")
    assert r.status_code == 200
    assert r.json() == []

def test_list_tasks_filter_by_priority_returns_only_matches(client: TestClient, created_task):
    r = client.get("/tasks?priority=Medium")
    assert r.status_code == 200
    ids = [task["id"] for task in r.json()]
    assert created_task["id"] in ids

def test_get_task_by_id_returns_task(client: TestClient, created_task):
    r = client.get(f"/tasks/{created_task['id']}")
    assert r.status_code == 200
    assert r.json()["id"] == created_task["id"]

def test_get_task_by_id_not_found_returns_404(client: TestClient):
    r = client.get("/tasks/no-such-id")
    assert r.status_code == 404

def test_patch_title_only_returns_200_and_updates_title(client: TestClient, created_task):
    r = client.patch(
        f"/tasks/{created_task['id']}",
        json={"title": "Updated title"},
    )
    assert r.status_code == 200
    assert r.json()["title"] == "Updated title"
    assert r.json()["status"] == "ToDo"

def test_patch_valid_transition_todo_to_inprogress_returns_200(client: TestClient, created_task):
    r = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "InProgress"

def test_patch_invalid_transition_todo_to_done_returns_422(client: TestClient, created_task):
    r = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "Done"},
    )
    assert r.status_code == 422
    assert "Invalid status transition" in r.json()["detail"]

def test_delete_existing_returns_204_no_body(client: TestClient, created_task):
    r = client.delete(f"/tasks/{created_task['id']}")
    assert r.status_code == 204
    assert r.content == b""

def test_delete_missing_returns_404(client: TestClient):
    r = client.delete("/tasks/no-such-id")
    assert r.status_code == 404
