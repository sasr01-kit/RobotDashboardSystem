import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import ImageCarousel from "../../modules/pixelbot/components/ImageCarousel";

// Test for ImageCarousel to ensure it handles empty states, navigation, and indicators correctly based on the images prop
vi.mock("../../modules/pixelbot/assets/chevron.svg", () => ({
  default: "chevron.svg",
}));

describe("ImageCarousel", () => {
  it("renders empty state when images is missing", () => {
    render(<ImageCarousel images={null} />);
    expect(screen.getByText("No images available")).toBeInTheDocument();
  });

  it("renders empty state when images is empty", () => {
    render(<ImageCarousel images={[]} />);
    expect(screen.getByText("No images available")).toBeInTheDocument();
  });

  it("renders the first image initially", () => {
    render(<ImageCarousel images={["img1.png", "img2.png"]} />);

    const image = screen.getByAltText("Drawing 1");
    expect(image).toBeInTheDocument();
    expect(image).toHaveAttribute("src", "img1.png");
  });

  it("shows hidden nav buttons when there is only one image", () => {
    const { container } = render(<ImageCarousel images={["img1.png"]} />);

    const prevButton = container.querySelector(".carousel-btn-prev");
    const nextButton = container.querySelector(".carousel-btn-next");

    expect(prevButton).toBeInTheDocument();
    expect(nextButton).toBeInTheDocument();
    expect(prevButton).toHaveStyle("visibility: hidden");
    expect(nextButton).toHaveStyle("visibility: hidden");
    expect(screen.queryByLabelText("Go to image 1")).not.toBeInTheDocument();
    });

  it("shows visible nav buttons and indicators when there are multiple images", () => {
    render(<ImageCarousel images={["img1.png", "img2.png", "img3.png"]} />);

    expect(screen.getByRole("button", { name: "Previous" })).toHaveStyle({
      visibility: "visible",
    });
    expect(screen.getByRole("button", { name: "Next" })).toHaveStyle({
      visibility: "visible",
    });

    expect(screen.getByLabelText("Go to image 1")).toBeInTheDocument();
    expect(screen.getByLabelText("Go to image 2")).toBeInTheDocument();
    expect(screen.getByLabelText("Go to image 3")).toBeInTheDocument();
  });

  it("moves to the next image when Next is clicked", () => {
    render(<ImageCarousel images={["img1.png", "img2.png", "img3.png"]} />);

    fireEvent.click(screen.getByRole("button", { name: "Next" }));

    const image = screen.getByAltText("Drawing 2");
    expect(image).toHaveAttribute("src", "img2.png");
  });

  it("wraps to the first image when Next is clicked on the last image", () => {
    render(<ImageCarousel images={["img1.png", "img2.png", "img3.png"]} />);

    fireEvent.click(screen.getByRole("button", { name: "Next" }));
    fireEvent.click(screen.getByRole("button", { name: "Next" }));
    fireEvent.click(screen.getByRole("button", { name: "Next" }));

    const image = screen.getByAltText("Drawing 1");
    expect(image).toHaveAttribute("src", "img1.png");
  });

  it("moves to the previous image when Previous is clicked", () => {
    render(<ImageCarousel images={["img1.png", "img2.png", "img3.png"]} />);

    fireEvent.click(screen.getByRole("button", { name: "Next" }));
    fireEvent.click(screen.getByRole("button", { name: "Previous" }));

    const image = screen.getByAltText("Drawing 1");
    expect(image).toHaveAttribute("src", "img1.png");
  });

  it("wraps to the last image when Previous is clicked on the first image", () => {
    render(<ImageCarousel images={["img1.png", "img2.png", "img3.png"]} />);

    fireEvent.click(screen.getByRole("button", { name: "Previous" }));

    const image = screen.getByAltText("Drawing 3");
    expect(image).toHaveAttribute("src", "img3.png");
  });

  it("jumps to a selected image when an indicator is clicked", () => {
    render(<ImageCarousel images={["img1.png", "img2.png", "img3.png"]} />);

    fireEvent.click(screen.getByLabelText("Go to image 3"));

    const image = screen.getByAltText("Drawing 3");
    expect(image).toHaveAttribute("src", "img3.png");
  });

  it("marks the current indicator as active", () => {
    render(<ImageCarousel images={["img1.png", "img2.png", "img3.png"]} />);

    const indicator1 = screen.getByLabelText("Go to image 1");
    const indicator2 = screen.getByLabelText("Go to image 2");

    expect(indicator1).toHaveClass("active");
    expect(indicator2).not.toHaveClass("active");

    fireEvent.click(indicator2);

    expect(indicator2).toHaveClass("active");
    expect(indicator1).not.toHaveClass("active");
  });
});