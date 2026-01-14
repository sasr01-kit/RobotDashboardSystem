import "./Homepage.css";

import kitLogo from './assets/kitLogo.svg';
import pixelbotLogo from './assets/pixelbotLogo.svg';
import turtlebotLogo from './assets/turtlebotLogo.svg';

import { Link } from 'react-router-dom';

function Homepage() {
    return (
        <div className="page">
            {/* Header */}
            <header className="header">
                <span className="header-line">Dashboard</span>
                <img
                    src={kitLogo}
                    alt="KIT Logo"
                    className="logo"
                />
            </header>

            {/* Title section */}
            <section className="title-section">
                <h1 className="title">SARAI</h1>
                <p className="subtitle">
                    Socially Assistive Robotics with Artificial Intelligence
                </p>
            </section>

            {/* Buttons */}
            <section className="button-section">
                <Link to="/pixelbot" className="card pixelbot">
                    <img
                    src={pixelbotLogo}
                    alt="Pixelbot Logo"
                    className="logo"
                    />
                    <p>Pixelbot</p>
                </Link>

                <Link to="/turtlebot" className="card turtlebot">
                    <img
                    src={turtlebotLogo}
                    alt="Turtlebot Logo"
                    className="logo"
                    />
                    <p>Turtlebot4</p>
                </Link>
            </section>
        </div>
    );
}

export default Homepage;
