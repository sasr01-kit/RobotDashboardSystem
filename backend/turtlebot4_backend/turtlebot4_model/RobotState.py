
from typing import Dict, Any
from turtlebot4_backend.turtlebot4_model.Subject import Subject
from turtlebot4_backend.turtlebot4_model.Path import Path

class RobotState(Subject):

    def __init__(
        self,
        path_model: Path,
        is_on: bool = False,
        battery_percentage: float = None,
        is_wifi_connected: bool = None,
        is_comms_connected: bool = None,
        is_raspberry_pi_connected: bool = None,
    ) -> None:
        super().__init__()
        self._is_on = is_on
        self._battery_percentage = battery_percentage
        self._is_wifi_connected = is_wifi_connected
        self._is_comms_connected = is_comms_connected
        self._is_raspberry_pi_connected = is_raspberry_pi_connected
        self._path_model = path_model
    # Getters
    def get_is_on(self) -> bool:
        return self._is_on

    def get_battery_percentage(self) -> float | None:
        return self._battery_percentage

    def get_is_wifi_connected(self) -> bool | None:
        return self._is_wifi_connected

    def get_is_comms_connected(self) -> bool | None:
        return self._is_comms_connected

    def get_is_raspberry_pi_connected(self) -> bool | None:
        return self._is_raspberry_pi_connected

    # Setters (each notifies observers on change)
    async def set_is_on(self, value: bool) -> None:
        if self._is_on != value:
            self._is_on = value
            await self.notify_observers({ 
                "type": "STATUS_UPDATE", 
                **self.toJSON() 
            })

    async def set_battery_percentage(self, value: float | None) -> None:
        if value is not None:
            value = max(0.0, min(100.0, value))  # clamp to [0, 100]
        if self._battery_percentage != value:
            self._battery_percentage = value
            await self.notify_observers({ 
                "type": "STATUS_UPDATE", 
                **self.toJSON() 
            })

    async def set_is_wifi_connected(self, value: bool | None) -> None:
        if self._is_wifi_connected != value:
            self._is_wifi_connected = value
            await self.notify_observers({ 
                "type": "STATUS_UPDATE", 
                **self.toJSON() 
            })

    async def set_is_comms_connected(self, value: bool | None) -> None:
        if self._is_comms_connected != value:
            self._is_comms_connected = value
            await self.notify_observers({ 
                "type": "STATUS_UPDATE", 
                **self.toJSON() 
            })

    async def set_is_raspberry_pi_connected(self, value: bool | None) -> None:
        if self._is_raspberry_pi_connected != value:
            self._is_raspberry_pi_connected = value
            await self.notify_observers({ 
                "type": "STATUS_UPDATE", 
                **self.toJSON() 
            })
    
    async def set_mode(self) -> None:
        # Mode is derived from path module state, so we just notify observers to re-check the mode
        await self.notify_observers({ 
            "type": "STATUS_UPDATE", 
            **self.toJSON()
        })

    async def set_docked(self) -> None:
        # Docked status is derived from path module state, so we just notify observers to re-check the docked status
        await self.notify_observers({ 
            "type": "STATUS_UPDATE", 
            **self.toJSON()    
        })

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
            "mode": (
                "Running Path Module" if self._path_model and self._path_model.get_is_path_module_active()
                else "Teleoperating"
            ),
            "isDocked": self._path_model.get_is_docked() if self._path_model else None
        }