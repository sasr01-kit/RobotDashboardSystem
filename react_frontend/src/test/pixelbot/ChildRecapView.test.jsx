import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import ChildRecapView from "../../modules/pixelbot/pages/ChildRecapView";
import { usePixelbotRecap } from "../../modules/pixelbot/hooks/usePixelbotRecap";

// Tests for ChildRecapView to ensure it renders all sections correctly based on the child data, 
// handles loading states, and that print functionality works as expected with proper cleanup after printing
vi.mock("../../modules/pixelbot/hooks/usePixelbotRecap");

vi.mock("../../modules/pixelbot/components/DashboardCard", () => ({
  default: ({ id, title, onPrint, children, subtitle, className }) => (
    <div id={id} data-testid={`dashboard-card-${id}`} className={className || ""}>
      <h4>{title}</h4>
      {subtitle ? <div>{subtitle}</div> : null}
      {onPrint ? <button onClick={onPrint}>Print {title}</button> : null}
      <div>{children}</div>
    </div>
  ),
}));

vi.mock("../../modules/pixelbot/components/ImageCarousel", () => ({
  default: ({ images }) => (
    <div data-testid="image-carousel">images:{images?.length ?? 0}</div>
  ),
}));

vi.mock("../../modules/pixelbot/components/BarChart", () => ({
  default: ({ averageLine, yAxisLabel, xAxisLabel, data }) => (
    <div data-testid="bar-chart">
      avg:{String(averageLine)}-y:{yAxisLabel}-x:{xAxisLabel}-points:{data?.length ?? 0}
    </div>
  ),
}));

vi.mock("../../modules/pixelbot/components/LineChart", () => ({
  default: ({ yAxisLabel, xAxisLabel, averageLine, data }) => (
    <div data-testid="line-chart">
      y:{yAxisLabel}-x:{xAxisLabel}-avg:{String(averageLine)}-points:
      {Array.isArray(data) ? data.length : "map"}
    </div>
  ),
}));

const baseChild = {
  name: "Child One",
  drawings: [{ id: "d1" }, { id: "d2" }],
  metricValues: {
    totalSessions: 2,
    sessionTrendPercentage: 10,
    totalWordCount: 100,
    averageWordCount: 50,
    averageIntimacyScore: 0.5,
    averageStrokeCount: 8,
    averageNumberColors: 3,
    averageFilledArea: 25,
    averageNumberObjects: 2,
    mostCommonObjects: [["ball", 3], ["tree", 1]],
    objectDiversity: 0.5,
  },
  sessionFrequencyData: [{ label: "Jan", value: 2 }],
  wordCountData: [{ label: "S1", value: 40 }, { label: "S2", value: 60 }],
  speechTimeData: [{ label: "S1", value: 10 }, { label: "S2", value: 20 }],
  intimacyScoreData: [{ label: "S1", value: 0.4 }, { label: "S2", value: 0.6 }],
};

function renderWithRouter(childId = "c1") {
  return render(
    <MemoryRouter initialEntries={[`/pixelbot/session/${childId}`]}>
      <Routes>
        <Route path="/pixelbot/session/:childId" element={<ChildRecapView />} />
      </Routes>
    </MemoryRouter>
  );
}

describe("ChildRecapView", () => {
  const printMock = vi.fn();
  let addEventListenerSpy;
  let removeEventListenerSpy;

  beforeEach(() => {
    vi.clearAllMocks();
    usePixelbotRecap.mockReturnValue({ child: baseChild, isLoading: false });
    window.print = printMock;
    addEventListenerSpy = vi.spyOn(window, "addEventListener");
    removeEventListenerSpy = vi.spyOn(window, "removeEventListener");
  });

  afterEach(() => {
    document.body.className = "";
    addEventListenerSpy.mockRestore();
    removeEventListenerSpy.mockRestore();
  });

  it("renders the recap page with all major sections and metrics", () => {
    renderWithRouter();

    expect(screen.getByText("Child One - Recap")).toBeInTheDocument();

    expect(screen.getByTestId("dashboard-card-recap-drawings")).toBeInTheDocument();
    expect(screen.getByTestId("dashboard-card-recap-speech")).toBeInTheDocument();
    expect(screen.getByTestId("dashboard-card-recap-sessions")).toBeInTheDocument();
    expect(screen.getByTestId("dashboard-card-recap-word-count")).toBeInTheDocument();
    expect(screen.getByTestId("dashboard-card-recap-intimacy")).toBeInTheDocument();
    expect(screen.getByTestId("dashboard-card-recap-story")).toBeInTheDocument();

    expect(screen.getByTestId("image-carousel")).toHaveTextContent("images:2");
    expect(screen.getByTestId("bar-chart")).toHaveTextContent(
      "avg:50-y:Words-x:Sessions-points:2"
    );
    expect(screen.getAllByTestId("line-chart")).toHaveLength(3);

    expect(screen.getByText("Average Stroke Count:")).toBeInTheDocument();
    expect(screen.getByText("8.0")).toBeInTheDocument();
    expect(screen.getByText("Average Colors Used:")).toBeInTheDocument();
    expect(screen.getByText("3.0")).toBeInTheDocument();
    expect(screen.getByText("Average Filled Area:")).toBeInTheDocument();
    expect(screen.getByText("25.0%")).toBeInTheDocument();

    expect(screen.getByText("Total Sessions")).toBeInTheDocument();
    expect(screen.getByText("2")).toBeInTheDocument();
    expect(screen.getByText("↑ 10% from last month")).toBeInTheDocument();

    expect(screen.getByText(/Total Word Count:/)).toBeInTheDocument();
    expect(screen.getByText("100")).toBeInTheDocument();

    expect(screen.getByText("Average Number of Objects")).toBeInTheDocument();
    expect(screen.getByText("2.0")).toBeInTheDocument();
    expect(screen.getByText("Most Common Objects")).toBeInTheDocument();
    expect(screen.getByText("ball")).toBeInTheDocument();
    expect(screen.getByText("tree")).toBeInTheDocument();
    expect(screen.getByText("Object Diversity")).toBeInTheDocument();
    expect(screen.getByText("0.5")).toBeInTheDocument();
    expect(screen.getByText("unique objects")).toBeInTheDocument();
  });

  it("shows loading when child is loading", () => {
    usePixelbotRecap.mockReturnValue({ child: null, isLoading: true });

    renderWithRouter();

    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("shows loading when child is missing", () => {
    usePixelbotRecap.mockReturnValue({ child: null, isLoading: false });

    renderWithRouter();

    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("renders a negative session trend correctly", () => {
    usePixelbotRecap.mockReturnValue({
      child: {
        ...baseChild,
        metricValues: {
          ...baseChild.metricValues,
          sessionTrendPercentage: -12,
        },
      },
      isLoading: false,
    });

    renderWithRouter();

    expect(screen.getByText("↓ 12% from last month")).toBeInTheDocument();
  });

  it("renders a zero session trend correctly", () => {
    usePixelbotRecap.mockReturnValue({
      child: {
        ...baseChild,
        metricValues: {
          ...baseChild.metricValues,
          sessionTrendPercentage: 0,
        },
      },
      isLoading: false,
    });

    renderWithRouter();

    expect(screen.getByText(/0% from last month/)).toBeInTheDocument();
  });

  it("renders no data available when there are no most common objects", () => {
    usePixelbotRecap.mockReturnValue({
      child: {
        ...baseChild,
        metricValues: {
          ...baseChild.metricValues,
          mostCommonObjects: [],
        },
      },
      isLoading: false,
    });

    renderWithRouter();

    expect(screen.getByText("No data available")).toBeInTheDocument();
  });

  it("renders empty drawings through the carousel when there are no drawings", () => {
    usePixelbotRecap.mockReturnValue({
      child: {
        ...baseChild,
        drawings: [],
      },
      isLoading: false,
    });

    renderWithRouter();

    expect(screen.getByTestId("image-carousel")).toHaveTextContent("images:0");
  });

  it("calls usePixelbotRecap with the route childId", () => {
    renderWithRouter("child-123");

    expect(usePixelbotRecap).toHaveBeenCalledWith("child-123");
  });

  it("prints the full page when the header print icon is clicked and cleans up after print", () => {
    renderWithRouter();

    const svg = document.querySelector(".print-icon");
    fireEvent.click(svg);

    expect(window.print).toHaveBeenCalled();
    expect(document.body.classList.contains("printing-single-widget")).toBe(true);

    const recapView = document.getElementById("child-recap-view");
    expect(recapView.classList.contains("print-visible")).toBe(true);
    expect(addEventListenerSpy).toHaveBeenCalledWith("afterprint", expect.any(Function));

    fireEvent(window, new Event("afterprint"));

    expect(document.body.classList.contains("printing-single-widget")).toBe(false);
    expect(recapView.classList.contains("print-visible")).toBe(false);
    expect(removeEventListenerSpy).toHaveBeenCalledWith(
      "afterprint",
      expect.any(Function)
    );
  });

  it("prints an individual card when a card print button is clicked and cleans up after print", () => {
    renderWithRouter();

    fireEvent.click(screen.getByText("Print Drawing(s)"));

    expect(window.print).toHaveBeenCalled();

    const drawingsCard = screen.getByTestId("dashboard-card-recap-drawings");
    expect(document.body.classList.contains("printing-single-widget")).toBe(true);
    expect(drawingsCard.classList.contains("print-visible")).toBe(true);
    expect(addEventListenerSpy).toHaveBeenCalledWith("afterprint", expect.any(Function));

    fireEvent(window, new Event("afterprint"));

    expect(document.body.classList.contains("printing-single-widget")).toBe(false);
    expect(drawingsCard.classList.contains("print-visible")).toBe(false);
    expect(removeEventListenerSpy).toHaveBeenCalledWith(
      "afterprint",
      expect.any(Function)
    );
  });

  it("passes expected props into chart mocks", () => {
    renderWithRouter();

    const lineChartTexts = screen
      .getAllByTestId("line-chart")
      .map((node) => node.textContent);

    expect(lineChartTexts).toHaveLength(3);
    expect(lineChartTexts).toEqual(
      expect.arrayContaining([
        expect.stringContaining("y:Minutes-x:Sessions"),
        expect.stringContaining("y:Sessions-x:Month"),
        expect.stringContaining("y:Score-x:Sessions-avg:0.5"),
      ])
    );
  });

  it("prints recap-speech card when its print button is clicked", () => {
    renderWithRouter();

    const card = document.getElementById("recap-speech");
    fireEvent.click(screen.getByText("Print Speech Time"));

    expect(card).toHaveClass("print-visible");
    expect(document.body).toHaveClass("printing-single-widget");
    expect(window.print).toHaveBeenCalledTimes(1);
  });

  it("prints recap-sessions card when its print button is clicked", () => {
    renderWithRouter();

    const card = document.getElementById("recap-sessions");
    fireEvent.click(screen.getByText("Print Total Sessions"));

    expect(card).toHaveClass("print-visible");
    expect(document.body).toHaveClass("printing-single-widget");
    expect(window.print).toHaveBeenCalledTimes(1);
  });

  it("prints recap-word-count card when its print button is clicked", () => {
    renderWithRouter();

    const card = document.getElementById("recap-word-count");
    fireEvent.click(screen.getByText("Print Word Count"));

    expect(card).toHaveClass("print-visible");
    expect(document.body).toHaveClass("printing-single-widget");
    expect(window.print).toHaveBeenCalledTimes(1);
  });

  it("prints recap-intimacy card when its print button is clicked", () => {
    renderWithRouter();

    const card = document.getElementById("recap-intimacy");
    fireEvent.click(screen.getByText("Print Intimacy Score"));

    expect(card).toHaveClass("print-visible");
    expect(document.body).toHaveClass("printing-single-widget");
    expect(window.print).toHaveBeenCalledTimes(1);
  });

  it("prints recap-story card when its print button is clicked", () => {
    renderWithRouter();

    const card = document.getElementById("recap-story");
    fireEvent.click(screen.getByText("Print Story Metrics"));

    expect(card).toHaveClass("print-visible");
    expect(document.body).toHaveClass("printing-single-widget");
    expect(window.print).toHaveBeenCalledTimes(1);
  });

  it("falls back to plain window.print when a recap print target element is missing", () => {
    renderWithRouter();

    const drawingsCard = document.getElementById("recap-drawings");
    drawingsCard.id = "recap-drawings-missing";

    fireEvent.click(screen.getByText("Print Drawing(s)"));

    expect(window.print).toHaveBeenCalledTimes(1);
    expect(document.body).not.toHaveClass("printing-single-widget");
    expect(addEventListenerSpy).not.toHaveBeenCalledWith(
      "afterprint",
      expect.any(Function)
    );
  });
});