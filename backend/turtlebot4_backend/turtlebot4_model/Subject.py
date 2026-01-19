# Subject.py
from abc import ABC
from typing import List
from Observer import Observer


class Subject(ABC):
    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, o: Observer) -> None:
        """
        Registers a new observer.

        @param o: The observer instance to be registered.
        """
        if o not in self._observers:
            self._observers.append(o)

    def detach(self, o: Observer) -> None:
        """
        Unregisters an existing observer.

        @param o: The observer instance to be deregistered.
        """
        if o in self._observers:
            self._observers.remove(o)

    def notifyObservers(self, data: dict) -> None:
        """
        Notifies all registered observers of a state change.
        """
        for observer in list(self._observers):
            observer.update(self, data)
