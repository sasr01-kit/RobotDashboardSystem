from typing import List, Dict, Any

class Teleoperate:
    def __init__(self):
        self._commands = []
        # Teleoperate needs to notify the controller when a new command is added, so it can publish to ROSBridge.
        # Thus it needs its own list of observers (the controller) and a notify mechanism. 
        self._observers = [] 

    # Observer pattern methods for notifying controller of new commands
    def attach(self, callback):
        if callback not in self._observers:
            self._observers.append(callback)

    def detach(self, callback):
        if callback in self._observers:
            self._observers.remove(callback)

    def notify(self):
        for cb in list(self._observers):
            cb(self, None)   # synchronous callback

    def add_command(self, command: str):
        if command == "STOP":
            self._commands.clear()
            self._commands.append(command)
        else:
            self._commands.append(command)

        self.notify()

    def get_command(self):
        if not self._commands:
            return None
        return self._commands.pop(0)

    def fromJSON(self, msg):
        if "command" in msg:
            self.add_command(msg["command"])
