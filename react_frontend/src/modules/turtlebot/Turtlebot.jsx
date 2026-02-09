import "./Turtlebot.css";
import { Routes, Route, Navigate } from 'react-router-dom';
import { ModeProvider } from './ModeUtil/ModeProvider.jsx';
import TurtlebotLayout from './TurtlebotLayout.jsx';
import TurtlebotStatusPage from './pages/TurtlebotStatusPage.jsx';
import TurtlebotMapPage from './pages/TurtlebotMapPage.jsx';
import TurtlebotFeedbackPage from './pages/TurtlebotFeedbackPage.jsx';
import { useTurtlebotStatus } from "./Hooks/useTurtlebotStatus.js";
import { useTurtlebotMap } from "./Hooks/useTurtlebotMap.js";
import { useTurtlebotFeedback } from "./Hooks/useTurtlebotFeedback.js";

export default function Turtlebot() {
    useTurtlebotStatus(); // Ensure status is loaded at top level
    useTurtlebotMap(); // Ensure map is loaded at top level
    useTurtlebotFeedback(); // Ensure feedback is loaded at top level
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
