import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import StackedBarChart from "../../modules/pixelbot/components/StackedBarChart";

// Tests for StackedBarChart to ensure it renders empty state when data is missing,
// builds chart options correctly for different data formats, and handles edge cases
vi.mock("highcharts", () => ({
  default: {},
}));

vi.mock("highcharts-react-official", () => ({
  default: ({ options }) => (
    <div data-testid="highcharts-mock">{JSON.stringify(options)}</div>
  ),
}));

describe("StackedBarChart", () => {
  it("renders empty state when data is missing", () => {
    render(<StackedBarChart data={null} />);
    expect(screen.getByText("No data available")).toBeInTheDocument();
  });

  it("renders empty state for empty array", () => {
    render(<StackedBarChart data={[]} />);
    expect(screen.getByText("No data available")).toBeInTheDocument();
  });

  it("renders empty state for empty Map", () => {
    render(<StackedBarChart data={new Map()} />);
    expect(screen.getByText("No data available")).toBeInTheDocument();
  });

  it("builds chart options correctly for Map input", () => {
    const data = new Map([
      [
        "Child A",
        [
          { label: "Intro", value: 2 },
          { label: "Play", value: 3 },
        ],
      ],
      [
        "Child B",
        [
          { label: "Intro", value: 1 },
          { label: "Play", value: 4 },
        ],
      ],
    ]);

    render(
      <StackedBarChart
        data={data}
        xAxisLabel="Activities"
        yAxisLabel="Count"
      />
    );

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);

    expect(options.chart.type).toBe("bar");
    expect(options.xAxis.categories).toEqual(["Intro", "Play"]);
    expect(options.xAxis.title.text).toBe("Activities");
    expect(options.yAxis.title.text).toBe("Count");

    expect(options.series).toHaveLength(2);
    expect(options.series[0]).toMatchObject({
      name: "Child A",
      data: [2, 3],
    });
    expect(options.series[1]).toMatchObject({
      name: "Child B",
      data: [1, 4],
    });
  });

  it("builds chart options correctly for legacy array-of-series input", () => {
    const data = [
      { name: "Speech", data: [5, 7, 2] },
      { name: "Drawing", data: [3, 4, 1] },
    ];

    render(<StackedBarChart data={data} />);

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);

    expect(options.series).toHaveLength(2);
    expect(options.series[0]).toMatchObject({
      name: "Speech",
      data: [5, 7, 2],
    });
    expect(options.series[1]).toMatchObject({
      name: "Drawing",
      data: [3, 4, 1],
    });

    expect(options.xAxis.categories).toEqual([
      "Session 1",
      "Session 2",
      "Session 3",
    ]);
  });

  it("builds chart options correctly for simple array input", () => {
    const data = [
      { label: "Week 1", value: 8 },
      { label: "Week 2", value: 6 },
    ];

    render(<StackedBarChart data={data} />);

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);

    expect(options.series).toHaveLength(1);
    expect(options.series[0]).toMatchObject({
      name: "Value",
      data: [8, 6],
    });

    expect(options.xAxis.categories).toEqual(["Week 1", "Week 2"]);
  });

  it("handles the defensive non-array path after hasData check", () => {
    const originalIsArray = Array.isArray;
    let callCount = 0;
    const isArraySpy = vi.spyOn(Array, "isArray").mockImplementation((value) => {
      callCount += 1;
      if (callCount === 1) return true;
      if (callCount === 2) return false;
      return originalIsArray(value);
    });

    render(<StackedBarChart data={[{ label: "Week 1", value: 8 }]} />);

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);
    expect(options.series).toEqual([]);
    expect(options.xAxis.categories).toEqual([]);

    isArraySpy.mockRestore();
  });
});