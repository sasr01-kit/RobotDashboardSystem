import { useCallback, useState } from "react";
import { useModeContext } from './ModeUtil/ModeContext.js';
import { useWebSocketContext } from './WebsocketUtil/WebsocketContext.js';
import { motion } from "framer-motion";
import dockIcon from './assets/dockIcon.svg';
import { useTurtlebotStatus } from "./Hooks/useTurtlebotStatus.js";

/* MOCK */
const MOCK_LATENCY = 600;

const DockingBlock = () => {
  const [dockingState, setDockingState] = useState("UNDOCKED");
  const [isPending, setIsPending] = useState(false);

  const isDocked = dockingState === "DOCKED";

  const mockSendCommand = (nextState) => {
    setIsPending(true);

    setTimeout(() => {
      setDockingState(nextState);
      setIsPending(false);
    }, MOCK_LATENCY);
  };

  const handleClick = useCallback(() => {
    if (isPending) return;

    if (isDocked) {
      mockSendCommand("UNDOCKED");
    } else {
      mockSendCommand("DOCKED");
    }
  }, [isDocked, isPending]);

  return (
    <motion.div
      className="command-execution-block"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="command-execution-row">
        <div className="dock-icon">
            <img src={dockIcon} alt="Dock Icon" className="path-icon" />
        </div>
        <div className="label-column">
            <span className="command-label">Docking </span>
            <motion.span
              className={`command-status ${isDocked ? "off" : "on"}`}
            >
              Status : {isDocked ? "Docked" : "Undocked"}
            </motion.span>
        </div>
        <motion.button
        className={`execution-button ${isDocked ? "start" : "stop"}`}
        onClick={handleClick}
        disabled={isPending}
        whileHover={!isPending ? { scale: 1.05 } : {}}
        whileTap={!isPending ? { scale: 0.95 } : {}}
      >
        <motion.span
          key={isPending ? "spinner" : isDocked ? "undock" : "dock"}
          className="button-label"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {isPending ? (
            <span className="spinner" />
          ) : isDocked ? (
            "UNDOCK"
          ) : (
            "DOCK"
          )}
        </motion.span>
      </motion.button>
      </div>
    </motion.div>
  );
};


/* REAL VERSION
const DockingBlock = () => {
  const { statusDTO } = useTurtlebotStatus();
  const { send } = useWebSocketContext();

  const [isPending, setIsPending] = useState(false);

  const isDocked = statusDTO.docking;

  const handleClick = useCallback(() => {
    if (isPending) return;

    setIsPending(true);

    send({
      type: "DOCKING_COMMAND",
      command: isDocked ? "UNDOCK" : "DOCK",
    });
  }, [isDocked, isPending, send]);

  useEffect(() => {
    if (
      (isPending && isDocked) ||
      (isPending && statusDTO.docking === false)
    ) {
      setIsPending(false);
    }
  }, [statusDTO, isDocked, isPending]);
  return (
    <motion.div
      className="docking-block"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="docking-row">
        <div className="dock-icon">
            <img src={dockIcon} alt="Dock Icon" className="path-icon" />
        </div>
        <span className="label">Docking Status</span>
        <motion.span
          className={`status ${isDocked ? "docked" : "undocked"}`}
          animate={{ scale: isDocked ? 1.1 : 1 }}
        >
          Status : {isDocked ? "DOCKED" : "UNDOCKED"}
        </motion.span>
      </div>

      <motion.button
        className={`execution-button ${isDocked ? "stop" : "start"}`}
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
                : isDocked
                ? "undock"
                : "dock"
            }
            className="button-label"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
        >
            {isPending ? (
            <span className="spinner" />
            ) : isDocked ? (
            "UNDOCK"
            ) : (
            "DOCK"
            )}
        </motion.span>
    </motion.button>
    </motion.div>
  );
}; */

export default DockingBlock;