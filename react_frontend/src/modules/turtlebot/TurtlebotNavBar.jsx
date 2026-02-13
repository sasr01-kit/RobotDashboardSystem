import { useNavigate, useLocation } from 'react-router-dom';
import { useModeContext } from './modeUtil/ModeContext.js';

// Navigation bar component for the Turtlebot dashboard, allowing users to switch between Status, Map, and Feedback pages.
const tabNames = ['Status', 'Map', 'Feedback'];
export default function TurtlebotNavBar() {
    const navigate = useNavigate();
    const location = useLocation();
    const { mode } = useModeContext();

    const activeTab = tabNames.find(tab => location.pathname.endsWith(tab.toLowerCase())) || 'Status';
    // Allow switching tabs, but disable Map and Feedback when in Teleoperating mode to prevent access to unavailable features
    const switchTab = (tabName) => {if (mode === 'Teleoperating' && (tabName === 'Map' || tabName === 'Feedback')) return;
        navigate(`/turtlebot/${tabName.toLowerCase()}`);
    };

    return (
        <div className="turtlebot-navbar">
            {tabNames.map((tabName) => (
                <button
                    key={tabName}
                    className={`tab-button ${activeTab === tabName ? 'active' : ''}
                        ${mode === 'Teleoperating' && (tabName === 'Map' || tabName === 'Feedback') ? 'disabled' : ''}`}
                    onClick={() => switchTab(tabName)}
                    disabled={mode === 'Teleoperating' && (tabName === 'Map' || tabName === 'Feedback')}
                    >
                    {tabName}      
                </button>
            ))}
        </div>
    );
}
