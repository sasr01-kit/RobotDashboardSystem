from abc import ABC, abstractmethod


class Observer(ABC):
    """
    Interface for objects that receive updates from a subject.

    This standardizes how models broadcast changes so different listeners can
    react without knowing the subject's internal details.
    """

    @abstractmethod
    async def update(self, source, data: dict) -> None:
        """
        Handle an update emitted by a subject.

        This is called whenever the subject wants to broadcast new data to its
        observers.

        Params:
            source: The subject that generated the update.
            data: JSON-serializable payload describing the update.

        Return:
            None.
        """
        pass