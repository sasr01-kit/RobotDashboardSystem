import { getBatteryIcon } from "../assets/batteryMap";
import { useTurtlebotStatus } from "../hooks/useTurtlebotStatus";
import { motion } from "framer-motion";

// Component to display the minimized status bar with key Turtlebot status indicators as icons
export const MinimizedStatusBar = () => {
  const { statusDTO } = useTurtlebotStatus();

  return (
    <motion.div 
      className="minimized-status-bar"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >

      <div
        className="mini-status-icon mini-power-icon"
        style={{ backgroundColor: statusDTO?.isOn ? "var(--success-green)" : "var(--error-red)" }}
      />

      <img
        src={getBatteryIcon(statusDTO?.batteryPercentage)}
        alt={`Battery ${statusDTO?.batteryPercentage}%`}
        className="mini-status-icon mini-battery-icon"
      />

      <div
        className="mini-status-icon mini-wifi-icon"
        style={{ backgroundColor: statusDTO?.isWifiConnected ? "var(--success-green)" : "var(--error-red)" }}
      />

      <div
        className="mini-status-icon mini-pi-icon"
        style={{ backgroundColor: statusDTO?.isRaspberryPiConnected ? "var(--success-green)" : "var(--error-red)" }}
      />

      <div
        className="mini-status-icon mini-comms-icon"
        style={{ backgroundColor: statusDTO?.isCommsConnected ? "var(--success-green)" : "var(--error-red)" }}
      />

    </motion.div>
  );
};
