import { createContext, useContext } from "react";

// Create a Context for the WebSocket connection for consistent access 
// across components and pages without prop drilling
const WebSocketContext = createContext(null);

export default WebSocketContext;

// Custom hook to access the WebSocket context
export function useWebSocketContext() {
  return useContext(WebSocketContext);
}