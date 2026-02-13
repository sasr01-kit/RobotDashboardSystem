// Global state and listener management for Turtlebot goal data, allowing 
// consistent goal-related data across different components without prop drilling 
// or multiple WebSocket subscriptions

// Default state structure for goal data
let globalGoalState = {
  pathHistory: [],
  isPathModuleActive: false,
  isDocked: false
};

const goalListeners = new Set();

export function updateGlobalGoalState(patch) {
  globalGoalState = { ...globalGoalState, ...patch };
  goalListeners.forEach(fn => fn(globalGoalState));
}

import { useState, useEffect } from "react";
import { useWebSocketContext } from "../websocketUtil/WebsocketContext";

export function useTurtlebotGoal() {
  const { subscribe } = useWebSocketContext();

  const [goalDTO, setGoalDTO] = useState(globalGoalState);

  useEffect(() => {
    // Hook is initialized, and subscribed to global goal state updates for consistency across components and pages
    goalListeners.add(setGoalDTO);
    setGoalDTO(globalGoalState);
    return () => goalListeners.delete(setGoalDTO);
  }, []);

  useEffect(() => {
    if (!subscribe) return;

    return subscribe((data) => {
      if (data.type !== "PATH_UPDATE") return;
      // Debug log for incoming path-related messages from the backend
      console.log("[GOAL HOOK] incoming PATH_DATA:", data);

      // Parse backend pathHistory for frontend use
      const parsedHistory = (data.pathHistory || []).map(entry => ({
        id: entry.id,
        label: entry.label,
        timestamp: entry.timestamp,
        goalType: entry.goalType,
        fuzzy_output_goal: entry.fuzzyOutput,
        feedback: entry.userFeedback || ""
      }));

      updateGlobalGoalState({
        pathHistory: parsedHistory,
        isPathModuleActive:
          data.isPathModuleActive ?? globalGoalState.isPathModuleActive,
        isDocked: data.isDocked ?? globalGoalState.isDocked
      });
    });
  }, [subscribe]);

  return goalDTO;
}
