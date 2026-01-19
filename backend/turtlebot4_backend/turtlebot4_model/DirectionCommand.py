# DirectionCommand.py
from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class VelocityPair:
    linear: float
    angular: float


class DirectionCommand(Enum):
    FORWARD = VelocityPair(linear=0.5, angular=0.0)
    BACKWARD = VelocityPair(linear=-0.5, angular=0.0)
    LEFT = VelocityPair(linear=0.0, angular=0.5)
    RIGHT = VelocityPair(linear=0.0, angular=-0.5)

    def to_dict(self) -> dict:
        """
        Convert this command into a JSON-friendly dictionary
        representing linear and angular velocity.
        """
        return {
            "linear": self.value.linear,
            "angular": self.value.angular
        }

    def __str__(self) -> str:
        return self.name
