// -------------------------------------------------------------
// GLOBAL FEEDBACK STORE
// -------------------------------------------------------------

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
import { useWebSocketContext } from "../WebsocketUtil/WebsocketContext";

export function useTurtlebotFeedback() {
  const { subscribe } = useWebSocketContext();

  const [feedbackDTO, setFeedbackDTO] = useState(globalFeedbackState);

  useEffect(() => {
    // Register this hook instance as a listener
    feedbackListeners.add(setFeedbackDTO);
    setFeedbackDTO(globalFeedbackState);

    return () => feedbackListeners.delete(setFeedbackDTO);
  }, []);

  useEffect(() => {
    if (!subscribe) return;

    return subscribe((data) => {
      console.log("[FEEDBACK HOOK] incoming:", data);
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
