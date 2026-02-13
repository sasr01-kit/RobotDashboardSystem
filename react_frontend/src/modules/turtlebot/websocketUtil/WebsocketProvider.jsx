import { useEffect, useRef, useState } from "react";
import WebSocketContext from "./WebsocketContext.js";

// Provider component to wrap around parts of the app that need access to the WebSocket connection
export default function WebSocketProvider({ children }) {
  const socketRef = useRef(null);
  const subscribersRef = useRef(new Set());
  const [isConnected, setIsConnected] = useState(false);

  const connect = () => {
    // Debug log for WebSocket connection attempts
    console.log("[WS] Attempting connection...");
    // Establish a WebSocket connection to the backend server, 
    // adjust the correct URL for the backend WebSocket endpoint as needed
    const ws = new WebSocket("ws://localhost:8080/ws");
    socketRef.current = ws;

    ws.onopen = () => {
      console.log("[WS] Connected");
      setIsConnected(true);
    };

    ws.onclose = () => {
      console.log("[WS] Disconnected. Reconnecting in 1s...");
      setIsConnected(false);
      setTimeout(connect, 1000); // Allows auto-reconnection
    };

    ws.onerror = (err) => {
      console.error("[WS] Error:", err);
      ws.close(); // Triggers reconnection
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        subscribersRef.current.forEach((cb) => cb(data));
      } catch (err) {
        console.error("[WS] Parse error:", err);
      }
    };
  };

  useEffect(() => {
    connect();
    return () => socketRef.current?.close();
  }, []);

  const send = (obj) => {
    const ws = socketRef.current;
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(obj));
    } else {
      console.warn("[WS] Tried to send but socket not open");
    }
  };

  const subscribe = (callback) => {
    subscribersRef.current.add(callback);
    return () => subscribersRef.current.delete(callback);
  };

  return (
    <WebSocketContext.Provider value={{ send, subscribe, isConnected }}>
      {children}
    </WebSocketContext.Provider>
  );
}
