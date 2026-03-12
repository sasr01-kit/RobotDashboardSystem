import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { FeedbackEntryBlock } from "../../modules/turtlebot/components/FeedbackEntryBlock";

//Tests for FeedbackEntryBlock to ensure it renders the entry fields and applies correct classes based on feedback value
describe("FeedbackEntryBlock", () => {
  it("renders all entry fields", () => {
    const entry = {
      startPoint: "A",
      endPoint: "B",
      duration: "12s",
      feedback: "good",
    };

    render(<FeedbackEntryBlock entry={entry} />);

    expect(screen.getByText("A")).toBeInTheDocument();
    expect(screen.getByText("B")).toBeInTheDocument();
    expect(screen.getByText("12s")).toBeInTheDocument();
    expect(screen.getByText("good")).toBeInTheDocument();
  });

  it('applies the "good" feedback class when feedback is good', () => {
    const entry = {
      startPoint: "Room 1",
      endPoint: "Room 2",
      duration: "8s",
      feedback: "good",
    };

    render(<FeedbackEntryBlock entry={entry} />);

    const feedbackTag = screen.getByText("good");
    expect(feedbackTag).toHaveClass("feedback-tag");
    expect(feedbackTag).toHaveClass("good");
    expect(feedbackTag).not.toHaveClass("bad");
  });

  it('applies the "bad" feedback class when feedback is not good', () => {
    const entry = {
      startPoint: "Room 1",
      endPoint: "Room 2",
      duration: "8s",
      feedback: "bad",
    };

    render(<FeedbackEntryBlock entry={entry} />);

    const feedbackTag = screen.getByText("bad");
    expect(feedbackTag).toHaveClass("feedback-tag");
    expect(feedbackTag).toHaveClass("bad");
    expect(feedbackTag).not.toHaveClass("good");
  });
});