import { FeedbackEntryBlock } from "./FeedbackEntryBlock";
import { motion } from 'framer-motion';

// Component to display the feedback log panel, showing a list of feedback entries
export const FeedbackLogPanel = ({ entries }) => {
  return (
    <motion.div 
      className="feedback-history-container"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >
        <div className="feedback-label-row">
                <span>Start Point</span>
                <span>End Point</span>
                <span>Duration</span>
                <span>Feedback</span>
        </div>
        <div className="feedback-log-panel">
        {entries.length === 0 ? (
            <div className="empty-log">No feedback entries yet.</div>
        ) : (
            entries.map((entry) => (
            <FeedbackEntryBlock key={entry.id} entry={entry} />
            ))
        )}
        </div>
    </motion.div>
  );
};
