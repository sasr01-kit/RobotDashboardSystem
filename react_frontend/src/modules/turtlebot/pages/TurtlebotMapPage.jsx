import '../styles/MapPage.css';
import '../styles/GoalLog.css';
import { useRef, useState, useEffect } from 'react';
import { useTurtlebotGoal, usePathHistoryActions } from '../hooks/useTurtlebotGoal';
import { GoalLogPanel } from "../components/GoalLogPanel";
import { PathLogDropdownNav } from '../components/PathLogDropdownNav';
import { MinimizedStatusBar } from '../components/MinimizedStatusBar';
import { motion, AnimatePresence } from 'framer-motion';
import MapView from '../components/MapView.jsx';

// This page provides a visual representation of the Turtlebot's environment and its path history.
// The useTurtlebotGoal hook is used to access the path history data from the backend.
export default function TurtlebotMapPage() {
  const { pathHistory } = useTurtlebotGoal();
  // Actions for managing path history storage on the backend (save, load latest, clear)
  const { save, loadLatest, clear } = usePathHistoryActions();
   const [isClearConfirmOpen, setIsClearConfirmOpen] = useState(false);

  // References to each log entry for smooth auto-scrolling when selected from the dropdown
  const entryRefs = useRef({});
  const [mapHeight, setMapHeight] = useState(null);

  // Function to scroll to a specific log entry when selected from the dropdown navigation
  const scrollToEntry = (id) => {
    const element = entryRefs.current[id];
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  };

  const confirmClear = () => {
    clear(); 
    setIsClearConfirmOpen(false);
  };

  return (
    <div className="turtlebot-map-page">
      <div className="map-page-grid">
        <div className="left-panel">
          <MinimizedStatusBar />
          <div className="map-view-container">
            <MapView onMapResize={setMapHeight} />
          </div>
        </div>

        <div className="right-panel">
          <div className="path-history-header">
            <PathLogDropdownNav logs={pathHistory} onSelect={scrollToEntry} />

            <motion.button
              className="save-path-history-button"
              onClick={save}
              whileTap={{ scale: 0.92, boxShadow: '0 2px 4px rgba(0,0,0,0.2)' }}
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
            >
              Save
            </motion.button>

            <motion.button
              className="load-latest-path-history-button"
              onClick={loadLatest}
              whileTap={{ scale: 0.92, boxShadow: '0 2px 4px rgba(0,0,0,0.2)' }}
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
            >
              Load
            </motion.button>

            <motion.button
              className="clear-path-history-button"
              onClick={() => setIsClearConfirmOpen(true)}
              disabled={!pathHistory || pathHistory.length === 0}
              whileTap={{ scale: 0.92, boxShadow: '0 2px 4px rgba(0,0,0,0.2)' }}
              whileHover={{ scale: 1.05 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
            >
              Clear
            </motion.button>
          </div>

          {/* GoalLogPanel height matches MapView height for consistent layout */}
          <div className="path-log-container" style={{ height: mapHeight ? `${mapHeight}px` : "28rem" }}>
            <GoalLogPanel logs={pathHistory} entryRefs={entryRefs} />
          </div>
        </div>
      </div>

      {/* Clear confirmation modal */}
      <AnimatePresence>
        {isClearConfirmOpen && (
          <motion.div
            className="confirm-modal-backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsClearConfirmOpen(false)}
          >
            <motion.div
              className="confirm-modal"
              initial={{ opacity: 0, y: 12, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 12, scale: 0.98 }}
              transition={{ type: "spring", stiffness: 320, damping: 26 }}
              onClick={(e) => e.stopPropagation()} 
              role="dialog"
              aria-modal="true"
              aria-labelledby="clear-modal-title"
            >
              <h3 id="clear-modal-title" className="confirm-modal-title">
                Clear current path history?
              </h3>

              <p className="confirm-modal-text">
                This will clear the panel and reset the current in-memory history.
                <strong> Remember to save before clearing.</strong>
              </p>

              <div className="confirm-modal-actions">
                <button
                  className="confirm-modal-cancel"
                  onClick={() => setIsClearConfirmOpen(false)}
                >
                  Cancel
                </button>

                <button
                  className="confirm-modal-clear"
                  onClick={confirmClear}
                >
                  Clear history
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};