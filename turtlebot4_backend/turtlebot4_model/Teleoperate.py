# Teleoperate.py
from typing import List, Dict, Any
from turtlebot4_model.Subject import Subject
from DirectionCommand import DirectionCommand
from geometry_msgs.msg import Twist  # ROS Twist message


class Teleoperate(Subject):
    def __init__(self) -> None:
        super().__init__()
        self._commands: List[DirectionCommand] = []

    # Getter
    def get_commands(self) -> List[DirectionCommand]:
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
    def fromJSON(self, msg: Dict[str, Any]) -> None:
        """
        Parses teleoperation input from the frontend.
        Example msg format:
        { "commands": ["FORWARD", "LEFT"] }
        """
        command_strs = msg.get("commands", [])
        for cmd_str in command_strs:
            try:
                # Convert string to DirectionCommand enum
                command = DirectionCommand[cmd_str.upper()]
                self.add_command(command)
            except KeyError:
                # Invalid command; ignore or log warning
                print(f"Warning: Invalid teleop command received: {cmd_str}")

    # Serialize commands to JSON for frontend confirmation
    def toJSON(self) -> Dict[str, Any]:
        """
        Returns JSON indicating teleoperation state and queued commands.
        """
        return {
            "teleoperationActive": len(self._commands) > 0,
            "queuedCommands": [str(cmd) for cmd in self._commands],
        }

    # Convert queued commands into Twist messages
    def get_twist_messages(self) -> List[Twist]:
        """
        Returns a list of ROS Twist messages for all queued commands.
        """
        return [cmd.to_twist() for cmd in self._commands]

    # Optional: clear the command queue after sending to the robot
    def clear_commands(self) -> None:
        self._commands.clear()
        self.notifyObservers(self.toJSON())
