# Observer.py
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    async def update(self, source, data: dict) -> None:
        pass