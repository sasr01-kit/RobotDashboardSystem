import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import DashboardCard from "../../modules/pixelbot/components/DashboardCard";

// Tests for DashboardCard to ensure it renders title, subtitle, icon, and print functionality correctly based on props
describe("DashboardCard", () => {
  it("renders title and children", () => {
    render(
      <DashboardCard id="card-1" title="My Card">
        <div>Card content</div>
      </DashboardCard>
    );

    expect(screen.getByText("My Card")).toBeInTheDocument();
    expect(screen.getByText("Card content")).toBeInTheDocument();
  });

  it("renders subtitle when provided", () => {
    render(
      <DashboardCard
        id="card-2"
        title="Summary"
        subtitle="This is a subtitle"
      >
        <div>Content</div>
      </DashboardCard>
    );

    expect(screen.getByText("This is a subtitle")).toBeInTheDocument();
  });

  it("does not render subtitle when not provided", () => {
    render(
      <DashboardCard id="card-3" title="Summary">
        <div>Content</div>
      </DashboardCard>
    );

    expect(
      screen.queryByText("This is a subtitle")
    ).not.toBeInTheDocument();
  });

  it("renders icon when provided", () => {
    render(
      <DashboardCard
        id="card-4"
        title="With Icon"
        icon={<span data-testid="card-icon">⭐</span>}
      >
        <div>Content</div>
      </DashboardCard>
    );

    expect(screen.getByTestId("card-icon")).toBeInTheDocument();
  });

  it("does not render print icon when onPrint is not provided", () => {
    render(
      <DashboardCard id="card-5" title="No Print">
        <div>Content</div>
      </DashboardCard>
    );

    expect(screen.queryByLabelText("Print")).not.toBeInTheDocument();
  });

  it("renders print icon when onPrint is provided", () => {
    render(
      <DashboardCard id="card-6" title="Printable" onPrint={vi.fn()}>
        <div>Content</div>
      </DashboardCard>
    );

    expect(screen.getByLabelText("Print")).toBeInTheDocument();
  });

  it("calls onPrint when print icon is clicked", () => {
    const onPrint = vi.fn();

    render(
      <DashboardCard id="card-7" title="Printable" onPrint={onPrint}>
        <div>Content</div>
      </DashboardCard>
    );

    fireEvent.click(screen.getByLabelText("Print"));

    expect(onPrint).toHaveBeenCalledTimes(1);
  });

  it("applies the id and custom className", () => {
    render(
      <DashboardCard
        id="card-8"
        title="Styled Card"
        className="teal-header"
      >
        <div>Content</div>
      </DashboardCard>
    );

    const card = document.getElementById("card-8");
    expect(card).toBeInTheDocument();
    expect(card).toHaveClass("dashboard-card");
    expect(card).toHaveClass("teal-header");
  });
});