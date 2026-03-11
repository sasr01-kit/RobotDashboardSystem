import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";
import HomeButton from "../../modules/global/HomeButton";

vi.mock("../../modules/global/assets/homeIcon.svg", () => ({
  default: "homeIcon.svg",
}));

describe("HomeButton", () => {
  it("renders a link to the homepage", () => {
    render(
      <MemoryRouter>
        <HomeButton />
      </MemoryRouter>
    );

    const link = screen.getByRole("link", { name: "Home" });

    expect(link).toBeInTheDocument();
    expect(link).toHaveAttribute("href", "/");
  });

  it("renders the home icon", () => {
    render(
      <MemoryRouter>
        <HomeButton />
      </MemoryRouter>
    );

    const image = screen.getByAltText("Home Icon");

    expect(image).toBeInTheDocument();
    expect(image).toHaveAttribute("src", "homeIcon.svg");
  });
});