# Teleoperate.py
from typing import List, Dict, Any
from turtlebot4_model.Subject import Subject
from .DirectionCommand import DirectionCommand


class Teleoperate(Subject):
    def __init__(self) -> None:
        super().__init__()
        self._commands: List[str] # = ["FORWARD", "LEFT"]

    # Getter
    def get_commands(self) -> List[str]:
        return self._commands

    # Setter
    def set_commands(self, commands: List[DirectionCommand]) -> None:
        self._commands = commands
        self.notifyObservers(self.toJSON())

    # Add a single command
    def add_command(self, command: DirectionCommand) -> None:
        self._commands.append(command)
        self.notifyObservers(self.toJSON())

    # Deserialize frontend JSON into DirectionCommand(s)

    def fromJSON(self, msg: Dict[str, Any]):
        """
        Parse JSON commands and append them as strings to the existing list.
        Expected format: { "commands": ["UP", "LEFT"] }
        """
        for cmd in msg["commands"]:
            self._commands.append(cmd.upper())  # normalize to uppercase

   
    # Serialize commands to JSON for frontend confirmation
    def toJSON(self) -> Dict[str, Any]:
        """
        Returns JSON indicating teleoperation state and queued commands.
        """
        return {
            "teleoperationActive": len(self._commands) > 0,
            #"queuedCommands": [str(cmd) for cmd in self._commands],
        }

    # Return queued commands as a list of Python dictionaries
    def get_teleop_commands(self) -> List[Dict[str, float]]:
        """
        Returns a list of dictionaries representing the linear and angular
        velocities for each queued DirectionCommand.
        """
        return [cmd.to_dict() for cmd in self._commands]

    # Optional: clear the command queue after processing
    def clear_commands(self) -> None:
        self._commands.clear()
        self.notifyObservers(self.toJSON())
