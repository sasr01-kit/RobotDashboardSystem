import { useEffect, useState } from "react"

export function usePixelbotSummary() {
    const [summaryStats, setSummaryStats] = useState(null); // SummaryStatsDTO
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    // MOCK DATA
    const generateMockBackendData = () => {
        const mockData = {};
        const startDate = new Date('2026-01-01');
        const endDate = new Date('2026-12-31');

        let currentDate = new Date(startDate);

        while (currentDate <= endDate) {
            // (YYYY-MM-DD)
            const dateStr = currentDate.toISOString().split('T')[0];
            // Random value (0-10)
            mockData[dateStr] = Math.floor(Math.random() * 11);

            currentDate.setDate(currentDate.getDate() + 1);
        }

        return mockData;
    };
    // END MOCK DATA

    useEffect(() => {
        fetchSummaryStats();
    }, []);

    async function fetchSummaryStats() {
        try {
            setIsLoading(true);
            setError(null);
            /*const response = await fetch(url);
            const data = await response.json();
            data.dailySessionsCount = transformBackendDataToHeatmap(data.dailySessionsCount);
            setSummaryStats(data);  TODO: Implement actual data fetching */
            setSummaryStats({ // MOCK DATA
                totalSessions: 315,
                avgSessionsPerChild: 10,
                dailySessionsCount: transformBackendDataToHeatmap(generateMockBackendData())
            });
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
            const currentDate = new Date(dateStr);
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