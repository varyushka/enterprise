from abc import ABC, abstractmethod
from .models import Task

class TaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task):
        pass

    @abstractmethod
    def get(self, task_id: str) -> Task:
        pass