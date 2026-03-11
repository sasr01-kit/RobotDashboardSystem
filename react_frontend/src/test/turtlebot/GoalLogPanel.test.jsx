import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { GoalLogPanel } from "../../modules/turtlebot/components/GoalLogPanel.jsx";

// Mocks animations to make testing more focused on functionality and more stable
vi.mock("framer-motion", () => ({
  motion: {
    div: ({ children, ...props }) => <div {...props}>{children}</div>,
  },
}));

vi.mock("../../modules/turtlebot/components/GoalEntryBlock", () => ({
  GoalEntryBlock: ({ log }) => (
    <div data-testid="goal-entry-block">{log.goalType}-{log.id}</div>
  ),
}));

// Tests for GoalLogPanel to ensure it renders empty state, logs in reverse order, and stores refs correctly
describe("GoalLogPanel", () => {
  it("renders empty state when there are no logs", () => {
    const entryRefs = { current: {} };

    render(<GoalLogPanel logs={[]} entryRefs={entryRefs} />);

    expect(screen.getByText("No goal logs yet.")).toBeInTheDocument();
  });

  it("renders logs in reverse order", () => {
    const logs = [
      { id: "1", goalType: "First" },
      { id: "2", goalType: "Second" },
      { id: "3", goalType: "Third" },
    ];
    const entryRefs = { current: {} };

    render(<GoalLogPanel logs={logs} entryRefs={entryRefs} />);

    const rendered = screen.getAllByTestId("goal-entry-block");
    expect(rendered[0]).toHaveTextContent("Third-3");
    expect(rendered[1]).toHaveTextContent("Second-2");
    expect(rendered[2]).toHaveTextContent("First-1");
  });

  it("stores rendered elements in entryRefs.current by log id", () => {
    const logs = [
      { id: "a1", goalType: "Alpha" },
      { id: "b2", goalType: "Beta" },
    ];
    const entryRefs = { current: {} };

    render(<GoalLogPanel logs={logs} entryRefs={entryRefs} />);

    expect(entryRefs.current["a1"]).toBeTruthy();
    expect(entryRefs.current["b2"]).toBeTruthy();
    expect(entryRefs.current["a1"]).toBeInstanceOf(HTMLDivElement);
    expect(entryRefs.current["b2"]).toBeInstanceOf(HTMLDivElement);
  });

  it("does not render the empty state when logs exist", () => {
    const logs = [{ id: "1", goalType: "Only" }];
    const entryRefs = { current: {} };

    render(<GoalLogPanel logs={logs} entryRefs={entryRefs} />);

    expect(screen.queryByText("No goal logs yet.")).not.toBeInTheDocument();
    expect(screen.getByTestId("goal-entry-block")).toBeInTheDocument();
  });
});