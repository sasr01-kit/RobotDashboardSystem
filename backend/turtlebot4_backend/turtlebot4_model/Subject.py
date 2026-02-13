from abc import ABC
from typing import List
from turtlebot4_backend.turtlebot4_model.Observer import Observer


class Subject(ABC):
    """
    Base class for models that broadcast updates to observers.

    This implements the Subject role in the observer pattern so models can
    notify UI listeners or other components when their state changes.
    """

    def __init__(self) -> None:
        """
        Initialize an empty observer list.

        This prepares the subject to register observers before any updates
        occur.

        Params:
            None.

        Return:
            None.
        """
        self._observers: List[Observer] = []  # Observers to notify on updates.

    def attach(self, o: Observer) -> None:
        """
        Register an observer to receive updates.

        This adds a listener so it will be notified on future state changes.

        Params:
            o: Observer instance to attach.

        Return:
            None.
        """
        if o not in self._observers:
            self._observers.append(o)

    def detach(self, o: Observer) -> None:
        """
        Remove an observer from receiving updates.

        This stops the listener from receiving further notifications.

        Params:
            o: Observer instance to detach.

        Return:
            None.
        """
        if o in self._observers:
            self._observers.remove(o)

    async def notify_observers(self, data: dict) -> None:
        """
        Notify all registered observers of a state change.

        This delivers the update payload to each observer in order.

        Params:
            data: JSON-serializable update payload.

        Return:
            None.
        """
        for observer in list(self._observers):
            await observer.update(self, data)
