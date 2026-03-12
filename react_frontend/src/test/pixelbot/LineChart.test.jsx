import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import LineChart from "../../modules/pixelbot/components/LineChart";

// Tests for LineChart to ensure it renders empty state when data is missing, 
// builds chart options correctly for different data formats, and handles edge cases
vi.mock("highcharts", () => ({
  default: {},
}));

vi.mock("highcharts-react-official", () => ({
  default: ({ options }) => (
    <div data-testid="highcharts-mock">{JSON.stringify(options)}</div>
  ),
}));

describe("LineChart", () => {
  it("renders empty state when data is missing", () => {
    render(<LineChart data={null} />);
    expect(screen.getByText("No data available")).toBeInTheDocument();
  });

  it("renders empty state for empty array", () => {
    render(<LineChart data={[]} />);
    expect(screen.getByText("No data available")).toBeInTheDocument();
  });

  it("renders empty state for empty Map", () => {
    render(<LineChart data={new Map()} />);
    expect(screen.getByText("No data available")).toBeInTheDocument();
  });

  it("builds chart options correctly for Map input", () => {
    const data = new Map([
      [
        "Child A",
        [
          { label: "Week 1", value: 2 },
          { label: "Week 2", value: 4 },
        ],
      ],
      [
        "Child B",
        [
          { label: "Week 1", value: 1 },
          { label: "Week 2", value: 3 },
        ],
      ],
    ]);

    render(
      <LineChart
        data={data}
        xAxisLabel="Weeks"
        yAxisLabel="Count"
        averageLine={2.5}
      />
    );

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);

    expect(options.chart.type).toBe("line");
    expect(options.xAxis.categories).toEqual(["Week 1", "Week 2"]);
    expect(options.xAxis.title.text).toBe("Weeks");
    expect(options.yAxis.title.text).toBe("Count");

    expect(options.series).toHaveLength(2);
    expect(options.series[0]).toMatchObject({
      name: "Child A",
      data: [2, 4],
    });
    expect(options.series[1]).toMatchObject({
      name: "Child B",
      data: [1, 3],
    });

    expect(options.legend.enabled).toBe(true);
    expect(options.yAxis.plotLines).toHaveLength(1);
    expect(options.yAxis.plotLines[0].value).toBe(2.5);
    expect(options.yAxis.plotLines[0].label.text).toBe("Average: 2.5");
  });

  it("builds chart options correctly for legacy array-of-series input", () => {
    const data = [
      { name: "Speech", data: [5, 7, 2] },
      { name: "Drawing", data: [3, 4, 1] },
    ];

    render(<LineChart data={data} />);

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
    expect(options.xAxis.categories).toEqual(["S1", "S2", "S3"]);
    expect(options.legend.enabled).toBe(true);
  });

  it("builds chart options correctly for simple array input", () => {
    const data = [
      { label: "Day 1", value: 8 },
      { label: "Day 2", value: 6 },
    ];

    render(<LineChart data={data} yAxisLabel="Sessions" />);

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);

    expect(options.series).toHaveLength(1);
    expect(options.series[0]).toMatchObject({
      name: "Sessions",
      data: [8, 6],
    });
    expect(options.xAxis.categories).toEqual(["Day 1", "Day 2"]);
    expect(options.legend.enabled).toBe(false);
  });

  it('uses "Value" as default series name when yAxisLabel is missing', () => {
    const data = [{ label: "Day 1", value: 9 }];

    render(<LineChart data={data} />);

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);
    expect(options.series[0].name).toBe("Value");
  });

  it("disables grid lines when showGrid is false", () => {
    const data = [{ label: "Day 1", value: 9 }];

    render(<LineChart data={data} showGrid={false} />);

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);
    expect(options.xAxis.gridLineWidth).toBe(0);
    expect(options.yAxis.gridLineWidth).toBe(0);
  });

  it("omits average line when averageLine is not provided", () => {
    const data = [{ label: "Day 1", value: 9 }];

    render(<LineChart data={data} />);

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);
    expect(options.yAxis.plotLines).toEqual([]);
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

    render(<LineChart data={[{ label: "Day 1", value: 9 }]} />);

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);
    expect(options.series).toEqual([]);
    expect(options.xAxis.categories).toEqual([]);

    isArraySpy.mockRestore();
  });
});