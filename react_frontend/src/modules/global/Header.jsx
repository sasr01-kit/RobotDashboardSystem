/**
 *  Class Description:
    - logo : string
    - title : string

    Optionals:
    - homeButton : HomeButton
    - translationButton : TranslationButton
    - showHomeButton : boolean
*/

import './Header.css';
import kitLogo from './assets/kitLogo.svg';
// OPT: import homeButton and translationButton
import HomeButton from './HomeButton';

export default function Header({ 
    title = 'Dashboard', // Standard value for header title, should be replaced for each module
    // OPT: 
    showHomeButton = true // showHomeButton : boolean
}) {
    return (
        <header className="global-header">
            {/* Inner container aligns with page max-width and paddings */}
            <div className="header-container">
                <div className="header-left">
                    {showHomeButton && <HomeButton />}
                    <span className="header-title">{title}</span>
                </div>
                <div className="header-right">
                    <img 
                        src={kitLogo} 
                        alt={"KIT Logo"} 
                        className="header-logo"
                    />
                </div>
            </div>
        </header>
    );
}