import { useState } from "react";
import '../Pixelbot.css';
import '../styles/ImageCarousel.css';
import chevron from '../assets/chevron.svg';

// ImageCarousel component to display a carousel of images
export default function ImageCarousel({ images }) {
    const [currentIndex, setCurrentIndex] = useState(0);

    function handleNext() {
        if (currentIndex < images.length - 1) {
            setCurrentIndex(currentIndex + 1);
        } else {
            setCurrentIndex(0);
        }
    }

    function handlePrev() {
        if (currentIndex > 0) {
            setCurrentIndex(currentIndex - 1);
        } else {
            setCurrentIndex(images.length - 1);
        }
    }

    if (!images || images.length === 0) {
        return <div className="carousel-empty">No images available</div>;
    }

    return (
        <div className="image-carousel">
            <div className="carousel-container">
                <button
                    className="carousel-btn carousel-btn-prev"
                    onClick={handlePrev}
                    aria-label="Previous"
                    style={{ visibility: images.length > 1 ? 'visible' : 'hidden' }}
                >
                    <img src={chevron} alt="chevron" className="chevron-icon carousel-chevron prev" />
                </button>
                <div className="carousel-image-wrapper">
                    <img
                        src={images[currentIndex]}
                        alt={`Drawing ${currentIndex + 1}`}
                        className="carousel-image"
                    />
                </div>
                <button
                    className="carousel-btn carousel-btn-next"
                    onClick={handleNext}
                    aria-label="Next"
                    style={{ visibility: images.length > 1 ? 'visible' : 'hidden' }}
                >
                    <img src={chevron} alt="chevron" className="chevron-icon carousel-chevron next" />
                </button>
            </div>
            {images.length > 1 && (
                <div className="carousel-indicators">
                    {images.map((_, index) => (
                        <button
                            key={index}
                            className={`carousel-indicator ${index === currentIndex ? 'active' : ''}`}
                            onClick={() => setCurrentIndex(index)}
                            aria-label={`Go to image ${index + 1}`}
                        />
                    ))}
                </div>
            )}
        </div>
    );
}