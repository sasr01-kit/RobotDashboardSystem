import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter } from "react-router-dom";
import PixelbotNavBar from "../../modules/pixelbot/PixelbotNavBar";
import { usePixelbotChildren } from "../../modules/pixelbot/hooks/usePixelbotChildren";
import { useNavigate, useLocation, useParams } from "react-router-dom";

// Tests for PixelbotNavBar to ensure it renders Summary and Child buttons, marks 
// active states based on the route, handles navigation correctly, and manages 
// the child dropdown state based on the children data and URL parameters
vi.mock("../../modules/pixelbot/hooks/usePixelbotChildren");

vi.mock("../../modules/pixelbot/assets/chevron.svg", () => ({
  default: "chevron.svg",
}));

vi.mock("react-router-dom", async () => {
  const actual = await vi.importActual("react-router-dom");
  return {
    ...actual,
    useNavigate: vi.fn(),
    useLocation: vi.fn(),
    useParams: vi.fn(),
  };
});

describe("PixelbotNavBar", () => {
  const navigate = vi.fn();

  const mockChildren = [
    {
      childId: "c1",
      name: "Child One",
      sessions: [{ sessionId: "s1" }, { sessionId: "s2" }],
    },
    {
      childId: "c2",
      name: "Child Two",
      sessions: [{ sessionId: "s3" }],
    },
  ];

  beforeEach(() => {
    vi.clearAllMocks();

    useNavigate.mockReturnValue(navigate);
    useLocation.mockReturnValue({ pathname: "/pixelbot/summary" });
    useParams.mockReturnValue({ childId: undefined, sessionId: undefined });
    usePixelbotChildren.mockReturnValue({
      children: mockChildren,
      isLoading: false,
    });
  });

  it("renders Summary and Child buttons", () => {
    render(
      <MemoryRouter>
        <PixelbotNavBar />
      </MemoryRouter>
    );

    expect(screen.getByRole("button", { name: "Summary" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /Child/i })).toBeInTheDocument();
  });

  it("marks Summary active on summary route", () => {
    useLocation.mockReturnValue({ pathname: "/pixelbot/summary" });

    render(
      <MemoryRouter>
        <PixelbotNavBar />
      </MemoryRouter>
    );

    expect(screen.getByRole("button", { name: "Summary" })).toHaveClass("active");
  });

  it("marks Child active on child route", () => {
    useLocation.mockReturnValue({ pathname: "/pixelbot/session/c1" });
    useParams.mockReturnValue({ childId: "c1", sessionId: undefined });

    render(
      <MemoryRouter>
        <PixelbotNavBar />
      </MemoryRouter>
    );

    expect(screen.getByRole("button", { name: /Child/i })).toHaveClass("active");
  });

  it("navigates to summary when Summary is clicked", () => {
    render(
      <MemoryRouter>
        <PixelbotNavBar />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: "Summary" }));

    expect(navigate).toHaveBeenCalledWith("/pixelbot/summary");
  });

  it("opens the child dropdown when Child is clicked", () => {
    render(
      <MemoryRouter>
        <PixelbotNavBar />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /Child/i }));

    expect(screen.getByText("Child One")).toBeInTheDocument();
    expect(screen.getByText("Child Two")).toBeInTheDocument();
  });

  it("shows Loading in dropdown when children are loading", () => {
    usePixelbotChildren.mockReturnValue({
      children: null,
      isLoading: true,
    });

    render(
      <MemoryRouter>
        <PixelbotNavBar />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /Child/i }));

    expect(screen.getByText("Loading...")).toBeInTheDocument();
  });

  it("shows sessions after selecting a child", () => {
    render(
      <MemoryRouter>
        <PixelbotNavBar />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /Child/i }));
    fireEvent.click(screen.getByText("Child One"));

    expect(screen.getByText("Recap")).toBeInTheDocument();
    expect(screen.getByText("s1")).toBeInTheDocument();
    expect(screen.getByText("s2")).toBeInTheDocument();
  });

  it("navigates to child recap when Recap is clicked", () => {
    render(
      <MemoryRouter>
        <PixelbotNavBar />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /Child/i }));
    fireEvent.click(screen.getByText("Child One"));
    fireEvent.click(screen.getByText("Recap"));

    expect(navigate).toHaveBeenCalledWith("/pixelbot/session/c1");
  });

  it("navigates to a specific session when a session is clicked", () => {
    render(
      <MemoryRouter>
        <PixelbotNavBar />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /Child/i }));
    fireEvent.click(screen.getByText("Child One"));
    fireEvent.click(screen.getByText("s2"));

    expect(navigate).toHaveBeenCalledWith("/pixelbot/session/c1/s2");
  });

  it("preselects child from URL params and shows sessions after opening dropdown", () => {
    useLocation.mockReturnValue({ pathname: "/pixelbot/session/c1/s1" });
    useParams.mockReturnValue({ childId: "c1", sessionId: "s1" });

    render(
      <MemoryRouter>
        <PixelbotNavBar />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /Child/i }));

    expect(screen.getByText("Recap")).toBeInTheDocument();
    expect(screen.getByText("s1")).toBeInTheDocument();
    expect(screen.getByText("s2")).toBeInTheDocument();
  });

  it("closes dropdown when clicking outside", () => {
    render(
      <MemoryRouter>
        <div>
          <PixelbotNavBar />
          <div data-testid="outside">Outside</div>
        </div>
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /Child/i }));
    expect(screen.getByText("Child One")).toBeInTheDocument();

    fireEvent.mouseDown(screen.getByTestId("outside"));

    expect(screen.queryByText("Child One")).not.toBeInTheDocument();
  });

  it("keeps dropdown open when mousedown happens inside the dropdown", () => {
    render(
      <MemoryRouter>
        <PixelbotNavBar />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /Child/i }));
    expect(screen.getByText("Child One")).toBeInTheDocument();

    const dropdownWrapper = document.querySelector(".nav-dropdown-wrapper");
    fireEvent.mouseDown(dropdownWrapper);

    expect(screen.getByText("Child One")).toBeInTheDocument();
  });

  it("does not crash when childId is set but children is not yet loaded", () => {
    useParams.mockReturnValue({ childId: "c1", sessionId: undefined });
    usePixelbotChildren.mockReturnValue({ children: null, isLoading: false });

    render(
      <MemoryRouter>
        <PixelbotNavBar />
      </MemoryRouter>
    );

    expect(screen.getByRole("button", { name: /Child/i })).toBeInTheDocument();
  });

  it("does not crash when childId is not found in children list", () => {
    useParams.mockReturnValue({ childId: "c99", sessionId: undefined });

    render(
      <MemoryRouter>
        <PixelbotNavBar />
      </MemoryRouter>
    );

    expect(screen.getByRole("button", { name: /Child/i })).toBeInTheDocument();
  });

  it("closes dropdown but does not reset selectedChildId when clicking outside while on a child page", () => {
    useParams.mockReturnValue({ childId: "c1", sessionId: undefined });
    useLocation.mockReturnValue({ pathname: "/pixelbot/session/c1" });

    render(
      <MemoryRouter>
        <div>
          <PixelbotNavBar />
          <div data-testid="outside">Outside</div>
        </div>
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /Child/i }));
    expect(screen.getByText("Child One")).toBeInTheDocument();

    fireEvent.mouseDown(screen.getByTestId("outside"));

    expect(screen.queryByText("Child One")).not.toBeInTheDocument();
  });

  it("marks Recap as session-selected when on the child recap page (childId set, no sessionId)", () => {
    useParams.mockReturnValue({ childId: "c1", sessionId: undefined });
    useLocation.mockReturnValue({ pathname: "/pixelbot/session/c1" });

    render(
      <MemoryRouter>
        <PixelbotNavBar />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByRole("button", { name: /Child/i }));

    const recapItem = screen.getByText("Recap");
    expect(recapItem.closest(".dropdown-item")).toHaveClass("session-selected");
  });
});