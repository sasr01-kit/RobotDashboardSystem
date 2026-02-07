import '../styles/StatusPage.css';
import '../styles/Teleoperation.css';
import '../styles/StatusComponents.css';
import '../styles/CommandExecution.css';
import battery from '../assets/battery.svg';
import wifi from '../assets/wifi.svg';
import raspberryPi from '../assets/raspberry.svg';
import comms from '../assets/comms.svg'; 
import PowerStatus from '../components/PowerStatus.jsx';
import ModeStatus from '../components/ModeStatus.jsx';
import { useTurtlebotStatus } from '../Hooks/useTurtlebotStatus.js';
import GeneralStatusBlock from '../components/GeneralStatusBlock.jsx';
import TeleoperationBlock from '../components/TeleoperationBlock.jsx';
import PathExecutionBlock from "../components/PathExecutionBlock.jsx";
import DockingBlock from "../components/DockingBlock.jsx";


export default function TurtlebotStatusPage() {
    const { statusDTO, isLoading, error } = useTurtlebotStatus();

    const batteryColor = statusDTO?.batteryPercentage === "N/A" ? "#FF5A5F"
                            : statusDTO.batteryPercentage < 50 ? "#FF5A5F" : "#5AAE61";
    const wifiColor = statusDTO?.isWifiConnected ? '#5AAE61' : '#FF5A5F';
    const piColor = statusDTO?.isRaspberryPiConnected ? '#5AAE61' : '#FF5A5F';
    const commsColor = statusDTO?.isCommsConnected ? '#5AAE61' : '#FF5A5F';

   
    if (isLoading) return <div className='loading-page'>Loading...</div>;
    if (error) return <div className='error-page'>Error: {error}</div>;
   
    return (
        <div className="turtlebot-status-page">
            <div className="status-row">
                <PowerStatus isOn={statusDTO?.isOn} />
                <GeneralStatusBlock icon={
                                <img
                                    src={battery}
                                    alt="Battery Icon"
                                    className="battery-icon"
                                />}
                    label="Battery"
                    status={statusDTO?.batteryPercentage === "N/A" ? "N/A" : `${statusDTO.batteryPercentage}%`}
                    statusColor={batteryColor}
                />
                <GeneralStatusBlock icon={
                                <img
                                    src={wifi}
                                    alt="WiFi Icon"
                                    className="wifi-icon"
                                />}
                    label="WiFi"
                    status={statusDTO?.isWifiConnected ? 'Connected' : 'Disconnected'}
                    statusColor={wifiColor}
                />
                <GeneralStatusBlock icon={<img
                                    src={raspberryPi}
                                    alt="Raspberry Pi Icon"
                                    className="raspberry-icon"
                                />}
                    label="Raspberry Pi"
                    status={statusDTO?.isRaspberryPiConnected ? 'Online' : 'Offline'}
                    statusColor={piColor}
                />
                <GeneralStatusBlock icon={<img
                                    src={comms}
                                    alt="Comms Icon"
                                    className="comms-icon"
                                />}
                    label="Comms"
                    status={statusDTO?.isCommsConnected ? 'Connected' : 'Disconnected'}
                    statusColor={commsColor}
                />
            </div>
            <div className="teleop-and-commands-container">
                    <TeleoperationBlock />
                   <div className="commands-column-container">
                    <ModeStatus />
                    <PathExecutionBlock />
                    <DockingBlock />
                    </div>
            </div>
        </div>
    );
};

