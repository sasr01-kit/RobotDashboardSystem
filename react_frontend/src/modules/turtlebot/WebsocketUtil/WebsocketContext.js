import { createContext, useContext } from "react";

const WebSocketContext = createContext(null);

export default WebSocketContext;

export function useWebSocketContext() {
  return useContext(WebSocketContext);
}