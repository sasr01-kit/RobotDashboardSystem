import '../styles/MapPage.css';
import '../styles/GoalLog.css';
import { useRef, useState } from 'react';
import { useTurtlebotGoal } from '../Hooks/useTurtlebotGoal';
import { useTurtlebotGoalMock } from '../Hooks/useTurtlebotGoalMock'; //MOCK DELETE
import { GoalLogPanel } from "../components/GoalLogPanel";
import { PathLogDropdownNav } from '../components/PathLogDropdownNav';
import { MinimizedStatusBar } from '../components/MinimizedStatusBar';
import MapView from '../components/MapView.jsx';

export default function TurtlebotMapPage() {
    const { logs, isLoading } = useTurtlebotGoalMock(); //MOCK CHANGE TO REAL
    const entryRefs = useRef({});
    const [mapHeight, setMapHeight] = useState(null);

    const scrollToEntry = (id) => {
        const element = entryRefs.current[id];
        if (element) {
            element.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
    };

    if (isLoading) return <div className="loading">Loading goal logs...</div>;

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
                    <PathLogDropdownNav logs={logs} onSelect={scrollToEntry} />
                    <div className="path-log-container" style={{ height: mapHeight ? `${mapHeight}px` : "28rem" }} >
                        <GoalLogPanel logs={logs} entryRefs={entryRefs} />
                    </div>
                </div>
            </div>
        </div>
    );
};
