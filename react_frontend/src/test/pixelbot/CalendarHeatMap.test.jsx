import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import CalendarHeatMap from "../../modules/pixelbot/components/CalendarHeatMap";

// Mocks Highcharts and HighchartsReact to allow testing of CalendarHeatMap without rendering actual charts
let capturedOptions;

vi.mock("highcharts", () => ({
  default: {},
}));

vi.mock("highcharts-react-official", () => ({
  default: ({ options }) => {
    capturedOptions = options;
    return <div data-testid="highcharts-mock">chart</div>;
  },
}));

vi.mock(
  "highcharts/modules/heatmap",
  () => ({
    default: vi.fn(() => {}),
  }),
  { virtual: true }
);

const sampleColorScale = {
  dataClasses: [
    { from: 0, to: 0 },
    { from: 1, to: 2 },
    { from: 3, to: 5 },
    { from: 6, to: 8 },
    { from: 9, to: 12 },
  ],
};

const formatterData = [
  { x: 0, y: 0, value: 1, date: new Date("2025-01-03") },
  { x: 0, y: 1, value: 2, date: new Date("2025-01-01") },

  { x: 1, y: 0, value: 3, date: new Date("2025-01-10") },
  { x: 1, y: 1, value: 4, date: new Date("2025-01-08") },

  { x: 2, y: 0, value: 5, date: new Date("2025-02-02") },
  { x: 2, y: 1, value: 6, date: new Date("2025-02-01") },
];

async function renderHeatmap(data = formatterData, colorScaleArg = sampleColorScale, onPrint = vi.fn()) {
  capturedOptions = undefined;

  const renderResult = render(
    <CalendarHeatMap
      id="heatmap"
      data={data}
      colorScale={colorScaleArg}
      onPrint={onPrint}
    />
  );

  await screen.findByTestId("highcharts-mock");
  return { ...renderResult, options: capturedOptions, onPrint };
}

async function renderHeatmapFromFreshImportWithHeatmapModule(heatmapModuleMock) {
  vi.resetModules();

  let localOptions;

  vi.doMock("highcharts", () => ({
    default: {},
  }));

  vi.doMock("highcharts-react-official", () => ({
    default: ({ options }) => {
      localOptions = options;
      return <div data-testid="highcharts-mock-fresh">chart</div>;
    },
  }));

  vi.doMock("highcharts/modules/heatmap", heatmapModuleMock, { virtual: true });

  const { default: FreshCalendarHeatMap } = await import(
    "../../modules/pixelbot/components/CalendarHeatMap"
  );

  render(
    <FreshCalendarHeatMap
      id="heatmap-fresh"
      data={formatterData}
      colorScale={sampleColorScale}
      onPrint={vi.fn()}
    />
  );

  await screen.findByTestId("highcharts-mock-fresh");
  return localOptions;
}

// Tests for CalendarHeatMap to ensure it loads the heatmap module, builds chart options correctly, 
// and handles edge cases in formatters and color scale enrichment
describe("CalendarHeatMap", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    capturedOptions = undefined;
  });

  it("renders chart after heatmap module loads", async () => {
    await renderHeatmap();

    expect(screen.getByText("Robot Usage History")).toBeInTheDocument();
    expect(screen.getByTestId("highcharts-mock")).toBeInTheDocument();
  });

  it("renders enriched legend labels", async () => {
    await renderHeatmap();

    expect(screen.getByText("No usage")).toBeInTheDocument();
    expect(screen.getByText("Low")).toBeInTheDocument();
    expect(screen.getByText("Medium")).toBeInTheDocument();
    expect(screen.getByText("High")).toBeInTheDocument();
    expect(screen.getByText("Intense")).toBeInTheDocument();

    expect(screen.getByText("0")).toBeInTheDocument();
    expect(screen.getByText("1–2")).toBeInTheDocument();
    expect(screen.getByText("3–5")).toBeInTheDocument();
    expect(screen.getByText("6–8")).toBeInTheDocument();
    expect(screen.getByText("9–12")).toBeInTheDocument();
  });

  it("calls onPrint when the print icon is clicked", async () => {
    const onPrint = vi.fn();
    const { container } = await renderHeatmap(formatterData, sampleColorScale, onPrint);

    fireEvent.click(container.querySelector(".print-icon"));
    expect(onPrint).toHaveBeenCalledTimes(1);
  });

  it("builds expected chart options", async () => {
    const { options } = await renderHeatmap();

    expect(options.chart.type).toBe("heatmap");
    expect(options.series[0].name).toBe("Robot Usage");
    expect(options.series[0].data).toHaveLength(6);
    expect(options.yAxis.categories).toEqual([
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
      "Sunday",
    ]);
  });

  it("handles missing colorScale gracefully", async () => {
    render(
      <CalendarHeatMap
        id="heatmap"
        data={formatterData}
        colorScale={undefined}
        onPrint={vi.fn()}
      />
    );

    await screen.findByTestId("highcharts-mock");

    expect(capturedOptions.colorAxis.dataClasses).toEqual([]);
  });

  it("xAxis formatter returns empty string when there is no data for the week", async () => {
    const { options } = await renderHeatmap();

    const result = options.xAxis.labels.formatter.call({ value: 99 });

    expect(result).toBe("");
  });

  it("xAxis formatter returns month name when previous week does not exist", async () => {
    const { options } = await renderHeatmap();

    const result = options.xAxis.labels.formatter.call({ value: 0 });

    expect(result).toBe("January");
  });

  it("xAxis formatter returns empty string when current and previous week are in the same month", async () => {
    const { options } = await renderHeatmap();

    const result = options.xAxis.labels.formatter.call({ value: 1 });

    expect(result).toBe("");
  });

  it("xAxis formatter returns month name when the month changes from previous week", async () => {
    const { options } = await renderHeatmap();

    const result = options.xAxis.labels.formatter.call({ value: 2 });

    expect(result).toBe("February");
  });

  it("xAxis formatter picks earliest date within a week using reduce comparison", async () => {
    const trickyData = [
      { x: 0, y: 0, value: 1, date: new Date("2025-01-09") },
      { x: 0, y: 1, value: 2, date: new Date("2025-01-02") },
    ];

    const { options } = await renderHeatmap(trickyData);

    const result = options.xAxis.labels.formatter.call({ value: 0 });
    expect(result).toBe("January");
  });

  it("xAxis formatter compares against earliest date of previous week using reduce", async () => {
    const trickyData = [
      { x: 0, y: 0, value: 1, date: new Date("2025-01-10") },
      { x: 0, y: 1, value: 2, date: new Date("2025-01-05") },
      { x: 1, y: 0, value: 3, date: new Date("2025-02-03") },
      { x: 1, y: 1, value: 4, date: new Date("2025-02-01") },
    ];

    const { options } = await renderHeatmap(trickyData);

    const result = options.xAxis.labels.formatter.call({ value: 1 });
    expect(result).toBe("February");
  });

  it("xAxis formatter handles current-week reduce comparator false branch", async () => {
    const orderedWeekData = [
      { x: 0, y: 0, value: 1, date: new Date("2025-01-02") },
      { x: 0, y: 1, value: 2, date: new Date("2025-01-09") },
    ];

    const { options } = await renderHeatmap(orderedWeekData);

    const result = options.xAxis.labels.formatter.call({ value: 0 });
    expect(result).toBe("January");
  });

  it("xAxis formatter handles previous-week reduce comparator false branch", async () => {
    const orderedPrevWeekData = [
      { x: 0, y: 0, value: 1, date: new Date("2025-01-05") },
      { x: 0, y: 1, value: 2, date: new Date("2025-01-10") },
      { x: 1, y: 0, value: 3, date: new Date("2025-02-01") },
      { x: 1, y: 1, value: 4, date: new Date("2025-02-03") },
    ];

    const { options } = await renderHeatmap(orderedPrevWeekData);

    const result = options.xAxis.labels.formatter.call({ value: 1 });
    expect(result).toBe("February");
  });

  it("tooltip formatter returns formatted date and value", async () => {
    const { options } = await renderHeatmap();

    const result = options.tooltip.formatter.call({
      point: {
        date: new Date("2025-02-01"),
        value: 6,
      },
    });

    expect(result).toContain("Sessions:");
    expect(result).toContain("<b>6</b>");
    expect(result).toContain("<b>");
    expect(result).toContain("<br/>");
  });

  it("enriches color classes correctly", async () => {
    const { options } = await renderHeatmap();

    expect(options.colorAxis.dataClasses[0]).toMatchObject({
      from: 0,
      to: 0,
      safeName: "No usage",
      label: "0",
      color: "#ebedf0",
    });

    expect(options.colorAxis.dataClasses[1]).toMatchObject({
      from: 1,
      to: 2,
      safeName: "Low",
      label: "1–2",
      color: "#c6e48b",
    });

    expect(options.colorAxis.dataClasses[2]).toMatchObject({
      from: 3,
      to: 5,
      safeName: "Medium",
      label: "3–5",
      color: "#7bc96f",
    });
  });

  it("uses fallback legend name and color for classes beyond predefined buckets", async () => {
    const extendedScale = {
      dataClasses: [
        { from: 0, to: 0 },
        { from: 1, to: 2 },
        { from: 3, to: 5 },
        { from: 6, to: 8 },
        { from: 9, to: 12 },
        { from: 13, to: 20 },
      ],
    };

    const { options } = await renderHeatmap(formatterData, extendedScale);

    expect(options.colorAxis.dataClasses[5]).toMatchObject({
      safeName: "Level 6",
      color: "#196127",
      label: "13–20",
    });
  });

  it("loads even when imported heatmap module is not a function", async () => {
    const options = await renderHeatmapFromFreshImportWithHeatmapModule(() => ({
      default: undefined,
      marker: "not-a-function",
    }));

    expect(screen.getByTestId("highcharts-mock-fresh")).toBeInTheDocument();
    expect(options.series[0].name).toBe("Robot Usage");
  });
});