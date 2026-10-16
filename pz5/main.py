from infrastructure.adapters import InMemoryTaskRepository, ConsoleNotificationAdapter
from application.use_cases import (
    CreateTaskUseCase, CreateTaskRequest,
    CompleteTaskUseCase, CompleteTaskRequest
)


def main():
    repo = InMemoryTaskRepository()
    notifier = ConsoleNotificationAdapter()

    create_uc = CreateTaskUseCase(repo)
    result = create_uc.execute(CreateTaskRequest(title="Зробити ПЗ на 5 файлів"))

    if result.is_success:
        task_data = result.value
        print(f"Створено: {task_data.title}")

        complete_uc = CompleteTaskUseCase(repo, notifier)
        complete_uc.execute(CompleteTaskRequest(task_id=task_data.id))


if __name__ == "__main__":
    main()