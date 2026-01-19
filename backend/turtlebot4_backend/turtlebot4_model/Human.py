# Human.py
from typing import Dict, Any


class Human:
    def __init__(
        self,
        human_id: str = "",
        position=None,
        proxemic_distances: Dict[str, Any] | None = None,
    ) -> None:
        """
        @param human_id: Unique identifier for the detected human.
        @param position: Pose representing the human's spatial position.
        @param proxemic_distances: Dictionary containing proxemic distance data.
        """
        self._id = human_id
        self._position = position
        self._proxemic_distances = proxemic_distances if proxemic_distances is not None else {}

    # Getters
    def get_id(self) -> str:
        return self._id

    def get_position(self):
        return self._position

    def get_proxemic_distances(self) -> Dict[str, Any]:
        return self._proxemic_distances

    # Setters
    def set_id(self, value: str) -> None:
        self._id = value

    def set_position(self, value) -> None:
        self._position = value

    def set_proxemic_distances(self, value: Dict[str, Any]) -> None:
        self._proxemic_distances = value
