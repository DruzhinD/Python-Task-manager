import asyncio
import logging
import datetime as dt
from typing import List, Coroutine
from uuid import UUID
from base_task import BaseTask
from base_task_info import BaseTaskInfo
from base_task_filter import BaseTaskFilter

class TaskManager():
    """#### Менеджер задач
    Существует в единственном экземпляре
    """
    _instance: 'TaskManager' = None

    #реализация синглтона
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.tasks: List[BaseTask] = []
        """Активные задачи
        """

    def run_task(self, task_info: BaseTaskInfo, coro: Coroutine):
        """#### Начать выполнение <u>задачи</u>
        #### Args:
            task_info (BaseTaskInfo): сведения о задаче
            coro (Coroutine): запущенная функция в корутине
        #### Returns:
            BaseTask: выполняемая задача
        """        
        #запускаем обернутую в функцию задачу
        task = asyncio.create_task(
            self._wrap_task(
                task_info=task_info,
                coro=coro)
        )
        #сведения о задаче
        task_record = BaseTask(
            task_info=task_info,
            task=task
        )
        #добавляем задачу в список активных
        self.tasks.append(task_record)
        return task_record


    async def _wrap_task(self, task_info: BaseTaskInfo, coro: Coroutine):
        """#### обертка для задачи
        #### Args:
            task_info (BaseTaskInfo): сведения о задаче
            coro (Coroutine): оборачиваемая корутинв
        #### Returns:
            Any: возвращаемые данные
        """
        try:
            result = await coro
            #задача завершена
            task_info.status = 'completed'
            task_info.completion_time = dt.datetime.now()
            task_info.result = result
            return result
        except Exception as ex:
            logging.info(ex)
            task_info.status = 'failed'
        #удаляем задачу из списка
        finally:
            self._remove_task(task_id=task_info.id)


    def _remove_task(self, task_id: UUID = None):
        """#### Удалить задачу из текущего списка
        #### Raises:
            ValueError: не задан ни один аргумент для поиска задачи
        """
        tasks = self.find_tasks(BaseTaskFilter(id=task_id))
        for task in tasks:
            try:
                self.tasks.remove(task)
            except ValueError as ex:
                logging.info(f'task already done #{task_id}')


    def cancel_task(self, filter_model: BaseTaskFilter):
        """#### Завершает задачи(-у), согласно заданному фильтру
        #### Args:
            filter_model (BaseTaskFilter): фильтр для задач
        #### Returns:
            bool: True - завершены были все задачи, соответствующие фильтру. 
            False - не все задачи были завершены или не было найдено задач, соответствующих фильтру
        """
        filtered_tasks = self.find_tasks(filter_model)

        result: bool = False
        for task in filtered_tasks:
            result = task.cancel()
        return result


    def find_tasks(self, filter_model: BaseTaskFilter):
        """#### Найти задачи, соответствующие фильтру
        #### Args:
            filter_model (TaskFilterModel): фильтр для выборки
        #### Raises:
            ValueError: фильтр не был задан
        """
        filter_dict = filter_model.to_dict()
        if len(filter_dict) == 0:
            raise ValueError('Filter is unset')

        filtered_tasks = [
            task for task in self.tasks
            if all(getattr(task.task_info, key) == value for key, value in filter_dict.items())
        ]
        return filtered_tasks