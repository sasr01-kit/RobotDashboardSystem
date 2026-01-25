from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from observers import ConcreteObserver

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    observer = ConcreteObserver(websocket)

    try:
        while True:
            # Optional: receive messages from frontend
            data = await websocket.receive_text()
            print("Received from client:", data)

    except WebSocketDisconnect:
        print("Client disconnected")