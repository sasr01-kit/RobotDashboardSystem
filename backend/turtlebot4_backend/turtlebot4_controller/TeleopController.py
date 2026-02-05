#!/usr/bin/env python3
import time
import threading
import roslibpy
from turtlebot4_model.Teleoperate import Teleoperate
from turtlebot4_model.DirectionCommand import DirectionCommand

from geometry_msgs.msg import Twist  # Only for message structure, not ROS 2

class TeleopController:
    def __init__(self, rosbridge_url='ws://localhost:9090'):
        # Connect to rosbridge
        self.client = roslibpy.Ros(host='localhost', port=9090)
        self.client.run()
        print("Connected to ROSBridge")

        # Teleoperate instance
        self.teleop = Teleoperate()

        # ROS topic
        self.cmd_vel_topic = roslibpy.Topic(self.client, '/cmd_vel', 'geometry_msgs/Twist')

        # Start publishing loop
        self.running = True
        self.timer = threading.Thread(target=self._publish_loop)
        self.timer.start()

    def _publish_loop(self):
        while self.running:
            self.send_drive_command()
            time.sleep(0.5)  # equivalent to timer period

    def send_drive_command(self):
        command_queue = self.teleop.get_commands()
        if not command_queue:
            print("Command queue empty. Stopping publisher.")
            self.running = False
            self.cmd_vel_topic.unadvertise()
            self.client.terminate()
            return

        cmd = command_queue.pop(0)
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

        self.cmd_vel_topic.publish(roslibpy.Message(msg))

    def stop(self):
        self.running = False
        self.cmd_vel_topic.unadvertise()
        self.client.terminate()
        print("Teleop stopped")