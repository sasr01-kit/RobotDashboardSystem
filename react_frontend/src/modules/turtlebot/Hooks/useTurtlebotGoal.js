// -------------------------------------------------------------
// GLOBAL PATH STORE
// -------------------------------------------------------------

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
import { useWebSocketContext } from "../WebsocketUtil/WebsocketContext";

export function useTurtlebotGoal() {
  const { subscribe } = useWebSocketContext();

  // Initialize from global store
  const [goalDTO, setGoalDTO] = useState(globalGoalState);

  // Subscribe this hook instance to global store updates
  useEffect(() => {
    goalListeners.add(setGoalDTO);
    setGoalDTO(globalGoalState);
    return () => goalListeners.delete(setGoalDTO);
  }, []);

  // Subscribe to WebSocket messages
  useEffect(() => {
    if (!subscribe) return;

    return subscribe((data) => {
      if (data.type !== "PATH_UPDATE") return;

      console.log("[GOAL HOOK] incoming PATH_DATA:", data);

      // Parse backend pathHistory
      const parsedHistory = (data.pathHistory || []).map(entry => ({
        id: entry.id,
        label: entry.label,
        timestamp: entry.timestamp,
        goalType: entry.goalType,

        // Split fuzzyOutput into goal + human parts if needed
        fuzzy_output_goal: entry.fuzzyOutput || "",
        fuzzy_output_human: entry.fuzzyOutput || "",

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
