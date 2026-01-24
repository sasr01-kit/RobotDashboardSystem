import { useEffect, useState } from "react";

export function usePixelbotChildren() {
    const [children, setChildren] = useState();
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    // MOCK DATA
    const sessionsData = [
        { sessionId: 's1' },
        { sessionId: 's2' },
        { sessionId: 's3' },
        { sessionId: 's4' },
        { sessionId: 's5' },
        { sessionId: 's6' },
        { sessionId: 's7' },
        { sessionId: 's8' },
    ];

    const childrenData = [
        { childId: 'child1', name: 'Child name', sessions: sessionsData },
        { childId: 'child2', name: 'Child name', sessions: sessionsData },
        { childId: 'child3', name: 'Child name', sessions: sessionsData },
        { childId: 'child4', name: 'Child name', sessions: sessionsData },
        { childId: 'child5', name: 'Child name', sessions: sessionsData },
        { childId: 'child6', name: 'Child name', sessions: sessionsData },
        { childId: 'child7', name: 'Child name', sessions: sessionsData },
        { childId: 'child8', name: 'Child name', sessions: sessionsData },
        { childId: 'child9', name: 'Child name', sessions: sessionsData },
    ];
    // END MOCK DATA

    useEffect(() => {
        fetchChildren();
    }, []);

    async function fetchChildren() {
        try {
            setIsLoading(true);
            setError(null);
            /*const response = await fetch(url);
            const data = await response.json();
            setChildren(data);  TODO: Implement actual data fetching */
            setChildren(childrenData);
            setError(null);
        }
        catch (err) {
            setError("Failed to fetch children data.");
            console.error(err);
        }
        finally {
            setIsLoading(false);
        }
    }

    return { children, isLoading, error };
}