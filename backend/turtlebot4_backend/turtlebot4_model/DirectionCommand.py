from enum import Enum
from typing import Dict
import copy


class DirectionCommand(Enum):
    """Robot movement commands with configurable speeds."""
    
    # Default speeds (class variables)
    LINEAR_SPEED = 0.5
    ANGULAR_SPEED = 1.0
    
    FORWARD = {
        'linear': {'x': LINEAR_SPEED, 'y': 0.0, 'z': 0.0},
        'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
    }
    
    BACKWARD = {
        'linear': {'x': -LINEAR_SPEED, 'y': 0.0, 'z': 0.0},
        'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
    }
    
    LEFT = {
        'linear': {'x': LINEAR_SPEED, 'y': 0.0, 'z': 0.0},
        'angular': {'x': 0.0, 'y': 0.0, 'z': -ANGULAR_SPEED}
    }
    
    RIGHT = {
        'linear': {'x': LINEAR_SPEED, 'y': 0.0, 'z': 0.0},
        'angular': {'x': 0.0, 'y': 0.0, 'z': ANGULAR_SPEED}
    }
    
    ROTATE_LEFT = {
        'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0},
        'angular': {'x': 0.0, 'y': 0.0, 'z': -ANGULAR_SPEED}
    }
    
    ROTATE_RIGHT = {
        'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0},
        'angular': {'x': 0.0, 'y': 0.0, 'z': ANGULAR_SPEED}
    }
    
    STOP = {
        'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0},
        'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
    }

    def get_message(self) -> Dict:
        """Returns a deep copy of the message."""
        return copy.deepcopy(self.value)
    
    @staticmethod
    def create_custom(linear_x: float = 0.0, angular_z: float = 0.0) -> Dict:
        """Create a custom velocity message."""
        return {
            'linear': {'x': linear_x, 'y': 0.0, 'z': 0.0},
            'angular': {'x': 0.0, 'y': 0.0, 'z': angular_z}
        }