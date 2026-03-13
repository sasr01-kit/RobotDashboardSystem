import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import BarChart from "../../modules/pixelbot/components/BarChart";

// Mocks Highcharts and HighchartsReact to allow testing of BarChart without rendering actual charts
vi.mock("highcharts", () => ({
  default: {},
}));

vi.mock("highcharts-react-official", () => ({
  default: ({ options }) => (
    <div data-testid="highcharts-mock">{JSON.stringify(options)}</div>
  ),
}));

// Tests for BarChart to ensure it handles empty data and builds chart options correctly based on props
describe("BarChart", () => {
  it("renders empty state when data is missing", () => {
    render(<BarChart data={null} />);
    expect(screen.getByText("No data available")).toBeInTheDocument();
  });

  it("renders empty state when data is empty", () => {
    render(<BarChart data={[]} />);
    expect(screen.getByText("No data available")).toBeInTheDocument();
  });

  it("builds chart options correctly", () => {
    const data = [
      { label: "Session 1", value: 5 },
      { label: "Session 2", value: 8 },
    ];

    render(
      <BarChart
        data={data}
        xAxisLabel="Sessions"
        yAxisLabel="Count"
        averageLine={6.5}
      />
    );

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);

    expect(options.chart.type).toBe("column");
    expect(options.xAxis.categories).toEqual(["S1", "S2"]);
    expect(options.xAxis.title.text).toBe("Sessions");
    expect(options.yAxis.title.text).toBe("Count");
    expect(options.series[0].name).toBe("Count");
    expect(options.series[0].data).toEqual([5, 8]);

    expect(options.yAxis.plotLines).toHaveLength(1);
    expect(options.yAxis.plotLines[0].value).toBe(6.5);
    expect(options.yAxis.plotLines[0].label.text).toBe("Average: 6.5");
  });

  it("omits average line when averageLine is not provided", () => {
    const data = [{ label: "Session 3", value: 4 }];

    render(<BarChart data={data} yAxisLabel="Value" />);

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);

    expect(options.yAxis.plotLines).toEqual([]);
  });

  it('uses "Value" as the default series name when yAxisLabel is missing', () => {
    const data = [{ label: "Session 1", value: 9 }];

    render(<BarChart data={data} />);

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);

    expect(options.series[0].name).toBe("Value");
  });
});