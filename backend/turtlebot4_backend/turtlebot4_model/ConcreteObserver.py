# ConcreteObserver.py
from Observer import Observer

class ConcreteObserver(Observer):
    def __init__(self, websocket_client: WebSocket) -> None:
        self._client = websocket_client

    async def update(self, source, data) -> None:
        await self._client.send_json({
            "source": source.__class__.__name__,
            "payload": data
        })
