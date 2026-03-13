# Pixelbot Robot Data Server Setup (FastAPI and Uvicorn)
This guide explains how to set up a small FastAPI server on the Pixelbot robot.  
This server exposes the robot’s locally stored children/session data so that the external backend, running on a laptop or server, can fetch it.

## Download the Pixelbot Server Script
Download the ready‑to‑use server file. Make sure to update the DATA_ROOT in the pixelbot_server file, if needed.

**`pixelbot-setup/pixelbot_server.py`** 

This script exposes endpoints which return raw JSON data stored on the robot. You need to copy or transfer this file to the pixelbot robot for the server to work.

## Create and Activate the Robot’s Virtual Environment
Because Pixelbot runs Ubuntu, Python tools must be installed first.
```bash
sudo apt install python3-pip
```

Then you need to install the venv support 
```bash
sudo apt install python3-venv python3-full
```

Create and activate the venv
```bash
python3 -m venv ~/pixelbot-venv
source ~/pixelbot-venv/bin/activate
```

Install FastAPI and Uvicorn inside the venv
```bash
pip install fastapi uvicorn
```

### Run the Pixelbot Data Server

For making the robot accessible at one concrete port you need to run the server with the following command (Replace 8000 with an available port number you can freely choose):

```bash
uvicorn pixelbot_server:app --host 0.0.0.0 --port 8000
```

To check if the chosen port number is available, you can use: 
```bash
sudo netstat -tulpn | greep: [port number]
```

The backend can now fetch data from the robot at:
```
http://<robot-ip>:[port number]
```
# Troubleshooting (Installing python tools on Ubuntu)

### python3-pip error: “file has unexpected size” or “failed to fetch” 
This error can occur when installing python3-pip. To fix it:
```bash
sudo apt-get update
```

### sudo apt-get update error: “Release is not valid yet” or "updates will be not applied"
This happens when the repository metadata is outdated or the system clock is off. To fix it:
```bash
sudo apt-get -o Acquire::Check-Valid-Until=false update
sudo apt-get update
```
