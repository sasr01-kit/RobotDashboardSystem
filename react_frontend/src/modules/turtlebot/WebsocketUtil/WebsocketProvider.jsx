import { useRef } from "react";
import { useWebSocket } from '../Hooks/useWebsocket';
import { WebSocketContext } from './WebsocketContext';

export default function WebSocketProvider({ children }) { 
  const { socket, lastMessage } = useWebSocket("ws://localhost:9090/ws"); 
  
  const subscribersRef = useRef(new Set()); 
  
  if (lastMessage) { 
    subscribersRef.current.forEach((callback) => callback(lastMessage)); 
  } 
  
  const subscribe = (callback) => { 
    subscribersRef.current.add(callback); 
    return () => { subscribersRef.current.delete(callback); }; 
  }; 

  return ( 
  <WebSocketContext.Provider 
    value={{ subscribe }}> {children} 
    </WebSocketContext.Provider> 
  ); 
}

