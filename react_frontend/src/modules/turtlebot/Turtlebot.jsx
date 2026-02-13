import "./Turtlebot.css";
import { Routes, Route, Navigate } from 'react-router-dom';
import { ModeProvider } from './modeUtil/ModeProvider.jsx';
import TurtlebotLayout from './TurtlebotLayout.jsx';
import TurtlebotStatusPage from './pages/TurtlebotStatusPage.jsx';
import TurtlebotMapPage from './pages/TurtlebotMapPage.jsx';
import TurtlebotFeedbackPage from './pages/TurtlebotFeedbackPage.jsx';
import { useTurtlebotStatus } from "./hooks/useTurtlebotStatus.js";
import { useTurtlebotMap } from "./hooks/useTurtlebotMap.js";
import { useTurtlebotFeedback } from "./hooks/useTurtlebotFeedback.js";

// The main Turtlebot component that sets up routing and context for the Turtlebot module.
export default function Turtlebot() {
    useTurtlebotStatus(); // Ensure status hook is loaded at top level and initialize global state
    useTurtlebotMap(); // Ensure map hook is loaded at top level and initialize global state
    useTurtlebotFeedback(); // Ensure feedback hook is loaded at top level and initialize global state
    return (
        <ModeProvider>
            <Routes>
                <Route element={<TurtlebotLayout />}>
                    <Route path="status" element={<TurtlebotStatusPage />} />
                    <Route path="map" element={<TurtlebotMapPage />} />
                    <Route path="feedback" element={<TurtlebotFeedbackPage />} />
                    <Route index element={<Navigate to="status" replace />} />
                    <Route path="*" element={<Navigate to="/turtlebot" replace />} /> {"Fallback"}
                </Route>
            </Routes>
        </ModeProvider>
    );
}
