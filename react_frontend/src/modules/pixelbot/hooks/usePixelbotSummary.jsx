import { useEffect, useState } from "react"

export function usePixelbotSummary() {
    const [summaryStats, setSummaryStats] = useState(null); // SummaryStatsDTO
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchSummaryStats();
    }, []);

    async function fetchSummaryStats() {
        try {
            setIsLoading(true);
            setError(null);
            const response = await fetch(`http://localhost:8080/pixelbot/summary`); // FOR REAL IMPLEMENTATION CHANGE url TO API ENDPOINT
            const data = await response.json();
            const summary = {
                totalSessions: data.totalSessionsThisMonth,
                avgSessionsPerChild: data.sessionsPerChild,
                sessionsPerDay: data.sessionsPerDay,
                sessionsGrowthRate: data.sessionsGrowthRate,
                dailySessionCounts: transformBackendDataToHeatmap(data.dailySessionCounts) 
            }

            setSummaryStats(summary);
            setIsLoading(false);
            setError(null);
        }
        catch (err) {
            setError("Failed to fetch summary stats");
            console.error(err);
        }
        finally {
            setIsLoading(false);
        }
    };

    // FOR REAL IMPLEMENTATION THIS FUNCTION WILL TRANSFORM BACKEND DATA(Map<string, integer>) TO HEATMAP DATA
    const transformBackendDataToHeatmap = (backendData) => {
        const heatmapData = [];

        const sortedDates = Object.keys(backendData).sort();
        if (sortedDates.length === 0) return [];

        const firstDate = new Date(sortedDates[0]);
        const lastDate = new Date(sortedDates[sortedDates.length - 1]);

        const firstMonday = new Date(firstDate);
        const dayOfWeek = firstMonday.getDay();
        const daysUntilMonday = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
        firstMonday.setDate(firstMonday.getDate() + daysUntilMonday);

        sortedDates.forEach(dateStr => {
            
            // dd-mm-yyyy → yyyy-mm-dd
            const [d, m, y] = dateStr.split("-");
            const currentDate = new Date(`${y}-${m}-${d}`);

            const value = backendData[dateStr];

            const diffTime = currentDate - firstMonday;
            const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
            const weekNumber = Math.floor(diffDays / 7);

            let dayIndex = currentDate.getDay();
            dayIndex = dayIndex === 0 ? 6 : dayIndex - 1;

            heatmapData.push({
                x: weekNumber,
                y: dayIndex,
                value: value,
                date: currentDate
            });
        });

        return heatmapData;
    };

    return { summaryStats, isLoading, error };
}