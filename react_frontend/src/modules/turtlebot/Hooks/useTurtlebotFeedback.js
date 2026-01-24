import { useEffect, useState } from "react";
import { useWebSocketContext } from "../WebsocketUtil/WebsocketContext";

export function useTurtlebotFeedback() {
  const { socket } = useWebSocketContext();

  const [feedbackSummaryDTO, setFeedbackSummaryDTO] = useState(null);
  const [feedbackEntries, setFeedbackEntries] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!socket) return;

    const handleMessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === "FEEDBACK_SUMMARY") {
          const summary = {
            goodRatio: data.goodRatio ?? 0,
            badRatio: data.badRatio ?? 0
          };

          setFeedbackSummaryDTO(summary);
          setIsLoading(false);
          setError(null);
          return;
        }

        if (data.type === "FEEDBACK_ENTRY") {
          const entry = {
            startPoint: data.startPoint,
            endPoint: data.endPoint,
            duration: data.duration,
            feedback: data.feedback
          };

          setFeedbackEntries((prev) => [...prev, entry]);

          setIsLoading(false);
          setError(null);
          return;
        }

      } catch (err) {
        setError("Failed to parse Turtlebot feedback");
        setIsLoading(false);
      }
    };

    socket.addEventListener("message", handleMessage);

    return () => {
      socket.removeEventListener("message", handleMessage);
    };
  }, [socket]);

  return { feedbackSummaryDTO, feedbackEntries, isLoading, error };
}
