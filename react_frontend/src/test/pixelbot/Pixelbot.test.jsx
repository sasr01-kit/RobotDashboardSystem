import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter, Routes, Route, Outlet } from "react-router-dom";
import Pixelbot from "../../modules/pixelbot/Pixelbot";

// Tests for Pixelbot to ensure it renders the correct views based on the route and 
// that the main layout is displayed with the Outlet for nested routes
vi.mock("../../modules/pixelbot/PixelbotLayout", () => ({
  default: () => (
    <div>
      PixelbotLayout
      <Outlet />
    </div>
  ),
}));

vi.mock("../../modules/pixelbot/pages/PixelbotSummaryView", () => ({
  default: () => <div>PixelbotSummaryView</div>,
}));

vi.mock("../../modules/pixelbot/pages/ChildRecapView", () => ({
  default: () => <div>ChildRecapView</div>,
}));

vi.mock("../../modules/pixelbot/pages/ChildSessionView", () => ({
  default: () => <div>ChildSessionView</div>,
}));

describe("Pixelbot", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("redirects /pixelbot to summary", () => {
    render(
      <MemoryRouter initialEntries={["/pixelbot"]}>
        <Routes>
          <Route path="/pixelbot/*" element={<Pixelbot />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("PixelbotLayout")).toBeInTheDocument();
    expect(screen.getByText("PixelbotSummaryView")).toBeInTheDocument();
  });

  it("renders ChildRecapView on /pixelbot/session/:childId", () => {
    render(
      <MemoryRouter initialEntries={["/pixelbot/session/c1"]}>
        <Routes>
          <Route path="/pixelbot/*" element={<Pixelbot />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("ChildRecapView")).toBeInTheDocument();
  });

  it("renders ChildSessionView on /pixelbot/session/:childId/:sessionId", () => {
    render(
      <MemoryRouter initialEntries={["/pixelbot/session/c1/s1"]}>
        <Routes>
          <Route path="/pixelbot/*" element={<Pixelbot />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("ChildSessionView")).toBeInTheDocument();
  });
});