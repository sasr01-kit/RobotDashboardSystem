# DirectionCommand.py
from enum import Enum
from dataclasses import dataclass
from geometry_msgs.msg import Twist  # ROS message type


@dataclass(frozen=True)
class VelocityPair:
    linear: float
    angular: float


class DirectionCommand(Enum):
    FORWARD = VelocityPair(linear=0.5, angular=0.0)
    BACKWARD = VelocityPair(linear=-0.5, angular=0.0)
    LEFT = VelocityPair(linear=0.0, angular=0.5)   # angular constant
    RIGHT = VelocityPair(linear=0.0, angular=-0.5) # angular constant

    def to_twist(self) -> Twist:
        """
        Convert this command to a ROS Twist message.
        """
        twist = Twist()
        twist.linear.x = self.value.linear
        twist.angular.z = self.value.angular
        return twist

    def __str__(self) -> str:
        return self.name
