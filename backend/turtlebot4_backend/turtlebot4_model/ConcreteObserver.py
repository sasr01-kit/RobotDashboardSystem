from fastapi import WebSocket
from turtlebot4_backend.turtlebot4_model.Observer import Observer

# ConcreteObserver implements the Observer interface and sends updates to a WebSocket client.
class ConcreteObserver(Observer):
    def __init__(self, websocket_client: WebSocket) -> None:
        self._client = websocket_client

    async def update(self, source, data) -> None:
        await self._client.send_json(data)
