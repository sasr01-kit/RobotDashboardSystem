import { useCallback, useState, useEffect } from "react";
import { useModeContext } from '../modeUtil/ModeContext.js';
import { useWebSocketContext } from '../websocketUtil/WebsocketContext.js';
import { motion } from "framer-motion";
import pathIcon from '../assets/pathExecution.svg';

// Component to control the Path Execution Module of the Turtlebot, with backend integration
const PathExecutionBlock = () => {
  const { mode } = useModeContext();
  const { send } = useWebSocketContext();
  // Local pending state to manage button disabled state and spinner if backend is still processing last command
  const [isPending, setIsPending] = useState(false);

  const isExecuting = mode === "Running Path Module";

  const handleClick = useCallback(() => {
    if (isPending) return;

    setIsPending(true);

    // Send command to backend to toggle path execution module
    send({
      isPathModuleActive: !isExecuting
    });
  }, [isExecuting, isPending, send]);

  useEffect(() => {
    // When backend updates mode, clear pending state
    if (isPending && mode !== undefined) {
      setIsPending(false);
    }
  }, [mode, isPending]);

  return (
    <motion.div
      className="command-execution-block"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="command-execution-row">
        <div className="path-icon">
          <img src={pathIcon} alt="Path Icon" className="path-icon" />
        </div>

        <div className="label-column">
          <span className="command-label">Path Module</span>

          <motion.span
            className={`command-status ${isExecuting ? "on" : "off"}`}
          >
            Status: {isExecuting ? "On" : "Off"}
          </motion.span>
        </div>
        
        <motion.button
          className={`execution-button ${isExecuting ? "stop" : "start"}`}
          onClick={handleClick}
          disabled={isPending}
          whileHover={!isPending ? { scale: 1.05 } : {}}
          whileTap={!isPending ? { scale: 0.95 } : {}}
        >
          <motion.span
            key={isPending ? "spinner" : isExecuting ? "stop" : "start"}
            className="button-label"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            {isPending ? (
              <span className="spinner" />
            ) : isExecuting ? (
              "STOP"
            ) : (
              "START"
            )}
          </motion.span>
        </motion.button>
      </div>
    </motion.div>
  );
};


export default PathExecutionBlock;