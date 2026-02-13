from fastapi import WebSocket
from turtlebot4_backend.turtlebot4_model.Observer import Observer


class ConcreteObserver(Observer):
    """
    Observer implementation that forwards updates to a WebSocket client.

    This bridges the observer pattern to live UI connections so state changes
    can be pushed to the frontend.
    """

    def __init__(self, websocket_client: WebSocket) -> None:
        """
        Initialize the observer with a websocket target.

        This stores the client so updates can be delivered as JSON messages.

        Params:
            websocket_client: Target WebSocket used to deliver updates.

        Return:
            None.
        """
        self._client = websocket_client  # WebSocket used to push updates.

    async def update(self, source, data) -> None:
        """
        Send an update payload to the connected WebSocket client.

        This pushes model changes to the frontend in real time.

        Params:
            source: Update emitter (unused by this observer).
            data: JSON-serializable payload to send.

        Return:
            None.
        """
        await self._client.send_json(data)
