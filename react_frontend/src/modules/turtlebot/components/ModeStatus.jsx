import { useModeContext } from '../modeUtil/ModeContext.js';

// Component to display the current mode status of the Turtlebot
export default function ModeStatus() {
    const { mode } = useModeContext();

    const message = mode || 'Unknown';

    const modeColor = message === 'Teleoperating' ? "var(--success-green)" : "var(--primary-blue)";

    return (
        <div className="mode-status">
            <span className="mode-label">You are:</span>
            <span className="mode-value" style={{ color: modeColor }}> 
                {message.toUpperCase()} 
            </span>
        </div>
    );
}