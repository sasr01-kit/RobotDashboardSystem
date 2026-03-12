import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import TurtlebotLayout from "../../modules/turtlebot/TurtlebotLayout";

vi.mock("../../modules/global/Header", () => ({
  default: ({ title }) => <div>{title}</div>,
}));

vi.mock("../../modules/turtlebot/TurtlebotNavBar", () => ({
  default: () => <div>TurtlebotNavBar</div>,
}));

// Tests for TurtlebotLayout to ensure correct rendering of header, navbar, and outlet content
describe("TurtlebotLayout", () => {
  it("renders header, navbar, and outlet content", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <Routes>
          <Route element={<TurtlebotLayout />}>
            <Route index element={<div>Outlet Content</div>} />
          </Route>
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("Turtlebot4 Dashboard")).toBeInTheDocument();
    expect(screen.getByText("TurtlebotNavBar")).toBeInTheDocument();
    expect(screen.getByText("Outlet Content")).toBeInTheDocument();
  });
});