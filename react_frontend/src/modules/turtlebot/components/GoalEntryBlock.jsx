import { FeedbackButton } from './FeedbackButton';

export const GoalEntryBlock = ({ log }) => {
  return (
    <div className="goal-entry-block">
      <div className="timestamp">{log.timestamp}</div>
      <div className="goal-status">{log.goalType + " goal"}</div>
      <div className="rule goal">Fuzzy-Logic: {log.fuzzy_output_goal}</div>
      <div className="feedback-buttons">
        <FeedbackButton className="good-feedback-button" label="GOOD" goalId={log.id} />
        <FeedbackButton className="bad-feedback-button" label="BAD" goalId={log.id} />
      </div>
    </div>
  );
};
