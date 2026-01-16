/*CHANGE THIS TO TURTLEBOT REDIRECTION FILE*/


import { Routes, Route, Navigate } from 'react-router-dom';
import { ModeProvider } from './ModeUtil/ModeProvider.jsx';
import TurtlebotLayout from './TurtlebotLayout.jsx';
import TurtlebotStatusPage from './TurtlebotStatusPage.jsx';
import TurtlebotMapPage from './TurtlebotMapPage.jsx';
import TurtlebotFeedbackPage from './TurtlebotFeedbackPage.jsx';


export default function Turtlebot() {
    return (
        <ModeProvider>
            <Routes>
                <Route element={<TurtlebotLayout />}>
                    <Route path="status" element={<TurtlebotStatusPage />} />
                    <Route path="map" element={<TurtlebotMapPage />} />
                    <Route path="feedback" element={<TurtlebotFeedbackPage />} />
                    <Route index element={<Navigate to="status" replace />} />
                </Route>
            </Routes>
        </ModeProvider>
    );
}
