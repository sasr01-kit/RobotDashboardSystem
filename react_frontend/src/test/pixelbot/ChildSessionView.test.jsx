import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import ChildSessionView from "../../modules/pixelbot/pages/ChildSessionView";
import { usePixelbotSession } from "../../modules/pixelbot/hooks/usePixelbotSession";
import { usePixelbotChildren } from "../../modules/pixelbot/hooks/usePixelbotChildren";

// Tests for ChildSessionView to ensure it renders all sections correctly based on the child data,
// handles loading states, and that print functionality works as expected with proper cleanup after printing
vi.mock("../../modules/pixelbot/hooks/usePixelbotSession");
vi.mock("../../modules/pixelbot/hooks/usePixelbotChildren");

vi.mock("../../modules/pixelbot/components/DashboardCard", () => ({
  default: ({ id, title, subtitle, onPrint, children, className }) => (
    <div
      id={id}
      data-testid={`dashboard-card-${id}`}
      className={className || ""}
    >
      <div>{title}</div>
      {subtitle ? <div>{subtitle}</div> : null}
      {onPrint ? (
        <button
          type="button"
          data-testid={`print-${id}`}
          onClick={onPrint}
        >
          Print {id}
        </button>
      ) : null}
      <div>{children}</div>
    </div>
  ),
}));

vi.mock("../../modules/pixelbot/components/ImageCarousel", () => ({
  default: ({ images }) => (
    <div data-testid="image-carousel">{JSON.stringify(images)}</div>
  ),
}));

function renderWithRouter(childId = "c1", sessionId = "s1") {
  return render(
    <MemoryRouter initialEntries={[`/pixelbot/session/${childId}/${sessionId}`]}>
      <Routes>
        <Route
          path="/pixelbot/session/:childId/:sessionId"
          element={<ChildSessionView />}
        />
      </Routes>
    </MemoryRouter>
  );
}

const mockChildren = [
  {
    childId: "c1",
    name: "Child One",
  },
  {
    childId: "c2",
    name: "Child Two",
  },
];

const mockSession = {
  drawing: ["img1.png", "img2.png"],
  transcript: [
    { name: "Robot", description: "Hello there" },
    { name: "Child", description: "Hi!" },
  ],
  storySummary: [
    { name: "Tree", description: "A green tree" },
    { name: "Sun", description: "A bright sun" },
  ],
  speechWidth: {
    intervention_count: 5,
    total_word_count: 120,
    average_word_count_per_intervention: 24,
    std_word_count_per_intervention: 3.2,
    total_speech_time: 45,
    average_speech_time_per_intervention: 9,
    std_speech_time_per_intervention: 1.8,
  },
  speechDepth: {
    average_intimacy_score: 0.7,
    std_intimacy_score: 0.1,
  },
  drawingWidth: {
    stroke_count: 12,
    total_stroke_length: 340,
    average_stroke_length: 28.3,
    std_stroke_length: 4.1,
    color_used_count: 6,
    pen_size_used_count: 3,
    amount_filled_area: 75,
  },
};

describe("ChildSessionView", () => {
  let printSpy;
  let addEventListenerSpy;
  let removeEventListenerSpy;

  beforeEach(() => {
    vi.clearAllMocks();

    usePixelbotChildren.mockReturnValue({
      children: mockChildren,
      isLoading: false,
    });

    usePixelbotSession.mockReturnValue({
      session: mockSession,
      isLoading: false,
    });

    printSpy = vi.spyOn(window, "print").mockImplementation(() => {});
    addEventListenerSpy = vi.spyOn(window, "addEventListener");
    removeEventListenerSpy = vi.spyOn(window, "removeEventListener");
  });

  afterEach(() => {
    printSpy.mockRestore();
    addEventListenerSpy.mockRestore();
    removeEventListenerSpy.mockRestore();
    document.body.className = '';
  });

  it("renders drawing, transcript, story summary, metrics, and child/session title", () => {
    renderWithRouter("c1", "s1");

    expect(screen.getByText("Drawing")).toBeInTheDocument();
    expect(screen.getByText("Text Transcript")).toBeInTheDocument();
    expect(screen.getByText("Story Summary")).toBeInTheDocument();
    expect(screen.getByText("Speech Data")).toBeInTheDocument();
    expect(screen.getByText("Drawing Data")).toBeInTheDocument();

    expect(screen.getByText("Child One - s1")).toBeInTheDocument();

    expect(screen.getByText("Robot:")).toBeInTheDocument();
    expect(screen.getByText("Hello there")).toBeInTheDocument();
    expect(screen.getByText("Child:")).toBeInTheDocument();
    expect(screen.getByText("Hi!")).toBeInTheDocument();

    expect(screen.getByText("Tree")).toBeInTheDocument();
    expect(screen.getByText("A green tree")).toBeInTheDocument();
    expect(screen.getByText("Sun")).toBeInTheDocument();
    expect(screen.getByText("A bright sun")).toBeInTheDocument();

    expect(screen.getByText("Number of intervention")).toBeInTheDocument();
    expect(screen.getByText("Amount of area filled")).toBeInTheDocument();

    expect(screen.getByTestId("image-carousel")).toBeInTheDocument();
  });

  it("shows the story summary subtitle with object count", () => {
    renderWithRouter("c1", "s1");

    expect(
      screen.getByText("Number of objects detected : 2")
    ).toBeInTheDocument();
  });

  it("shows Loading when session is loading", () => {
    usePixelbotSession.mockReturnValue({
      session: null,
      isLoading: true,
    });

    renderWithRouter("c1", "s1");

    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("shows Loading when session is missing even if isLoading is false", () => {
    usePixelbotSession.mockReturnValue({
      session: null,
      isLoading: false,
    });

    renderWithRouter("c1", "s1");

    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("renders blank child name when matching child is not found", () => {
  usePixelbotChildren.mockReturnValue({
    children: [{ childId: "other-child", name: "Someone Else" }],
    isLoading: false,
  });

  renderWithRouter("c1", "s1");

  expect(screen.getByRole("heading", { level: 3 })).toHaveTextContent(/-\s*s1/);
});

  it("renders blank child name when children is null", () => {
    usePixelbotChildren.mockReturnValue({
      children: null,
      isLoading: false,
    });

    renderWithRouter("c1", "s1");

    expect(screen.getByRole("heading", { level: 3 })).toHaveTextContent(/-\s*s1/);
  });

  it("prints the full child session view when the page print icon is clicked", () => {
    const { container } = renderWithRouter("c1", "s1");

    const root = document.getElementById("child-session-view");
    const printIcon = container.querySelector(".page-header .print-icon");

    fireEvent.click(printIcon);

    expect(root).toHaveClass("print-visible");
    expect(document.body).toHaveClass("printing-single-widget");
    expect(window.print).toHaveBeenCalledTimes(1);
    expect(window.addEventListener).toHaveBeenCalledWith(
      "afterprint",
      expect.any(Function)
    );
  });

  it("removes print classes after afterprint fires", () => {
    const { container } = renderWithRouter("c1", "s1");

    const root = document.getElementById("child-session-view");
    const printIcon = container.querySelector(".page-header .print-icon");

    fireEvent.click(printIcon);

    const cleanupCall = addEventListenerSpy.mock.calls.find(
      ([eventName]) => eventName === "afterprint"
    );
    const cleanupFn = cleanupCall[1];

    cleanupFn();

    expect(root).not.toHaveClass("print-visible");
    expect(document.body).not.toHaveClass("printing-single-widget");
    expect(window.removeEventListener).toHaveBeenCalledWith(
      "afterprint",
      cleanupFn
    );
  });

  it("wires dashboard card print handlers", () => {
    renderWithRouter("c1", "s1");

    expect(screen.getByTestId("print-session-drawing")).toBeInTheDocument();
    expect(screen.getByTestId("print-session-transcript")).toBeInTheDocument();
    expect(screen.getByTestId("print-session-summary")).toBeInTheDocument();
    expect(screen.getByTestId("print-session-speech-data")).toBeInTheDocument();
    expect(screen.getByTestId("print-session-drawing-data")).toBeInTheDocument();
  });

  it("prints session-drawing card when its print button is clicked", () => {
    renderWithRouter("c1", "s1");

    const drawingCard = document.getElementById("session-drawing");
    fireEvent.click(screen.getByTestId("print-session-drawing"));

    expect(drawingCard).toHaveClass("print-visible");
    expect(document.body).toHaveClass("printing-single-widget");
    expect(window.print).toHaveBeenCalledTimes(1);
  });

  it("prints session-transcript card when its print button is clicked", () => {
    renderWithRouter("c1", "s1");

    const transcriptCard = document.getElementById("session-transcript");
    fireEvent.click(screen.getByTestId("print-session-transcript"));

    expect(transcriptCard).toHaveClass("print-visible");
    expect(document.body).toHaveClass("printing-single-widget");
    expect(window.print).toHaveBeenCalledTimes(1);
  });

  it("prints session-summary card when its print button is clicked", () => {
    renderWithRouter("c1", "s1");

    const summaryCard = document.getElementById("session-summary");
    fireEvent.click(screen.getByTestId("print-session-summary"));

    expect(summaryCard).toHaveClass("print-visible");
    expect(document.body).toHaveClass("printing-single-widget");
    expect(window.print).toHaveBeenCalledTimes(1);
  });

  it("prints session-speech-data card when its print button is clicked", () => {
    renderWithRouter("c1", "s1");

    const speechCard = document.getElementById("session-speech-data");
    fireEvent.click(screen.getByTestId("print-session-speech-data"));

    expect(speechCard).toHaveClass("print-visible");
    expect(document.body).toHaveClass("printing-single-widget");
    expect(window.print).toHaveBeenCalledTimes(1);
  });

  it("prints session-drawing-data card when its print button is clicked", () => {
    renderWithRouter("c1", "s1");

    const drawingDataCard = document.getElementById("session-drawing-data");
    fireEvent.click(screen.getByTestId("print-session-drawing-data"));

    expect(drawingDataCard).toHaveClass("print-visible");
    expect(document.body).toHaveClass("printing-single-widget");
    expect(window.print).toHaveBeenCalledTimes(1);
  });

  it("falls back to plain window.print when the target print element is missing", () => {
    renderWithRouter("c1", "s1");

    const drawingCard = document.getElementById("session-drawing");
    drawingCard.id = "session-drawing-missing";

    fireEvent.click(screen.getByTestId("print-session-drawing"));

    expect(window.print).toHaveBeenCalledTimes(1);
    expect(document.body).not.toHaveClass("printing-single-widget");
    expect(window.addEventListener).not.toHaveBeenCalledWith(
      "afterprint",
      expect.any(Function)
    );
  });
});