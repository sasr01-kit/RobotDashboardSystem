import '../styles/ChildSessionView.css';
import DashboardCard from '../components/DashboardCard';
import ImageCarousel from '../components/ImageCarousel';
import { usePixelbotSession } from '../hooks/usePixelbotSession';
import { usePixelbotChildren } from '../hooks/usePixelbotChildren';
import { useParams } from 'react-router-dom';

export default function ChildSessionView() {
    const { childId, sessionId } = useParams();
    const { children } = usePixelbotChildren(); // Fetch all children data with hook
    const { session, isLoading } = usePixelbotSession(childId, sessionId); // Fetch specific session data with hook

    const child = children ? children.find(c => c.childId == childId) : null;
    const name = child ? child.name : '';

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

    if (isLoading || !session) {
        return <div>Loading...</div>;
    }

    return (
        <div id="child-session-view" className="child-recap-page">
            <div className="page-header">
                <svg onClick={() => handlePrint('child-session-view')} className="print-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ cursor: 'pointer' }}>
                    <polyline points="6 9 6 2 18 2 18 9"></polyline>
                    <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                    <rect x="6" y="14" width="12" height="8"></rect>
                </svg>
                <h3>{name} - {sessionId}</h3>
            </div>

            <div className="child-recap-view">
                <div className="session-grid">
                    {/* Left Column */}
                    <div className="session-column-drawing-and-transcript">
                        <DashboardCard id="session-drawing" title="Drawing" onPrint={() => handlePrint('session-drawing')}>
                            <ImageCarousel images={session.drawing} />
                        </DashboardCard>

                        <DashboardCard id="session-transcript" title="Text Transcript" onPrint={() => handlePrint('session-transcript')} className="transparent">
                            <div className="transcript-container"> 
                                {session.transcript?.map((line, index) => (
                                    <div key={index}>
                                        <strong>{line.name}:</strong> {line.description}
                                    </div>
                            ))}
                        </div>
                        </DashboardCard>
                    </div>

                    {/* Middle Column */}
                    <div className="session-column">
                        <DashboardCard
                            id="session-summary"
                            title="Story Summary"
                            subtitle={`Number of objects detected : ${session.storySummary?.length}`}
                            onPrint={() => handlePrint('session-summary')}
                            className="teal-header"
                        >
                            <div className="summary-table-container">
                                <table className="summary-table">
                                    <thead>
                                        <tr>
                                            <th>Name</th>
                                            <th>Description</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {session.storySummary?.map((item, index) => (
                                            <tr key={index}>
                                                <td>{item.name}</td>
                                                <td>{item.description}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </DashboardCard>
                    </div>

                    {/* Right Column */}
                    <div className="session-column-specific-metrics">
                       <DashboardCard id="session-speech-data" title="Speech Data" onPrint={() => handlePrint('session-speech-data')} className="teal-header">
                            <div className="data-list">
                                <div className="data-row">
                                    <span className="label">Number of intervention </span>
                                    <span className="value">{session.speechWidth?.intervention_count}</span>
                                </div>
                                <div className="data-row">
                                    <span className="label">Total word count </span>
                                    <span className="value">{session.speechWidth?.total_word_count}</span>
                                </div>
                                <div className="data-row">
                                    <span className="label">Average word count per intervention </span>
                                    <span className="value">{session.speechWidth?.average_word_count_per_intervention}</span>
                                </div>
                                <div className="data-row">
                                    <span className="label">Standard word count per intervention </span>
                                    <span className="value">{session.speechWidth?.std_word_count_per_intervention}</span>
                                </div>
                                  <div className="data-row">
                                    <span className="label">Total speech time </span>
                                    <span className="value">{session.speechWidth?.total_speech_time}</span>
                                </div>
                                <div className="data-row">
                                    <span className="label">Average speech time per intervention </span>
                                    <span className="value">{session.speechWidth?.average_speech_time_per_intervention}</span>
                                </div>
                                <div className="data-row">
                                    <span className="label">Standard word count per intervention </span>
                                    <span className="value">{session.speechWidth?.std_speech_time_per_intervention}</span>
                                </div>
                                <div className="data-row">
                                    <span className="label">Average intimacy sore</span>
                                    <span className="value">{session.speechDepth?.average_intimacy_score}</span>
                                </div>
                                <div className="data-row">
                                    <span className="label">Standard intimacy sore</span>
                                    <span className="value">{session.speechDepth?.std_intimacy_score}</span>
                                </div>
                            </div>
                        </DashboardCard>

                        <DashboardCard id="session-drawing-data" title="Drawing Data" onPrint={() => handlePrint('session-drawing-data')} className="teal-header">
                            <div className="data-list">
                                <div className="data-row" >
                                    <span className="label">Number of strokes</span>
                                    <span className="value">{session.drawingWidth?.stroke_count}</span>
                                </div>
                                <div className="data-row" >
                                    <span className="label">Total stroke length </span>
                                    <span className="value">{session.drawingWidth?.total_stroke_length}</span>
                                </div>
                                <div className="data-row" >
                                    <span className="label">Average stroke length</span>
                                    <span className="value">{session.drawingWidth?.average_stroke_length}</span>
                                </div>
                                <div className="data-row" >
                                    <span className="label">Standard deviation of stroke length</span>
                                    <span className="value">{session.drawingWidth?.std_stroke_length}</span>
                                </div>
                                <div className="data-row" >
                                    <span className="label">Number of colors used</span>
                                    <span className="value">{session.drawingWidth?.color_used_count}</span>
                                </div>
                                <div className="data-row" >
                                    <span className="label">Pen size used count</span>
                                    <span className="value">{session.drawingWidth?.pen_size_used_count}</span>
                                </div>
                                <div className="data-row" >
                                    <span className="label">Amount of area filled</span>
                                    <span className="value">{session.drawingWidth?.amount_filled_area}</span>
                                </div>
                            </div>
                        </DashboardCard>
                    </div>
                </div>
            </div>
        </div>
    );
}