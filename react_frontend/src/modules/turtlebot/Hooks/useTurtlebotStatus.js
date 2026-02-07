import { useState, useEffect } from "react";
import { useWebSocketContext } from "../WebsocketUtil/WebsocketContext";

export function useTurtlebotStatus() {
  const { subscribe } = useWebSocketContext();

  const [statusDTO, setStatusDTO] = useState({
    isOn: false,
    batteryPercentage: "N/A",
    isWifiConnected: false,
    isCommsConnected: false,
    isRaspberryPiConnected: false,
  });

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!subscribe) return;

    return subscribe((data) => {
      try {
        if (data.type !== "STATUS_UPDATE") return;

        setStatusDTO(prev => ({
          ...prev,
          isOn: data.isOn ?? prev.isOn,
          batteryPercentage: data.batteryPercentage ?? prev.batteryPercentage,
          isWifiConnected: data.isWifiConnected ?? prev.isWifiConnected,
          isCommsConnected: data.isCommsConnected ?? prev.isCommsConnected,
          isRaspberryPiConnected: data.isRaspberryPiConnected ?? prev.isRaspberryPiConnected,
          //mode: data.mode ? "RUNNING PATH MODULE" : "TELEOPERATION"
        }));

        setIsLoading(false);
        setError(null);
      } catch {
        setError("Failed to parse Turtlebot status");
        setIsLoading(false);
      }
    });
  }, [subscribe]);

  return { statusDTO, isLoading, error };
}