import '../styles/MapPage.css';
import '../styles/GoalLog.css';
import { useRef, useState } from 'react';
import { useTurtlebotGoal } from '../Hooks/useTurtlebotGoal';
import { GoalLogPanel } from "../components/GoalLogPanel";
import { PathLogDropdownNav } from '../components/PathLogDropdownNav';
import { MinimizedStatusBar } from '../components/MinimizedStatusBar';
import MapView from '../components/MapView.jsx';

export default function TurtlebotMapPage() {
    const { pathHistory } = useTurtlebotGoal();
    const entryRefs = useRef({});
    const [mapHeight, setMapHeight] = useState(null);

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
                    <PathLogDropdownNav logs={pathHistory} onSelect={scrollToEntry} />
                    <div className="path-log-container" style={{ height: mapHeight ? `${mapHeight}px` : "28rem" }} >
                        <GoalLogPanel logs={pathHistory} entryRefs={entryRefs} />
                    </div>
                </div>
            </div>
        </div>
    );
};
