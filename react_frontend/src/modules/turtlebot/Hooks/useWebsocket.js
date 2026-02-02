import { useEffect, useRef, useCallback } from "react";

export const useWebSocket = (url) => {
  const socketRef = useRef(null);

  useEffect(() => {
    const socket = new WebSocket(url);
    socketRef.current = socket;

    socket.onopen = () => console.log('WS connected');
    socket.onclose = () => console.log('WS disconnected');
    socket.onerror = (e) => console.error('WS error', e);

    return () => socket.close();
  }, [url]);

  const send = useCallback((message) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify(message));
    }
  }, []);

  return {
    socket: socketRef.current,
    send,
  };
};