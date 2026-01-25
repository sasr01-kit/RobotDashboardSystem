import { useWebSocket } from '../../Hooks/useWebsocket';
import { WebSocketContext } from './WebsocketContext';

const WebSocketProvider = ({ children }) => {
  const ws = useWebSocket("ws://localhost:9090");

  return (
    <WebSocketContext.Provider value={ws}>
      {children}
    </WebSocketContext.Provider>
  );
};

export default WebSocketProvider;
