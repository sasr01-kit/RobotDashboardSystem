import { useNavigate, useLocation } from 'react-router-dom';
import './Pixelbot.css';

const tabNames = ['Summary', 'Child'];

export default function PixelbotNavBar() {
    const navigate = useNavigate();
    const location = useLocation();

    const activeTab = tabNames.find(tab => location.pathname.endsWith(tab.toLowerCase())) || 'Summary';
    const switchTab = (tabName) => {
        navigate(`/pixelbot/${tabName.toLowerCase()}`);
    };

    return (
        <div className="pixelbot-navbar">
            {tabNames.map((tabName) => (
                <button
                    key={tabName}
                    className={`tab-button ${activeTab === tabName ? 'active' : ''}`}
                    onClick={() => switchTab(tabName)}
                >
                    {tabName}
                </button>
            ))}
        </div>
    );
}
