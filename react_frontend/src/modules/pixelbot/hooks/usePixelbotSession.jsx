import { useEffect, useState } from "react";

export function usePixelbotSession(childId, sessionId) {
  const [session, setSession] = useState(null); // SessionDTO
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
        // Fetch specific session
        const res = await fetch(
          `http://localhost:8080/pixelbot/children/${childId}/sessions/${sessionId}`
        );
        if (!res.ok) throw new Error("Session not found");

        const sessionListEntryDTO = await res.json();

        setSession(sessionListEntryDTO);
        setChild(null);
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