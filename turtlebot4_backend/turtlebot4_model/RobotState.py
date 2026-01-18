
from typing import Dict, Any
from Subject import Subject
from Path import Path

class RobotState(Subject):
    def __init__(
        self,
        is_on: bool = False,
        battery_percentage: float = 0.0,
        is_wifi_connected: bool = False,
        is_comms_connected: bool = False,
        is_raspberry_pi_connected: bool = False,
    ) -> None:
        super().__init__()
        self._is_on = is_on
        self._battery_percentage = battery_percentage
        self._is_wifi_connected = is_wifi_connected
        self._is_comms_connected = is_comms_connected
        self._is_raspberry_pi_connected = is_raspberry_pi_connected

    # Getters
    def get_is_on(self) -> bool:
        return self._is_on

    def get_battery_percentage(self) -> float:
        return self._battery_percentage

    def get_is_wifi_connected(self) -> bool:
        return self._is_wifi_connected

    def get_is_comms_connected(self) -> bool:
        return self._is_comms_connected

    def get_is_raspberry_pi_connected(self) -> bool:
        return self._is_raspberry_pi_connected

    # Setters (each notifies observers on change)
    def set_is_on(self, value: bool) -> None:
        if self._is_on != value:
            self._is_on = value
            self.notify()

    def set_battery_percentage(self, value: float) -> None:
        value = max(0.0, min(100.0, value))  # clamp to [0, 100]
        if self._battery_percentage != value:
            self._battery_percentage = value
            self.notify()

    def set_is_wifi_connected(self, value: bool) -> None:
        if self._is_wifi_connected != value:
            self._is_wifi_connected = value
            self.notify()

    def set_is_comms_connected(self, value: bool) -> None:
        if self._is_comms_connected != value:
            self._is_comms_connected = value
            self.notify()

    def set_is_raspberry_pi_connected(self, value: bool) -> None:
        if self._is_raspberry_pi_connected != value:
            self._is_raspberry_pi_connected = value
            self.notify()

    def toJSON(self) -> Dict[str, Any]:
        """
        Converts the internal state of the robot into a structured JSON
        representation suitable for external use.

        @return: A dict ready to be serialized to JSON for the frontend.
        """
        return {
            "isOn": self._is_on,
            "batteryPercentage": self._battery_percentage,
            "isWifiConnected": self._is_wifi_connected,
            "isCommsConnected": self._is_comms_connected,
            "isRaspberryPiConnected": self._is_raspberry_pi_connected,
            "mode" : Path.get_is_path_module_active(),
        }