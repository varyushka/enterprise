from dataclasses import dataclass
from enum import Enum
from uuid import UUID

class TaskStatus(Enum):
    TODO = "TODO"
    DONE = "DONE"

@dataclass
class Task:
    id: UUID
    title: str
    status: TaskStatus = TaskStatus.TODO

    def complete(self) -> None:
        if self.status == TaskStatus.DONE:
            raise ValueError('Already completed')
        self.status = TaskStatus.DONE