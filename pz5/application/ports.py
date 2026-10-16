from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from domain.entities import Task

class TaskRepository(ABC):
    @abstractmethod
    def get(self, task_id: UUID) -> Optional[Task]:
        pass

    @abstractmethod
    def save(self, task: Task) -> None:
        pass

class NotificationPort(ABC):
    @abstractmethod
    def notify_task_completed(self, task: Task) -> None:
        pass