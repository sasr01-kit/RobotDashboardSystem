import { useState, useEffect } from "react";
import { useWebSocketContext } from "../WebsocketUtil/WebsocketContext";

export function useTurtlebotStatus() {
  const { subscribe } = useWebSocketContext();

  const [statusDTO, setStatusDTO] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!subscribe) return;

    return subscribe((data) => {
      try {
        if (data.type !== "STATUS_UPDATE") return;

        setStatusDTO({
          isOn: data.power,
          batteryPercentage: data.battery,
          isWifiConnected: data.wifi,
          isCommsConnected: data.comms,
          isRaspberryPiConnected: data.raspberryPi,
          mode: data.mode,
          docking: data.docking,
        });

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