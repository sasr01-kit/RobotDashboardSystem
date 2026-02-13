// Global state and listener management for Turtlebot feedback, allowing 
// consistent feedback data across different components without prop drilling 
// or multiple WebSocket subscriptions

// Default state structure for feedback data
let globalFeedbackState = {
  feedbackSummary: null,
  feedbackEntries: []
};

const feedbackListeners = new Set();

export function updateGlobalFeedbackState(patch) {
  globalFeedbackState = { ...globalFeedbackState, ...patch };
  feedbackListeners.forEach(fn => fn(globalFeedbackState));
}

import { useEffect, useState } from "react";
import { useWebSocketContext } from "../websocketUtil/WebsocketContext";

// Custom hook to provide Turtlebot feedback data to components
export function useTurtlebotFeedback() {
  const { subscribe } = useWebSocketContext();

  const [feedbackDTO, setFeedbackDTO] = useState(globalFeedbackState);

  useEffect(() => {
    // Hook is initialized, and subscribed to global feedback state updates for consistency across components and pages
    feedbackListeners.add(setFeedbackDTO);
    setFeedbackDTO(globalFeedbackState);

    return () => feedbackListeners.delete(setFeedbackDTO);
  }, []);

  useEffect(() => {
    if (!subscribe) return;

    return subscribe((data) => {
      // Debug log for incoming feedback-related messages from the backend
      console.log("[FEEDBACK HOOK] incoming:", data);
      // Parse incoming Websocket messages
      try {
        if (data.type === "FEEDBACK_SUMMARY") {
          updateGlobalFeedbackState({
            feedbackSummary: {
              goodRatio: data.goodRatio ?? 0,
              badRatio: data.badRatio ?? 0,
            }
          });
        }

        if (data.type === "FEEDBACK_ENTRY") {
          updateGlobalFeedbackState({
            feedbackEntries: [
              ...globalFeedbackState.feedbackEntries,
              {
                startPoint: data.startPoint,
                endPoint: data.endPoint,
                duration: data.duration,
                feedback: data.feedback,
              }
            ]
          });
        }
      } catch {
        console.error("Failed to parse Turtlebot feedback");
      }
    });
  }, [subscribe]);

  return {
    feedbackSummaryDTO: feedbackDTO.feedbackSummary,
    feedbackEntries: feedbackDTO.feedbackEntries
  };
}
