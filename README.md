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
- **Turtlebot4**: ROS 2 environment with rosbridge server

### Installation

1. Clone the repository:
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

### Running the Application

1. **Start the Frontend**:
   ```bash
   cd react_frontend
   npm run dev  # or pnpm dev
   ```

2. **Start the Backend** (if applicable for your robot):
   ```bash
   cd backend
   # Run appropriate backend service
   ```

3. Access the dashboard at `http://localhost:5173` (or the port shown in your terminal that started the frontend server)

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
