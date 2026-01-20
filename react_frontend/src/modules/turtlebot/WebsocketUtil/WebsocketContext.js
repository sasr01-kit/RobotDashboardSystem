import { createContext, useContext } from "react";

export const WebSocketContext = createContext(null);

export const useWebSocketContext = () => useContext(WebSocketContext);