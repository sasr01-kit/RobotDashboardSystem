from abc import ABC, abstractmethod

# Observer defines the interface for observers that want to receive updates from subjects (like Teleoperate).
class Observer(ABC):
    @abstractmethod
    async def update(self, source, data: dict) -> None:
        pass