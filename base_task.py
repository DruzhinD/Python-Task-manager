from dataclasses import dataclass
from asyncio import Task
from typing import Optional
from base_task_info import BaseTaskInfo

@dataclass
class BaseTask:
    """#### Базовый объект задачи
    """
    task_info: BaseTaskInfo
    """сведения о задаче
    """
    task: Task
    """выполняемая задача
    """
    
    def __eq__(self, value: Optional['BaseTask']):
        if value is None:
            return False
        elif not isinstance(value, BaseTask):
            return False
        elif self.task_info.id == value.task_info.id:
            return True
        return False

    async def wait_for(self):
        """#### Ожидать завершения задачи
        """
        result = await self.task
        return result

    def cancel(self):
        """#### отменить задачу
        """
        result = self.task.cancel()
        return result