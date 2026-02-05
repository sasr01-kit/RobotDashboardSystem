import { useEffect, useState } from "react";

export function usePixelbotRecap(childId, sessionId = null) {
  const [session, setSession] = useState(null);
  const [child, setChild] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Early return if no childId
    if (!childId) {
      setChild(null);
      setSession(null);
      return;
    }

    const fetchData = async () => {
      setIsLoading(true);
      setError(null);

      try {
        if (!sessionId) {
          // Fetch child recap
          const res = await fetch(`http://localhost:8080/pixelbot/children/${childId}`);
          if (!res.ok) throw new Error("Child not found");

          const data = await res.json();

          const totalSessions = data.sessions.length;
          const recapData = {
            childName: data.name,
            wordCountData: data.sessions.map(s => ({
              label: s.sessionId,
              value: parseInt(s.speechWidth?.totalWordCount) || 0
            })),
            speechTimeData: data.sessions.map(s => ({
              label: s.sessionId,
              value: (s.speechWidth?.totalSpeechTime || 0) / 60,
            })),
            colorsUsedData: [], // Backend does not provide colors used data currently
            drawings: data.sessions.map(s => s.drawing).filter(Boolean),
            metricValues: {
              totalSessions: totalSessions,
              totalSessionsTrend: "0", // Placeholder can be changed with real trend data logic
              totalWordCount: data.sessions.reduce(
                (sum, s) => sum + (parseInt(s.speechWidth?.totalWordCount) || 0),
                0
              ),
              totalWordCountTrend: "0", // Placeholder can be changed with real trend data logic
              averageIntimacyScore: totalSessions === 0
                ? 0
                : data.sessions.reduce(
                    (sum, s) => sum + (parseFloat(s.speechDepth?.avgIntimacyScore) || 0),
                    0
                  ) / totalSessions,
              averageIntimacyScoreTrend: "0" // Placeholder can be changed with real trend data logic
            }
          };

          setChild(recapData);
          setSession(null);
        } else {
          // Fetch specific session
          const res = await fetch(
            `http://localhost:8080/pixelbot/children/${childId}/sessions/${sessionId}`
          );
          if (!res.ok) throw new Error("Session not found");

          const data = await res.json();

          const normalizedSession = {
            // 
            ...data,
            drawing: data.drawing
              ? [
                  {
                    ...data.drawing,
                    imagePath: data.drawing.imagePath
                  }
                ]
              : []
          };

          setSession(normalizedSession);
          setChild(null);
        }
      } catch (err) {
        setError("Failed to load data.");
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [childId, sessionId]);

  return { child, session, isLoading, error };
}
