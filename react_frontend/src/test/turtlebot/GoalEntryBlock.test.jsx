import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { GoalEntryBlock } from "../../modules/turtlebot/components/GoalEntryBlock.jsx";

// Mocks animations to make testing more focused on functionality and more stable
vi.mock("../../modules/turtlebot/components/FeedbackButton", () => ({
  FeedbackButton: ({ className, label, goalId }) => (
    <button data-testid={`feedback-${label.toLowerCase()}`} className={className}>
      {label}-{goalId}
    </button>
  ),
}));

// Tests for GoalEntryBlock to ensure it renders the goal log details and feedback buttons 
// with correct classes and labels based on the log data
describe("GoalEntryBlock", () => {
  it("renders goal log details", () => {
    const log = {
      id: "goal-123",
      timestamp: "12:30:00",
      goalType: "Navigation",
      fuzzy_output_goal: "0.82",
    };

    render(<GoalEntryBlock log={log} />);

    expect(screen.getByText("12:30:00")).toBeInTheDocument();
    expect(screen.getByText("Navigation goal")).toBeInTheDocument();
    expect(screen.getByText("Fuzzy-Logic: 0.82")).toBeInTheDocument();
  });

  it("renders GOOD and BAD feedback buttons with the correct goalId", () => {
    const log = {
      id: "goal-456",
      timestamp: "13:00:00",
      goalType: "Delivery",
      fuzzy_output_goal: "0.67",
    };

    render(<GoalEntryBlock log={log} />);

    expect(screen.getByTestId("feedback-good")).toHaveTextContent("GOOD-goal-456");
    expect(screen.getByTestId("feedback-bad")).toHaveTextContent("BAD-goal-456");
  });

  it("applies the expected feedback button classes", () => {
    const log = {
      id: "goal-789",
      timestamp: "14:00:00",
      goalType: "Escort",
      fuzzy_output_goal: "0.45",
    };

    render(<GoalEntryBlock log={log} />);

    expect(screen.getByTestId("feedback-good")).toHaveClass("good-feedback-button");
    expect(screen.getByTestId("feedback-bad")).toHaveClass("bad-feedback-button");
  });
});