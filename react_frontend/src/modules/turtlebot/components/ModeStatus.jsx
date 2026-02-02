import { useModeContext } from '../ModeUtil/ModeContext.js';

export default function ModeStatus() {
    const { mode } = useModeContext();

    const message = mode || 'Unknown';

    const modeColor = message === 'Teleoperating' ? '#5AAE61' : '#2196F3';

    return (
        <div className="mode-status">
            <span className="mode-label">You are:</span>
            <span className="mode-value" style={{ color: modeColor }}> 
                {message.toUpperCase()} 
            </span>
        </div>
    );
}