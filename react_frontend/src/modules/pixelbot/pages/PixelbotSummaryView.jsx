import "../styles/PixelbotSummaryView.css";
import CalendarHeatMap from "../components/CalendarHeatMap";
import { usePixelbotSummary } from "../hooks/usePixelbotSummary";

export default function PixelbotSummaryView() {
    const { summaryStats, isLoading } = usePixelbotSummary(); // Custom hook to fetch pixelbot summary data

    function handlePrint(elementId) { // Print functionality
        if (elementId) {
            const element = document.getElementById(elementId);
            if (element) {
                element.classList.add('print-visible');
                document.body.classList.add('printing-single-widget');

                const cleanup = () => {
                    element.classList.remove('print-visible');
                    document.body.classList.remove('printing-single-widget');
                    window.removeEventListener('afterprint', cleanup);
                };

                window.addEventListener('afterprint', cleanup);
                window.print();
            }
        } else {
            window.print();
        }
    }

    if (isLoading || !summaryStats) {
        return <div>Loading...</div>;
    }

    return (
        <div className="pixelbot-summary-page">
            <div className="summary-cards">
                <div className="summary-card teal">
                    <div className="card-info">
                        <span className="card-title">Total Sessions</span>
                        <span className="card-subtitle">Total sessions this month.      </span>
                        <span className="card-subtitle"> A <strong>{formatGrowthRate(summaryStats.sessionsGrowthRate)}% </strong> variation in usage compared with the previous month! </span> 
                    </div>
                    <span className="card-value">{summaryStats.totalSessions}</span>
                </div>

                <div className="summary-card dark">
                    <div className="card-info">
                        <span className="card-title">Sessions per day</span>
                        <span className="card-subtitle"> Daily average of robot sessions, based on all activity recorded this year up to today.</span>
                    </div>
                    <span className="card-value">{summaryStats.sessionsPerDay ?? 10}</span>
                </div>

                <div className="summary-card transparent">
                    <div className="card-info">
                        <span className="card-title">Sessions per child</span>
                        <span className="card-subtitle">Average sessions per child, based on all sessions recorded this year. </span>
                    </div>
                    <span className="card-value">{summaryStats.avgSessionsPerChild}</span>
                </div>
            </div>

            <CalendarHeatMap id="summary-heatmap" data={summaryStats.dailySessionCounts} onPrint={() => handlePrint('summary-heatmap')} />
        </div>
    );

    
    function formatGrowthRate(rate) {
        if (rate > 0) return `+${rate}`;
        return `${rate}`;
    }

}



