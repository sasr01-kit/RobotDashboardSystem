# DirectionCommand.py
from enum import Enum
from dataclasses import dataclass



class DirectionCommand(Enum):
    FORWARD = 0.5
    BACKWARD = -0.5
    RIGHT = 1.0
    LEFT = -1.0
    STOP = 0
