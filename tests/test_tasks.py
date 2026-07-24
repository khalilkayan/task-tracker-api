from datetime import date, timedelta

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


def test_create_task_with_valid_due_date_returns_201_and_exposes_due_date(client: TestClient):
    future_date = date.today() + timedelta(days=7)

    r = client.post(
        "/tasks",
        json={"title": "Due soon", "due_date": future_date.isoformat()},
    )

    assert r.status_code == 201
    assert r.json()["due_date"] == future_date.isoformat()


def test_create_task_without_due_date_returns_none(client: TestClient):
    r = client.post("/tasks", json={"title": "No due date"})

    assert r.status_code == 201
    body = r.json()
    assert "due_date" in body
    assert body["due_date"] is None


def test_patch_task_due_date_can_add_change_and_remove(client: TestClient):
    created_task = client.post("/tasks", json={"title": "Due date task"})
    assert created_task.status_code == 201

    task_id = created_task.json()["id"]
    first_due_date = date.today() + timedelta(days=7)
    second_due_date = date.today() + timedelta(days=14)

    first_patch = client.patch(
        f"/tasks/{task_id}",
        json={"due_date": first_due_date.isoformat()},
    )
    assert first_patch.status_code == 200
    first_body = first_patch.json()
    assert first_body["due_date"] == first_due_date.isoformat()
    assert first_body["title"] == "Due date task"

    second_patch = client.patch(
        f"/tasks/{task_id}",
        json={"due_date": second_due_date.isoformat()},
    )
    assert second_patch.status_code == 200
    second_body = second_patch.json()
    assert second_body["due_date"] == second_due_date.isoformat()
    assert second_body["title"] == "Due date task"

    remove_patch = client.patch(f"/tasks/{task_id}", json={"due_date": None})
    assert remove_patch.status_code == 200
    removed_body = remove_patch.json()
    assert removed_body["due_date"] is None
    assert removed_body["title"] == "Due date task"


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

def test_list_tasks_search_matches_title_case_insensitively(client: TestClient):
    matching_task = client.post("/tasks", json={"title": "Quantum project"})
    non_matching_task = client.post("/tasks", json={"title": "Routine cleanup"})
    assert matching_task.status_code == 201
    assert non_matching_task.status_code == 201

    r = client.get("/tasks?q=qUa")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["id"] == matching_task.json()["id"]


def test_list_tasks_search_matches_description_case_insensitively(client: TestClient):
    matching_task = client.post(
        "/tasks",
        json={"title": "Task with details", "description": "A quick quiz note"},
    )
    non_matching_task = client.post(
        "/tasks",
        json={"title": "Other task", "description": "No match here"},
    )
    assert matching_task.status_code == 201
    assert non_matching_task.status_code == 201

    r = client.get("/tasks?q=qUi")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["id"] == matching_task.json()["id"]


def test_list_tasks_whitespace_search_behaves_like_no_filter(client: TestClient):
    first_task = client.post("/tasks", json={"title": "First task"})
    second_task = client.post("/tasks", json={"title": "Second task"})
    assert first_task.status_code == 201
    assert second_task.status_code == 201

    r = client.get("/tasks", params={"q": "   "})
    assert r.status_code == 200
    assert {task["id"] for task in r.json()} == {
        first_task.json()["id"],
        second_task.json()["id"],
    }


def test_list_tasks_search_no_match_returns_200_and_empty_list(client: TestClient):
    created_task = client.post("/tasks", json={"title": "Existing task"})
    assert created_task.status_code == 201

    r = client.get("/tasks", params={"q": "mismatch"})
    assert r.status_code == 200
    assert r.json() == []


def test_list_tasks_search_combines_with_status_and_priority(client: TestClient):
    matching_to_do_task = client.post(
        "/tasks",
        json={"title": "Alpha report", "priority": "High"},
    )
    matching_in_progress_task = client.post(
        "/tasks",
        json={"title": "Alpha report", "priority": "High"},
    )
    non_matching_in_progress_task = client.post(
        "/tasks",
        json={"title": "Beta report", "priority": "High"},
    )
    matching_low_priority_task = client.post(
        "/tasks",
        json={"title": "Alpha report", "priority": "Low"},
    )
    assert matching_to_do_task.status_code == 201
    assert matching_in_progress_task.status_code == 201
    assert non_matching_in_progress_task.status_code == 201
    assert matching_low_priority_task.status_code == 201

    patched_matching_task = client.patch(
        f"/tasks/{matching_in_progress_task.json()['id']}",
        json={"status": "InProgress"},
    )
    patched_non_matching_task = client.patch(
        f"/tasks/{non_matching_in_progress_task.json()['id']}",
        json={"status": "InProgress"},
    )
    assert patched_matching_task.status_code == 200
    assert patched_non_matching_task.status_code == 200

    r = client.get(
        "/tasks",
        params={"q": "alpha", "status": "InProgress", "priority": "High"},
    )
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["id"] == matching_in_progress_task.json()["id"]


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
