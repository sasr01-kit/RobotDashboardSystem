import "../styles/ChildRecapView.css";
import DashboardCard from '../components/DashboardCard';
import ImageCarousel from '../components/ImageCarousel';
import BarChart from '../components/BarChart';
import LineChart from '../components/LineChart';
import { useParams } from "react-router-dom";
import { usePixelbotRecap } from "../hooks/usePixelbotRecap";

export default function ChildRecapView() {
    const { childId } = useParams();
    const { child, isLoading } = usePixelbotRecap(childId); // Custom hook to fetch just child data (can be changed)


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
                <h3>{child.name} - Recap</h3>
            </div>
            <div className="child-recap-view">
                <div className="recap-grid">
                    {/* Left Column - Drawings & Speech Time */}
                    <div className="recap-column">
                        <DashboardCard id="recap-drawings" title="Drawing(s)" onPrint={() => handlePrint('recap-drawings')}>
                            <ImageCarousel images={child.drawings} />
                            <div style={{ marginTop: '20px', padding: '10px', backgroundColor: 'rgba(0,0,0,0.02)', borderRadius: '8px' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                                    <span style={{ fontSize: '13px', color: '#666' }}>Average Stroke Count:</span>
                                    <span style={{ fontSize: '14px', fontWeight: '600' }}>{child.metricValues.averageStrokeCount.toFixed(1)}</span>
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                                    <span style={{ fontSize: '13px', color: '#666' }}>Average Colors Used:</span>
                                    <span style={{ fontSize: '14px', fontWeight: '600' }}>{child.metricValues.averageNumberColors.toFixed(1)}</span>
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                    <span style={{ fontSize: '13px', color: '#666' }}>Average Filled Area:</span>
                                    <span style={{ fontSize: '14px', fontWeight: '600' }}>{child.metricValues.averageFilledArea.toFixed(1)}%</span>
                                </div>
                            </div>
                        </DashboardCard>

                        <DashboardCard id="recap-speech" title="Speech Time" onPrint={() => handlePrint('recap-speech')} className="transparent">
                            <LineChart
                                data={child.speechTimeData}
                                xAxisLabel="Sessions"
                                yAxisLabel="Minutes"
                            />
                        </DashboardCard>
                    </div>

                    {/* Middle Column - Total Sessions & Word Count & Intimacy Score */}
                    <div className="recap-column">
                        <DashboardCard
                            id="recap-sessions"
                            title="Total Sessions"
                            onPrint={() => handlePrint('recap-sessions')}
                            className="transparent"
                        >
                            <div style={{ display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
                                <div>
                                    <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#333' }}>
                                        {child.metricValues.totalSessions}
                                    </div>
                                    <div style={{ fontSize: '14px', color: child.metricValues.sessionTrendPercentage >= 0 ? '#4CAF50' : '#F44336', marginTop: '5px' }}>
                                        {child.metricValues.sessionTrendPercentage >= 0 ? '↑' : '↓'} {Math.abs(child.metricValues.sessionTrendPercentage)}% from last month
                                    </div>
                                </div>
                                <LineChart
                                    data={child.sessionFrequencyData}
                                    xAxisLabel="Month"
                                    yAxisLabel="Sessions"
                                />
                            </div>
                        </DashboardCard>

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
                                xAxisLabel="Sessions"
                                averageLine={child.metricValues.averageWordCount}
                            />
                            <div style={{ marginTop: '15px', textAlign: 'center', fontSize: '14px', color: '#666' }}>
                                <strong>Total Word Count:</strong> {child.metricValues.totalWordCount}
                            </div>
                        </DashboardCard>

                        <DashboardCard
                            id="recap-intimacy"
                            title="Intimacy Score"
                            onPrint={() => handlePrint('recap-intimacy')}
                            className="transparent"
                        >
                            <LineChart
                                data={child.intimacyScoreData}
                                xAxisLabel="Sessions"
                                yAxisLabel="Score"
                                averageLine={child.metricValues.averageIntimacyScore}
                            />
                        </DashboardCard>
                    </div>

                    {/* Right Column - Story Metrics */}
                    <div className="recap-column">
                        <DashboardCard
                            id="recap-story"
                            title="Story Metrics"
                            onPrint={() => handlePrint('recap-story')}
                        >
                            <div style={{ padding: '10px' }}>
                                <div style={{ marginBottom: '20px' }}>
                                    <div style={{ fontSize: '15px', color: '#666', marginBottom: '5px', fontWeight: '600' }}>Average Number of Objects</div>
                                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#333' }}>
                                        {child.metricValues.averageNumberObjects.toFixed(1)}
                                    </div>
                                </div>

                                <div style={{ marginBottom: '20px' }}>
                                    <div style={{ fontSize: '15px', color: '#666', marginBottom: '5px', fontWeight: '600' }}>Most Common Objects</div>
                                    {child.metricValues.mostCommonObjects.length > 0 ? (
                                        <ol style={{ margin: 0, paddingLeft: '20px' }}>
                                            {child.metricValues.mostCommonObjects.map(([name, count], idx) => (
                                                <li key={idx} style={{ fontSize: '13px', marginBottom: '5px' }}>
                                                    <strong>{name}</strong> ({count})
                                                </li>
                                            ))}
                                        </ol>
                                    ) : (
                                        <div style={{ fontSize: '13px', color: '#999' }}>No data available</div>
                                    )}
                                </div>

                                <div>
                                    <div style={{ fontSize: '15px', color: '#666', marginBottom: '5px', fontWeight: '600' }}>Object Diversity</div>
                                    <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#333' }}>
                                        {child.metricValues.objectDiversity}
                                    </div>
                                    <div style={{ fontSize: '12px', color: '#999' }}>unique objects</div>
                                </div>
                            </div>
                        </DashboardCard>
                    </div>
                </div>
            </div>
        </div>
    );
}
