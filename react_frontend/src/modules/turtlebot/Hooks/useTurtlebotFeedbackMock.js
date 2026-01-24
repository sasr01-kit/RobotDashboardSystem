import { useEffect, useState } from "react";

export function useTurtlebotFeedbackMock() {
  const [feedbackSummaryDTO, setFeedbackSummaryDTO] = useState({
    goodRatio: 0,
    badRatio: 0
  });

  const [feedbackEntries, setFeedbackEntries] = useState([]);
  const [isLoading] = useState(false);
  const [error] = useState(null);

  useEffect(() => {
    let goodCount = 0;
    let badCount = 0;

    const interval = setInterval(() => {
      // Generate a random entry
      const newEntry = {
        id: crypto.randomUUID(),
        startPoint: `Goal ${Math.floor(Math.random() * 5) + 1}`,
        endPoint: `Goal ${Math.floor(Math.random() * 5) + 1}`,
        duration: `${String(Math.floor(Math.random() * 10)).padStart(2, "0")}:${String(Math.floor(Math.random() * 60)).padStart(2, "0")}:${String(Math.floor(Math.random() * 60)).padStart(2, "0")}`,
        feedback: Math.random() > 0.3 ? "GOOD" : "BAD"
      };

      // Update entry list
      setFeedbackEntries(prev => [...prev, newEntry]);

      // Update summary
      if (newEntry.feedback === "GOOD") goodCount++;
      else badCount++;

      setFeedbackSummaryDTO({
        goodRatio: goodCount,
        badRatio: badCount
      });
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return {
    feedbackSummaryDTO,
    feedbackEntries,
    isLoading,
    error
  };
}
