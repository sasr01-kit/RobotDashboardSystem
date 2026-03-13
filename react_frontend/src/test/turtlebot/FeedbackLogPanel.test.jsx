import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { FeedbackLogPanel } from "../../modules/turtlebot/components/FeedbackLogPanel";

// Mocks animations to make testing more focused on functionality and more stable
vi.mock("framer-motion", () => ({
  motion: {
    div: ({ children, ...props }) => <div {...props}>{children}</div>,
  },
}));

// Tests for FeedbackLogPanel to ensure it renders headers, empty state, and list of feedback entries correctly
describe("FeedbackLogPanel", () => {
  it("renders the header labels", () => {
    render(<FeedbackLogPanel entries={[]} />);

    expect(screen.getByText("Start Point")).toBeInTheDocument();
    expect(screen.getByText("End Point")).toBeInTheDocument();
    expect(screen.getByText("Duration")).toBeInTheDocument();
    expect(screen.getByText("Feedback")).toBeInTheDocument();
  });

  it("renders empty state when there are no entries", () => {
    render(<FeedbackLogPanel entries={[]} />);

    expect(screen.getByText("No feedback entries yet.")).toBeInTheDocument();
  });

  it("renders a list of feedback entries", () => {
    const entries = [
      {
        id: 1,
        startPoint: "A",
        endPoint: "B",
        duration: "10s",
        feedback: "good",
      },
      {
        id: 2,
        startPoint: "C",
        endPoint: "D",
        duration: "15s",
        feedback: "bad",
      },
    ];

    render(<FeedbackLogPanel entries={entries} />);

    expect(screen.getByText("A")).toBeInTheDocument();
    expect(screen.getByText("B")).toBeInTheDocument();
    expect(screen.getByText("10s")).toBeInTheDocument();
    expect(screen.getByText("good")).toBeInTheDocument();

    expect(screen.getByText("C")).toBeInTheDocument();
    expect(screen.getByText("D")).toBeInTheDocument();
    expect(screen.getByText("15s")).toBeInTheDocument();
    expect(screen.getByText("bad")).toBeInTheDocument();

    expect(screen.queryByText("No feedback entries yet.")).not.toBeInTheDocument();
  });
});