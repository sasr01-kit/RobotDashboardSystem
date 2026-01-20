import { Routes, Route } from "react-router-dom";
import PixelbotLayout from "./PixelbotLayout.jsx";

import PixelbotSummary from "./pages/PixelbotSummary";
import PixelbotChildRecap from "./pages/PixelbotChildRecap";
import PixelbotSession from "./pages/PixelbotSession";

export default function Pixelbot() {
  return (
    <Routes>
      <Route path="/" element={<PixelbotLayout />}>
        <Route index element={<PixelbotSummary />} />

        <Route
          path="child/:childId"
          element={<PixelbotChildRecap />}
        />

        <Route
          path="child/:childId/session/:sessionId"
          element={<PixelbotSession />}
        />
      </Route>
    </Routes>
  );
}