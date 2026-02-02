import { useEffect, useState } from "react";

export function useWebSocket(url) { 
  const [socket, setSocket] = useState(null); 
  const [lastMessage, setLastMessage] = useState(null); 
  useEffect(() => { 
    const ws = new WebSocket(url); 

    ws.onopen = () => console.log("WS connected"); 
    ws.onclose = () => console.log("WS disconnected"); 
    ws.onerror = (err) => console.log("WS error", err); 

    ws.onmessage = (event) => { 
      try { 
        const data = JSON.parse(event.data); 
        setLastMessage(data); 
      } catch (err) { 
        console.error("WS parse error", err); 
      } 
    }; 
    
    setSocket(ws); 
    return () => ws.close(); 
  }, [url]); return { socket, lastMessage }; 
}

/* export const useWebSocket = (url) => {
  const socketRef = useRef(null);
  const listenersRef = useRef(new Set());

  useEffect(() => {
    const socket = new WebSocket(url);
    socketRef.current = socket;

    socket.onopen = () => console.log('WS connected');
    socket.onclose = () => console.log('WS disconnected');
    socket.onerror = (e) => console.error('WS error', e);

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        listenersRef.current.forEach((cb) => cb(data));
      } catch (err) {
        console.error("WS parse error", err);
      }
    };

    return () => socket.close();
  }, [url]);

  const send = useCallback((message) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(message));
    }
  }, []);

  // Consumers subscribe to the provider for centralized listening
  const subscribe = useCallback((callback) => {
    listenersRef.current.add(callback);
    return () => listenersRef.current.delete(callback);
  }, []);

  return { send, subscribe };
}; */