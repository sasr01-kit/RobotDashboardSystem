import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import MetricCard from "../../modules/pixelbot/components/MetricCard";

// Tests for MetricCard to ensure it renders title, value, and unit correctly
describe("MetricCard", () => {
  it("renders title, value, and unit", () => {
    render(
      <MetricCard
        title="Sessions"
        value={42}
        unit="%"
      />
    );

    expect(screen.getByText("Sessions")).toBeInTheDocument();
    expect(screen.getByText("42%")).toBeInTheDocument();
  });

  it("renders icon when provided", () => {
    render(
      <MetricCard
        title="Battery"
        value={90}
        unit="%"
        icon={<span data-testid="metric-icon">🔋</span>}
      />
    );

    expect(screen.getByTestId("metric-icon")).toBeInTheDocument();
  });

  it("renders trend subtitle when trendValue is truthy", () => {
    render(
      <MetricCard
        title="Usage"
        value={12}
        unit="h"
        trendValue="+2"
      />
    );

    expect(screen.getByText("+2h than last month")).toBeInTheDocument();
  });

  it("does not render trend subtitle when trendValue is missing", () => {
    render(
      <MetricCard
        title="Usage"
        value={12}
        unit="h"
      />
    );

    expect(screen.queryByText(/than last month/i)).not.toBeInTheDocument();
  });

  it("does not render trend subtitle when trendValue is 0", () => {
    render(
      <MetricCard
        title="Usage"
        value={12}
        unit="h"
        trendValue={0}
      />
    );

    expect(screen.queryByText(/than last month/i)).not.toBeInTheDocument();
  });
});