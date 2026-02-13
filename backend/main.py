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
from turtlebot4_backend.turtlebot4_model.Map import Map
from turtlebot4_backend.turtlebot4_controller.MapController import MapController
from turtlebot4_backend.turtlebot4_model.Path import Path
from turtlebot4_backend.turtlebot4_controller.PathController import PathController

from pixelbot_backend.pixelbot_storage.DataRepository import DataRepository 
from pixelbot_backend.pixelbot_controller.ChildAPI import ChildAPI 
from pixelbot_backend.pixelbot_controller.SessionAPI import SessionAPI
from pixelbot_backend.pixelbot_controller.GlobalMetricsAPI import GlobalMetricsAPI

# Main FastAPI application for the dashboard backend
app = FastAPI()

# Store all connected WebSocket clients
connected_clients = set()

# Initialize models and controllers
teleoperate = Teleoperate()
teleop_controller = TeleopController(teleoperate)
map_model = Map()
map_controller = MapController(map_model)
path_model = Path()
path_controller = PathController(path_model, map_model)
robot_state = RobotState(path_model) 
status_controller = StatusController(robot_state)

# WebSocket endpoint for real-time communication with the turtlebot4 dashboard
@app.websocket("/ws") 
async def websocket_endpoint(websocket: WebSocket): 
    await websocket.accept() 
    
    # Create and attach observer for this client
    observer = ConcreteObserver(websocket) 
    robot_state.attach(observer) 
    map_model.attach(observer)
    map_controller._send_initial_map_png()
    path_model.attach(observer)
    path_model.set_path_controller(path_controller)

    # Listen for incoming messages from the client and handle commands
    try: 
        while True: 
            raw = await websocket.receive_text() 
            msg = json.loads(raw) 
            print(f"[WS] Parsed JSON: {msg}")
        
            if "command" in msg: 
                teleoperate.fromJSON(msg) 

            if "isPathModuleActive" in msg:
                await path_model.fromJSON(msg)
                await robot_state.set_mode()
          

            if "dockStatus" in msg:
                await path_model.fromJSON(msg)
                await robot_state.set_docked()

            if msg.get("type") == "GOAL_FEEDBACK":
                await path_model.apply_feedback(msg)


    except WebSocketDisconnect: 
        robot_state.detach(observer)
        map_model.detach(observer)
        path_model.detach(observer)

# Pixelbot REST API
repository = DataRepository() 
# Ane's local data path: "C:/Users/aneca/OneDrive/Uni/pse_data_example/saved_drawing"
# Use your local data path here. If using Pixelbot robot connection, use the path to the robot instead.
# Pixelbot path: "http://192.168.2.70:8000"
child_api = ChildAPI("/mnt/c/Users/kelly/Desktop/Uni/PSE/pse_data_example/saved_drawing", repository) 
global_metrics_api = GlobalMetricsAPI(child_api)
session_api = SessionAPI(child_api) 

# CORS middleware to allow frontend to access REST API without CORS errors
app.add_middleware( 
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# REST API endpoints for Pixelbot data retrieval
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
