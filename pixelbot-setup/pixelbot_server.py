from fastapi import FastAPI
from fastapi.responses import FileResponse
import os

app = FastAPI()

#If the files containing the children's session information are located in another directory, change the data_root.
DATA_ROOT = "/home/pixelbot/pse_data_example/saved_drawing"

@app.get("/children")
def list_children():
  return {"children": os.listdir(DATA_ROOT)}

@app.get("/sessions/{child_name}")
def list_sessions(child_name: str):
  child_path = os.path.join(DATA_ROOT, child_name)
  if not os.path.isdir(child_path):
    return {"Error": "Child not found"}
  return{"Sessions": os.listdir(child_path)}

@app.get("/file/{child_name}/{session_name}/{file_name}")
def get_file(child_name: str, session_name: str, file_name: str):
  file_path = os.path.join(DATA_ROOT, child_name, session_name, file_name)
  if not os.path.isfile(file_path):
    return {"Error": "File not found"}
  return FileResponse(file_path)
