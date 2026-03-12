import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { useTurtlebotFeedback } from "../../modules/turtlebot/hooks/useTurtlebotFeedback";
import { FeedbackSummaryChart } from "../../modules/turtlebot/components/FeedbackSummaryChart";

vi.mock("../../modules/turtlebot/hooks/useTurtlebotFeedback", () => ({
  useTurtlebotFeedback: vi.fn(),
}));

vi.mock("highcharts", () => ({
  default: {},
}));

vi.mock("highcharts-react-official", () => ({
  default: ({ options }) => (
    <div data-testid="highcharts-mock">{JSON.stringify(options)}</div>
  ),
}));

// Tests for FeedbackSummaryChart to ensure it renders the chart with correct feedback ratios and handles missing data properly
describe("FeedbackSummaryChart", () => {
  it("renders chart with feedback ratios", () => {
    useTurtlebotFeedback.mockReturnValue({
      feedbackSummaryDTO: {
        goodRatio: 70,
        badRatio: 30,
      },
    });

    render(<FeedbackSummaryChart />);

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);

    expect(options.chart.type).toBe("pie");
    expect(options.series[0].name).toBe("Feedback");

    expect(options.series[0].data[0]).toMatchObject({
      name: "GOOD",
      y: 70,
      color: "var(--success-green)",
    });

    expect(options.series[0].data[1]).toMatchObject({
      name: "BAD",
      y: 30,
      color: "var(--error-red)",
    });
  });

  it("defaults ratios to 0 when feedbackSummaryDTO is missing", () => {
    useTurtlebotFeedback.mockReturnValue({
      feedbackSummaryDTO: null,
    });

    render(<FeedbackSummaryChart />);

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);

    expect(options.series[0].data[0].y).toBe(0);
    expect(options.series[0].data[1].y).toBe(0);
  });

  it("uses 0 for missing goodRatio or badRatio", () => {
    useTurtlebotFeedback.mockReturnValue({
      feedbackSummaryDTO: {
        goodRatio: undefined,
        badRatio: undefined,
      },
    });

    render(<FeedbackSummaryChart />);

    const options = JSON.parse(screen.getByTestId("highcharts-mock").textContent);

    expect(options.series[0].data[0].y).toBe(0);
    expect(options.series[0].data[1].y).toBe(0);
  });
});