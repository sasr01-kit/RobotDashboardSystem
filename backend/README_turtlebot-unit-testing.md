# Running Unit Tests — TurtleBot4 Backend
 
This guide walks you through everything you need to do after cloning the repository to run the unit tests locally. No ROS installation, no robot hardware, and no prior Python experience is required.
 
---
 
## Prerequisites
 
You need **Python 3.10 or higher** installed on your machine. To check, open a terminal and run:
 
```bash
python3 --version
```
 
If you see `Python 3.10.x` or higher, you are good to go. If not, install Python from [https://www.python.org/downloads](https://www.python.org/downloads).
 
---
 
## Step 1 — Navigate to the repository
 
Open a terminal and navigate to the root of the cloned repository:
 
```bash
cd ~/ros2_ws/src/RobotDashboardSystem
```
  
---
 
## Step 2 — Create a virtual environment
 
A virtual environment is an isolated Python workspace. It keeps the packages you install for this project separate from the rest of your computer, so nothing conflicts.
 
You only need to do this **once** per machine:
 
```bash
python3 -m venv .venv
```
 
This creates a hidden folder called `.venv` inside the repository. You do not need to touch it directly.
 
---
 
## Step 3 — Activate the virtual environment
 
You need to do this **every time you open a new terminal** before running tests:
 
```bash
source .venv/bin/activate
```
 
Once activated, your terminal prompt will change to show `(.venv)` at the start, like this:
 
```
(.venv) user@machine:~/ros2_ws/src/RobotDashboardSystem$
```
 
This confirms the virtual environment is active. All Python commands from this point will use it.
 
> **To deactivate** when you are done, simply run: `deactivate`
 
---
 
## Step 4 — Upgrade pip tooling
 
This ensures your package installer is up to date. Run this once after creating the virtual environment:
 
```bash
python -m pip install --upgrade pip setuptools wheel
```
 
---
 
## Step 5 — Install the required testing packages
 
Install pytest and its coverage/mock plugins:
 
```bash
python -m pip install pytest pytest-cov pytest-mock
```
 
You only need to do this **once** per virtual environment. If you have already done this before, skip to Step 6.
 
---
 
## Step 6 — Run the tests
 
Make sure you are in the repository root and the virtual environment is active (you should see `(.venv)` in your prompt), then run:
 
```bash
PYTHONPATH=backend pytest backend/turtlebot4_backend/test/ -v \
  --cov=turtlebot4_backend.turtlebot4_model \
  --cov=turtlebot4_backend.turtlebot4_controller \
  --cov-report=term-missing \
  --cov-config=backend/.coveragerc
```
