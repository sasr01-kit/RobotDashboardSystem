import time
import threading
import roslibpy
from typing import Callable, Dict, Optional

class RosbridgeConnection:
    """
    Simple RosbridgeConnection wrapper around roslibpy.Ros for clarity and reuse.

    - Keeps connection state (isConnected)
    - Provides simple subscribe/publish/call_service helpers
    """
    def __init__(self, host: str = 'localhost', port: int = 9090):
        """
        Initialize connection settings and internal caches.

        This sets up the object with host/port and empty caches so later calls
        can reuse topics/services and manage connection state safely.

        Params:
            host: Hostname for the rosbridge websocket server.
            port: Port for the rosbridge websocket server.

        Return:
            None.
        """
        # Connection parameters.
        self.host = host
        self.port = port

        # roslibpy client instance (None until connect()).
        self.client: Optional[roslibpy.Ros] = None
        self.isConnected: bool = False

        # Keep created Topic objects so they can be reused/unsubscribed later.
        self._topics: Dict[str, roslibpy.Topic] = {}

        # Keep created Service objects if needed.
        self._services: Dict[str, roslibpy.Service] = {}

    def connect(self, timeout: float = 5.0) -> None:
        """
        Connect to rosbridge and wait until the socket is ready.

        This ensures the websocket is usable before any subscribe/publish call
        and fails fast if the server is unreachable.

        Params:
            timeout: Seconds to wait before raising an error.

        Return:
            None.
        """
        if self.client:
            return  # already created

        self.client = roslibpy.Ros(host=self.host, port=self.port)
        self.client.run()

        # Wait until roslibpy reports connected or timeout
        start = time.time()
        while not getattr(self.client, 'is_connected', False):
            if time.time() - start > timeout:
                raise RuntimeError(f'Could not connect to rosbridge at {self.host}:{self.port}')
            time.sleep(0.05)

        self.isConnected = True

    def subscribe(self, topic_name: str, msg_type: str, callback: Callable[[dict], None]) -> roslibpy.Topic:
        """
        Subscribe to a ROS topic and return the Topic object.

        This registers a callback for incoming messages and caches the topic
        so future calls can reuse it.

        Params:
            topic_name: ROS2 topic name (e.g. '/battery_state').
            msg_type: ROS2 message type string (e.g. 'sensor_msgs/msg/BatteryState').
            callback: Function invoked with the decoded message dict.

        Return:
            The roslibpy.Topic instance used for the subscription.
        """
        if not self.client or not self.isConnected:
            raise RuntimeError('Not connected. Call connect() first.')

        # Reuse existing Topic if previously created
        if topic_name in self._topics:
            topic = self._topics[topic_name]
        else:
            topic = roslibpy.Topic(self.client, topic_name, msg_type)
            self._topics[topic_name] = topic

        topic.subscribe(callback)
        return topic

    def unsubscribe(self, topic_name: str, callback: Optional[Callable] = None) -> None:
        """
        Unsubscribe from a topic or from a specific callback.

        This frees resources and stops message delivery when a subscription is
        no longer needed.

        Params:
            topic_name: ROS2 topic name to unsubscribe from.
            callback: Optional callback to remove; if omitted, unsubscribes all.

        Return:
            None.
        """
        topic = self._topics.get(topic_name)
        if not topic:
            return
        if callback:
            try:
                topic.unsubscribe(callback)
            except Exception:
                pass
        else:
            try:
                topic.unsubscribe()
            except Exception:
                pass

    def publish(self, topic_name: str, message: dict, msg_type: Optional[str] = None) -> None:
        """
        Publish a message dict to a ROS topic.

        This sends outbound data to ROS and creates the topic on first use if
        needed.

        Params:
            topic_name: ROS2 topic name to publish to.
            message: Plain dict matching the ROS message structure.
            msg_type: ROS2 message type required on first publish to a topic.

        Return:
            None.
        """
        if not self.client or not self.isConnected:
            raise RuntimeError('Not connected. Call connect() first.')

        topic = self._topics.get(topic_name)
        if topic is None:
            if msg_type is None:
                raise ValueError('msg_type is required for first publish to a new topic')
            topic = roslibpy.Topic(self.client, topic_name, msg_type)
            self._topics[topic_name] = topic

        topic.publish(roslibpy.Message(message))

    def call_service(self, service_name: str, service_type: str, request: dict, timeout: float = 5.0) -> dict:
        """
        Call a ROS service and wait for a response.

        This wraps the async-style service call and blocks until a response
        arrives or the timeout is reached.

        Params:
            service_name: ROS service name to call.
            service_type: ROS service type string.
            request: Request payload as a plain dict.
            timeout: Seconds to wait before raising an error.

        Return:
            Response payload as a dict.
        """
        if not self.client or not self.isConnected:
            raise RuntimeError('Not connected. Call connect() first.')

        # Reuse or create service object
        service = self._services.get(service_name)
        if service is None:
            service = roslibpy.Service(self.client, service_name, service_type)
            self._services[service_name] = service

        service_request = roslibpy.ServiceRequest(request)

        result_container = {}
        done = threading.Event()
        error_container = {}

        def _on_response(resp):
            result_container['response'] = resp
            done.set()

        def _on_error(err):
            error_container['error'] = err
            done.set()

        # Call and wait
        service.call(service_request, callback=_on_response, error_callback=_on_error)
        if not done.wait(timeout):
            raise TimeoutError(f'Service {service_name} did not respond within {timeout} seconds')

        if 'error' in error_container:
            raise RuntimeError(f'Service call error: {error_container["error"]}')

        return result_container.get('response', {})

    def terminate(self) -> None:
        """
        Clean up topics and services and close the websocket client.

        This ensures subscriptions are removed and the underlying connection
        is shut down cleanly.

        Params:
            None.

        Return:
            None.
        """
        # Unsubscribe and clear topics
        for name, topic in list(self._topics.items()):
            try:
                topic.unsubscribe()
            except Exception:
                pass
        self._topics.clear()

        # Close services
        self._services.clear()

        # Terminate client
        if self.client:
            try:
                self.client.terminate()
            except Exception:
                pass
            self.client = None
        self.isConnected = False