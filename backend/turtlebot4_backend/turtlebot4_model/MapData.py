from typing import List, Dict, Any

class MapData:
    """
    Represents the static base layer of the map.
    Contains map resolution, dimensions, and occupancy grid.
    """

    def __init__(
        self,
        resolution: float = 0.0,
        width: float = 0.0,
        height: float = 0.0,
        occupancyGrid: List[int] = None
    ) -> None:
        self._resolution = resolution
        self._width = width
        self._height = height
        self._occupancyGrid = occupancyGrid if occupancyGrid is not None else []

    # Getters
    def get_resolution(self) -> float:
        return self._resolution

    def get_width(self) -> float:
        return self._width

    def get_height(self) -> float:
        return self._height

    def get_occupancyGrid(self) -> List[int]:
        return self._occupancyGrid

    #  Setters
    def set_resolution(self, value: float) -> None:
        self._resolution = value

    def set_width(self, value: float) -> None:
        self._width = value

    def set_height(self, value: float) -> None:
        self._height = value

    def set_occupancyGrid(self, value: List[int]) -> None:
        self._occupancyGrid = value

    def toJSON(self) -> Dict[str, Any]:
        """
        Convert the static map data into a JSON-ready dictionary for frontend.
        """
        return {
            "resolution": self._resolution,
            "width": self._width,
            "height": self._height,
            "occupancyGrid": self._occupancyGrid
        }
