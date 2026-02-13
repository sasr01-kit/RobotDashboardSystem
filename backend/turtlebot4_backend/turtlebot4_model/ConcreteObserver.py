from fastapi import WebSocket
from turtlebot4_backend.turtlebot4_model.Observer import Observer


class ConcreteObserver(Observer):
    """Implementation of the Observer interface from Observer Pattern that forwards updates to a WebSocket client."""

    def __init__(self, websocket_client: WebSocket) -> None:
        """Initialize the observer.

        Params:
            websocket_client: Target WebSocket used to deliver updates.
        Returns:
            None
        """
        self._client = websocket_client

    async def update(self, source, data) -> None:
        """Send an update payload to the connected WebSocket client.

        Params:
            source: Update emitter (unused by this observer).
            data: JSON-serializable payload to send.
        Returns:
            None
        """
        await self._client.send_json(data)
