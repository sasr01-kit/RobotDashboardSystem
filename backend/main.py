"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from ConcreteObserver import ConcreteObserver
from Subject import Subject
from RobotState import RobotState
from Path import Path

app = FastAPI()

robot_state = RobotState()
path = Path()
#Map to be added

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    observer = ConcreteObserver(websocket)

    # Attach observer to all subjects you want to stream
    robot_state.attach(observer)
    path.attach(observer)

    try:
        while True:
            # If your frontend sends messages, read them here
            await websocket.receive_text()

    except WebSocketDisconnect:
        # Clean up when the client disconnects
        robot_state.detach(observer)
        path.detach(observer)
"""
import asyncio
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware # avoid fetch errors

from pixelbot_backend.pixelbot_storage.DataRepository import DataRepository 
from pixelbot_backend.pixelbot_controller.ChildAPI import ChildAPI 
from pixelbot_backend.pixelbot_controller.SessionAPI import SessionAPI

app = FastAPI()

# Turtlebot mockup websocket API
# Store all connected WebSocket clients
connected_clients = set()

async def mock_robot_loop():
    battery = 100.0

    while True:
        # Simulate battery drain
        battery = max(0, battery - random.uniform(0.5, 2.0))

        # Random toggles
        is_on = random.choice([True, False])
        wifi = random.choice([True, False])
        comms = random.choice([True, False])
        rpi = random.choice([True, False])

        # Build the message
        message = {
            "type": "STATUS_UPDATE",
            "isOn": is_on,
            "batteryPercentage": round(battery, 1),
            "isWifiConnected": wifi,
            "isCommsConnected": comms,
            "isRaspberryPiConnected": rpi,
            "mode": random.choice(["IDLE", "NAVIGATING", "DOCKING"])
        }

        # Broadcast to all connected clients
        dead_clients = []
        for ws in connected_clients:
            try:
                await ws.send_json(message)
            except:
                dead_clients.append(ws)

        # Remove disconnected clients
        for ws in dead_clients:
            connected_clients.remove(ws)

        await asyncio.sleep(2)


@app.on_event("startup")
async def start_mock():
    asyncio.create_task(mock_robot_loop())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("WS ROUTE HIT")
    await websocket.accept()

    connected_clients.add(websocket)

    try:
        while True:
            await websocket.receive_text()  # ignore client messages
    except WebSocketDisconnect:
        print("Client disconnected")
        connected_clients.remove(websocket)

# Pixelbot REST API
repository = DataRepository() 
child_api = ChildAPI("C:/Users/kelly/Desktop/Uni/PSE/pse_data_example/saved_drawing", repository) 
session_api = SessionAPI(child_api) 

app.add_middleware( 
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.get("/pixelbot/children") 
def get_children(): 
    return child_api.send_children() 

@app.get("/pixelbot/children/{child_id}") 
def get_child(child_id: str): 
    child = child_api.send_child(child_id) 
    if child is None: 
        raise HTTPException(status_code=404, detail="Child not found") 
    return child 

@app.get("/pixelbot/children/{child_id}/sessions/{session_id}") 
def get_session(child_id: str, session_id: str): 
    session = session_api.send_session(child_id, session_id) 
    if session is None: 
        raise HTTPException(status_code=404, detail="Session not found") 
    return session
