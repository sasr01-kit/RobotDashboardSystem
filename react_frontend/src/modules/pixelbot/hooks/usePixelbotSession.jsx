import { useEffect, useState } from "react";

export function usePixelbotSession(childId, sessionId = null) {
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
          const res = await fetch(`http://localhost:9090/pixelbot/children/${childId}`);
          if (!res.ok) throw new Error("Child not found");

          const data = await res.json();
          setChild(data);
          setSession(null);
        } else {
          // Fetch specific session
          const res = await fetch(
            `http://localhost:9090/pixelbot/children/${childId}/sessions/${sessionId}`
          );
          if (!res.ok) throw new Error("Session not found");

          const data = await res.json();

          setSession(data);
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
