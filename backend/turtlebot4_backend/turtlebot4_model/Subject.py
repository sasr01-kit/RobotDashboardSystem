from abc import ABC
from typing import List
from turtlebot4_backend.turtlebot4_model.Observer import Observer

# Subject defines the interface for subjects that maintain a list of observers and notify them of state changes.
class Subject(ABC):

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, o: Observer) -> None:
        if o not in self._observers:
            self._observers.append(o)

    def detach(self, o: Observer) -> None:
        if o in self._observers:
            self._observers.remove(o)

    async def notify_observers(self, data: dict) -> None:
        """
        Notifies all registered observers of a state change.
        """
        for observer in list(self._observers):
            await observer.update(self, data)
