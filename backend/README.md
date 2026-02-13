# Robot Dashboard System - Backend

Python-based backend services for the Robot Dashboard System. This layer connects the React frontend to the different robot backends (Pixelbot and TurtleBot4) and exposes a FastAPI HTTP/WebSocket API.

## Overview

The backend provides:
- A FastAPI application (entry point: `main.py`) for the web frontend
- Integration with:
  - **Pixelbot**
  - **TurtleBot4**
- Demo utilities under `demo/` for system testing or demonstrations

## Tech Stack

- **Python 3.8+**
- **FastAPI** and **Uvicorn**
- **roslibpy**
- **ROS 2 Humble** (for TurtleBot4 integration)
- **rosbridge_server** (WebSocket bridge between ROS and the backend)

## Project Structure

```text
backend/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── pixelbot_backend/    # Pixelbot data and session handling
└── turtlebot4_backend/  # TurtleBot4 ROS integration
```

For details specific to TurtleBot4, also see:
- `backend/turtlebot4_backend/README.md`

## Prerequisites

- **Python** 3.8 or newer
- **pip** for dependency management
- **ROS 2 Humble** with TurtleBot4 packages (on the ROS machine)
- **rosbridge_server** installed and available in the ROS 2 environment (use `sudo apt install ros-humble-rosbridge-suite`)

> Note: ROS 2 and rosbridge commands are typically executed on the robot or a ROS-enabled machine (e.g., Ubuntu). The FastAPI backend can run on the same machine or a different one, as long as it can reach the rosbridge server over the network.

## ROS 2 Workspace (ros2_ws)

You should create a ROS 2 workspace on the ROS-enabled machine and place this repository inside the workspace `src` folder so ROS tools can find any packages or demo launch files included here.

Typical steps (Ubuntu / ROS 2 environment):

```bash
# create workspace and src
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Clone our repository into the workspace src
git clone https://github.com/sasr01-kit/RobotDashboardSystem.git

# Return to workspace root, source ROS, install dependencies and build
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

Notes:
- If you already have a local copy of `RobotDashboardSystem`, move or copy that folder into `~/ros2_ws/src/` instead of cloning from GitHub.
- The `rosdep install` step attempts to install any system package dependencies required by ROS packages in the workspace.
- These commands are intended for a Linux/Ubuntu ROS environment; Windows users should follow ROS 2 on Windows instructions and adapt workspace commands accordingly.
- After a successful build, any ROS packages in the workspace will be available to `ros2 launch` and `ros2 run`.

## Installation

From the repository root:

```bash
cd backend

# (Optional for Windows) Create and activate a virtual Linux environment in the terminal
python -m venv venv # Install venv once
.\venv\Scripts\Activate.ps1  # for Windows PowerShell

# Install dependencies
pip install -r requirements.txt
```

## Runtime Setup (Order Matters)

The following sequence mirrors `setup_commands.txt`. The order is important and should be followed as listed.

### 1. ROS 2 & rosbridge (ROS machine)

On the ROS-enabled machine (e.g., Ubuntu terminal):

```bash
# Reminder: This step requires the ros-humble-rosbridge-suite package
source /opt/ros/humble/setup.bash
ros2 launch rosbridge_server rosbridge_websocket_launch.xml
```

This starts the rosbridge WebSocket server that the backend uses to communicate with the TurtleBot4.

### 2. Optional Pre-Setup Testing (Robot / ROS machine)

These steps are optional, but should be executed **before** starting the backend/frontend if you want to verify the robot-side setup.

#### Teleoperation / Navigation (TurtleBot4)

```bash
# Run SLAM or navigation
ros2 launch turtlebot4_navigation slam.launch.py

# Start TurtleBot4 node
ros2 run turtlebot4_node turtlebot4_node
```

#### Map-Only Demo

From the ROS machine, using the demo map launch (clone the following repo into the src folder (/src/) in the ROS workspace: https://github.com/sasr01-kit/map_only_launch.git). This also requires to re-build our ROS2 workspace:

```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
# Now ros2 knows the package map_only_launch and can launch it
ros2 launch map_only_launch map_server_launch.py
```

### 3. Backend (FastAPI) and Frontend

After the ROS and optional pre-setup tests are running, start the backend and frontend.

#### Backend (FastAPI)

From the repository root, in a terminal that has access to Python and the backend dependencies:

```bash
cd backend

# First-time setup (if not yet done)
pip install -r requirements.txt

# Start FastAPI (default: port 8080)
source /opt/ros/humble/setup.bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

#### Frontend (React)

From another terminal:

```bash
cd react_frontend

# First-time setup
npm ci          # or: pnpm install

# Start development server (default: port 5173)
npm run dev     # or: pnpm dev
```

The React frontend expects the backend to be reachable on port `8080` by default.

### 4. Post-Setup Testing

After everything is running, you can verify the system by using the following commands.

```bash
# Inspect velocity commands
ros2 topic echo /cmd_vel

# Additional info about the topic
ros2 topic info /cmd_vel
```

Publish test status messages:

```bash
# Battery
ros2 topic pub /battery_state sensor_msgs/msg/BatteryState "{percentage: 0.82}"

# WiFi
ros2 topic pub /wifi_state std_msgs/msg/Bool "{data: true}"

# Raspberry Pi
ros2 topic pub /pi_state std_msgs/msg/Bool "{data: true}"

# Communications
ros2 topic pub /comms_state std_msgs/msg/Bool "{data: true}"
```

#### Map Testing

```bash
ros2 run map_only_launch pose_publisher
```

#### Pixelbot Backend Test

This step requires the Pixelbot test (mock) files to be available on the computer. Their location (path) can be defined in the CONFIG part of `test_full_pipeline`.
From the `backend` directory or any environment where `pixelbot_backend` is importable run:

```bash
# General child data test
python3 -m pixelbot_backend.test_full_pipeline
# Connection test
python3 -m pixelbot_backend.test_pixelbot_connection
```

## Port Conventions

- `8000`: Pixelbot (backend ↔ robot)
- `8080`: FastAPI (frontend ↔ backend)
- `9090`: TurtleBot4 (backend ↔ robot via rosbridge)

## Troubleshooting

- Ensure the ROS 2 environment is correctly sourced before running any `ros2` commands.
- Verify that the rosbridge server is reachable from the backend machine (network/firewall configuration).
- Confirm that the backend is listening on port `8080` and the frontend is configured to use this port.
- For Pixelbot issues, run the full pipeline test:
  - `python3 -m pixelbot_backend.test_full_pipeline`
- Restart the browser page when data doesn't arrive in the web app
