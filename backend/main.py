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
from fastapi.middleware.cors import CORSMiddleware # avoid fetch errors in REST API
import json

from turtlebot4_backend.turtlebot4_model.RobotState import RobotState
from turtlebot4_backend.turtlebot4_controller.StatusController import StatusController
from turtlebot4_backend.turtlebot4_model.ConcreteObserver import ConcreteObserver
from turtlebot4_backend.turtlebot4_model.Teleoperate import Teleoperate
from turtlebot4_backend.turtlebot4_controller.TeleopController import TeleopController

from pixelbot_backend.pixelbot_storage.DataRepository import DataRepository 
from pixelbot_backend.pixelbot_controller.ChildAPI import ChildAPI 
from pixelbot_backend.pixelbot_controller.SessionAPI import SessionAPI
from pixelbot_backend.pixelbot_controller.GlobalMetricsAPI import GlobalMetricsAPI

app = FastAPI()

# Turtlebot mockup websocket API
# Store all connected WebSocket clients
connected_clients = set()

robot_state = RobotState() 
status_controller = StatusController(robot_state)
teleoperate = Teleoperate()
teleop_controller = TeleopController(teleoperate)

@app.on_event("startup") 
async def startup_event(): 
    status_controller.subscribeToStatus()


@app.websocket("/ws") 
async def websocket_endpoint(websocket: WebSocket): 
    await websocket.accept() 
    
    observer = ConcreteObserver(websocket) 
    robot_state.attach(observer) 

    try: 
        while True: 
            raw = await websocket.receive_text() 
            msg = json.loads(raw) 
            print(f"[WS] Parsed JSON: {msg}")
        
            # Route teleoperate messages 
            if "command" in msg: 
                teleoperate.fromJSON(msg) 

    except WebSocketDisconnect: 
        robot_state.detach(observer)


# Pixelbot REST API
repository = DataRepository() 
# Use your local data path here. If using Pixelbot robot connection, use the path to the robot instead.
# Pixelbot path: "http://192.168.2.70:8000"
child_api = ChildAPI("/mnt/c/Users/kelly/Desktop/Uni/PSE/pse_data_example/saved_drawing", repository) 
global_metrics_api = GlobalMetricsAPI(child_api)
session_api = SessionAPI(child_api) 

app.add_middleware( 
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.get("/pixelbot/summary")
def get_pixelbot_summary(): 
    return global_metrics_api.send_global_metrics_summary()

@app.get("/pixelbot/children/{child_id}/recap")
def get_recap(child_id: str):
    return global_metrics_api.send_child_recap(child_id)

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
