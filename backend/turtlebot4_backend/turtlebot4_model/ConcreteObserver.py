# ConcreteObserver.py
from Observer import Observer


class ConcreteObserver(Observer):
    def __init__(self, websocket_client) -> None:
        """
        @param websocket_client: Communication layer used to push data
                                 to the frontend (e.g., a WebSocket).
        """
        self._client = websocket_client

    def update(self, source, data) -> None:
        """
        Forwards updated model data to the frontend.

        @param source: The subject that triggered the update.
        @param data: A JSON-like dict containing the updated state.
        """
        # Example: send serialized JSON to the frontend
        self._client.send_json({
            "source": source.__class__.__name__,
            "payload": data
        })
