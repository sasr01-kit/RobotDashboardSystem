from typing import List, Dict, Any

class Teleoperate:
    """
    Stores teleoperation commands and notifies listeners.

    This keeps a queue of drive commands from the UI and alerts controllers so
    they can publish commands to the robot.
    """
    def __init__(self):
        """
        Initialize the command queue and observer list.

        This prepares the model to accept commands and to notify controllers
        whenever a new command arrives.

        Params:
            None.

        Return:
            None.
        """
        self._commands = []
        # Teleoperate needs to notify the controller when a new command is added, so it can publish to ROSBridge.
        # Thus it needs its own list of observers (the controller) and a notify mechanism. 
        self._observers = [] 

    # Observer pattern methods for notifying controller of new commands
    def attach(self, callback):
        """
        Register a callback to receive command notifications.

        This allows controllers to react immediately when a new command is queued.

        Params:
            callback: Function invoked when a command is added.

        Return:
            None.
        """
        if callback not in self._observers:
            self._observers.append(callback)

    def detach(self, callback):
        """
        Remove a previously registered callback.

        This stops a controller from receiving further notifications.

        Params:
            callback: Function to remove.

        Return:
            None.
        """
        if callback in self._observers:
            self._observers.remove(callback)

    def notify(self):
        """
        Notify all observers that a new command is available.

        This triggers synchronous callbacks so controllers can publish promptly.

        Params:
            None.

        Return:
            None.
        """
        for cb in list(self._observers):
            cb(self, None)   # synchronous callback

    def add_command(self, command: str):
        """
        Add a new command to the queue and notify observers.

        This queues commands in order; STOP clears the queue to prioritize a halt.

        Params:
            command: Drive command string (e.g., FORWARD, LEFT, STOP).

        Return:
            None.
        """
        if command == "STOP":
            self._commands.clear() # ensures that once a stop command is appended, the entire queue is cleared, and the robot instantly comes to a halt.
            self._commands.append(command)
        else:
            self._commands.append(command)

        self.notify()

    def get_command(self):
        """
        Pop the next command from the queue.

        This allows controllers to fetch commands in FIFO order.

        Params:
            None.

        Return:
            The next command string, or None if no commands are queued.
        """
        if not self._commands:
            return None
        return self._commands.pop(0)

    def fromJSON(self, msg):
        """
        Load a command from a JSON-style message.

        This accepts a frontend payload and queues the command if present.

        Params:
            msg: Dict that may contain a "command" field.

        Return:
            None.
        """
        if "command" in msg:
            self.add_command(msg["command"])
