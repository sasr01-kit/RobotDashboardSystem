import asyncio
from typing import Any, Dict, List
from turtlebot4_backend.turtlebot4_controller.RosbridgeConnection import RosbridgeConnection
from turtlebot4_backend.turtlebot4_model.Map import Map
from turtlebot4_backend.turtlebot4_model.MapData import MapData
from turtlebot4_backend.turtlebot4_model.Human import Human


class MapController:
    """
    Subscribes to /map, /humans, and /odom via RosbridgeConnection.
    Sends MAP_DATA once and POSE_DATA continuously.
    """

    def __init__(
        self,
        map_model: Map,
        rosbridge_host: str = "localhost",
        rosbridge_port: int = 9090
    ) -> None:

        self._map_model = map_model
        self._map_received = False
        self._loop = asyncio.get_event_loop()

        # Connect to rosbridge
        self._ros = RosbridgeConnection(rosbridge_host, rosbridge_port)
        self._ros.connect()
        print("[MapController] Connected to rosbridge")

        # Subscribe to topics
        self._ros.subscribe("/map", "nav_msgs/msg/OccupancyGrid", self._map_callback)
        print("[MapController] Subscribed to /map")

        self._ros.subscribe("/humans", "geometry_msgs/msg/PoseArray", self._humans_callback)
        print("[MapController] Subscribed to /humans")

        self._ros.subscribe("/odom", "nav_msgs/msg/Odometry", self._robot_pose_callback)
        print("[MapController] Subscribed to /odom")

    # -------------------------------------------------------------------------
    # SEND MAP PNG ON STARTUP
    # -------------------------------------------------------------------------
    def _send_initial_map_png(self):
        """If the map PNG is already available, send MAP_DATA immediately."""
        if self._map_model._mapDataPNG:
            print("[MapController] Sending initial MAP_DATA on startup")

            async def send_initial():
                await self._map_model.notify_observers({
                    "type": "MAP_DATA",
                    "mapData": {
                        "resolution": self._map_model._mapData.get_resolution(),
                        "width": self._map_model._mapData.get_width(),
                        "height": self._map_model._mapData.get_height(),
                        "occupancyGridPNG": self._map_model._mapDataPNG
                    }
                })

            self._loop.call_soon_threadsafe(lambda: asyncio.create_task(send_initial()))

    # -------------------------------------------------------------------------
    # MAP CALLBACK (STATIC)
    # -------------------------------------------------------------------------
    def _map_callback(self, message: Dict[str, Any]) -> None:
        if self._map_received:
            return

        print("[MapController] Static map received")

        info = message.get("info", {})
        resolution = info.get("resolution", 0.05)
        width_cells = info.get("width", 0)
        height_cells = info.get("height", 0)

        width_m = width_cells * resolution
        height_m = height_cells * resolution

        occupancy_grid = list(message.get("data", []))

        map_data = MapData(
            resolution=resolution,
            width=width_m,
            height=height_m,
            occupancyGrid=occupancy_grid
        )

        # Schedule async update
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self._map_model.set_mapData(map_data))
        )

        self._map_received = True
        print("[MapController] MAP_DATA sent")

    # -------------------------------------------------------------------------
    # HUMANS CALLBACK (DYNAMIC)
    # -------------------------------------------------------------------------
    def _humans_callback(self, message: Dict[str, Any]) -> None:
        poses = message.get("poses", [])
        humans: List[Human] = []

        for idx, pose in enumerate(poses):
            pos = pose.get("position", {})
            humans.append(
                Human(
                    human_id=f"human_{idx+1}",
                    position={
                        "x": pos.get("x", 0.0),
                        "y": pos.get("y", 0.0),
                        "z": pos.get("z", 0.0)
                    },
                    proxemic_distances=None
                )
            )

        # Schedule async update
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self._map_model.set_detectedHumans(humans))
        )

        print(f"[MapController] POSE_DATA: {len(humans)} humans updated")

    # -------------------------------------------------------------------------
    # ROBOT POSE CALLBACK (DYNAMIC)
    # -------------------------------------------------------------------------
    def _robot_pose_callback(self, message: Dict[str, Any]) -> None:
        pose = message.get("pose", {}).get("pose", {})
        if not pose:
            return

        pos = pose.get("position", {})
        ori = pose.get("orientation", {})

        robot_pose = {
            "position": {
                "x": pos.get("x", 0.0),
                "y": pos.get("y", 0.0),
                "z": pos.get("z", 0.0)
            },
            "orientation": {
                "x": ori.get("x", 0.0),
                "y": ori.get("y", 0.0),
                "z": ori.get("z", 0.0),
                "w": ori.get("w", 1.0)
            }
        }

        # Schedule async update
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self._map_model.set_robotPose(robot_pose))
        )

        print(f"[MapController] POSE_DATA: robot pose updated")

    # -------------------------------------------------------------------------
    # SHUTDOWN
    # -------------------------------------------------------------------------
    def shutdown(self) -> None:
        try:
            self._ros.terminate()
        except Exception:
            pass
        print("[MapController] Shutdown complete")
