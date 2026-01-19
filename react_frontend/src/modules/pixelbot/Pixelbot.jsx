import { Routes, Route } from "react-router-dom";
import PixelbotSummary from "./pages/PixelbotSummary";
import PixelbotChildRecap from "./pages/PixelbotChildRecap";
import PixelbotSession from "./pages/PixelbotSession";

export default function Pixelbot() {
  return (
    <Routes>
      <Route index element={<PixelbotSummary />} />
      <Route path="children/:childId" element={<PixelbotChildRecap />} />
      <Route path="sessions/:sessionId" element={<PixelbotSession />} />
    </Routes>
  );
}
