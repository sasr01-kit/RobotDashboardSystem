import os
import base64
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any
from turtlebot4_backend.turtlebot4_model.Subject import Subject
from turtlebot4_backend.turtlebot4_model.MapData import MapData
from geometry_msgs.msg import PoseStamped

class Map(Subject):
    """Manage map data, pose updates, and observer notifications."""

    # Save directory for generated map PNGs.
    SAVE_DIR = os.path.expanduser("~/ros2_ws/src/RobotDashboardSystem")

    def __init__(self, mapData=None, robotPose=None, globalGoal=None, intermediateWaypoints=None):
        """Initialize the map model and optional state.

        Params:
            self: Map instance.
            mapData: Initial map data model.
            robotPose: Initial robot pose.
            globalGoal: Initial global goal pose.
            intermediateWaypoints: Initial list of waypoint poses.

        Returns:
            None.
        """
        super().__init__()
        self._mapData = mapData if mapData else MapData()
        self._mapDataPNG = None
        self._robotPose = robotPose
        self._globalGoal = globalGoal
        self._intermediateWaypoints = intermediateWaypoints or []

        if mapData:
            self._convert_mapdata_to_png()

    def _convert_mapdata_to_png(self) -> None:
        """Convert map data into a PNG and store it as base64.
        Base64 is a text-safe encoding for binary data, so the PNG can be
        included in JSON payloads without raw bytes.

        Params:
            self: Map instance.

        Returns:
            None.
        """
        mapData = self._mapData
        width = int(mapData.get_width() / mapData.get_resolution())
        height = int(mapData.get_height() / mapData.get_resolution())

        grid = np.array(mapData.get_occupancyGrid(), dtype=np.int8)
        if len(grid) != width * height:
            print("Warning: occupancy grid size mismatch.")
            grid = np.resize(grid, (height * width))

        grid = grid.reshape((height, width))

        visual_grid = grid.copy()
        visual_grid[visual_grid == -1] = 50

        png_path = os.path.join(self.SAVE_DIR, 'warehouse_map.png')
        plt.figure(figsize=(8, 8))
        plt.imshow(visual_grid, cmap='gray_r', origin='lower')
        plt.colorbar(label='Occupancy Value')
        plt.title('Warehouse Occupancy Grid Heatmap')
        plt.savefig(png_path)
        plt.close()

        with open(png_path, "rb") as f:
            self._mapDataPNG = base64.b64encode(f.read()).decode("utf-8")

    async def set_mapData(self, value: MapData) -> None:
        """Update map data, regenerate PNG, and notify observers.

        Params:
            self: Map instance.
            value: New map data.

        Returns:
            None.
        """
        self._mapData = value
        self._convert_mapdata_to_png()

        await self.notify_observers({
            "type": "MAP_DATA",
            "mapData": {
                "resolution": self._mapData.get_resolution(),
                "width": self._mapData.get_width(),
                "height": self._mapData.get_height(),
                "occupancyGridPNG": self._mapDataPNG
            }
        })

    # DYNAMIC POSE UPDATE
    async def set_robotPose(self, value: PoseStamped) -> None:
        """Update the robot pose and notify observers.

        Params:
            self: Map instance.
            value: New robot pose.

        Returns:
            None.
        """
        self._robotPose = value
        await self._send_pose_update()

    async def set_globalGoal(self, value: PoseStamped) -> None:
        """Update the global goal and notify observers.

        Params:
            self: Map instance.
            value: New global goal pose.

        Returns:
            None.
        """
        self._globalGoal = value
        await self._send_pose_update()

    async def set_intermediateWaypoints(self, value) -> None:
        """Update intermediate waypoints and notify observers.

        Params:
            self: Map instance.
            value: New list of waypoint poses.

        Returns:
            None.
        """
        self._intermediateWaypoints = value
        await self._send_pose_update()

    async def set_detectedHumans(self, humans) -> None:
        """Update detected humans and notify observers.

        Params:
            self: Map instance.
            humans: Collection of detected human objects.

        Returns:
            None.
        """
        self._detectedHumans = humans
        await self._send_pose_update()

    # Helper to send POSE_DATA
    async def _send_pose_update(self):
        """Send the latest pose-related data to observers.

        Params:
            self: Map instance.

        Returns:
            None.
        """
        await self.notify_observers({
            "type": "POSE_DATA",
            "robotPose": self._pose_to_dict(self._robotPose),
            "globalGoal": self._pose_to_dict(self._globalGoal),
            "intermediateWaypoints": [self._pose_to_dict(p) for p in self._intermediateWaypoints],
            "humans": [h.toJSON() for h in getattr(self, "_detectedHumans", [])]
        })

    def _pose_to_dict(self, pose):
        """Convert a pose to a JSON-compatible dict.

        Params:
            self: Map instance.
            pose: Pose mapping or PoseStamped instance.

        Returns:
            Dict[str, Any] | None: Converted pose data, or None if not set.
        """
        if pose is None:
            return None

        # Pose can be a dict (simulator) or a PoseStamped (real robot)
        if isinstance(pose, dict):
            return {
                "position": {
                    "x": pose.get("position", {}).get("x", 0.0),
                    "y": pose.get("position", {}).get("y", 0.0),
                    "z": pose.get("position", {}).get("z", 0.0),
                },
                "orientation": {
                    "x": pose.get("orientation", {}).get("x", 0.0),
                    "y": pose.get("orientation", {}).get("y", 0.0),
                    "z": pose.get("orientation", {}).get("z", 0.0),
                    "w": pose.get("orientation", {}).get("w", 1.0),
                }
            }

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

