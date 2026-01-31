#!/usr/bin/env python3
import rclpy     
from turtlebot4_model.Teleoperate import Teleoperate
from turtlebot4_model.DirectionCommand import DirectionCommand

from rclpy.node import Node
from geometry_msgs.msg import Twist

class TeleopNode(Node):
    def __init__(self):
        super().__init__("teleoperation")
        self.cmd_vel_pub_ = self.create_publisher(Twist, "/cmd_vel", 10)
        self.timer_= self.create_timer(0.5, self.send_velocity_command)
         # Create an instance of Teleoperate
        self.teleop = Teleoperate()
        self.get_logger().info("Teleop communiction established")

    def send_drive_command(self):
            commandQueue_ = self.teleop.get_commands()
            if not commandQueue_:
            # No commands in the queue; do nothing
                 # Queue is empty → stop node
                self.get_logger().info("Command queue empty. Shutting down node.")
                self.timer_.cancel()       # Stop the timer
                rclpy.shutdown()           # Shutdown ROS 2
                return

            cmd = commandQueue_.pop(0)
            msg = Twist()

            if cmd == "FORWARD":
                msg.linear.x = DirectionCommand.FORWARD.value
                msg.angular.z = 0.0

                self.get_logger().info("Command detected: UP")


            elif cmd == "BACKWARD":
                msg.linear.x = DirectionCommand.BACKWARD.value
                msg.angular.z = 0.0
                self.get_logger().info("Command detected: DOWN")

            elif cmd == "LEFT":
                msg.linear.x = DirectionCommand.FORWARD.value
                msg.angular.z = DirectionCommand.LEFT.value
                self.get_logger().info("Command detected: LEFT")

            elif cmd == "RIGHT":
                msg.linear.x = DirectionCommand.FORWARD.value
                msg.angular.z = DirectionCommand.RIGHT.value            
                self.get_logger().info("Command detected: RIGHT")

            elif cmd == "ROTATE_RIGHT":
                msg.angular.z = DirectionCommand.RIGHT.value
                self.get_logger().info("Command detected: ROTATE_RIGHT")

            elif cmd == "ROTATE_LEFT":
                msg.angular.z = DirectionCommand.LEFT.value
                self.get_logger().info("Command detected: ROTATE_RIGHT")
                
            self.cmd_vel_pub_.publish(msg)

    def stop_robot():
        pass

def main (args=None):
    rclpy.init(args=args)
    node = TeleopNode()
    rclpy.spin(node)

'''

'''