import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import Header from "../../modules/global/Header";

vi.mock("../../modules/global/assets/kitLogo.svg", () => ({
  default: "kitLogo.svg",
}));

vi.mock("../../modules/global/HomeButton", () => ({
  default: () => <div data-testid="home-button">HomeButton</div>,
}));

describe("Header", () => {
  it("renders the header title", () => {
    render(
      <MemoryRouter>
        <Header title="Pixelbot Dashboard" />
      </MemoryRouter>
    );

    expect(screen.getByText("Pixelbot Dashboard")).toBeInTheDocument();
  });

  it("renders default title when none is provided", () => {
    render(
      <MemoryRouter>
        <Header />
      </MemoryRouter>
    );

    expect(screen.getByText("Dashboard")).toBeInTheDocument();
  });

  it("renders the HomeButton when showHomeButton is true", () => {
    render(
      <MemoryRouter>
        <Header showHomeButton={true} />
      </MemoryRouter>
    );

    expect(screen.getByTestId("home-button")).toBeInTheDocument();
  });

  it("does not render the HomeButton when showHomeButton is false", () => {
    render(
      <MemoryRouter>
        <Header showHomeButton={false} />
      </MemoryRouter>
    );

    expect(screen.queryByTestId("home-button")).not.toBeInTheDocument();
  });

  it("renders the KIT logo", () => {
    render(
      <MemoryRouter>
        <Header />
      </MemoryRouter>
    );

    const logo = screen.getByAltText("KIT Logo");

    expect(logo).toBeInTheDocument();
    expect(logo).toHaveAttribute("src", "kitLogo.svg");
  });
});