import '../styles/MapPage.css';
import '../styles/GoalLog.css';
import { useRef, useState } from 'react';
import { useTurtlebotGoal, useSavePathHistory } from '../hooks/useTurtlebotGoal';
import { GoalLogPanel } from "../components/GoalLogPanel";
import { PathLogDropdownNav } from '../components/PathLogDropdownNav';
import { MinimizedStatusBar } from '../components/MinimizedStatusBar';
import { motion } from 'framer-motion';
import MapView from '../components/MapView.jsx';

// This page provides a visual representation of the Turtlebot's environment and its path history.
// The useTurtlebotGoal hook is used to access the path history data from the backend.
export default function TurtlebotMapPage() {
    const { pathHistory } = useTurtlebotGoal();
    const savePathHistory = useSavePathHistory();
    // Ref to store references to each log entry for smooth auto-scrolling when selected from the dropdown
    const entryRefs = useRef({});
    const [mapHeight, setMapHeight] = useState(null);

    // Function to scroll to a specific log entry when selected from the dropdown navigation
    const scrollToEntry = (id) => {
        const element = entryRefs.current[id];
        if (element) {
            element.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
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
                            onClick={savePathHistory}
                            whileTap={{ scale: 0.92, boxShadow: '0 2px 4px rgba(0,0,0,0.2)' }}
                            whileHover={{ scale: 1.05 }}
                            transition={{ type: "spring", stiffness: 300, damping: 20 }}
                        >
                            Save
                        </motion.button>
                    </div>
                    {/* GoalLogPanel height matches MapView height for consistent layout */}
                    <div className="path-log-container" style={{ height: mapHeight ? `${mapHeight}px` : "28rem" }} >
                        <GoalLogPanel logs={pathHistory} entryRefs={entryRefs} />
                    </div>
                </div>
            </div>
        </div>
    );
};
