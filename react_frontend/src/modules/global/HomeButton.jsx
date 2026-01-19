import './HomeButton.css';
import { Link } from 'react-router-dom';

export default function HomeButton() {
    return ( 
        <Link to="/" className="home-button" aria-label="Home">
            <svg 
                src='./assets/homeIcon.svg' 
                alt="Home Icon" 
                className="home-icon"
            />
        </Link>
    );
}
