import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { FeedbackButton } from "../../modules/turtlebot/components/FeedbackButton";
import { useWebSocketContext } from "../../modules/turtlebot/websocketUtil/WebsocketContext";

vi.mock("../../modules/turtlebot/websocketUtil/WebsocketContext", () => ({
  useWebSocketContext: vi.fn(),
}));

// Mocks animations to make testing more focused on functionality and more stable
vi.mock("framer-motion", () => ({
  motion: {
    button: ({ children, ...props }) => <button {...props}>{children}</button>,
  },
}));

// Tests for FeedbackButton to ensure it renders the label and sends correct feedback on click
describe("FeedbackButton", () => {
  const send = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    useWebSocketContext.mockReturnValue({ send });
  });

  it("renders the label", () => {
    render(
      <FeedbackButton className="good" label="GOOD" goalId="goal-1" />
    );

    expect(screen.getByRole("button", { name: "GOOD" })).toBeInTheDocument();
  });

  it('sends "good" feedback when label is GOOD', () => {
    render(
      <FeedbackButton className="good" label="GOOD" goalId="goal-1" />
    );

    fireEvent.click(screen.getByRole("button", { name: "GOOD" }));

    expect(send).toHaveBeenCalledWith({
      type: "GOAL_FEEDBACK",
      goalId: "goal-1",
      feedback: "good",
    });
  });

  it('sends "bad" feedback when label is not GOOD', () => {
    render(
      <FeedbackButton className="bad" label="BAD" goalId="goal-2" />
    );

    fireEvent.click(screen.getByRole("button", { name: "BAD" }));

    expect(send).toHaveBeenCalledWith({
      type: "GOAL_FEEDBACK",
      goalId: "goal-2",
      feedback: "bad",
    });
  });

  it("applies the provided className", () => {
    render(
      <FeedbackButton className="good-btn" label="GOOD" goalId="goal-1" />
    );

    const button = screen.getByRole("button", { name: "GOOD" });
    expect(button).toHaveClass("feedback-button");
    expect(button).toHaveClass("good-btn");
  });
});