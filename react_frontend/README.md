# Robot Dashboard System - Frontend

React-based frontend for the Robot Dashboard System, providing an intuitive interface for monitoring and controlling multiple robots.

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Highcharts** - Data visualization
- **WebSocket** - Real-time communication (TurtleBot4) and backend connection

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or pnpm
- Running backend API (see `backend/README.md` for setup and startup order)

### Installation

```bash
npm ci  # or pnpm install
```

For contributors: Use `npm ci` (or `pnpm install`) to reproduce exact dependencies from the lockfile.

### Development

1. Ensure the backend FastAPI service is running (by default on port `8080`). See `backend/README.md` for details.
2. Start the frontend dev server:

```bash
npm run dev  # or pnpm dev
```

The development server will start at `http://localhost:5173`.

### Build

```bash
npm run build  # or pnpm build
```

Production build will be output to the `dist/` directory.

### Preview Production Build

```bash
npm run preview  # or pnpm preview
```

## Project Structure

```
src/
├── App.jsx                  # Main app component and routing
├── main.jsx                 # Application entry point
├── index.css                # Global styles sheet
└── modules/
    ├── global/              # Shared components
    │   ├── Header.jsx       # Navigation header
    │   └── HomeButton.jsx   # Return to homepage button
    ├── robotSelection/      # Robot selection
    │   └── Homepage.jsx     # Landing page with robot cards
    ├── turtlebot/           # TurtleBot4 dashboard module
    │   ├── Turtlebot.jsx    # Main dashboard component
    │   ├── TurtlebotLayout.jsx
    │   ├── TurtlebotNavBar.jsx
    │   ├── components/      # Reusable UI components
    │   ├── Hooks/           # Custom React hooks for backend communication
    │   ├── pages/           # Dashboard pages/views
    │   ├── WebsocketUtil/   # WebSocket connection management for backend communication
    │   └── ModeUtil/        # Mode switching utilities
    └── pixelbot/            # Pixelbot dashboard module
        ├── Pixelbot.jsx     # Main dashboard component
        ├── PixelbotLayout.jsx
        ├── PixelbotNavBar.jsx
        ├── components/      # Charts and UI components
        ├── hooks/           # Data fetching hooks
        ├── pages/           # Dashboard views
        └── types/           
```

## Key Features

### Homepage
- Robot selection interface
- Navigation to individual robot dashboards

### TurtleBot4 Dashboard
- **Teleoperation**: Manual robot control
- **Map View**: Real-time robot position and mapping
- **Path Planning**: Interactive path creation and navigation
- **Status Monitoring**: Battery, connection status, and feedback
- **WebSocket Integration**: Real-time bidirectional ROS communication

### Pixelbot Dashboard
- **Summary View**: Overview of all children and sessions
- **Child Recap**: Individual child interaction history
- **Session View**: Detailed session analysis with drawings and speech data
- **Data Visualization**: Charts, heatmaps, and metrics
- **Image Carousel**: Drawing visualization

## Development Guidelines

### Adding a New Robot Dashboard

1. Create a new module under `src/modules/<robot-name>/`
2. Implement the main component, layout, and navigation
3. Add routing in `App.jsx`
4. Create a robot card on the homepage

### Code Style

- Use functional components with hooks
- Keep components focused and reusable
- Place shared components in `modules/global/`
- Use CSS modules or scoped styles for component styling

### Component Naming

- Components: PascalCase (e.g., `MapView.jsx`)
- Hooks: camelCase with "use" prefix (e.g., `useRobotStatus.jsx`)
- Utilities: camelCase (e.g., `websocketManager.js`)

## Troubleshooting

### Port Already in Use

If port 5173 is already in use, Vite will automatically try the next available port. Check the terminal output for the actual URL.

### WebSocket Connection Issues

Ensure the backend server is running and accessible.

### Module Resolution Errors

Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm ci
```

## License

This project is developed for the SARAI institute in the scope of PSE (Praxis der Software-Entwicklung).
