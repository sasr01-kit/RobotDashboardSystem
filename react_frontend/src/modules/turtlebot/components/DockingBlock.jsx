import { motion } from "framer-motion"; // Provides animation for the components
import { useCallback, useState, useEffect } from "react";
import { useWebSocketContext } from '../websocketUtil/WebsocketContext.js';
import { useTurtlebotStatus } from "../hooks/useTurtlebotStatus.js";
import dockIcon from '../assets/dockIcon.svg';

// Component to control docking/undocking the Turtlebot, with backend integration
const DockingBlock = () => {
  const { statusDTO } = useTurtlebotStatus();
  const { send } = useWebSocketContext();

  // Local pending state to manage button disabled state and spinner if backend is still processing last command
  const [isPending, setIsPending] = useState(false);

  const isDocked = statusDTO.isDocked;

  const handleClick = useCallback(() => {
    if (isPending) return;

    setIsPending(true);

    // Send command to backend to toggle docking state
    send({
      dockStatus: !isDocked
    });
  }, [isDocked, isPending, send]);

  useEffect(() => {
    // When backend already updates the docking state, clear pending
    if (isPending && statusDTO.isDocked === isDocked) {
      setIsPending(false);
    }
  }, [statusDTO, isDocked, isPending]);

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
          <span className="command-label">Docking</span>

          <motion.span
            className={`command-status ${isDocked ? "on" : "off"}`}
            animate={{ scale: isDocked ? 1.1 : 1 }}
          >
            Status : {isDocked ? "Docked" : "Undocked"}
          </motion.span>
        </div>

        <motion.button
          className={`execution-button ${isDocked ? "stop" : "start"}`}
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

export default DockingBlock;