import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import GeneralStatusBlock from "../../modules/turtlebot/components/GeneralStatusBlock.jsx";

// Mocks animations to make testing more focused on functionality and more stable
vi.mock("framer-motion", () => ({
  motion: {
    div: ({ children, ...props }) => <div {...props}>{children}</div>,
  },
}));

// Tests for GeneralStatusBlock to ensure it renders the icon, label, and status correctly, as well as
// handling null/undefined/empty status as "N/A"
describe("GeneralStatusBlock", () => {
  it("renders icon, label, and status", () => {
    render(
      <GeneralStatusBlock
        icon={<span data-testid="status-icon">🔋</span>}
        label="Battery"
        status="85%"
        statusClass="good"
      />
    );

    expect(screen.getByTestId("status-icon")).toBeInTheDocument();
    expect(screen.getByText("Battery")).toBeInTheDocument();
    expect(screen.getByText("85%")).toBeInTheDocument();
  });

  it('renders "N/A" when status is null', () => {
    render(
      <GeneralStatusBlock
        icon={<span>📶</span>}
        label="WiFi"
        status={null}
        statusClass="unknown"
      />
    );

    expect(screen.getByText("N/A")).toBeInTheDocument();
  });

  it('renders "N/A" when status is undefined', () => {
    render(
      <GeneralStatusBlock
        icon={<span>📶</span>}
        label="WiFi"
        status={undefined}
        statusClass="unknown"
      />
    );

    expect(screen.getByText("N/A")).toBeInTheDocument();
  });

  it('renders "N/A" when status is "null%"', () => {
    render(
      <GeneralStatusBlock
        icon={<span>🔋</span>}
        label="Battery"
        status="null%"
        statusClass="unknown"
      />
    );

    expect(screen.getByText("N/A")).toBeInTheDocument();
  });

  it('renders "N/A" when status is an empty string', () => {
    render(
      <GeneralStatusBlock
        icon={<span>🌐</span>}
        label="Network"
        status=""
        statusClass="unknown"
      />
    );

    expect(screen.getByText("N/A")).toBeInTheDocument();
  });

  it("applies the provided statusClass", () => {
    render(
      <GeneralStatusBlock
        icon={<span>🔋</span>}
        label="Battery"
        status="42%"
        statusClass="warning"
      />
    );

    const value = screen.getByText("42%");
    expect(value).toHaveClass("status-value");
    expect(value).toHaveClass("warning");
  });
});