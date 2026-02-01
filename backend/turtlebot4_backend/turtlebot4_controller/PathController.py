import time
import json
from typing import Dict
from turtlebot4_backend.turtlebot4_controller.RosbridgeConnection import RosbridgeConnection
from turtlebot4_backend.turtlebot4_model.Path import Path
from turtlebot4_backend.turtlebot4_model.PathLogEntry import PathLogEntry


class PathController:
    """
    Tracks intermediate and global goals published by a fuzzy logic system.
    - Records each goal with timestamp and fuzzy rule used
    - Only active when Path module is activated
    - Automatically disables subscriptions and ignores callbacks when inactive
    """
    def __init__(self, path_model: Path, ros_host: str = 'localhost', ros_port: int = 9090):
        self._ros = RosbridgeConnection(host=ros_host, port=ros_port)
        self._connected = False

        # Path module model
        self._path_model = path_model

        # Track the latest robot pose
        self.latest_pose = {'x': None, 'y': None, 'stamp': None}

        # Topic configuration
        self._goal_topic_name = '/ruleOutput'
        self._goal_msg_type = 'std_msgs/msg/String'
        self._pose_topic_name = '/odom'
        self._pose_msg_type = 'nav_msgs/msg/Odometry'

        # Keep track of subscribed topics for safe cleanup
        self._subscribed_topics = []

        # Monitor Path module activation
        self._check_activation_thread_started = False

    def connect(self):
        """Connect to rosbridge and start subscriptions if the Path module is active."""
        if self._connected:
            return

        self._ros.connect()
        self._connected = True

        # Start a thread to monitor Path module activation
        if not self._check_activation_thread_started:
            import threading
            threading.Thread(target=self._monitor_path_module_activation, daemon=True).start()
            self._check_activation_thread_started = True

    def _monitor_path_module_activation(self):
        """
        Continuously checks if Path module is active.
        If active, ensures subscriptions are present.
        If inactive, unsubscribes to avoid unsafe callbacks.
        """
        import time
        while self._connected:
            is_active = self._path_model.get_is_path_module_active()

            if is_active and not self._subscribed_topics:
                # Subscribe to topics
                self._subscribed_topics.append(
                    self._ros.subscribe(self._goal_topic_name, self._goal_msg_type, self._rule_callback)
                )
                self._subscribed_topics.append(
                    self._ros.subscribe(self._pose_topic_name, self._pose_msg_type, self._pose_callback)
                )
                print("[PathController] Subscriptions activated because Path module is active")

            elif not is_active and self._subscribed_topics:
                # Unsubscribe from all topics
                for topic in self._subscribed_topics:
                    try:
                        topic.unsubscribe()
                    except Exception:
                        pass
                self._subscribed_topics = []
                print("[PathController] Subscriptions deactivated because Path module is inactive")

            time.sleep(0.5)

    def _pose_callback(self, msg: Dict):
        """Update the latest robot pose only if Path module is active."""
        if not self._path_model.get_is_path_module_active():
            return

        pose = msg.get('pose', {}).get('pose', {})
        position = pose.get('position', {})
        x = position.get('x', None)
        y = position.get('y', None)

        self.latest_pose = {
            'x': x,
            'y': y,
            'stamp': time.time()
        }

        print(f"[POSE] x={x:.2f}, y={y:.2f}, stamp={self.latest_pose['stamp']}")

    def _rule_callback(self, msg: Dict):
        """Record a goal when a fuzzy rule output is received, only if active."""
        if not self._path_model.get_is_path_module_active():
            return

        data_str = msg.get('data', 'UNKNOWN')
        goal_type = None  # default None
        rule_str = data_str

        # Attempt to parse JSON from fuzzy system
        try:
            data_dict = json.loads(data_str)
            rule_str = data_dict.get('rule', 'UNKNOWN')
            goal_type = data_dict.get('goal_type', None)  # dynamic, e.g., "global" or "intermediate"
        except Exception:
            pass  # keep as string, goal_type remains None

        if self.latest_pose['x'] is None or self.latest_pose['y'] is None:
            print("[PathController] No pose available yet, skipping log")
            return

        # Dynamic ID for the log entry
        entry_id = f"goal_{len(self._path_model.get_path_history()) + 1}"

        # Create PathLogEntry
        entry = PathLogEntry(
            label="Goal Entry",
            id=entry_id,
            goal_type=goal_type,
            timestamp=self.latest_pose['stamp'],
            fuzzy_output=rule_str,
            user_feedback=None
        )

        # Add entry to Path model
        self._path_model.add_log_entry(entry)

        print(f"[GOAL LOGGED] x={self.latest_pose['x']:.2f}, "
              f"y={self.latest_pose['y']:.2f}, "
              f"goal_type='{goal_type}', rule='{rule_str}', stamp={self.latest_pose['stamp']}")

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
