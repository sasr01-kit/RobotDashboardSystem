import { useEffect, useState } from "react";

export function usePixelbotChildren() {
  const [children, setChildren] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchChildren = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const res = await fetch("http://localhost:8080/pixelbot/children");
        if (!res.ok) throw new Error("Failed to fetch children");

        const data = await res.json();
        
        // Map the API response to the ChildDto structure for consistency
        const childDTO = data.map(child => ({ 
            childId: child.child_id, 
            name: child.name, 
            sessions: child.sessions.map(s => ({ 
                sessionId: s.sessionId  
            })) 
        }));

        setChildren(childDTO);
      } catch (err) {
        setError("Failed to fetch children data.");
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchChildren();
  }, []);

  return { children, isLoading, error };
}
