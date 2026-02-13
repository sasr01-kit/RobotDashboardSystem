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
    Bridges ROS messages to async model updates for the UI.
    """

    def __init__(
        self,
        path_model: Path,
        map_model: Map,
        rosbridge_host: str = "localhost",
        rosbridge_port: int = 9090
    ) -> None:
        """
        Set up ROS subscriptions and async dispatch to models.

        This connects to rosbridge and wires incoming topic data to the
        path/map models so the frontend can stay up to date.

        Params:
            path_model: Path model that stores logs and path state.
            map_model: Map model used to publish goals and poses.
            rosbridge_host: Hostname for the rosbridge websocket server.
            rosbridge_port: Port for the rosbridge websocket server.

        Return:
            None.
        """
        self._path_model = path_model 
        self._map_model = map_model  

        # Event loop used to safely schedule async model updates.
        self._loop = asyncio.get_event_loop()
        self._connected = False  # Tracks rosbridge connection state.
        self._subscribed_topics = []  # Track subscriptions for clean shutdowns.

        # Rosbridge websocket connection for topic IO.
        self._ros = RosbridgeConnection(rosbridge_host, rosbridge_port)
        self._ros.connect()
        self._connected = True
        print("[PathController] Connected to rosbridge")

        # Subscriptions
        # /odom: robot pose 
        self._ros.subscribe("/odom", "nav_msgs/msg/Odometry", self._pose_callback)
        print("[PathController] Subscribed to /odom")

        # /rule_output: rule logs 
        # Note: naming convention of the topic name may vary. The client must confirm the 
        # name of the topic adverised by their specific turtlebot, and replace with the correct name.
        # /rule_output acts as a placeholder in order to work with the publishers created in our mock data. 
        self._ros.subscribe("/rule_output", "std_msgs/msg/String", self._rule_callback)
        print("[PathController] Subscribed to /rule_output")

        # /gary/goal_pose: global goal 
        self._ros.subscribe("/gary/goal_pose", "geometry_msgs/msg/PoseStamped", self._global_goal_callback)
        print("[PathController] Subscribed to /gary/goal_pose")

        # /dock_status: docking status
        self._ros.subscribe("/dock_status", "irobot_create_msgs/msg/DockStatus", self._dock_status_callback)
        print("[PathController] Subscribed to /dock_status")

    def _pose_callback(self, message: Dict[str, Any]) -> None:
        """
        Update the robot pose in the map model.

        This keeps the UI aligned with the robot's live position while the
        path module is active.

        Params:
            message: Rosbridge JSON payload for nav_msgs/msg/Odometry.

        Return:
            None.
        """
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

        # Schedule async update on MapModel.
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self._map_model.set_robotPose(robot_pose))
        )

        print("[PathController] Robot pose updated via MapModel")

    def _rule_callback(self, msg: Dict) -> None:
        """
        Process rule output messages and update goals and logs.

        Rule outputs provide planning intent, so we translate them into
        intermediate goals, global goals, and a log entry for review.

        Params:
            msg: Rosbridge JSON payload for std_msgs/msg/String.

        Return:
            None.
        """
        if not self._path_model.get_is_path_module_active():
            return

        raw = msg.get("data")

        # If input is already a dict (e.g. from mock/test), use it directly.
        if isinstance(raw, dict):
            data = raw

        # If input is a JSON string, parse it.
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

        # 1. Intermediate waypoint.
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

        # 2. Global goal.
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

        # 3. Log rule entry.
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
        """
        Update the global goal marker from /gary/goal_pose.

        Note: the exact name of the topic must be changed based on the precise name of the topic 
        used by the client. The '/gary/goal_pose' is meant to act as a placeholder in order for 
        these subscribers to work with the mock data. The notation of '/gary/goal_pose' was used 
        to make the users aware of how the topic naming could potentially look. Therefore it is 
        meant to strictly act as an example, since the topic name will vary based on the 
        naming conventions for each turtlebot4, and the topics that they advertise. 

        This method keeps the UI goal marker aligned with the planner's active target
        while the path module is active.

        Params:
            message: Rosbridge JSON payload for geometry_msgs/msg/PoseStamped.

        Return:
            None.
        """
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

        # Schedule async update on MapModel.
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self._map_model.set_globalGoal(goal))
        )

        print("[PathController] Global goal updated via MapModel")

    def _dock_status_callback(self, msg: Dict[str, Any]) -> None:
        """
        Track docking status reported by the robot.

        This mirrors the robot's docking state into the path model so the UI
        can show current status.

        Params:
            msg: Rosbridge JSON payload for irobot_create_msgs/msg/DockStatus.

        Return:
            None.
        """
        is_docked = bool(msg.get("is_docked", False))

        # Reflect in PathModel.
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self._path_model.set_is_docked(is_docked))
        )

        print(f"[PathController] Dock status updated from robot: is_docked={is_docked}")
    

    def dock(self) -> None:
        """
        Publish a simulated docked status.

        This user-triggered command updates /dock_status to reflect a docked
        state, which is useful for UI testing or manual control.

        Params:
            None.

        Return:
            None.
        """
        if not self._connected:
            print("[PathController] Not connected to rosbridge. Call connect() first.")
            return
        
        # Create status message indicating docked.
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
        Publish a simulated undocked status.

        This user-triggered command updates /dock_status to reflect an undocked
        state, which is useful for UI testing or manual control.

        Params:
            None.

        Return:
            None.
        """
        if not self._connected:
            print("[PathController] Not connected to rosbridge. Call connect() first.")
            return
        
        # Create status message indicating undocked.
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
        """
        Send a stop command to halt robot motion.

        This provides an immediate safety stop by publishing a zero-velocity
        command to the robot.

        Params:
            None.

        Return:
            None.
        """
        self._ros.publish(
            "/cmd_vel",
            DirectionCommand.STOP.get_message(),
            msg_type=
            "geometry_msgs/msg/Twist",
           
        )
        print("[PathController] Published STOP command to /cmd_vel")

    def get_records(self):
        """
        Fetch the current path history.

        This provides the UI with the accumulated log entries for review.

        Params:
            None.

        Return:
            List of PathLogEntry items stored in the path model.
        """
        return self._path_model.get_path_history()
   
    def stop(self):
        """
        Stop subscriptions and close the rosbridge connection.

        This releases resources and prevents further callbacks during shutdown.

        Params:
            None.

        Return:
            None.
        """
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
