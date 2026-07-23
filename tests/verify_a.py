from pydantic import ValidationError

from app.models import TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from app.storage import add_task, get_all_tasks, get_task_by_id, update_task, delete_task, _reset


def expect_pass(label, condition):
    if condition:
        print(f"PASS: {label}")
    else:
        raise AssertionError(f"FAIL: {label}")


def expect_fail(label, action):
    try:
        action()
    except Exception:
        print(f"PASS: {label}")
        return
    raise AssertionError(f"FAIL: {label}")


_reset()

expect_fail("whitespace title rejected", lambda: TaskCreate(title="   "))
expect_fail("empty title rejected", lambda: TaskCreate(title=""))
expect_fail("title over 200 chars rejected", lambda: TaskCreate(title="x" * 201))

task = TaskCreate(title="Test task")
expect_pass(
    "defaults applied",
    task.status == TaskStatus.TODO
    and task.priority == TaskPriority.MEDIUM
    and task.description == ""
)

expect_fail("extra field rejected on TaskCreate", lambda: TaskCreate(title="Test", fake_field="bad"))
expect_fail("id rejected on TaskCreate", lambda: TaskCreate(title="Test", id="bad"))
expect_fail("created_at rejected on TaskUpdate", lambda: TaskUpdate(created_at="bad"))
expect_fail("invalid status rejected", lambda: TaskCreate(title="Test", status="Invalid"))

print("--- Part A verifications complete ---")