from typing import Dict, Optional
from uuid import UUID
from application.ports import TaskRepository, NotificationPort
from domain.entities import Task

class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self._storage: Dict[UUID, Task] = {}

    def get(self, task_id: UUID) -> Optional[Task]:
        return self._storage.get(task_id)

    def save(self, task: Task) -> None:
        self._storage[task.id] = task

class ConsoleNotificationAdapter(NotificationPort):
    def notify_task_completed(self, task: Task) -> None:
        print(f"[NOTIFY] Завершено: {task.title} ({task.id})")