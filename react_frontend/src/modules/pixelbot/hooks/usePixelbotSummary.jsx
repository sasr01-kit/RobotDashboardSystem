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
            const summaryStatsDTO = {
                totalSessions: data.totalSessionsThisMonth,
                avgSessionsPerChild: data.sessionsPerChild,
                sessionsPerDay: data.sessionsPerDay,
                sessionsGrowthRate: data.sessionsGrowthRate,
                dailySessionCounts: transformBackendDataToHeatmap(data.dailySessionCounts),
                colorScale: data.colorScale || getDefaultColorScale()
            }

            setSummaryStats(summaryStatsDTO);
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

    
    // HIGHCHARTS HEATMAP EXPECTS DATA IN THE FORM OF {x: weekNumber, y: dayOfWeek, value: count, date: DateObject}
    const transformBackendDataToHeatmap = (backendData) => {
        const parseDate = (dateStr) => {
            const [d, m, y] = dateStr.split("-");
            return new Date(Date.UTC(y, m - 1, d));
        };

        const entries = Object.entries(backendData)
            .map(([key, value]) => ({
                date: parseDate(key),
                value
            }))
            .sort((a, b) => a.date - b.date);

        if (entries.length === 0) return [];

        const firstDate = entries[0].date;
        const firstMonday = new Date(firstDate);
        const day = firstMonday.getUTCDay();
        firstMonday.setUTCDate(firstMonday.getUTCDate() + (day === 0 ? -6 : 1 - day));

        return entries.map(({ date, value }) => {
            const diffDays = Math.floor((date - firstMonday) / 86400000);
            const weekNumber = Math.floor(diffDays / 7);

            let dayIndex = date.getUTCDay();
            dayIndex = dayIndex === 0 ? 6 : dayIndex - 1;

            return {
                x: weekNumber,
                y: dayIndex,
                value,
                date
            };
        });
    };
    return { summaryStats, isLoading, error };
}