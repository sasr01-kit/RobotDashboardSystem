import { useModeContext } from './ModeUtil/ModeContext.js';
import { useTurtlebotStatus } from './Hooks/useTurtlebotStatus.js';


export default function TurtlebotStatusPage() {
    const { mode } = useModeContext();
    const { statusDTO, isLoading, error } = useTurtlebotStatus();
   
    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
   
    return (
        <div className="turtlebot-status-page">
            <h2>Turtlebot Status</h2>
            <p>Mode: {mode || 'Unknown'}</p>
            <p>Battery: {statusDTO?.battery}%</p>
            <p>WiFi: {statusDTO?.wifi ? 'Connected' : 'Disconnected'}</p>
            <p>Raspberry Pi: {statusDTO?.raspberryPi ? 'Online' : 'Offline'}</p>
            <p>Communications: {statusDTO?.comms ? 'OK' : 'Failed'}</p>
            <p>Docking: {statusDTO?.docking ? 'Docked' : 'Undocked'}</p>
        </div>
    );
};

