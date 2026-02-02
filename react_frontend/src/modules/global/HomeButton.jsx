import './HomeButton.css';
import homeIcon from './assets/homeIcon.svg'
import { Link } from 'react-router-dom';

export default function HomeButton() {
    return ( 
        <Link to="/" className="home-button" aria-label="Home">
            <img 
                src={homeIcon} 
                alt="Home Icon" 
                className="home-icon"
            />
        </Link>
    );
}
