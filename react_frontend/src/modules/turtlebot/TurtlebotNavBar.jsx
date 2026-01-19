import { useNavigate, useLocation } from 'react-router-dom';
import { useModeContext } from './ModeUtil/ModeContext.js';


const tabNames = ['Status', 'Map', 'Feedback'];
export default function TurtlebotNavBar() {
    const navigate = useNavigate();
    const location = useLocation();
    const { mode } = useModeContext();


    const activeTab = tabNames.find(tab => location.pathname.endsWith(tab.toLowerCase())) || 'Status';
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
