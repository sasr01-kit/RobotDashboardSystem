#!/usr/bin/env python3
import time
import threading
import asyncio
import roslibpy

from turtlebot4_backend.turtlebot4_controller.RosbridgeConnection import RosbridgeConnection
from turtlebot4_backend.turtlebot4_model.Teleoperate import Teleoperate
from turtlebot4_backend.turtlebot4_model.DirectionCommand import DirectionCommand


class TeleopController:
    def __init__( 
        self, 
        teleop: Teleoperate, 
        ros_host: str = 'localhost', 
        ros_port: int = 9090, 
        loop: asyncio.AbstractEventLoop | None = None 
    ):
        self.teleop = teleop
        self._ros = RosbridgeConnection(host=ros_host, port=ros_port)
        self._loop = loop or asyncio.get_event_loop()

        # Waits for teleop updates and publishes to ROSBridge when they occur
        teleop.attach(self._on_teleop_update)

        # Connect to rosbridge
        self.client = roslibpy.Ros(host=ros_host, port=ros_port)
        self.client.run()
        print("[TeleopController] Connecting to ROSBridge...")

        # Wait until connected
        for _ in range(50):  # ~5 seconds
            if self.client.is_connected:
                break
            time.sleep(0.1)

        if not self.client.is_connected:
            print("[TeleopController] ERROR: Could not connect to ROSBridge")
            return

        print("[TeleopController] Connected to ROSBridge")

        # Correct ROS 1 message type for rosbridge
        self.cmd_vel_topic = roslibpy.Topic(
            self.client,
            '/cmd_vel',
            'geometry_msgs/msg/Twist'
        )
        self.cmd_vel_topic.advertise()
        print("[TeleopController] /cmd_vel advertised")


    # Teleoperate model calls this synchronously → schedule async work
    def _on_teleop_update(self, source, data):
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self._publish_drive_command())
        )

    async def _publish_drive_command(self):
        self._ros.connect()
        cmd = self.teleop.get_command()
        if not cmd:
            return

        msg = {
            'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0},
            'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
        }

        if cmd == "FORWARD":
            msg['linear']['x'] = DirectionCommand.FORWARD.value
            print("Command detected: FORWARD")

        elif cmd == "BACKWARD":
            msg['linear']['x'] = DirectionCommand.BACKWARD.value
            print("Command detected: BACKWARD")

        elif cmd == "LEFT":
            msg['linear']['x'] = DirectionCommand.FORWARD.value
            msg['angular']['z'] = DirectionCommand.LEFT.value
            print("Command detected: LEFT")

        elif cmd == "RIGHT":
            msg['linear']['x'] = DirectionCommand.FORWARD.value
            msg['angular']['z'] = DirectionCommand.RIGHT.value
            print("Command detected: RIGHT")

        elif cmd == "ROTATE_LEFT":
            msg['angular']['z'] = DirectionCommand.LEFT.value
            print("Command detected: ROTATE_LEFT")

        elif cmd == "ROTATE_RIGHT":
            msg['angular']['z'] = DirectionCommand.RIGHT.value
            print("Command detected: ROTATE_RIGHT")

        elif cmd == "STOP":
            print("Command detected: STOP")

        print("[TeleopController] Publishing:", msg)

        try:
            self._ros.publish( '/cmd_vel', msg, msg_type='geometry_msgs/msg/Twist' )
            print("[TeleopController] Published to /cmd_vel")
        except Exception as e:
            print("[TeleopController] ERROR publishing:", e)


    def stop(self):
        try:
            self.cmd_vel_topic.unadvertise()
        except Exception:
            pass

        try:
            self.client.terminate()
        except Exception:
            pass

        print("[TeleopController] Teleop stopped")
