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
        """
        Initialize rosbridge subscriptions and prepare async dispatch.

        This wires ROS topic callbacks to the async map model so the UI can
        receive static map data once and live pose updates continuously.

        Params:
            map_model: Map model that publishes updates to observers.
            rosbridge_host: Hostname for the rosbridge websocket server.
            rosbridge_port: Port for the rosbridge websocket server.

        Return:
            None.
        """

        self._map_model = map_model
        self._map_received = False

        # ROS callbacks run synchronously, but the WebSocket
        # updates are asynchronous and require 'await'. The event loop is used to safely
        # schedule async tasks from inside these synchronous ROS callbacks.
        self._loop = asyncio.get_event_loop()

        # Connect to rosbridge
        self._ros = RosbridgeConnection(rosbridge_host, rosbridge_port)
        self._ros.connect()
        print("[MapController] Connected to rosbridge")

        # Subscribe to topics
        # /map: static map data 
        self._ros.subscribe("/map", "nav_msgs/msg/OccupancyGrid", self._map_callback)
        print("[MapController] Subscribed to /map")

        # /humans: dynamic human poses 
        self._ros.subscribe("/humans", "geometry_msgs/msg/PoseArray", self._humans_callback)
        print("[MapController] Subscribed to /humans")

        # /odom: dynamic robot pose 
        self._ros.subscribe("/odom", "nav_msgs/msg/Odometry", self._robot_pose_callback)
        print("[MapController] Subscribed to /odom")


    def _send_initial_map_png(self):
        """
        Send MAP_DATA once if a cached PNG is already available.

        This avoids waiting for /map messages during startup so the frontend can
        render a map as soon as possible when prior data exists.

        Params:
            None.

        Return:
            None.
        """
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

    def _map_callback(self, message: Dict[str, Any]) -> None:
        """
        Handle the static /map message and publish MAP_DATA once.

        The map is static, so we process it only the first time to reduce
        bandwidth and avoid redundant frontend work.

        Params:
            message: Rosbridge JSON payload for nav_msgs/msg/OccupancyGrid.

        Return:
            None.
        """
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

        # Schedule async update to map model
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self._map_model.set_mapData(map_data))
        )

        self._map_received = True
        print("[MapController] MAP_DATA sent")

    def _humans_callback(self, message: Dict[str, Any]) -> None:
        """
        Handle /humans updates and publish POSE_DATA for detected humans.

        Human positions are dynamic, so each update is forwarded to keep the UI
        in sync with the latest tracked poses.

        Params:
            message: Rosbridge JSON payload for geometry_msgs/msg/PoseArray.

        Return:
            None.
        """
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

        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self._map_model.set_detectedHumans(humans))
        )

        print(f"[MapController] POSE_DATA: {len(humans)} humans updated")

    def _robot_pose_callback(self, message: Dict[str, Any]) -> None:
        """
        Handle /odom updates and publish the robot pose.

        The robot pose changes continuously, so each update is pushed to the UI
        to keep navigation and visualization accurate.

        Params:
            message: Rosbridge JSON payload for nav_msgs/msg/Odometry.

        Return:
            None.
        """
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

        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self._map_model.set_robotPose(robot_pose))
        )

        print(f"[MapController] POSE_DATA: robot pose updated")

    def shutdown(self) -> None:
        """
        Close rosbridge connections and release resources.

        This ensures sockets are closed cleanly and the controller stops
        receiving callbacks when the application exits.

        Params:
            None.

        Return:
            None.
        """
        try:
            self._ros.terminate()
        except Exception:
            pass
        print("[MapController] Shutdown complete")
