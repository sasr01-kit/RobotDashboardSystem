// Global state and listener management for Turtlebot status data, allowing 
// consistent status-related data across different components without prop drilling 
// or multiple WebSocket subscriptions

// Default state structure for status data
let globalStatusState = {
  isOn: false,
  batteryPercentage: null,
  isWifiConnected: false,
  isCommsConnected: false,
  isRaspberryPiConnected: false,
  mode: "Teleoperating",
  isDocked: true
};

const listeners = new Set();

export function updateGlobalStatusState(patch) {
  globalStatusState = { ...globalStatusState, ...patch };
  listeners.forEach(fn => fn(globalStatusState));
}

import { useState, useEffect } from "react";
import { useWebSocketContext } from "../websocketUtil/WebsocketContext";

// Custom hook to provide Turtlebot status data to components
export function useTurtlebotStatus() {
  const { subscribe } = useWebSocketContext();
  const [statusDTO, setStatusDTO] = useState(globalStatusState);
  const [error, setError] = useState(null);

  useEffect(() => {
    listeners.add(setStatusDTO);
    setStatusDTO(globalStatusState);
    return () => listeners.delete(setStatusDTO);
  }, []);

  useEffect(() => {
    if (!subscribe) return;

    return subscribe((data) => {
      // Debug log for incoming status-related messages from the backend
      console.log("[STATUS HOOK] incoming:", data);

      try {
        if (data.type !== "STATUS_UPDATE") return;

        updateGlobalStatusState({
          isOn: data.isOn,
          batteryPercentage: data.batteryPercentage,
          isWifiConnected: data.isWifiConnected,
          isCommsConnected: data.isCommsConnected,
          isRaspberryPiConnected: data.isRaspberryPiConnected,
          mode: data.mode,
          isDocked: data.isDocked
        });

        setError(null);
      } catch {
        setError("Failed to parse Turtlebot status");
      }
    });
  }, [subscribe]);

  return { statusDTO, error };
}
