import './styles/MapPage.css';
import './styles/GoalLog.css';
import { useRef } from 'react';
import { useTurtlebotGoal } from './Hooks/useTurtlebotGoal';
import { useTurtlebotGoalMock } from './Hooks/useTurtlebotGoalMock'; //MOCK DELETE
import { GoalLogPanel } from "./GoalLogPanel";
import { PathLogDropdownNav } from './PathLogDropdownNav';
import { MinimizedStatusBar } from './MinimizedStatusBar';

export default function TurtlebotMapPage() {
    const { logs, isLoading } = useTurtlebotGoalMock(); //MOCK CHANGE TO REAL
    const entryRefs = useRef({});

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
                </div>
                <div className="right-panel">
                    <PathLogDropdownNav logs={logs} onSelect={scrollToEntry} />
                    <div className="path-log-container">
                        <GoalLogPanel logs={logs} entryRefs={entryRefs} />
                    </div>
                </div>
            </div>
        </div>
    );
};
