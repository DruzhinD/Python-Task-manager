from dataclasses import dataclass
import datetime as dt
from uuid import UUID, uuid4
from typing import Optional, Any, Literal

@dataclass
class BaseTaskInfo:
    """#### Базовый контейнер для сведений о выполняемой задачи
    """
    id: UUID = uuid4()
    """идентификатор задачи
    """
    creation_time: dt.datetime = dt.datetime.now()
    """время запуска задачи
    """
    completion_time: dt.datetime = None
    """время завершения задачи
    """
    description: str = None
    """описание задачи
    """
    status: Literal['running', 'completed', 'failed'] = 'running'
    """статус задачи
    """
    result: Any = None
    """возвращенные данные из задачи
    """
    exception: Exception = None
    """исключение, полученное в результате ошибки во время выполнения задачи
    """

    def __eq__(self, value: Optional['BaseTaskInfo']):
        if value is None:
            return False
        elif not isinstance(value, 'BaseTaskInfo'):
            return False
        elif self.id == value.id:
            return True
        return False