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
                dailySessionCounts: transformBackendDataToHeatmap(data.dailySessionCounts),
                colorScale: data.colorScale || getDefaultColorScale()
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

    /*
    // Backend API Response Example
    {
    "totalSessionsThisMonth": 245,
    "sessionsPerChild": 12.5,
    "sessionsPerDay": 8.2,
    "sessionsGrowthRate": 15.3,
    "dailySessionCounts": {
        "01-02-2026": 8,
        "02-02-2026": 12,
        "03-02-2026": 5,
        // ... more dates
    },
    "colorScale": {
        "dataClasses": [
        {
            "from": 0,
            "to": 0,
            "color": "#ebedf0",
            "name": "No usage",
            "label": "0"
        },
        {
            "from": 1,
            "to": 2,
            "color": "#c6e48b",
            "name": "Low",
            "label": "1–2"
        },
        {
            "from": 3,
            "to": 5,
            "color": "#7bc96f",
            "name": "Medium",
            "label": "3–5"
        },
        {
            "from": 6,
            "to": 8,
            "color": "#239a3b",
            "name": "High",
            "label": "6–8"
        },
        {
            "from": 9,
            "to": 999,
            "color": "#196127",
            "name": "Intense",
            "label": "9+"
        }
        ]
    }
    }

    // NOTES:
    // - colorScale is optional. If not provided, default colors will be used
    // - Each dataClass needs: from, to, color, name, and label fields
    // - The 'label' field is what appears in the legend below the heatmap
    // - The 'name' field is used for tooltips and first/last legend labels 
    */

    // THIS CAN BE MOVED TO BACKEND BUT FOR NOW BACKEND DOES NOT PROVIDE DATA IN HEATMAP FORMAT SO TRANSFORMING HERE
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

    // FOR FALLBACK, CAN BE REMOVED ONCE BACKEND PROVIDES COLOR SCALE CONFIG
    const getDefaultColorScale = () => ({
        dataClasses: [
            {
                from: 0,
                to: 0,
                color: '#ebedf0',
                name: 'No usage',
                label: '0'
            },
            {
                from: 1,
                to: 2,
                color: '#c6e48b',
                name: 'Low',
                label: '1–2'
            },
            {
                from: 3,
                to: 5,
                color: '#7bc96f',
                name: 'Medium',
                label: '3–5'
            },
            {
                from: 6,
                to: 8,
                color: '#239a3b',
                name: 'High',
                label: '6–8'
            },
            {
                from: 9,
                to: 999,
                color: '#196127',
                name: 'Intense',
                label: '9+'
            }
        ]
    });

    return { summaryStats, isLoading, error };
}