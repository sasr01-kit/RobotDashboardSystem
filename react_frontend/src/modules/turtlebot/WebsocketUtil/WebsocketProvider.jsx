import { useWebSocket } from '../../Hooks/useWebsocket';
import { WebSocketContext } from './WebsocketContext';

const WebSocketProvider = ({ children }) => {
    /* CHANGE TO ACTUAL WEBSOCKET ENTRY POINT LATER */
  const ws = useWebSocket("ws://localhost:8080");

  return (
    <WebSocketContext.Provider value={ws}>
      {children}
    </WebSocketContext.Provider>
  );
};

export default WebSocketProvider;
