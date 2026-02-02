import "../styles/ChildRecapView.css";
import DashboardCard from '../components/DashboardCard';
import MetricCard from '../components/MetricCard';
import ImageCarousel from '../components/ImageCarousel';
import BarChart from '../components/BarChart';
import LineChart from '../components/LineChart';
import StackedBarChart from '../components/StackedBarChart';
import WordCheckIcon from '../assets/wordCheck.svg';
import UsersIcon from '../assets/users.svg';
import { usePixelbotSession } from "../hooks/usePixelbotSession";
import { useParams } from "react-router-dom";

export default function ChildRecapView() {
    const { childId } = useParams();
    const { child, isLoading } = usePixelbotSession(childId); // Custom hook to fetch just child data (can be changed)

    function handlePrint(elementId) { // Print function
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

    if (isLoading || !child) {
        return <div>Loading...</div>;
    }

    return (
        <div id="child-recap-view" className="child-recap-page">
            <div className="page-header">
                <svg onClick={() => handlePrint('child-recap-view')} className="print-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ cursor: 'pointer' }}>
                    <polyline points="6 9 6 2 18 2 18 9"></polyline>
                    <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                    <rect x="6" y="14" width="12" height="8"></rect>
                </svg>
                <h3>{child.childName} — Recap</h3>
            </div>
            <div className="child-recap-view">
                <div className="recap-grid">
                    {/* Left Column - Drawings & Speech Time */}
                    <div className="recap-column">
                        <DashboardCard id="recap-drawings" title="Drawing(s)" onPrint={() => handlePrint('recap-drawings')}>
                            <ImageCarousel images={child.drawings} />
                        </DashboardCard>

                        <DashboardCard id="recap-speech" title="Speech Time" onPrint={() => handlePrint('recap-speech')} className="transparent">
                            <LineChart
                                data={child.speechTimeData}
                                xAxisLabel="Sessions"
                                yAxisLabel="Minutes"
                            />
                        </DashboardCard>
                    </div>

                    {/* Middle Column - Word Count & Colors Used */}
                    <div className="recap-column">
                        <DashboardCard
                            id="recap-word-count"
                            title="Word Count"
                            onPrint={() => handlePrint('recap-word-count')}
                            className="transparent"
                        >
                            <BarChart
                                data={child.wordCountData}
                                color="#4CAF50"
                                yAxisLabel="Words"
                            />
                        </DashboardCard>

                        <DashboardCard
                            id="recap-colors"
                            title="Colors Used"
                            onPrint={() => handlePrint('recap-colors')}
                            className="transparent"
                        >
                            <StackedBarChart
                                data={child.colorsUsedData}
                                orientation="horizontal"
                                xAxisLabel="Usage Count"
                            />
                        </DashboardCard>
                    </div>

                    {/* Right Column - Metrics */}
                    <div className="recap-column">
                        <MetricCard
                            title="Total Sessions"
                            value={child.metricValues.totalSessions}
                            subtitle="From last month"
                            trendValue={child.metricValues.totalSessionsTrend}
                            icon={<img src={UsersIcon} alt="" style={{ width: 28, height: 28, opacity: 0.6 }} />}
                        />

                        <MetricCard
                            title="Total Word Count"
                            value={child.metricValues.totalWordCount}
                            subtitle="Across all month"
                            trendValue={child.metricValues.totalWordCountTrend}
                            icon={<img src={WordCheckIcon} alt="" style={{ width: 28, height: 28, opacity: 0.6 }} />}
                        />

                        <MetricCard
                            title="Average Intimacy Score"
                            value={child.metricValues.averageIntimacyScore}
                            subtitle="From last month"
                            unit="%"
                            trendValue={child.metricValues.averageIntimacyScoreTrend}
                            icon={<img src={UsersIcon} alt="" style={{ width: 28, height: 28, opacity: 0.6 }} />}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
}
