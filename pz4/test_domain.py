import pytest
from datetime import datetime, timezone, timedelta
from todo_app.domain.models import Task, Project
from todo_app.domain.value_objects import Deadline, TaskStatus, Priority
from todo_app.domain.services import TaskPriorityCalculator


def test_task_start_rule():
    task = Task(title="Test", description="Test task")
    task.start()
    assert task.status == TaskStatus.IN_PROGRESS


def test_task_cannot_start_if_not_todo():
    task = Task(title="Test", description="Test task")
    task.start()
    with pytest.raises(ValueError, match="Only TODO tasks can be started"):
        task.start()


def test_task_complete_rule():
    task = Task(title="Test", description="Test task")
    task.start()
    task.complete()
    assert task.status == TaskStatus.DONE


def test_task_cannot_complete_twice():
    task = Task(title="Test", description="Test task")
    task.complete()
    with pytest.raises(ValueError, match="Task is already completed"):
        task.complete()


def test_deadline_cannot_be_in_past():
    past_date = datetime.now(timezone.utc) - timedelta(days=1)
    with pytest.raises(ValueError, match="Deadline cannot be in the past"):
        Deadline(due_date=past_date)


def test_project_add_and_remove_task():
    project = Project(name="Test Project")
    task = Task(title="Task 1", description="Desc")

    project.add_task(task)
    assert len(project.tasks) == 1

    project.remove_task(task.id)
    assert len(project.tasks) == 0


def test_task_priority_calculator():
    future_date = datetime.now(timezone.utc) + timedelta(days=1)
    task = Task(title="Test", description="Desc", due_date=Deadline(due_date=future_date))

    priority = TaskPriorityCalculator.calculate_priority(task)
    assert priority == Priority.MEDIUM