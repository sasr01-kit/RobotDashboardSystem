import { useState, useEffect } from 'react';
import { useWebSocketContext } from '../WebsocketUtil/WebsocketContext.js';

export function useTurtlebotGoal() {
  const { subscribe } = useWebSocketContext();
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState(null);

  
  useEffect(() => {
    if (!subscribe) return;

    return subscribe((data) => {
      if (data.type !== "GOAL_LOG_UPDATE") return;

      try {
        setLogs((prev) => [
          {
            id: data.id,
            label: data.label,
            fuzzy_output_goal: data.fuzzy_output_goal,
            fuzzy_output_human: data.fuzzy_output_human,
            timestamp: data.timestamp,
            feedback: data.feedback,
          },
          ...prev,
        ]);
      } catch {
        setError("Failed to handle goal log");
      }
    });
  }, [subscribe]);

  return { logs, error };
}
