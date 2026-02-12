import { useEffect, useRef, useState } from "react";
import WebSocketContext from "./WebsocketContext.js";

export default function WebSocketProvider({ children }) {
  const socketRef = useRef(null);
  const subscribersRef = useRef(new Set());
  const [isConnected, setIsConnected] = useState(false);

  const connect = () => {
    console.log("[WS] Attempting connection...");
    const ws = new WebSocket("ws://localhost:8080/ws");
    socketRef.current = ws;

    ws.onopen = () => {
      console.log("[WS] Connected");
      setIsConnected(true);
    };

    ws.onclose = () => {
      console.log("[WS] Disconnected. Reconnecting in 1s...");
      setIsConnected(false);
      setTimeout(connect, 1000); // auto-reconnect
    };

    ws.onerror = (err) => {
      console.error("[WS] Error:", err);
      ws.close(); // triggers reconnect
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
