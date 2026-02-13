#!/usr/bin/env python3
import time
import threading
import asyncio
import roslibpy

from turtlebot4_backend.turtlebot4_controller.RosbridgeConnection import RosbridgeConnection
from turtlebot4_backend.turtlebot4_model.Teleoperate import Teleoperate
from turtlebot4_backend.turtlebot4_model.DirectionCommand import DirectionCommand

class TeleopController:
    """
    Subscribes to Teleoperate model updates and publishes drive commands to ROSBridge.
    """
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
        self._ros.connect()

        # Waits for teleop updates and publishes to ROSBridge when they occur
        teleop.attach(self._on_teleop_update)

        print("[TeleopController] Connecting to ROSBridge...")

        # Wait until connected
        for _ in range(50):  # ~5 seconds
            if self._ros.isConnected:
                break
            time.sleep(0.1)

        if not self._ros.isConnected:
            print("[TeleopController] ERROR: Could not connect to ROSBridge")
            return

        print("[TeleopController] Connected to ROSBridge")
        # Advertise the topic with an empty message to ensure it exists before we try to publish real commands
        self._ros.publish('/cmd_vel', {}, msg_type='geometry_msgs/msg/Twist')  
        print("[TeleopController] /cmd_vel advertised")

    # Teleoperate model calls this synchronously → schedule async work
    def _on_teleop_update(self, source, data):
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self._publish_drive_command())
        )

    async def _publish_drive_command(self):
        cmd = self.teleop.get_command()
        if not cmd:
            return

        try:
            # Convert string → enum (e.g. "FORWARD" → DirectionCommand.FORWARD)
            direction_cmd = DirectionCommand[cmd]

            # Get the Twist dict from the enum
            msg = direction_cmd.get_message()

            print(f"[TeleopController] Command detected: {cmd}")
            print("[TeleopController] Publishing:", msg)

            # Publish via rosbridge
            self._ros.publish(
                "/cmd_vel",
                msg,
                msg_type="geometry_msgs/msg/Twist"
            )

            print("[TeleopController] Published to /cmd_vel")

        except KeyError:
            print(f"[TeleopController] Unknown command: {cmd}")

        except Exception as e:
            print(f"[TeleopController] ERROR publishing: {e}")# Get the next command from teleop
    


    def stop(self):
        try:
            self._ros.unadvertise('/cmd_vel')
        except Exception:
            pass

        try:
            self._ros.terminate()
        except Exception:
            pass

        print("[TeleopController] Teleop stopped")
