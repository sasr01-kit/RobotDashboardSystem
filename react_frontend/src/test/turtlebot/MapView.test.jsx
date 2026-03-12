import { render, screen, waitFor } from "@testing-library/react";
import { vi, describe, it, expect, beforeEach } from "vitest";
import MapView from "../../modules/turtlebot/components/MapView.jsx";
import { useTurtlebotMap } from "../../modules/turtlebot/hooks/useTurtlebotMap.js";

vi.mock("../../modules/turtlebot/hooks/useTurtlebotMap.js", () => ({
  useTurtlebotMap: vi.fn(),
}));

// Tests for MapView to ensure it renders legend items, draws map entities correctly based on hook data, and handles missing data properly
describe("MapView", () => {
  let mockCtx;

  beforeEach(() => {
    vi.clearAllMocks();

    mockCtx = {
      clearRect: vi.fn(),
      drawImage: vi.fn(),
      beginPath: vi.fn(),
      arc: vi.fn(),
      fill: vi.fn(),
      stroke: vi.fn(),
      fillStyle: "",
      strokeStyle: "",
      lineWidth: 0,
    };

    HTMLCanvasElement.prototype.getContext = vi.fn(() => mockCtx);

    class MockImage {
      constructor() {
        this.width = 500;
        this.height = 300;
        this._src = "";
        this.onload = null;
      }

      set src(value) {
        this._src = value;
        // simulate async image load
        setTimeout(() => {
          if (this.onload) this.onload();
        }, 0);
      }

      get src() {
        return this._src;
      }
    }

    vi.stubGlobal("Image", MockImage);
  });

  it("renders legend items", () => {
    useTurtlebotMap.mockReturnValue({
      mapUrl: null,
    });

    render(<MapView />);

    expect(screen.getByText("Public Zone (7.6m)")).toBeInTheDocument();
    expect(screen.getByText("Social Zone (3.6m)")).toBeInTheDocument();
    expect(screen.getByText("Personal Zone (1.2m)")).toBeInTheDocument();
    expect(screen.getByText("Intimate Zone (0.45m)")).toBeInTheDocument();
    expect(screen.getByText("Human Position")).toBeInTheDocument();
    expect(screen.getByText("Global Goal")).toBeInTheDocument();
    expect(screen.getByText("Intermediate Waypoint")).toBeInTheDocument();
    expect(screen.getByText("Robot Position")).toBeInTheDocument();
  });

  it("draws map entities and calls onMapResize after image load", async () => {
    const onMapResize = vi.fn();

    useTurtlebotMap.mockReturnValue({
      mapUrl: "/test-map.png",
      resolution: 0.05,
      humans: [
        {
          position: { x: 1, y: 2 },
          proxemicDistances: {
            public: 7.6,
            social: 3.6,
            personal: 1.2,
            intimate: 0.45,
          },
        },
      ],
      globalGoal: {
        position: { x: 3, y: 4 },
      },
      intermediateWaypoints: [
        { position: { x: 5, y: 6 } },
        { position: { x: 7, y: 8 } },
      ],
      robotPose: {
        position: { x: 9, y: 10 },
      },
    });

    render(<MapView onMapResize={onMapResize} />);

    await waitFor(() => {
      expect(onMapResize).toHaveBeenCalledWith(300);
    });

    expect(mockCtx.clearRect).toHaveBeenCalled();
    expect(mockCtx.drawImage).toHaveBeenCalled();

    // Human: 4 zones + 1 human dot
    // Global goal: 1 arc
    // Waypoints: 2 arcs
    // Robot: 1 arc
    expect(mockCtx.arc).toHaveBeenCalledTimes(9);

    expect(mockCtx.fill).toHaveBeenCalled();
    expect(mockCtx.stroke).toHaveBeenCalled();
  });

  it("does not attempt drawing when mapUrl is missing", () => {
    useTurtlebotMap.mockReturnValue({
      mapUrl: null,
      resolution: 0.05,
    });

    const onMapResize = vi.fn();

    render(<MapView onMapResize={onMapResize} />);

    expect(mockCtx.drawImage).not.toHaveBeenCalled();
    expect(onMapResize).not.toHaveBeenCalled();
  });

  it("draws base map without optional entities and without onMapResize callback", async () => {
    useTurtlebotMap.mockReturnValue({
      mapUrl: "/test-map.png",
      resolution: 0.05,
      humans: null,
      globalGoal: null,
      intermediateWaypoints: null,
      robotPose: null,
    });

    render(<MapView />);

    await waitFor(() => {
      expect(mockCtx.drawImage).toHaveBeenCalled();
    });

    expect(mockCtx.arc).not.toHaveBeenCalled();
    expect(mockCtx.stroke).not.toHaveBeenCalled();
  });

  it("uses fallback proxemic zones object when a human has no proxemicDistances", async () => {
    useTurtlebotMap.mockReturnValue({
      mapUrl: "/test-map.png",
      resolution: 0.05,
      humans: [
        {
          position: { x: 2, y: 4 },
        },
      ],
      globalGoal: null,
      intermediateWaypoints: null,
      robotPose: null,
    });

    render(<MapView />);

    await waitFor(() => {
      // 4 proxemic-zone arcs + 1 human dot arc
      expect(mockCtx.arc).toHaveBeenCalledTimes(5);
    });

    const firstZoneArcCall = mockCtx.arc.mock.calls[0];
    expect(Number.isNaN(firstZoneArcCall[2])).toBe(true);
    expect(mockCtx.fill).toHaveBeenCalled();
  });

  it("skips waypoint drawing when intermediateWaypoints is an empty array", async () => {
    useTurtlebotMap.mockReturnValue({
      mapUrl: "/test-map.png",
      resolution: 0.05,
      humans: null,
      globalGoal: null,
      intermediateWaypoints: [],
      robotPose: null,
    });

    render(<MapView />);

    await waitFor(() => {
      expect(mockCtx.drawImage).toHaveBeenCalled();
    });

    expect(mockCtx.arc).not.toHaveBeenCalled();
    expect(mockCtx.stroke).not.toHaveBeenCalled();
  });
});