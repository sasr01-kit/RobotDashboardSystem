import asyncio
import json
import time
from datetime import datetime
from typing import Any, Dict
from turtlebot4_backend.turtlebot4_controller.RosbridgeConnection import RosbridgeConnection
from turtlebot4_backend.turtlebot4_model.Map import Map
from turtlebot4_backend.turtlebot4_model.Path import Path  
from turtlebot4_backend.turtlebot4_model.PathLogEntry import PathLogEntry
from turtlebot4_backend.turtlebot4_model.DirectionCommand import DirectionCommand

class PathController:
    """
    Subscribes to path-related topics via RosbridgeConnection.
    """

    def __init__(
        self,
        path_model: Path,
        map_model: Map,
        rosbridge_host: str = "localhost",
        rosbridge_port: int = 9090
    ) -> None:
        self._path_model = path_model
        self._map_model = map_model

        # Event loop for scheduling async model updates
        self._loop = asyncio.get_event_loop()
        self._connected = False

        # Connect to rosbridge
        self._ros = RosbridgeConnection(rosbridge_host, rosbridge_port)
        self._ros.connect()
        self._connected = True
        print("[PathController] Connected to rosbridge")

        # Subscriptions
        # /odom: robot pose 
        self._ros.subscribe("/odom", "nav_msgs/msg/Odometry", self._pose_callback)
        print("[PathController] Subscribed to /odom")

        # /rule_output: rule logs 
        self._ros.subscribe("/rule_output", "std_msgs/msg/String", self._rule_callback)
        print("[PathController] Subscribed to /rule_output")

        # /gary/goal_pose: global goal 
        self._ros.subscribe("/gary/goal_pose", "geometry_msgs/msg/PoseStamped", self._global_goal_callback)
        print("[PathController] Subscribed to /gary/goal_pose")

        # /dock_status: docking status
        self._ros.subscribe("/dock_status", "irobot_create_msgs/msg/DockStatus", self._dock_status_callback)
        print("[PathController] Subscribed to /dock_status")

    def _pose_callback(self, message: Dict[str, Any]) -> None:
        if not self._path_model.get_is_path_module_active():
             return

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

        # Schedule async update on MapModel
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self._map_model.set_robotPose(robot_pose))
        )

        print("[PathController] Robot pose updated via MapModel")

    def _rule_callback(self, msg: Dict):
        if not self._path_model.get_is_path_module_active():
            return

        raw = msg.get("data")

        # if input is already a dict (e.g. from mock/test), use it directly
        if isinstance(raw, dict):
            data = raw

        # if input is a JSON string, parse it
        elif isinstance(raw, str):
            try:
                data = json.loads(raw)
            except Exception:
                print("[PathController] Invalid rule JSON:", raw)
                return

        else:
            print("[PathController] Unexpected rule message format:", raw)
            return


        goal_type = data.get("goal_type", "")
        position = data.get("position", {})
        rule_str = data.get("rule", "")

        # 1. Intermediate waypoint
        if goal_type == "intermediate":
            waypoint = {
                "position": {
                    "x": position.get("x", 0.0),
                    "y": position.get("y", 0.0),
                    "z": 0.0
                },
                "orientation": {"x": 0, "y": 0, "z": 0, "w": 1}
            }

            updated = self._map_model._intermediateWaypoints + [waypoint]

            self._loop.call_soon_threadsafe(
                lambda: asyncio.create_task(self._map_model.set_intermediateWaypoints(updated))
            )

        # 2. Global goal
        if goal_type == "global":
            goal = {
                "position": {
                    "x": position.get("x", 0.0),
                    "y": position.get("y", 0.0),
                    "z": 0.0
                },
                "orientation": {"x": 0, "y": 0, "z": 0, "w": 1}
            }

            self._loop.call_soon_threadsafe(
                lambda: asyncio.create_task(self._map_model.set_globalGoal(goal))
            )

        # 3. Log rule entry
        entry = PathLogEntry(
            label="Goal Entry",
            id=f"goal_{len(self._path_model.get_path_history()) + 1}",
            goal_type=goal_type,
            timestamp=datetime.now(),
            fuzzy_output=rule_str,
            user_feedback=""
        )

        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self._path_model.add_log_entry(entry))
        )

        print(f"[PathController] Logged rule: {rule_str}, type={goal_type}")

    def _global_goal_callback(self, message: Dict[str, Any]) -> None:
        if not self._path_model.get_is_path_module_active():
            return

        pose = message.get("pose", {})
        pos = pose.get("position", {})

        goal = {
            "position": {
                "x": pos.get("x", 0.0),
                "y": pos.get("y", 0.0),
                "z": pos.get("z", 0.0)
            },
            "orientation": pose.get("orientation", {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            })
        }

        # Schedule async update on MapModel
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self._map_model.set_globalGoal(goal))
        )

        print("[PathController] Global goal updated via MapModel")

    def _dock_status_callback(self, msg: Dict[str, Any]) -> None:
        is_docked = bool(msg.get("is_docked", False))

        # reflect in PathModel
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self._path_model.set_is_docked(is_docked))
        )

        print(f"[PathController] Dock status updated from robot: is_docked={is_docked}")
    

    def dock(self) -> None:
        """
        Publishes a docking status to the /dock_status topic.
        This is a user-triggered command.
        """
        if not self._connected:
            print("[PathController] Not connected to rosbridge. Call connect() first.")
            return
        
        # Create status message indicating docked
        dock_status_msg = {
            "is_docked": True,
            "dock_visible": True,
            "header": {
                "stamp": {
                    "sec": int(time.time()),
                    "nanosec": int((time.time() % 1) * 1e9)
                },
                "frame_id": "base_link"
            }
        }
        
        self._ros.publish("/dock_status", dock_status_msg)
        print("[PathController] Published dock status: docked=True")

    def undock(self) -> None:
        """
        Publishes an undocking status to the /dock_status topic.
        This is a user-triggered command.
        """
        if not self._connected:
            print("[PathController] Not connected to rosbridge. Call connect() first.")
            return
        
        # Create status message indicating undocked
        dock_status_msg = {
            "is_docked": False,
            "dock_visible": False,
            "header": {
                "stamp": {
                    "sec": int(time.time()),
                    "nanosec": int((time.time() % 1) * 1e9)
                },
                "frame_id": "base_link"
            }
        }
    
        self._ros.publish("/dock_status", dock_status_msg)
        print("[PathController] Published dock status: docked=False")

    def cancelNavigation(self) -> None:
        self._ros.publish(
            "/cmd_vel",
            DirectionCommand.STOP.get_message(),
            msg_type=
            "geometry_msgs/msg/Twist",
           
        )
        print("[PathController] Published STOP command to /cmd_vel")

    def get_records(self):
        """Return the current path history as a list of PathLogEntry."""
        return self._path_model.get_path_history()
   
    def stop(self):
        """Clean up subscriptions and terminate connection."""
        self._connected = False

        # Unsubscribe all topics
        for topic in self._subscribed_topics:
            try:
                topic.unsubscribe()
            except Exception:
                pass
        self._subscribed_topics = []

        # Terminate rosbridge connection
        self._ros.terminate()
        print("[PathController] Stopped and disconnected from rosbridge")
