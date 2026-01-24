import { motion } from 'framer-motion';
import { useWebSocketContext } from '../WebsocketUtil/WebsocketContext';

/* MOCK VERSION : */
export const FeedbackButton = ({ className, label, goalId }) => { 

    const handleClick = () => { 
        console.log( `%c[MOCK FEEDBACK]`, 
            "color: #4a90e2; font-weight: bold;", 
            `Goal ID: ${goalId}, Feedback: ${label}` ); 
        }; 
        
    return ( 
        <motion.button 
            className={`feedback-button ${className}`}
            onClick={handleClick} 
            whileTap={{ scale: 0.95}} 
            whileHover={{ scale: 1.05 }}
            transition={{ type: "spring", stiffness: 300, damping: 20 }} 
        >
            {label} 
        </motion.button> 
    ); 
};



/* REAL VERSION : 
export const FeedbackButton = ({ label, goalId }) => {
  const { send } = useWebSocketContext();

  const handleClick = () => {
    send({
      type: "GOAL_FEEDBACK",
      goalId,
      feedback: label === "GOOD" ? "positive" : "negative",
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
}; */
