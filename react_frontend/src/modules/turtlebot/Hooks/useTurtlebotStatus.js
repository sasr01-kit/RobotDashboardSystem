import { useState, useEffect, useRef } from 'react';
import { useWebSocketContext } from '../WebsocketUtil/WebsocketContext.js';


// TEMPORARY MOCK — replace later with real WebSocket version
function useTurtlebotStatus() {


     return { statusDTO: {
        isOn: true,
        battery: 100,
        wifi: true,
        raspberryPi: true,
        comms: true,
        mode: 'Running Path Module',
        docking: false, },
        isLoading: false,
        error: null,
        connectWebSocket: () => {},
        disconnectWebSocket: () => {},
    };
}


export { useTurtlebotStatus };


/* REAL VERSION
export function useTurtlebotStatus() {
  const { socket } = useWebSocketContext();

  const [statusDTO, setStatusDTO] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!socket) return;

    const handleMessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type !== "STATUS_UPDATE") { return; }

        const status = {
          isOn: data.power,
          batteryPercentage: data.battery,
          isWifiConnected: data.wifi,
          isCommsConnected: data.comms,
          isRaspberryPiConnected: data.raspberryPi,
          mode: data.mode,
          docking: data.docking,
        };

        setStatusDTO(status);
        setIsLoading(false);
        setError(null);
      } catch (err) {
        setError("Failed to parse Turtlebot status");
        setIsLoading(false);
      }
    };

    socket.addEventListener("message", handleMessage);

    return () => {
      socket.removeEventListener("message", handleMessage);
    };
  }, [socket]);

  return { statusDTO, isLoading, error };
} */
