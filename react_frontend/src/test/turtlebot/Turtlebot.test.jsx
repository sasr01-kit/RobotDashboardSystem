import { render } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import Turtlebot from "../../modules/turtlebot/Turtlebot";

import { useTurtlebotStatus } from "../../modules/turtlebot/hooks/useTurtlebotStatus";
import { useTurtlebotMap } from "../../modules/turtlebot/hooks/useTurtlebotMap";
import { useTurtlebotFeedback } from "../../modules/turtlebot/hooks/useTurtlebotFeedback";

vi.mock("../../modules/turtlebot/hooks/useTurtlebotStatus");
vi.mock("../../modules/turtlebot/hooks/useTurtlebotMap");
vi.mock("../../modules/turtlebot/hooks/useTurtlebotFeedback");

vi.mock("../../modules/turtlebot/pages/TurtlebotStatusPage", () => ({
  default: () => <div>StatusPage</div>,
}));

vi.mock("../../modules/turtlebot/pages/TurtlebotMapPage", () => ({
  default: () => <div>MapPage</div>,
}));

vi.mock("../../modules/turtlebot/pages/TurtlebotFeedbackPage", () => ({
  default: () => <div>FeedbackPage</div>,
}));

vi.mock("../../modules/turtlebot/TurtlebotLayout", () => ({
  default: () => <div>Layout</div>,
}));

vi.mock("../../modules/turtlebot/modeUtil/ModeProvider.jsx", () => ({
  ModeProvider: ({ children }) => <div>{children}</div>,
}));

// Tests on initialization of hooks upon landing page and proper route rendering 
describe("Turtlebot", () => {
  it("initializes turtlebot hooks", () => {
    render(
      <MemoryRouter initialEntries={["/turtlebot"]}>
        <Routes>
          <Route path="/turtlebot/*" element={<Turtlebot />} />
        </Routes>
      </MemoryRouter>
    );

    expect(useTurtlebotStatus).toHaveBeenCalled();
    expect(useTurtlebotMap).toHaveBeenCalled();
    expect(useTurtlebotFeedback).toHaveBeenCalled();
  });
});