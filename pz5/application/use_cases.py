from dataclasses import dataclass
from uuid import UUID, uuid4
from application.common import Result, Error, ErrorCode
from application.ports import TaskRepository, NotificationPort
from domain.entities import Task


@dataclass(frozen=True)
class CreateTaskRequest:
    title: str


@dataclass(frozen=True)
class CompleteTaskRequest:
    task_id: str


@dataclass(frozen=True)
class TaskResponse:
    id: str
    title: str
    status: str

    @classmethod
    def from_entity(cls, task: Task):
        return cls(id=str(task.id), title=task.title, status=task.status.value)


class CreateTaskUseCase:
    def __init__(self, tasks: TaskRepository):
        self.tasks = tasks

    def execute(self, request: CreateTaskRequest) -> Result:
        if not request.title.strip():
            return Result.failure(Error(ErrorCode.VALIDATION_ERROR, "Task title empty"))
        task = Task(id=uuid4(), title=request.title)
        self.tasks.save(task)
        return Result.success(TaskResponse.from_entity(task))


class CompleteTaskUseCase:
    def __init__(self, tasks: TaskRepository, notifier: NotificationPort):
        self.tasks = tasks
        self.notifier = notifier

    def execute(self, request: CompleteTaskRequest) -> Result:
        try:
            task_id = UUID(request.task_id)
            task = self.tasks.get(task_id)
            if not task:
                return Result.failure(Error(ErrorCode.NOT_FOUND, "Task not found"))

            task.complete()
            self.tasks.save(task)
            self.notifier.notify_task_completed(task)
            return Result.success(TaskResponse.from_entity(task))
        except ValueError as exc:
            return Result.failure(Error(ErrorCode.VALIDATION_ERROR, str(exc)))