import { useCallback, useState } from "react";
import { useModeContext } from '../ModeUtil/ModeContext.js';
import { useWebSocketContext } from '../WebsocketUtil/WebsocketContext.js';
import { motion } from "framer-motion";
import pathIcon from '../assets/pathExecution.svg';

/* MOCK */
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
};


/* REAL VERSION
const PathExecutionBlock = () => {
  const { mode, setMode } = useModeContext();
  const { send } = useWebSocketContext();

  const [isPending, setIsPending] = useState(false);

  const isExecuting = mode === RUNNING;

  const handleClick = useCallback(() => {
    if (isPending) return;

    setIsPending(true);

    send({
      type: "PATH_EXECUTION_COMMAND",
      command: isExecuting ? "STOP" : "START",
    });
  }, [isExecuting, isPending, send]);

  useEffect(() => {
    if (
      (isPending && isExecuting) ||
      (isPending && mode === "Teleoperating")
    ) {
      setIsPending(false);
    }
  }, [mode, isExecuting, isPending]);

  return (
    <motion.div
      className="path-execution-block"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="path-row">
        <span className="label">Execution Status</span>
        <motion.span
          className={`status ${isExecuting ? "on" : "off"}`}
          animate={{ scale: isExecuting ? 1.1 : 1 }}
        >
          {isExecuting ? "ON" : "OFF"}
        </motion.span>
      </div>

      <motion.button
          className={`execution-button ${isExecuting ? "stop" : "start"}`}
          onClick={handleClick}
          disabled={isPending}
          whileHover={!isPending ? { scale: 1.05 } : {}}
          whileTap={!isPending ? { scale: 0.95 } : {}}
        >
       
          <span className="button-placeholder">
            PROCESSING
          </span>

            <motion.span
                key={
                    isPending
                    ? "spinner"
                    : isExecuting
                    ? "stop"
                    : "start"
            }
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
    </motion.div>
  );
}; */

export default PathExecutionBlock;