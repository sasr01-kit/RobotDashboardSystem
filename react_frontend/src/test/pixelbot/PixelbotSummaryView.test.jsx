import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import PixelbotSummaryView from "../../modules/pixelbot/pages/PixelbotSummaryView";
import { usePixelbotSummary } from "../../modules/pixelbot/hooks/usePixelbotSummary";

// Tests for PixelbotSummaryView to ensure it renders summary cards and heatmap correctly 
// based on the summaryStats, formats growth rate properly, handles print functionality for the heatmap, 
// and cleans up print classes after printing properly
vi.mock("../../modules/pixelbot/hooks/usePixelbotSummary");

vi.mock("../../modules/pixelbot/components/CalendarHeatMap", () => ({
  default: ({ id, onPrint, data, colorScale }) => (
    <div id={id} data-testid="calendar-heatmap">
      <button onClick={onPrint} data-testid="print-heatmap">
        Print Heatmap
      </button>
      <span data-testid="heatmap-data-length">{data?.length ?? 0}</span>
      <span data-testid="heatmap-colors-length">{colorScale?.length ?? 0}</span>
    </div>
  ),
}));

const mockSummaryStats = {
  totalSessions: 42,
  avgSessionsPerChild: 4,
  sessionsPerDay: 2,
  sessionsGrowthRate: 10,
  dailySessionCounts: [],
  colorScale: [],
};

describe("PixelbotSummaryView", () => {
  let printSpy;
  let addEventListenerSpy;
  let removeEventListenerSpy;

  beforeEach(() => {
    vi.clearAllMocks();

    usePixelbotSummary.mockReturnValue({
      summaryStats: mockSummaryStats,
      isLoading: false,
    });

    printSpy = vi.spyOn(window, "print").mockImplementation(() => {});
    addEventListenerSpy = vi.spyOn(window, "addEventListener");
    removeEventListenerSpy = vi.spyOn(window, "removeEventListener");
  });

  afterEach(() => {
    printSpy.mockRestore();
    addEventListenerSpy.mockRestore();
    removeEventListenerSpy.mockRestore();
    document.body.className = "";
  });

  it("renders summary cards and heatmap", () => {
    render(<PixelbotSummaryView />);

    expect(screen.getByText("Total Sessions")).toBeInTheDocument();
    expect(screen.getByText("Sessions per day")).toBeInTheDocument();
    expect(screen.getByText("Sessions per child")).toBeInTheDocument();

    expect(screen.getByText("42")).toBeInTheDocument();
    expect(screen.getByText("2")).toBeInTheDocument();
    expect(screen.getByText("4")).toBeInTheDocument();

    expect(screen.getByTestId("calendar-heatmap")).toBeInTheDocument();
  });

  it("shows Loading when isLoading is true", () => {
    usePixelbotSummary.mockReturnValue({
      summaryStats: null,
      isLoading: true,
    });

    render(<PixelbotSummaryView />);

    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("shows Loading when summaryStats is missing even if isLoading is false", () => {
    usePixelbotSummary.mockReturnValue({
      summaryStats: null,
      isLoading: false,
    });

    render(<PixelbotSummaryView />);

    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("formats positive growth rate with a leading plus sign", () => {
    usePixelbotSummary.mockReturnValue({
      summaryStats: {
        ...mockSummaryStats,
        sessionsGrowthRate: 10,
      },
      isLoading: false,
    });

    render(<PixelbotSummaryView />);

    expect(screen.getByText(/\+10%/)).toBeInTheDocument();
  });

  it("formats zero growth rate without a leading plus sign", () => {
    usePixelbotSummary.mockReturnValue({
      summaryStats: {
        ...mockSummaryStats,
        sessionsGrowthRate: 0,
      },
      isLoading: false,
    });

    render(<PixelbotSummaryView />);

    expect(screen.getByText(/0%/)).toBeInTheDocument();
    expect(screen.queryByText(/\+0%/)).not.toBeInTheDocument();
  });

  it("formats negative growth rate without a leading plus sign", () => {
    usePixelbotSummary.mockReturnValue({
      summaryStats: {
        ...mockSummaryStats,
        sessionsGrowthRate: -7,
      },
      isLoading: false,
    });

    render(<PixelbotSummaryView />);

    expect(screen.getByText(/-7%/)).toBeInTheDocument();
  });

  it("uses fallback value 10 when sessionsPerDay is nullish", () => {
    usePixelbotSummary.mockReturnValue({
      summaryStats: {
        ...mockSummaryStats,
        sessionsPerDay: null,
      },
      isLoading: false,
    });

    render(<PixelbotSummaryView />);

    expect(screen.getByText("10")).toBeInTheDocument();
  });

  it("passes heatmap container id and print handler to CalendarHeatMap", () => {
    render(<PixelbotSummaryView />);

    expect(document.getElementById("summary-heatmap")).toBeInTheDocument();
    expect(screen.getByTestId("print-heatmap")).toBeInTheDocument();
  });

  it("prints a specific widget and adds print classes when heatmap print is clicked", () => {
    render(<PixelbotSummaryView />);

    const heatmap = document.getElementById("summary-heatmap");
    fireEvent.click(screen.getByTestId("print-heatmap"));

    expect(heatmap).toHaveClass("print-visible");
    expect(document.body).toHaveClass("printing-single-widget");
    expect(window.print).toHaveBeenCalledTimes(1);
    expect(window.addEventListener).toHaveBeenCalledWith(
      "afterprint",
      expect.any(Function)
    );
  });

  it("cleans up print classes after afterprint fires", () => {
    render(<PixelbotSummaryView />);

    const heatmap = document.getElementById("summary-heatmap");
    fireEvent.click(screen.getByTestId("print-heatmap"));

    const cleanupCall = addEventListenerSpy.mock.calls.find(
      ([eventName]) => eventName === "afterprint"
    );
    const cleanupFn = cleanupCall[1];

    cleanupFn();

    expect(heatmap).not.toHaveClass("print-visible");
    expect(document.body).not.toHaveClass("printing-single-widget");
    expect(window.removeEventListener).toHaveBeenCalledWith(
      "afterprint",
      cleanupFn
    );
  });

  it("falls back to plain window.print when heatmap target element is missing", () => {
    render(<PixelbotSummaryView />);

    const heatmap = document.getElementById("summary-heatmap");
    heatmap.id = "summary-heatmap-missing";

    fireEvent.click(screen.getByTestId("print-heatmap"));

    expect(window.print).toHaveBeenCalledTimes(1);
    expect(document.body).not.toHaveClass("printing-single-widget");
    expect(window.addEventListener).not.toHaveBeenCalledWith(
      "afterprint",
      expect.any(Function)
    );
  });
});