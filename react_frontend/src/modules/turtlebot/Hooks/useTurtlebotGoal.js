import { useState, useEffect } from 'react';
import { useWebSocketContext } from '../WebsocketUtil/WebsocketContext.js';

export function useTurtlebotGoal() {
  const { socket } = useWebSocketContext();
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!socket) return;

    const handleMessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === "GOAL_LOG_UPDATE") {
          const log = {
            id: data.id,
            label: data.label,
            fuzzy_output_goal: data.fuzzy_output_goal,
            fuzzy_output_human: data.fuzzy_output_human,
            timestamp: data.timestamp,
            feedback: data.feedback,
          };
          setLogs((prev) => [log, ...prev]);
        }
      } catch {
        setError("Failed to parse goal log");
      }
    };

    socket.addEventListener("message", handleMessage);
    return () => socket.removeEventListener("message", handleMessage);
  }, [socket]);

  return { logs, error };
}
