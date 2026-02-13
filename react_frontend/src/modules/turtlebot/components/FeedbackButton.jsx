import { motion } from 'framer-motion';
import { useWebSocketContext } from '../websocketUtil/WebsocketContext';

// Reusable button component, used for good button and bad button to send feedback to the backend
export const FeedbackButton = ({ className, label, goalId }) => {
  const { send } = useWebSocketContext();

  // Handle button click by sending feedback to backend
  const handleClick = () => {
    send({
      type: "GOAL_FEEDBACK",
      goalId,
      feedback: label === "GOOD" ? "good" : "bad",
    });
  };

  return (
    <motion.button
      className={`feedback-button ${className}`}
      onClick={handleClick}
      whileTap={{ scale: 0.92, boxShadow: '0 2px 4px rgba(0,0,0,0.2)' }}
      whileHover={{ scale: 1.05 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
    >
      {label}
    </motion.button>
  );
}; 