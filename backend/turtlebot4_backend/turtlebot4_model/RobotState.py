
from typing import Dict, Any
from turtlebot4_backend.turtlebot4_model.Subject import Subject
from turtlebot4_backend.turtlebot4_model.Path import Path

class RobotState(Subject):
    """
    Stores live status fields for the robot and exposes them to observers.

    This model centralizes state so the UI can render battery, connectivity,
    mode, and dock status consistently.
    """

    def __init__(
        self,
        path_model: Path,
        is_on: bool = False,
        battery_percentage: float = None,
        is_wifi_connected: bool = None,
        is_comms_connected: bool = None,
        is_raspberry_pi_connected: bool = None,
    ) -> None:
        """
        Initialize robot status fields and observer support.

        This sets initial status values and links to the path model so
        derived fields like mode and docked state can be computed.

        Params:
            path_model: Path model used to derive mode and docked status.
            is_on: Initial power state of the robot.
            battery_percentage: Initial battery percent, or None if unknown.
            is_wifi_connected: Initial wifi connection state, or None if unknown.
            is_comms_connected: Initial communications link state, or None if unknown.
            is_raspberry_pi_connected: Initial Raspberry Pi link state, or None if unknown.

        Return:
            None.
        """
        super().__init__()
        self._is_on = is_on
        self._battery_percentage = battery_percentage
        self._is_wifi_connected = is_wifi_connected
        self._is_comms_connected = is_comms_connected
        self._is_raspberry_pi_connected = is_raspberry_pi_connected
        self._path_model = path_model

    # Getters
    def get_is_on(self) -> bool:
        """
        Return the current power state.

        This indicates whether the robot is reported as on.

        Params:
            None.

        Return:
            True if on, otherwise False.
        """
        return self._is_on

    def get_battery_percentage(self) -> float | None:
        """
        Return the current battery percentage.

        This provides the battery level in the 0-100 range when known.

        Params:
            None.

        Return:
            Battery percentage or None if unknown.
        """
        return self._battery_percentage

    def get_is_wifi_connected(self) -> bool | None:
        """
        Return the wifi connection state.

        This indicates whether the robot is connected to wifi.

        Params:
            None.

        Return:
            True/False if known, otherwise None.
        """
        return self._is_wifi_connected

    def get_is_comms_connected(self) -> bool | None:
        """
        Return the communications link state.

        This indicates whether the robot's comms link is healthy.

        Params:
            None.

        Return:
            True/False if known, otherwise None.
        """
        return self._is_comms_connected

    def get_is_raspberry_pi_connected(self) -> bool | None:
        """
        Return the Raspberry Pi connection state.

        This indicates whether the Pi is reachable.

        Params:
            None.

        Return:
            True/False if known, otherwise None.
        """
        return self._is_raspberry_pi_connected

    # Setters 
    async def set_is_on(self, value: bool) -> None:
        """
        Update the power state and notify observers.

        This keeps the UI in sync when the robot powers on or off.

        Params:
            value: New power state.

        Return:
            None.
        """
        if self._is_on != value:
            self._is_on = value
            await self.notify_observers({ 
                "type": "STATUS_UPDATE", 
                **self.toJSON() 
            })

    async def set_battery_percentage(self, value: float | None) -> None:
        """
        Update the battery percentage and notify observers.

        This clamps values into a safe range before publishing updates.

        Params:
            value: New battery percentage or None if unknown.

        Return:
            None.
        """
        if value is not None:
            value = max(0.0, min(100.0, value))  # clamp to [0, 100]
        if self._battery_percentage != value:
            self._battery_percentage = value
            await self.notify_observers({ 
                "type": "STATUS_UPDATE", 
                **self.toJSON() 
            })

    async def set_is_wifi_connected(self, value: bool | None) -> None:
        """
        Update wifi connection state and notify observers.

        This reports connectivity changes to the UI.

        Params:
            value: New wifi state or None if unknown.

        Return:
            None.
        """
        if self._is_wifi_connected != value:
            self._is_wifi_connected = value
            await self.notify_observers({ 
                "type": "STATUS_UPDATE", 
                **self.toJSON() 
            })

    async def set_is_comms_connected(self, value: bool | None) -> None:
        """
        Update comms link state and notify observers.

        This reports comms changes to the UI.

        Params:
            value: New comms state or None if unknown.

        Return:
            None.
        """
        if self._is_comms_connected != value:
            self._is_comms_connected = value
            await self.notify_observers({ 
                "type": "STATUS_UPDATE", 
                **self.toJSON() 
            })

    async def set_is_raspberry_pi_connected(self, value: bool | None) -> None:
        """
        Update Raspberry Pi connection state and notify observers.

        This reports Pi connectivity changes to the UI.

        Params:
            value: New Pi connection state or None if unknown.

        Return:
            None.
        """
        if self._is_raspberry_pi_connected != value:
            self._is_raspberry_pi_connected = value
            await self.notify_observers({ 
                "type": "STATUS_UPDATE", 
                **self.toJSON() 
            })
    
    async def set_mode(self) -> None:
        """
        Notify observers that the derived mode may have changed.

        Mode is based on the path module state, so no local field is set;
        observers simply re-read the computed value.

        Params:
            None.

        Return:
            None.
        """
        # Mode is derived from path module state, so we just notify observers to re-check the mode.
        await self.notify_observers({ 
            "type": "STATUS_UPDATE", 
            **self.toJSON()
        })

    async def set_docked(self) -> None:
        """
        Notify observers that the derived docked state may have changed.

        Docked status is based on the path module state, so no local field is
        set; observers simply re-read the computed value.

        Params:
            None.

        Return:
            None.
        """
        # Docked status is derived from path module state, so we just notify observers to re-check the docked status.
        await self.notify_observers({ 
            "type": "STATUS_UPDATE", 
            **self.toJSON()    
        })

    def toJSON(self) -> Dict[str, Any]:
        """
        Convert the robot state into a JSON-ready structure.

        This formats fields for frontend consumption and includes derived
        mode and dock status.

        Params:
            None.

        Return:
            Dict ready to be serialized to JSON for the frontend.
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