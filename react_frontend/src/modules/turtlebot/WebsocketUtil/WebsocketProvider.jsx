import { useEffect, useRef } from "react";
import { useWebSocket } from '../Hooks/useWebsocket';
import { WebSocketContext } from './WebsocketContext';

export default function WebSocketProvider({ children }) { 
  const { socket, lastMessage } = useWebSocket("ws://localhost:8080/ws"); 
  
  const subscribersRef = useRef(new Set()); 
  
  useEffect(() => { 
    if (!lastMessage) return; 
    subscribersRef.current.forEach((callback) => callback(lastMessage)); 
  }, [lastMessage]);
  
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

