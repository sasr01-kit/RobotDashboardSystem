# Robot Dashboard System

A comprehensive dashboard system for monitoring and controlling multiple robots, developed as part of the PSE Project for the SARAI institute at KIT.

## Overview

The Robot Dashboard System provides an intuitive web-based interface that allows users to:
- Access and manage multiple robot dashboards from a centralized homepage
- Visualize (real-time) robot data and metrics
- Enable bidirectional communication with robots (e.g., ROS integration for TurtleBot4)
- Monitor robot status, paths, and telemetry
- Track interaction sessions and analyze data

Currently supports:
- **Pixelbot**: Session management, child interaction tracking, and data visualization
- **Turtlebot4**: Full ROS integration with mapping, path planning, teleoperation, and status monitoring

## Getting Started

### Prerequisites

- **Frontend**: Node.js (v16 or higher) and npm/pnpm
- **Backend**: Python 3.8+
- **TurtleBot4**: ROS 2 environment with rosbridge server

See the component-specific READMEs for detailed setup:
- Frontend: `react_frontend/README.md`
- Backend: `backend/README.md`

### Installation

1. Clone the repository. Please note that before cloning, the ros2 workspace must be set up correctly, and this repository must be placed inside the `src` folder of the ros2 workspace. Detailed information for this can be found in the backend README.
   ```bash
   git clone https://github.com/sasr01-kit/RobotDashboardSystem.git
   cd RobotDashboardSystem
   ```

2. **Frontend Setup**:
   ```bash
   cd react_frontend
   npm ci  # or pnpm install
   ```

3. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Running the Application (High-Level)

The exact sequence of commands is important for ROS-based robots. A detailed, step-by-step guide (including ROS 2, rosbridge, and testing commands) is available in `backend/README.md`. The following summarizes the typical flow:

1. **Start ROS 2 and rosbridge** on the ROS-enabled machine (e.g., TurtleBot4 / Ubuntu).
2. (Optional) **Run pre-setup tests** for TurtleBot4 navigation/teleop and map-only demos.
3. **Start the Backend (FastAPI)**:
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8080
   ```
4. **Start the Frontend**:
   ```bash
   cd react_frontend
   npm run dev  # or pnpm dev
   ```
5. Access the dashboard at `http://localhost:5173` (or the port shown in your frontend terminal).

## Project Structure

```
RobotDashboardSystem/
├── react_frontend/          # React-based web interface
│   ├── src/
│   │   ├── modules/
│   │   │   ├── global/      # Shared components (Header, Navigation)
│   │   │   ├── robotSelection/  # Homepage and robot selection
│   │   │   ├── turtlebot/   # TurtleBot4 dashboard
│   │   │   └── pixelbot/    # Pixelbot dashboard
│   │   └── ...
│   └── ...
├── backend/
│   ├── pixelbot_backend/    # Pixelbot data management
│   └── turtlebot4_backend/  # TurtleBot4 ROS integration
└── README.md
```

## Features

### TurtleBot4 Dashboard
- Real-time robot status monitoring
- Interactive map visualization
- Path planning and navigation
- Teleoperation controls
- Feedback and logging system

### Pixelbot Dashboard
- Calendar heatmaps and summary metrics
- Child session overview
- Interaction data visualization
- Drawing and speech analysis
- Historical session recap

## Contributing

For contributors: 
- Run `npm ci` (or `pnpm install`) to reproduce exact frontend dependencies
- Follow the existing code structure and naming conventions
- Ensure all changes are tested before committing

## License

This project is developed for the SARAI institute in the scope of PSE (Praxis der Software-Entwicklung).
