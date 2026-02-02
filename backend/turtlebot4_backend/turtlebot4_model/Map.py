import os
import base64
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Optional, Dict, Any
from Subject import Subject
from geometry_msgs.msg import PoseStamped
from .MapData import MapData

class Map(Subject):
    """
    Represents the robot's map, including dynamic data (robot pose, goals)
    and static map data (occupancy grid converted to PNG for frontend visualization).
    """

    # Absolute path for saving the map PNG
    SAVE_DIR = os.path.expanduser("~/turtlebot4_ws/src/RobotDashboardSystem")

    def __init__(
        self,
        mapData: Optional[MapData] = None,
        robotPose: Optional[PoseStamped] = None,
        globalGoal: Optional[PoseStamped] = None,
        intermediateWaypoints: Optional[List[PoseStamped]] = None
    ) -> None:
        super().__init__()
        self._mapData = mapData if mapData is not None else MapData()
        self._mapDataPNG: Optional[str] = None
        self._robotPose = robotPose
        self._globalGoal = globalGoal
        self._intermediateWaypoints = intermediateWaypoints if intermediateWaypoints is not None else []

        # Convert initial mapData to PNG if provided
        if mapData:
            self._convert_mapdata_to_png()

    # ===== Getters =====
    def get_mapData(self) -> MapData:
        return self._mapData

    def get_robotPose(self) -> Optional[PoseStamped]:
        return self._robotPose

    def get_globalGoal(self) -> Optional[PoseStamped]:
        return self._globalGoal

    def get_intermediateWaypoints(self) -> List[PoseStamped]:
        return self._intermediateWaypoints

    # ===== Setters =====
    def set_mapData(self, value: MapData) -> None:
        self._mapData = value
        self._convert_mapdata_to_png()  # Convert to PNG immediately
        self.notify()

    def set_robotPose(self, value: PoseStamped) -> None:
        self._robotPose = value
        self.notify()

    def set_globalGoal(self, value: PoseStamped) -> None:
        self._globalGoal = value
        self.notify()

    def set_intermediateWaypoints(self, value: List[PoseStamped]) -> None:
        self._intermediateWaypoints = value
        self.notify()

    # ===== Internal helper for PNG conversion =====
    def _convert_mapdata_to_png(self) -> None:
        """
        Converts the MapData occupancy grid into a heatmap PNG using matplotlib,
        saves it to disk, and stores the base64-encoded PNG for JSON output.
        """
        mapData = self._mapData
        width = int(mapData.get_width() / mapData.get_resolution())
        height = int(mapData.get_height() / mapData.get_resolution())

        grid = np.array(mapData.get_occupancyGrid(), dtype=np.int8)
        if len(grid) != width * height:
            # fallback for mismatched size
            print("Warning: occupancy grid size mismatch.")
            grid = np.resize(grid, (height * width))

        grid = grid.reshape((height, width))

        # Visualization logic
        visual_grid = grid.copy()
        visual_grid[visual_grid == -1] = 50  # unknown -> middle gray

        png_path = os.path.join(self.SAVE_DIR, 'warehouse_map.png')
        plt.figure(figsize=(8, 8))
        plt.imshow(visual_grid, cmap='gray_r', origin='lower')
        plt.colorbar(label='Occupancy Value')
        plt.title('Warehouse Occupancy Grid Heatmap')
        plt.savefig(png_path)
        plt.close()
        print(f'Occupancy grid heatmap saved as {png_path}')

        # Encode PNG to base64
        with open(png_path, "rb") as f:
            self._mapDataPNG = base64.b64encode(f.read()).decode("utf-8")

    # ===== JSON Serialization =====
    def toJSON(self) -> Dict[str, Any]:
        """
        Returns JSON-ready dict including static map as PNG base64 and dynamic data.
        """
        def pose_to_dict(pose: Optional[PoseStamped]):
            if pose is None:
                return None
            return {
                "position": {
                    "x": pose.pose.position.x,
                    "y": pose.pose.position.y,
                    "z": pose.pose.position.z
                },
                "orientation": {
                    "x": pose.pose.orientation.x,
                    "y": pose.pose.orientation.y,
                    "z": pose.pose.orientation.z,
                    "w": pose.pose.orientation.w
                }
            }

        return {
            "mapData": {
                "resolution": self._mapData.get_resolution(),
                "width": self._mapData.get_width(),
                "height": self._mapData.get_height(),
                "occupancyGridPNG": self._mapDataPNG  # base64 encoded PNG
            },
            "robotPose": pose_to_dict(self._robotPose),
            "globalGoal": pose_to_dict(self._globalGoal),
            "intermediateWaypoints": [pose_to_dict(p) for p in self._intermediateWaypoints]
        }
