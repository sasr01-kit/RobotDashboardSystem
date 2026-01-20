import './Pixelbot.css'

import { Routes, Route, Navigate } from "react-router-dom";
import PixelbotSummary from "./pages/PixelbotSummary";
import PixelbotChildRecap from "./pages/PixelbotChildRecap";
import PixelbotSession from "./pages/PixelbotSession";
import PixelbotLayout from "./PixelbotLayout";

export default function Pixelbot() {
  return (
    <Routes>
      <Route element={<PixelbotLayout />}>
        <Route index element={<PixelbotSummary />} />
        <Route path="children/:childId" element={<PixelbotChildRecap />} />
        // Change routing to children/:childId/:sessionId
        <Route path="sessions/:sessionId" element={<PixelbotSession />} />
        <Route path="*" element={<Navigate to="/pixelbot" replace />} /> {"Fallback"}
      </Route>
    </Routes>
  );
}
