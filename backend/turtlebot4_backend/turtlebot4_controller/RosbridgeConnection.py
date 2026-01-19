"""
RosbridgeConnection
A small helper class to manage a roslibpy WebSocket connection to rosbridge,
with convenient subscribe / publish / service-call helpers.

Usage (example):
    conn = RosbridgeConnection(host='localhost', port=9090)
    conn.connect(timeout=10.0)

    # subscribe
    def scan_cb(msg):
        print('scan msg:', msg.get('ranges', [])[:5])
    sub = conn.subscribe('/scan', 'sensor_msgs/LaserScan', scan_cb)

    # publish (accepts either a dict or a roslibpy.Message)
    conn.publish('/cmd_vel', {'linear': {'x': 0.1, 'y': 0.0, 'z': 0.0},
                              'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}})

    # call a service (roslibpy.Service instance)
    # service = roslibpy.Service(conn.client, '/some_service', 'pkg/ServiceType')
    # req = roslibpy.ServiceRequest({...})
    # resp = conn.call_service(service, req, timeout=5.0)

    # when finished:
    conn.disconnect()
"""
from typing import Callable, Dict, Any, Optional
import threading
import time

import roslibpy


class RosbridgeConnection:
    def __init__(self, host: str = 'localhost', port: int = 9090):
        self.host: str = host
        self.port: int = port
        self.client: Optional[roslibpy.Ros] = None
        self.isConnected: bool = False

        # internal maps for reuse / cleanup
        self._topics: Dict[str, roslibpy.Topic] = {}
        self._topic_cbs: Dict[str, Callable[[Dict[str, Any]], None]] = {}
        self._lock = threading.Lock()

    def connect(self, timeout: float = 5.0) -> None:
        """
        Establish connection to rosbridge. Blocks until connected or timeout.
        Raises TimeoutError on failure.
        """
        if self.client is not None:
            # already created a client; if connected just return
            if self.isConnected:
                return
            # otherwise terminate and recreate
            try:
                self.client.terminate()
            except Exception:
                pass
            self.client = None

        self.client = roslibpy.Ros(host=self.host, port=self.port)

        # Start the roslibpy client run loop in a daemon thread.
        # roslibpy.Ros.run() manages the WebSocket event loop.
        t = threading.Thread(target=self.client.run, name='roslibpy-run', daemon=True)
        t.start()

        # wait for connection
        deadline = time.time() + timeout
        while time.time() < deadline:
            if getattr(self.client, 'is_connected', False):
                self.isConnected = True
                # optional: attach listeners (best-effort, roslibpy supports these)
                try:
                    self.client.on_close(self._on_close)
                    self.client.on_error(self._on_error)
                except Exception:
                    # older/newer versions may not have these helpers; ignore
                    pass
                return
            time.sleep(0.1)

        # timed out
        raise TimeoutError(f'Could not connect to rosbridge at {self.host}:{self.port} within {timeout}s')

    def _on_close(self, *args, **kwargs):
        # internal handler: mark disconnected
        self.isConnected = False

    def _on_error(self, *args, **kwargs):
        # internal handler: mark disconnected (roslibpy may call this on error)
        self.isConnected = False

    def subscribe(self, topic_name: str, msg_type: str, callback: Callable[[Dict[str, Any]], None]):
        """
        Subscribe to a topic. msg_type should be the ROS message type string, e.g. 'sensor_msgs/LaserScan'.

        Returns the roslibpy.Topic object so the caller can call .unsubscribe() if desired.
        """
        if not self.client or not self.isConnected:
            raise RuntimeError('Not connected to rosbridge; call connect() first')

        with self._lock:
            if topic_name in self._topics:
                topic = self._topics[topic_name]
            else:
                topic = roslibpy.Topic(self.client, topic_name, msg_type)
                self._topics[topic_name] = topic

            # roslibpy passes the received message (a dict) to the callback
            topic.subscribe(callback)
            self._topic_cbs[topic_name] = callback

        return topic

    def unsubscribe(self, topic_name: str):
        """
        Unsubscribe if previously subscribed via subscribe().
        """
        with self._lock:
            topic = self._topics.get(topic_name)
            cb = self._topic_cbs.get(topic_name)
            if topic and cb:
                try:
                    topic.unsubscribe(cb)
                except Exception:
                    # fallback to calling unsubscribe without cb (some versions)
                    try:
                        topic.unsubscribe()
                    except Exception:
                        pass
                finally:
                    del self._topic_cbs[topic_name]
                    # optionally, keep topic object for reuse; remove to free memory:
                    del self._topics[topic_name]

    def publish(self, topic_name: str, message: Any, msg_type: Optional[str] = None) -> None:
        """
        Publish a message. message can be a roslibpy.Message or a plain dict.
        If the topic hasn't been created previously, msg_type is required to create it the first time.
        """
        if not self.client or not self.isConnected:
            raise RuntimeError('Not connected to rosbridge; call connect() first')

        with self._lock:
            topic = self._topics.get(topic_name)
            if topic is None:
                if msg_type is None:
                    raise ValueError('msg_type is required for first-time publish to a topic')
                topic = roslibpy.Topic(self.client, topic_name, msg_type)
                self._topics[topic_name] = topic

        # prepare payload
        if isinstance(message, roslibpy.Message):
            payload = message
        elif isinstance(message, dict):
            payload = roslibpy.Message(message)
        else:
            # allow objects that are convertible to dict (not strictly necessary)
            try:
                payload = roslibpy.Message(dict(message))
            except Exception:
                raise TypeError('message must be a roslibpy.Message or a dict-like object')

        topic.publish(payload)

    def call_service(self, service: roslibpy.Service, request: roslibpy.ServiceRequest, timeout: float = 5.0) -> Dict[str, Any]:
        """
        Call a roslibpy.Service and block until response or timeout.
        Returns the response (a dict). Raises TimeoutError on timeout, or Exception on service error.
        """
        if not self.client or not self.isConnected:
            raise RuntimeError('Not connected to rosbridge; call connect() first')

        done = threading.Event()
        result: Dict[str, Any] = {}
        error: Optional[Exception] = None

        def cb(res):
            nonlocal result
            result = res
            done.set()

        def eb(err):
            nonlocal error
            # roslibpy passes error details as a string or dict
            error = Exception(f'service call error: {err}')
            done.set()

        # roslibpy.Service.call accepts callback and errback keyword args
        try:
            service.call(request, callback=cb, errback=eb)
        except TypeError:
            # fallback for older versions (positional)
            try:
                service.call(request, cb, eb)
            except Exception as e:
                raise

        if not done.wait(timeout):
            raise TimeoutError('Service call timed out after {:.1f}s'.format(timeout))

        if error is not None:
            raise error

        return result

    def disconnect(self) -> None:
        """
        Cleanly disconnect from rosbridge and unsubscribe all topics.
        """
        with self._lock:
            for topic_name, cb in list(self._topic_cbs.items()):
                topic = self._topics.get(topic_name)
                if topic:
                    try:
                        topic.unsubscribe(cb)
                    except Exception:
                        try:
                            topic.unsubscribe()
                        except Exception:
                            pass
            self._topic_cbs.clear()
            self._topics.clear()

        if self.client:
            try:
                # terminate stops the run loop and closes the websocket
                self.client.terminate()
            except Exception:
                pass
            finally:
                self.client = None
                self.isConnected = False


if __name__ == '__main__':
    # Quick demo when run as a script (connects to localhost:9090)
    conn = RosbridgeConnection('localhost', 9090)
    try:
        conn.connect(timeout=10.0)
        print('Connected:', conn.isConnected)

        # subscribe to scan (print first 5 ranges)
        def scan_cb(msg):
            ranges = msg.get('ranges', [])
            print('scan sample:', ranges[:5])

        conn.subscribe('/scan', 'sensor_msgs/LaserScan', scan_cb)

        # publish a short cmd_vel (must have msg type if not published before)
        import time
        time.sleep(1.0)
        conn.publish('/cmd_vel', {'linear': {'x': 0.1, 'y': 0.0, 'z': 0.0},
                                  'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}},
                     msg_type='geometry_msgs/Twist')
        time.sleep(1.0)

    finally:
        conn.disconnect()
        print('Disconnected')