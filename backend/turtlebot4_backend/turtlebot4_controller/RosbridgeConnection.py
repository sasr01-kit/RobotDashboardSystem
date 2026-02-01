"""
Simple RosbridgeConnection wrapper around roslibpy.Ros for clarity and reuse.

- Keeps connection state (isConnected)
- Provides simple subscribe/publish/call_service helpers

Usage (example at bottom):
  conn = RosbridgeConnection('robot-ip', 9090)
  conn.connect()
  conn.subscribe('/battery_state', 'sensor_msgs/msg/BatteryState', callback)
  conn.publish('/some_topic', {'data': 'hi'}, msg_type='std_msgs/msg/String')
  resp = conn.call_service('/do_something', 'some_pkg/srv/SomeService', {'arg': 1})
  conn.terminate()
"""

import time
import threading
import roslibpy
from typing import Callable, Dict, Optional

class RosbridgeConnection:
    def __init__(self, host: str = 'localhost', port: int = 9090):
        # Connection parameters
        self.host = host
        self.port = port

        # roslibpy client instance (None until connect())
        self.client: Optional[roslibpy.Ros] = None

        # Simple flag other code can check
        self.isConnected: bool = False

        # Keep created Topic objects so we can reuse/unsubscribe later
        self._topics: Dict[str, roslibpy.Topic] = {}

        # Keep created Service objects if needed
        self._services: Dict[str, roslibpy.Service] = {}

    def connect(self, timeout: float = 5.0) -> None:
        """Establish connection to rosbridge websocket and wait until connected.
        Raises RuntimeError on failure to connect within timeout.
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
        """Subscribe to a topic and return the roslibpy.Topic object.

        - topic_name: ROS2 topic name (e.g. '/battery_state')
        - msg_type: ROS2 message type string as exposed by rosbridge (e.g. 'sensor_msgs/msg/BatteryState')
        - callback: function invoked with the decoded message (a Python dict)
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
        """Unsubscribe a previously subscribed callback or remove the topic entirely."""
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
        """Publish a message (dictionary) to a topic.

        - If the topic was not created before, msg_type is required to instantiate it.
        - message should be a plain Python dict matching the ROS message structure.
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
        """Call a ROS service synchronously and return the response dict.

        This method wraps roslibpy.Service.call (which is async-style) and waits
        for a response up to `timeout` seconds.
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
        """Clean up topics, services and terminate the roslibpy client."""
        # Unsubscribe and clear topics
        for name, topic in list(self._topics.items()):
            try:
                topic.unsubscribe()
            except Exception:
                pass
        self._topics.clear()

        # Close services (roslibpy.Service has no explicit terminate; just drop refs)
        self._services.clear()

        # Terminate client
        if self.client:
            try:
                self.client.terminate()
            except Exception:
                pass
            self.client = None
        self.isConnected = False


# Small example to illustrate usage (very minimal)
if __name__ == '__main__':
    def print_battery(msg):
        # msg is a dict delivered by roslibpy for sensor_msgs/msg/BatteryState
        voltage = msg.get('voltage')
        percent = msg.get('percentage')
        present = msg.get('present')
        print(f'[example] battery: voltage={voltage}, percent={percent}, present={present}')

    conn = RosbridgeConnection('localhost', 9090)
    try:
        conn.connect()
        print('Connected to rosbridge.')
        conn.subscribe('/battery_state', 'sensor_msgs/msg/BatteryState', print_battery)

        # Keep process alive to receive messages
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        conn.terminate()