import { useCallback, useState, useEffect } from "react";
import { useModeContext } from '../ModeUtil/ModeContext.js';
import { useWebSocketContext } from '../WebsocketUtil/WebsocketContext.js';
import { motion } from "framer-motion";
import pathIcon from '../assets/pathExecution.svg';

/* MOCK 
const MOCK_LATENCY = 600;

const PathExecutionBlock = () => {
  const { mode, setMode } = useModeContext();
  const [isPending, setIsPending] = useState(false);

  const isExecuting = mode === 'Running Path Module';
  const mockSendCommand = (nextMode) => {
    setIsPending(true);

    setTimeout(() => {
      setMode(nextMode);
      setIsPending(false);
    }, MOCK_LATENCY);
  };

  const handleClick = useCallback(() => {
    if (isPending) return;

    if (isExecuting) {
      mockSendCommand('Teleoperating');
    } else {
      mockSendCommand('Running Path Module');
    }
  }, [isExecuting, isPending]);

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
}; */

const PathExecutionBlock = () => {
  const { mode } = useModeContext();
  const { send } = useWebSocketContext();

  const [isPending, setIsPending] = useState(false);

  // Real execution state from backend
  const isExecuting = mode === "Running Path Module";

  const handleClick = useCallback(() => {
    if (isPending) return;

    setIsPending(true);

    // Send real backend command
    send({
      isPathModuleActive: !isExecuting
    });
  }, [isExecuting, isPending, send]);

  useEffect(() => {
    // When backend updates mode, clear pending
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

        {/* Icon */}
        <div className="path-icon">
          <img src={pathIcon} alt="Path Icon" className="path-icon" />
        </div>

        {/* Labels */}
        <div className="label-column">
          <span className="command-label">Path Module</span>

          <motion.span
            className={`command-status ${isExecuting ? "on" : "off"}`}
          >
            Status: {isExecuting ? "On" : "Off"}
          </motion.span>
        </div>

        {/* Button */}
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