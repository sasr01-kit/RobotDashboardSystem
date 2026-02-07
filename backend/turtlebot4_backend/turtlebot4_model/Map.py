import os
import base64
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Optional, Dict, Any
from turtlebot4_backend.turtlebot4_model.Subject import Subject
from turtlebot4_backend.turtlebot4_model.MapData import MapData
from geometry_msgs.msg import PoseStamped

class Map(Subject):
    SAVE_DIR = os.path.expanduser("~/ros2_ws/src/RobotDashboardSystem")

    def __init__(self, mapData=None, robotPose=None, globalGoal=None, intermediateWaypoints=None):
        super().__init__()
        self._mapData = mapData if mapData else MapData()
        self._mapDataPNG = None
        self._robotPose = robotPose
        self._globalGoal = globalGoal
        self._intermediateWaypoints = intermediateWaypoints or []

        if mapData:
            self._convert_mapdata_to_png()

    # PNG conversion 
    def _convert_mapdata_to_png(self) -> None:
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

    # STATIC MAP UPDATE
    async def set_mapData(self, value: MapData) -> None:
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
        self._robotPose = value
        await self._send_pose_update()

    async def set_globalGoal(self, value: PoseStamped) -> None:
        self._globalGoal = value
        await self._send_pose_update()

    async def set_intermediateWaypoints(self, value) -> None:
        self._intermediateWaypoints = value
        await self._send_pose_update()

    async def set_detectedHumans(self, humans) -> None:
        self._detectedHumans = humans
        await self._send_pose_update()

    # Helper to send POSE_DATA
    async def _send_pose_update(self):
        await self.notify_observers({
            "type": "POSE_DATA",
            "robotPose": self._pose_to_dict(self._robotPose),
            "globalGoal": self._pose_to_dict(self._globalGoal),
            "intermediateWaypoints": [self._pose_to_dict(p) for p in self._intermediateWaypoints],
            "humans": [h.toJSON() for h in getattr(self, "_detectedHumans", [])]
        })

    def _pose_to_dict(self, pose):
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
