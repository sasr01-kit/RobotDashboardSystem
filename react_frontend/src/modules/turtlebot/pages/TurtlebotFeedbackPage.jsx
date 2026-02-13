import '../styles/FeedbackPage.css';
import { FeedbackLogPanel } from "../components/FeedbackLogPanel.jsx";
import { useTurtlebotFeedback } from "../hooks/useTurtlebotFeedback.js";
import { FeedbackSummaryChart } from '../components/FeedbackSummaryChart';
import { motion } from 'framer-motion';

// This page displays a summary of feedback received from the Turtlebot, as well as a detailed log of individual feedback entries. 
// It uses the useTurtlebotFeedback hook to access feedback data.
export default function TurtlebotFeedbackPage() {
    const { feedbackEntries } = useTurtlebotFeedback(); 

    return (
        <div className="turtlebot-feedback-page">
            <div className="feedback-summary-container">
                <h2 className="feedback-summary-title">Feedback Summary</h2>
                <motion.div 
                    className="feedback-summary-chart"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <FeedbackSummaryChart />
                </motion.div>
            </div>
            <div className="feedback-log-container">
                <h2 className="feedback-log-title">Feedback History</h2>
                <FeedbackLogPanel entries={feedbackEntries} />
            </div>
        </div>
    );
};
