import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import PixelbotLayout from "../../modules/pixelbot/PixelbotLayout";

// Tests for PixelbotLayout to ensure it renders header, navbar, and outlet content correctly based on the route
vi.mock("../../modules/global/Header", () => ({
  default: ({ title }) => <div>{title}</div>,
}));

vi.mock("../../modules/pixelbot/PixelbotNavBar.jsx", () => ({
  default: () => <div>PixelbotNavBar</div>,
}));

describe("PixelbotLayout", () => {
  it("renders header, navbar, and outlet content", () => {
    render(
      <MemoryRouter initialEntries={["/pixelbot/summary"]}>
        <Routes>
          <Route element={<PixelbotLayout />}>
            <Route path="*" element={<div>Outlet Content</div>} />
          </Route>
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("Pixelbot Dashboard")).toBeInTheDocument();
    expect(screen.getByText("PixelbotNavBar")).toBeInTheDocument();
    expect(screen.getByText("Outlet Content")).toBeInTheDocument();
  });

  it("renders correctly on a child/session route", () => {
    render(
      <MemoryRouter initialEntries={["/pixelbot/session/c1/s1"]}>
        <Routes>
          <Route path="/pixelbot/session/:childId/:sessionId" element={<PixelbotLayout />}>
            <Route index element={<div>Child Outlet</div>} />
          </Route>
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText("Pixelbot Dashboard")).toBeInTheDocument();
    expect(screen.getByText("PixelbotNavBar")).toBeInTheDocument();
    expect(screen.getByText("Child Outlet")).toBeInTheDocument();
  });
});