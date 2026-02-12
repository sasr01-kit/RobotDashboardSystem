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
        @param position: Dict with x, y, z coordinates.
        @param proxemic_distances: Optional proxemic distance data.
        """
        self._id = human_id
        self._position = position or {"x": 0.0, "y": 0.0, "z": 0.0}

        # If no proxemic distances provided, use standard zones defined by Hall (1966)
        self._proxemic_distances = proxemic_distances or {
            "intimate": 0.45,  
            "personal": 1.2,
            "social": 3.6,
            "public": 7.6
        }

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

    # JSON serialization for frontend
    def toJSON(self) -> Dict[str, Any]:
        return {
            "id": self._id,
            "position": {
                "x": self._position.get("x", 0.0),
                "y": self._position.get("y", 0.0),
                "z": self._position.get("z", 0.0),
            },
            "proxemicDistances": self._proxemic_distances
        }
