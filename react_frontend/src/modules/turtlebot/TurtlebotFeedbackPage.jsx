import './styles/FeedbackPage.css';
import { FeedbackLogPanel } from "./FeedbackLogPanel";
import { useTurtlebotFeedbackMock } from "./Hooks/useTurtlebotFeedbackMock";

export default function TurtlebotFeedbackPage() {
    const { feedbackEntries } = useTurtlebotFeedbackMock(); //MOCK PLEASE UPDATE WITH ISLOADING WITH REAL ONE

    return (
        <div className="turtlebot-feedback-page">
            <div className="feedback-log-container">
                <FeedbackLogPanel entries={feedbackEntries} />
            </div>
        </div>
    );
};
