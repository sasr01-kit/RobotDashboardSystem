import { getBatteryIcon } from "./assets/batteryMap";
import { useTurtlebotStatus } from "./Hooks/useTurtlebotStatus";

export const MinimizedStatusBar = () => {
  const { statusDTO } = useTurtlebotStatus();

  return (
    <div className="minimized-status-bar">

      <div
        className="mini-status-icon mini-power-icon"
        style={{ backgroundColor: statusDTO?.isOn ? "var(--success-green)" : "var(--error-red)" }}
      />

      <img
        src={getBatteryIcon(statusDTO?.battery)}
        alt={`Battery ${statusDTO?.battery}%`}
        className="mini-status-icon mini-battery-icon"
      />

      <div
        className="mini-status-icon mini-wifi-icon"
        style={{ backgroundColor: statusDTO?.wifi ? "var(--success-green)" : "var(--error-red)" }}
      />

      <div
        className="mini-status-icon mini-pi-icon"
        style={{ backgroundColor: statusDTO?.raspberryPi ? "var(--success-green)" : "var(--error-red)" }}
      />

      <div
        className="mini-status-icon mini-comms-icon"
        style={{ backgroundColor: statusDTO?.comms ? "var(--success-green)" : "var(--error-red)" }}
      />

    </div>
  );
};
