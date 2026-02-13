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
        """
        Initialize static map metadata and occupancy grid.

        This stores map dimensions and grid values so other components can
        render or reason about the environment.

        Params:
            resolution: Meters per cell in the occupancy grid.
            width: Map width in meters.
            height: Map height in meters.
            occupancyGrid: Flattened grid values (0-100 or -1) by cell.

        Return:
            None.
        """
        self._resolution = resolution
        self._width = width
        self._height = height
        self._occupancyGrid = occupancyGrid if occupancyGrid is not None else []

    # Getters
    def get_resolution(self) -> float:
        """
        Get the map resolution.

        This returns the resolution of the map in meters per cell.

        Params:
            None.

        Return:
            Resolution in meters per cell.
        """
        return self._resolution

    def get_width(self) -> float:
        """
        Get the map width.

        This returns the width in meters for layout and scaling.

        Params:
            None.

        Return:
            Map width in meters.
        """
        return self._width

    def get_height(self) -> float:
        """
        Get the map height.

        This returns the height in meters for layout and scaling.

        Params:
            None.

        Return:
            Map height in meters.
        """
        return self._height

    def get_occupancyGrid(self) -> List[int]:
        """
        Get the occupancy grid values.

        This returns the flattened list of cell values for rendering or logic.

        Params:
            None.

        Return:
            List of occupancy values.
        """
        return self._occupancyGrid

    #  Setters
    def set_resolution(self, value: float) -> None:
        """
        Set the map resolution.

        This updates meters per cell to match new map metadata.

        Params:
            value: New resolution in meters per cell.

        Return:
            None.
        """
        self._resolution = value

    def set_width(self, value: float) -> None:
        """
        Set the map width.

        This updates the width in meters for layout and scaling.

        Params:
            value: New width in meters.

        Return:
            None.
        """
        self._width = value

    def set_height(self, value: float) -> None:
        """
        Set the map height.

        This updates the height in meters for layout and scaling.

        Params:
            value: New height in meters.

        Return:
            None.
        """
        self._height = value

    def set_occupancyGrid(self, value: List[int]) -> None:
        """
        Set the occupancy grid values.

        This replaces the flattened grid with updated cell data.

        Params:
            value: List of occupancy values.

        Return:
            None.
        """
        self._occupancyGrid = value

    def toJSON(self) -> Dict[str, Any]:
        """
        Convert the map data into a JSON-ready dictionary.

        This prepares the data for sending to the frontend or external APIs.

        Params:
            None.

        Return:
            Dictionary with resolution, width, height, and occupancy grid.
        """
        return {
            "resolution": self._resolution,
            "width": self._width,
            "height": self._height,
            "occupancyGrid": self._occupancyGrid
        }
