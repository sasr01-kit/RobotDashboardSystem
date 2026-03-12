import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import Homepage from "../../modules/robotSelection/Homepage";

vi.mock("../../modules/global/Header.jsx", () => ({
  default: ({ title }) => <div>{title}</div>,
}));

vi.mock("../../modules/homepage/assets/pixelbotLogo.svg", () => ({
  default: "pixelbotLogo.svg",
}));

vi.mock("../../modules/homepage/assets/turtlebotLogo.svg", () => ({
  default: "turtlebotLogo.svg",
}));

// Tests for Homepage to ensure it renders the title, subtitle, robot cards with logos, and correct links to routes
describe("Homepage", () => {
  it("renders the homepage title and subtitle", () => {
    render(
      <MemoryRouter>
        <Homepage />
      </MemoryRouter>
    );

    expect(screen.getByText("SARAI Dashboard")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "SARAI" })).toBeInTheDocument();
    expect(
      screen.getByText("Socially Assistive Robotics with Artificial Intelligence")
    ).toBeInTheDocument();
  });

  it("renders Pixelbot and Turtlebot cards with logos", () => {
    render(
      <MemoryRouter>
        <Homepage />
      </MemoryRouter>
    );

    expect(screen.getByText("Pixelbot")).toBeInTheDocument();
    expect(screen.getByText("Turtlebot4")).toBeInTheDocument();

    expect(screen.getByAltText("Pixelbot Logo")).toBeInTheDocument();
    expect(screen.getByAltText("Turtlebot Logo")).toBeInTheDocument();
  });

  it("links to the correct routes", () => {
    render(
      <MemoryRouter>
        <Homepage />
      </MemoryRouter>
    );

    const pixelbotLink = screen.getByRole("link", { name: /pixelbot/i });
    const turtlebotLink = screen.getByRole("link", { name: /turtlebot4/i });

    expect(pixelbotLink).toHaveAttribute("href", "/pixelbot");
    expect(turtlebotLink).toHaveAttribute("href", "/turtlebot");
  });
});