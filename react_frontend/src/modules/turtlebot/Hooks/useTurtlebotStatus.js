// -------------------------------------------------------------
// GLOBAL STORE (persists across page changes)
// -------------------------------------------------------------

let globalStatusState = {
  isOn: false,
  batteryPercentage: null,
  isWifiConnected: false,
  isCommsConnected: false,
  isRaspberryPiConnected: false,
  mode: "Teleoperating",
  isDocked: true
};

// All hook instances subscribe here
const listeners = new Set();

// Called by WebSocket callback to update global state
export function updateGlobalStatusState(patch) {
  globalStatusState = { ...globalStatusState, ...patch };
  listeners.forEach(fn => fn(globalStatusState));
}



// -------------------------------------------------------------
// HOOK
// -------------------------------------------------------------

import { useState, useEffect } from "react";
import { useWebSocketContext } from "../WebsocketUtil/WebsocketContext";

export function useTurtlebotStatus() {
  const { subscribe } = useWebSocketContext();

  // Initialize from global state (not defaults)
  const [statusDTO, setStatusDTO] = useState(globalStatusState);
  const [error, setError] = useState(null);

  // Subscribe this hook instance to global store updates
  useEffect(() => {
    listeners.add(setStatusDTO);

    // Immediately sync with latest global state
    setStatusDTO(globalStatusState);

    return () => listeners.delete(setStatusDTO);
  }, []);

  // Subscribe to WebSocket messages
  useEffect(() => {
    if (!subscribe) return;

    return subscribe((data) => {
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
