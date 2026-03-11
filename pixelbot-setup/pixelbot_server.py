from fastapi import FastAPI
from fastapi.responses import FileResponse
import base64
import os

app = FastAPI()

#If the files containing the children's session information are located in another directory, change the data_root.
DATA_ROOT = "/home/pixelbot/pse_data_example/saved_drawing"

@app.get("/children")
def list_children():
  return {"children": os.listdir(DATA_ROOT)}

@app.get("/{child_name}/sessions")
def list_sessions(child_name: str):
  child_path = os.path.join(DATA_ROOT, child_name)
  if not os.path.isdir(child_path):
    return {"Error": "Child not found"}
  return {"sessions": os.listdir(child_path)}

@app.get("/file/{child_name}/{session_id}/{file_name}")
def get_file(child_name: str, session_id: str, file_name: str):
  file_path = os.path.join(DATA_ROOT, child_name, session_id, file_name)
  if not os.path.isfile(file_path):
    return {"Error": "File not found"}
  if file_name.lower().endswith(".png"):
    with open(file_path, "rb") as file:
      drawing_b64_format = base64.b64encode(file.read()).decode("utf-8")
      return { "base64": drawing_b64_format }
  return FileResponse(file_path)

@app.get("/file/{child_name}/{session_id}")
def list_files(child_name: str, session_id: str):
  file_path = os.path.join(DATA_ROOT, child_name, session_id)
  if not os.path.isdir(file_path):
    return {"Error": "File not found"}
  return {"files": os.listdir(file_path)}
