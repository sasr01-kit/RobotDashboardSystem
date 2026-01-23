import './Pixelbot.css'
import { Routes, Route, Navigate } from "react-router-dom";
import PixelbotLayout from './PixelbotLayout';
import PixelbotSummaryView from './pages/PixelbotSummaryView';
import ChildRecapView from './pages/ChildRecapView';
import ChildSessionView from './pages/ChildSessionView';

export default function Pixelbot() {
  return (
    <Routes>
      <Route element={<PixelbotLayout />}>
        <Route path="summary" element={<PixelbotSummaryView />} />
        <Route path="session/:childId" element={<ChildRecapView />} />
        <Route path="session/:childId/:sessionId" element={<ChildSessionView />} />
        <Route index element={<Navigate to="summary" replace />} />
        <Route path="*" element={<Navigate to="/pixelbot" replace />} /> {"Fallback"}
      </Route>
    </Routes>
  );
}
