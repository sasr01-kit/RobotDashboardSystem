export const FeedbackEntryBlock = ({ entry }) => {
  const { startPoint, endPoint, duration, feedback } = entry;

  return (
    <div className="feedback-entry-block">
      <span>{startPoint}</span>
      <span>{endPoint}</span>
      <span>{duration}</span>
      <span className={`feedback-tag ${feedback === "GOOD" ? "good" : "bad"}`}>{feedback}</span>
    </div>
  );
};
