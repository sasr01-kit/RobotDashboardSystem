import asyncio
import threading
import time
from typing import Callable, List, Awaitable, Dict

from turtlebot4_backend.turtlebot4_controller.RosbridgeConnection import RosbridgeConnection
from turtlebot4_backend.turtlebot4_model.RobotState import RobotState
from turtlebot4_backend.turtlebot4_model.Subject import Subject

class StatusController:
    """
    Subscribes to robot status topics via RosbridgeConnection and updates RobotState.
    Also provides a listener API for WebSocket handlers to receive status updates.
    """
    def __init__(
        self,
        robot_state: RobotState,
        ros_host: str = 'localhost',
        ros_port: int = 9090,
        loop: asyncio.AbstractEventLoop | None = None
    ):
        self.robot_state = robot_state
        self._ros = RosbridgeConnection(host=ros_host, port=ros_port)

        # This loop is used to schedule async notifications to websocket listeners:
        self._loop = loop or asyncio.get_event_loop()
        self._listeners: List[Callable[[Dict], Awaitable[None]]] = []
        self.subscribeToStatus()

    def subscribeToStatus(self) -> None:
        """Connect to rosbridge and subscribe to status topics."""

        def _connect_and_subscribe():
            try:
                self._ros.connect()
            except Exception:
                async def _mark_off_and_notify():
                    await self.robot_state.set_is_on(False)
                    await self._notify_listeners()

                self._loop.call_soon_threadsafe(
                    lambda: asyncio.create_task(_mark_off_and_notify())
                )
                return

            async def _mark_on_and_notify():
                # Notify listeners immediately that the robot is on as the connection is established, 
                # as it means the robot is powered on and rosbridge is running. 
                # The other status fields will be updated asynchronously as their respective messages are received.
                await self.robot_state.set_is_on(True) 
                await self._notify_listeners()

            self._loop.call_soon_threadsafe(
                lambda: asyncio.create_task(_mark_on_and_notify())
            )

            # Subscribe to status topics
            for name, typ, cb in [
                ('/battery_state', 'sensor_msgs/msg/BatteryState', self._battery_cb),
                ('/wifi_state', 'std_msgs/msg/Bool', self._wifi_cb),
                ('/pi_state', 'std_msgs/msg/Bool', self._pi_cb),
                ('/comms_state', 'std_msgs/msg/Bool', self._comms_cb),
            ]:
                try:
                    self._ros.subscribe(name, typ, cb)
                except Exception:
                    pass

        threading.Thread(target=_connect_and_subscribe, daemon=True).start()

    # These callbacks are invoked by the (synchronous) ROS client in its own thread.
    # We therefore schedule the async updater on the asyncio loop in a thread-safe way.
    def _battery_cb(self, msg: dict) -> None:
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self.updateBattery(msg))
        )

    def _wifi_cb(self, msg: dict) -> None:
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self.updateWifi(msg))
        )

    def _pi_cb(self, msg: dict) -> None:
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self.updatePiConnection(msg))
        )

    def _comms_cb(self, msg: dict) -> None:
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self.updateCommsConnection(msg))
        )

    # Async updaters that modify RobotState and notify listeners upon proper value changes 
    async def updateBattery(self, msg: dict) -> None:
        batteryPercentage = None
        if isinstance(msg, dict) and 'percentage' in msg and msg['percentage'] is not None:
            try:
                batteryPercentage = float(msg['percentage'])
            except (ValueError, TypeError):
                pass

        # msg may contain 'percentage' in [0,1] or [0,100]; normalize for future proofing.
        if batteryPercentage is not None:
            if 0.0 <= batteryPercentage <= 1.0:
                batteryPercentage *= 100.0
            batteryPercentage = max(0.0, min(100.0, batteryPercentage))
            await self.robot_state.set_battery_percentage(round(batteryPercentage, 1))
            await self._notify_listeners()

    async def updateWifi(self, msg: dict) -> None:
        val = self._extract_bool_from_msg(msg)
        if val is not None:
            await self.robot_state.set_is_wifi_connected(val)
            await self._notify_listeners()

    async def updatePiConnection(self, msg: dict) -> None:
        val = self._extract_bool_from_msg(msg)
        if val is not None:
            await self.robot_state.set_is_raspberry_pi_connected(val)
            await self._notify_listeners()

    async def updateCommsConnection(self, msg: dict) -> None:
        val = self._extract_bool_from_msg(msg)
        if val is not None:
            await self.robot_state.set_is_comms_connected(val)
            await self._notify_listeners()

    # helper to pull boolean out of std_msgs/Bool-like or dict {'data': True}
    def _extract_bool_from_msg(self, msg: dict) -> bool | None:
        if msg is None:
            return None
        if isinstance(msg, bool):
            return msg
        if isinstance(msg, dict):
            if 'data' in msg:
                return bool(msg['data'])
            if 'value' in msg:
                return bool(msg['value'])
        return None

    # Listener API for WebSocket handlers: attach an async callback(msg_dict)
    def attach_listener(self, cb: Callable[[Dict], Awaitable[None]]) -> Callable[[], None]:
        self._listeners.append(cb)

        def detach():
            try:
                self._listeners.remove(cb)
            except ValueError:
                pass

        return detach

    async def _notify_listeners(self) -> None:
        for listener in list(self._listeners):
            try:
                await listener(self.robot_state.toJSON())
            except Exception:
                pass

    def stop(self) -> None:
        try:
            self._ros.terminate()
        except Exception:
            pass