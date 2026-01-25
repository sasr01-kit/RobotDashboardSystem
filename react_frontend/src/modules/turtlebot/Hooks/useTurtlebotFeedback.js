import { useEffect, useState } from "react";
import { useWebSocketContext } from "../WebsocketUtil/WebsocketContext";

export function useTurtlebotFeedback() {
  const { subscribe } = useWebSocketContext();

  const [feedbackSummaryDTO, setFeedbackSummaryDTO] = useState(null);
  const [feedbackEntries, setFeedbackEntries] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!subscribe) return;

    return subscribe((data) => {
      try {
        if (data.type === "FEEDBACK_SUMMARY") {
          setFeedbackSummaryDTO({
            goodRatio: data.goodRatio ?? 0,
            badRatio: data.badRatio ?? 0,
          });
          setIsLoading(false);
          setError(null);
        }

        if (data.type === "FEEDBACK_ENTRY") {
          setFeedbackEntries((prev) => [
            ...prev,
            {
              startPoint: data.startPoint,
              endPoint: data.endPoint,
              duration: data.duration,
              feedback: data.feedback,
            },
          ]);
          setIsLoading(false);
          setError(null);
        }
      } catch {
        setError("Failed to parse Turtlebot feedback");
        setIsLoading(false);
      }
    });
  }, [subscribe]);

  return { feedbackSummaryDTO, feedbackEntries, isLoading, error };
}
