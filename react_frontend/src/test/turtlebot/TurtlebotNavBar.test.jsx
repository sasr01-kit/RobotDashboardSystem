import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import TurtlebotNavBar from "../../modules/turtlebot/TurtlebotNavBar";

import { useNavigate, useLocation } from "react-router-dom";
import { useModeContext } from "../../modules/turtlebot/modeUtil/ModeContext";

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: vi.fn(),
    useLocation: vi.fn(),
  };
});

vi.mock("../../modules/turtlebot/modeUtil/ModeContext", () => ({
  useModeContext: vi.fn(),
}));

describe("TurtlebotNavBar", () => {
  const navigate = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    useNavigate.mockReturnValue(navigate);
  });

  it("renders all tabs", () => {
    useLocation.mockReturnValue({ pathname: "/turtlebot/status" });
    useModeContext.mockReturnValue({ mode: "Autonomous" });

    render(
      <MemoryRouter>
        <TurtlebotNavBar />
      </MemoryRouter>
    );

    expect(screen.getByText("Status")).toBeInTheDocument();
    expect(screen.getByText("Map")).toBeInTheDocument();
    expect(screen.getByText("Feedback")).toBeInTheDocument();
  });

  it("highlights the active tab", () => {
    useLocation.mockReturnValue({ pathname: "/turtlebot/map" });
    useModeContext.mockReturnValue({ mode: "Autonomous" });

    render(
      <MemoryRouter>
        <TurtlebotNavBar />
      </MemoryRouter>
    );

    expect(screen.getByText("Map")).toHaveClass("active");
  });

  it("navigates when clicking a tab", () => {
    useLocation.mockReturnValue({ pathname: "/turtlebot/status" });
    useModeContext.mockReturnValue({ mode: "Autonomous" });

    render(
      <MemoryRouter>
        <TurtlebotNavBar />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByText("Map"));

    expect(navigate).toHaveBeenCalledWith("/turtlebot/map");
  });

  it("disables Map and Feedback in Teleoperating mode", () => {
    useLocation.mockReturnValue({ pathname: "/turtlebot/status" });
    useModeContext.mockReturnValue({ mode: "Teleoperating" });

    render(
      <MemoryRouter>
        <TurtlebotNavBar />
      </MemoryRouter>
    );

    expect(screen.getByText("Map")).toHaveClass("disabled");
    expect(screen.getByText("Feedback")).toHaveClass("disabled");
    expect(screen.getByText("Map")).toHaveAttribute("aria-disabled", "true");
    expect(screen.getByText("Feedback")).toHaveAttribute("aria-disabled", "true");
  });

  it("does not navigate when clicking disabled tabs in Teleoperating mode", () => {
    useLocation.mockReturnValue({ pathname: "/turtlebot/status" });
    useModeContext.mockReturnValue({ mode: "Teleoperating" });

    render(
      <MemoryRouter>
        <TurtlebotNavBar />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByText("Map"));

    expect(navigate).not.toHaveBeenCalled();
  });

  it("defaults active tab to Status when route does not match known tabs", () => {
    useLocation.mockReturnValue({ pathname: "/turtlebot/unknown" });
    useModeContext.mockReturnValue({ mode: "Autonomous" });

    render(
      <MemoryRouter>
        <TurtlebotNavBar />
      </MemoryRouter>
    );

    expect(screen.getByText("Status")).toHaveClass("active");
  });

  it("still navigates to Status in Teleoperating mode", () => {
    useLocation.mockReturnValue({ pathname: "/turtlebot/map" });
    useModeContext.mockReturnValue({ mode: "Teleoperating" });

    render(
      <MemoryRouter>
        <TurtlebotNavBar />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByText("Status"));

    expect(navigate).toHaveBeenCalledWith("/turtlebot/status");
  });

  it("blocks switchTab guard for Map in Teleoperating mode", () => {
    useLocation.mockReturnValue({ pathname: "/turtlebot/status" });
    useModeContext.mockReturnValue({ mode: "Teleoperating" });

    render(
      <MemoryRouter>
        <TurtlebotNavBar />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByText("Map"));

    expect(navigate).not.toHaveBeenCalled();
  });

  it("blocks switchTab guard for Feedback in Teleoperating mode", () => {
    useLocation.mockReturnValue({ pathname: "/turtlebot/status" });
    useModeContext.mockReturnValue({ mode: "Teleoperating" });

    render(
      <MemoryRouter>
        <TurtlebotNavBar />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByText("Feedback"));

    expect(navigate).not.toHaveBeenCalled();
  });
});