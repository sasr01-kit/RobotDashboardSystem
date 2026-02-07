import roslibpy
import numpy as np
from typing import Optional
from turtlebot4_model.Map import Map
from turtlebot4_model.MapData import MapData
from turtlebot4_model.Human import Human
from typing import Dict



class MapController:
    """
    Receives the static OccupancyGrid map via ROSBridge,
    converts it into a MapData object, and injects it into the Map model.
    """

    def __init__(
        self,
        map_model: Map,
        rosbridge_host: str = 'localhost',
        rosbridge_port: int = 9090
    ) -> None:
        self._map_model = map_model
        self._map_received = False

        # ROSBridge connection
        self._ros = roslibpy.Ros(
            host=rosbridge_host,
            port=rosbridge_port
        )
        self._ros.run()

        # Subscribe to /map (latched topic)
        self._map_subscriber = roslibpy.Topic(
            self._ros,
            '/map',
            'nav_msgs/OccupancyGrid'
        )
        self._map_subscriber.subscribe(self._map_callback)

        print("MapController connected to rosbridge and subscribed to /map")

    def _map_callback(self, message: dict) -> None:
        """
        Handles the OccupancyGrid message received from rosbridge.
        This should only run once for the static map.
        """
        if self._map_received:
            return  # Ignore further updates

        print("Static map received from ROSBridge")

        info = message['info']

        resolution = info['resolution']
        width_cells = info['width']
        height_cells = info['height']

        # Convert to meters (consistent with your Map logic)
        width_m = width_cells * resolution
        height_m = height_cells * resolution

        occupancy_grid = list(message['data'])  # flat list[int]

        # Create MapData instance
        map_data = MapData(
            resolution=resolution,
            width=width_m,
            height=height_m,
            occupancyGrid=occupancy_grid
        )

        # Inject into Map model (this triggers PNG + base64 conversion)
        self._map_model.set_mapData(map_data)

        self._map_received = True

        print("MapData injected into Map model")

        # Optional: unsubscribe since map is static
        self._map_subscriber.unsubscribe()

    def _create_pose_array_message(
        self, 
        positions: List[Dict[str, float]], 
        frame_id: str = "map"
    ) -> Dict[str, Any]:
        """
        Creates a PoseArray message from a list of positions.
        
        @param positions: List of dictionaries with 'x' and 'y' keys
        @param frame_id: Frame ID for the header (default: "map")
        @return: Dictionary representing a PoseArray message
        """
        pose_array_msg = {
            "header": {
                "stamp": {
                    "secs": 0,
                    "nsecs": 0
                },
                "frame_id": frame_id
            },
            "poses": []
        }

        # Add each position as a Pose
        for pos in positions:
            pose = {
                "position": {
                    "x": pos.get("x", 0.0),
                    "y": pos.get("y", 0.0),
                    "z": pos.get("z", 0.0)
                },
                "orientation": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0,
                    "w": 1.0
                }
            }
            pose_array_msg["poses"].append(pose)

        return pose_array_msg
    
    def setHumanPositions(self) -> None:
        """
        Publishes two hardcoded human positions to the /humans topic.
        Message type: geometry_msgs/PoseArray
        """
        # Hardcoded human positions to mock the data
        human_positions = [
            {"x": 1.5, "y": 1.0},  # Human 1
            {"x": 2.5, "y": 2.0}   # Human 2
        ]

        # Create PoseArray message using helper method
        pose_array_msg = self._create_pose_array_message(human_positions, frame_id="map")


        # Publish to /humans topic
        self._humans_publisher.publish(roslibpy.Message(pose_array_msg))
        print(f"[MapController] Published {len(human_positions)} human positions to /humans")

    def updateHumanPositions(self) -> None:
        """
        A callback method that establishes a subscription to the human position data.
        It extracts the data required to position the humans on the map,
        and sets the appropriate values to the list of detected humans in the map model.
        """
        def _humans_callback(message: dict) -> None:
            """
            Internal callback that processes human position data from /humans topic.
            """
            poses = message.get('poses', [])
            
            if not poses:
                print("[MapController] No humans detected in message")
                return

            # Create list of Human objects
            detected_humans: List[Human] = []


            for idx, pose in enumerate(poses):
                position = pose.get('position', {})
                
                # Extract x, y coordinates
                x = position.get('x', 0.0)
                y = position.get('y', 0.0)
                z = position.get('z', 0.0)

                # Create position dict for Human object
                human_position = {
                    "x": x,
                    "y": y,
                    "z": z
                }

                # Create Human object
                human = Human(
                    human_id=f"human_{idx + 1}",
                    position=human_position,
                    proxemic_distances=None
                )

                detected_humans.append(human)

                print(f"[MapController] Human {idx + 1} detected at x={x:.2f}, y={y:.2f}")

            # Update the Map model with detected humans
            # Assuming your Map class has a method to set humans list
            if hasattr(self._map_model, 'set_humans'):
                self._map_model.set_detectedHumans(detected_humans)
                print(f"[MapController] Updated map model with {len(detected_humans)} humans")
            else:
                print("[MapController] Warning: Map model doesn't have 'set_humans' method")

        # Subscribe to /humans topic with the callback
        self._humans_subscriber.subscribe(_humans_callback)
        print("[MapController] Subscribed to /humans topic for updates")
        
    def updateRobotPose(self) -> None:
        """
        A callback method that establishes a subscription to the robot pose data.
        It extracts the robot's position from /odom and updates the Map model.
        """
        def _robot_pose_callback(message: dict) -> None:
            """
            Internal callback that processes robot pose data from /odom topic.
            """
            # Extract pose from Odometry message
            pose = message.get('pose', {}).get('pose', {})
            
            if not pose:
                print("[MapController] No pose data in odometry message")
                return
            
            position = pose.get('position', {})
            orientation = pose.get('orientation', {})
            
            # Extract position coordinates
            x = position.get('x', 0.0)
            y = position.get('y', 0.0)
            z = position.get('z', 0.0)
            
            # Extract orientation quaternion
            qx = orientation.get('x', 0.0)
            qy = orientation.get('y', 0.0)
            qz = orientation.get('z', 0.0)
            qw = orientation.get('w', 1.0)
            
            # Create robot pose dict (PoseStamped-like format)
            robot_pose = {
                "position": {
                    "x": x,
                    "y": y,
                    "z": z
                },
                "orientation": {
                    "x": qx,
                    "y": qy,
                    "z": qz,
                    "w": qw
                }
            }
            
            # Update the Map model with robot pose
            self._map_model.set_robotPose(robot_pose)
            print(f"[MapController] Robot pose updated: x={x:.2f}, y={y:.2f}")
        
        # Create subscriber if not already created
        if not hasattr(self, '_robot_pose_subscriber'):
            self._robot_pose_subscriber = roslibpy.Topic(
                self._ros,
                '/odom',
                'nav_msgs/msg/Odometry'
            )
        
        # Subscribe to /odom topic with the callback
        self._robot_pose_subscriber.subscribe(_robot_pose_callback)
        print("[MapController] Subscribed to /odom topic for robot pose updates")

    
 
    def shutdown(self) -> None:
        """
        Clean shutdown of rosbridge connection.
        """
        if self._map_subscriber:
            self._map_subscriber.unsubscribe()
        if self._ros:
            self._ros.terminate()
        print("MapController shutdown complete")