# Простой менеджер задач python
Используется для управления выполняемыми асинхронными задачами. Не требует установки дополнительных зависимостей.

### Решает задачи:
* получения активных задач;
* прерывания выполнения задач;
* получение описания задачи.

### Использование
* Перед началом задачи требуется описать её через `BaseTaskInfo` или его наследников.
* Начать задачу через `TaskManager().run_task(...)`
* Пример
```python
import asyncio
from task_manager import TaskManager, BaseTaskInfo

#функция, выступающая телом задачи
async def test():
    await asyncio.sleep(1)

#менеджер задач
task_manager = TaskManager()
#сведения о задаче
task1 = BaseTaskInfo(description='task1')
#запуск задачи
task_manager.run_task(task1, test())
```

### TODO
- [ ] возможность оборачивания в задачу синхронной функции посредством `asyncio.to_thread` & `ThreadPoolExecutor`