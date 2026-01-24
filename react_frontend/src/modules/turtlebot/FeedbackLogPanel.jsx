import { FeedbackEntryBlock } from "./FeedbackEntryBlock";

export const FeedbackLogPanel = ({ entries }) => {
  return (
    <div className="feedback-history-container">
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
    </div>
  );
};
