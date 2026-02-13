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
        """
        Initialize status tracking and start subscriptions.

        This sets up rosbridge access, keeps shared state, and begins listening
        for status updates so the UI can react immediately.

        Params:
            robot_state: Shared state model updated by incoming status messages.
            ros_host: Hostname for the rosbridge websocket server.
            ros_port: Port for the rosbridge websocket server.
            loop: Optional asyncio loop for scheduling async notifications.

        Return:
            None.
        """
        self.robot_state = robot_state
        self._ros = RosbridgeConnection(host=ros_host, port=ros_port)

        # This loop is used to schedule async notifications to websocket listeners:
        self._loop = loop or asyncio.get_event_loop()
        self._listeners: List[Callable[[Dict], Awaitable[None]]] = []
        self.subscribeToStatus()

    def subscribeToStatus(self) -> None:
        """
        Connect to rosbridge and subscribe to status topics.

        This runs connection/subscription in a background thread so the caller
        is not blocked during startup.

        Params:
            None.

        Return:
            None.
        """

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
                # Connection implies robot and rosbridge are online.
                # Other fields update as their messages arrive.
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
        """
        Bridge battery messages into the async updater.

        The ROS client calls this synchronously, so we schedule the async
        handler on the event loop.

        Params:
            msg: Decoded ROS message dict for battery state.

        Return:
            None.
        """
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self.updateBattery(msg))
        )

    def _wifi_cb(self, msg: dict) -> None:
        """
        Bridge wifi messages into the async updater.

        This schedules the async handler so it runs on the event loop.

        Params:
            msg: Decoded ROS message dict for wifi state.

        Return:
            None.
        """
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self.updateWifi(msg))
        )

    def _pi_cb(self, msg: dict) -> None:
        """
        Bridge Raspberry Pi messages into the async updater.

        This schedules the async handler so it runs on the event loop.

        Params:
            msg: Decoded ROS message dict for Pi connection state.

        Return:
            None.
        """
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self.updatePiConnection(msg))
        )

    def _comms_cb(self, msg: dict) -> None:
        """
        Bridge comms messages into the async updater.

        This schedules the async handler so it runs on the event loop.

        Params:
            msg: Decoded ROS message dict for communications state.

        Return:
            None.
        """
        self._loop.call_soon_threadsafe(
            lambda: asyncio.create_task(self.updateCommsConnection(msg))
        )

    # Async updaters that modify RobotState and notify listeners upon proper value changes 
    async def updateBattery(self, msg: dict) -> None:
        """
        Update the battery percentage in RobotState.

        This normalizes input to 0-100 and notifies listeners when a valid
        value is received.

        Params:
            msg: Decoded ROS message dict for battery state.

        Return:
            None.
        """
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
        """
        Update wifi connectivity state in RobotState.

        This extracts a boolean and notifies listeners when a valid value is
        received.

        Params:
            msg: Decoded ROS message dict for wifi state.

        Return:
            None.
        """
        val = self._extract_bool_from_msg(msg)
        if val is not None:
            await self.robot_state.set_is_wifi_connected(val)
            await self._notify_listeners()

    async def updatePiConnection(self, msg: dict) -> None:
        """
        Update Raspberry Pi connectivity state in RobotState.

        This extracts a boolean and notifies listeners when a valid value is
        received.

        Params:
            msg: Decoded ROS message dict for Pi connection state.

        Return:
            None.
        """
        val = self._extract_bool_from_msg(msg)
        if val is not None:
            await self.robot_state.set_is_raspberry_pi_connected(val)
            await self._notify_listeners()

    async def updateCommsConnection(self, msg: dict) -> None:
        """
        Update communications connectivity state in RobotState.

        This extracts a boolean and notifies listeners when a valid value is
        received.

        Params:
            msg: Decoded ROS message dict for communications state.

        Return:
            None.
        """
        val = self._extract_bool_from_msg(msg)
        if val is not None:
            await self.robot_state.set_is_comms_connected(val)
            await self._notify_listeners()

    # helper to pull boolean out of std_msgs/Bool-like or dict {'data': True}
    def _extract_bool_from_msg(self, msg: dict) -> bool | None:
        """
        Extract a boolean value from common ROS message shapes.

        This handles bools directly and dicts that wrap the value under keys
        like 'data' or 'value'.

        Params:
            msg: Decoded ROS message dict or primitive value.

        Return:
            True/False when a value is present, otherwise None.
        """
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
        """
        Register a websocket listener for status updates.

        This lets UI handlers receive RobotState changes as they happen and
        returns a function to detach the listener later.

        Params:
            cb: Async callback that accepts a status dict.

        Return:
            A function that removes the callback when called.
        """
        self._listeners.append(cb)

        def detach():
            try:
                self._listeners.remove(cb)
            except ValueError:
                pass

        return detach

    async def _notify_listeners(self) -> None:
        """
        Notify all registered listeners with the latest RobotState.

        This pushes state updates to each listener and ignores per-listener
        errors to avoid blocking others.

        Params:
            None.

        Return:
            None.
        """
        for listener in list(self._listeners):
            try:
                await listener(self.robot_state.toJSON())
            except Exception:
                pass

    def stop(self) -> None:
        """
        Terminate the rosbridge connection.

        This stops incoming status messages and releases websocket resources.

        Params:
            None.

        Return:
            None.
        """
        try:
            self._ros.terminate()
        except Exception:
            pass