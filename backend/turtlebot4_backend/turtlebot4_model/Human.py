from typing import Dict, Any

class Human:
    """Represent a detected human and related proxemic distances."""

    def __init__(
        self,
        human_id: str = "",
        position=None,
        proxemic_distances: Dict[str, Any] | None = None,
    ) -> None:
        """Initialize a human instance.

        Params:
            self: Human instance.
            human_id: Unique identifier for the detected human.
            position: Mapping with x, y, z coordinates.
            proxemic_distances: Optional proxemic distance data.

        Returns:
            None.
        """
        self._id = human_id
        self._position = position or {"x": 0.0, "y": 0.0, "z": 0.0}

        # If no proxemic distances provided, use standard zones defined by Edward T. Hall
        self._proxemic_distances = proxemic_distances or {
            "intimate": 0.45,  
            "personal": 1.2,
            "social": 3.6,
            "public": 7.6
        }

    # Getters
    def get_id(self) -> str:
        """Return the human identifier.

        Params:
            self: Human instance.

        Returns:
            str: Human identifier.
        """
        return self._id

    def get_position(self):
        """Return the current position mapping.

        Params:
            self: Human instance.

        Returns:
            Dict[str, Any]: Position with x, y, z coordinates.
        """
        return self._position

    def get_proxemic_distances(self) -> Dict[str, Any]:
        """Return the proxemic distance configuration.

        Params:
            self: Human instance.

        Returns:
            Dict[str, Any]: Proxemic distance values by zone.
        """
        return self._proxemic_distances

    # Setters
    def set_id(self, value: str) -> None:
        """Set the human identifier.

        Params:
            self: Human instance.
            value: Human identifier.

        Returns:
            None.
        """
        self._id = value

    def set_position(self, value) -> None:
        """Set the position mapping.

        Params:
            self: Human instance.
            value: Position with x, y, z coordinates.

        Returns:
            None.
        """
        self._position = value

    def set_proxemic_distances(self, value: Dict[str, Any]) -> None:
        """Set the proxemic distance configuration.

        Params:
            self: Human instance.
            value: Proxemic distance values by zone.

        Returns:
            None.
        """
        self._proxemic_distances = value

    # JSON serialization for frontend
    def toJSON(self) -> Dict[str, Any]:
        """Serialize the human instance for frontend consumption.

        Params:
            self: Human instance.

        Returns:
            Dict[str, Any]: JSON-compatible human payload.
        """
        return {
            "id": self._id,
            "position": {
                "x": self._position.get("x", 0.0),
                "y": self._position.get("y", 0.0),
                "z": self._position.get("z", 0.0),
            },
            "proxemicDistances": self._proxemic_distances
        }
