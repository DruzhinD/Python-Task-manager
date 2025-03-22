from typing import Optional
from uuid import UUID
from dataclasses import dataclass

@dataclass
class BaseTaskFilter():
    """#### Модель фильтра для поиска задач(-и)
    """
    id: Optional[UUID] = None
    
    def to_dict(self):
        items = dict()
        for item in self.__dict__.items():
            if item[1] is not None:
                items.update(item)
        return items