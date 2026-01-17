import { Outlet } from 'react-router-dom';
import TurtlebotNavBar from './TurtlebotNavBar';

/* Provides the navigation bar layout for the turtlebot4 dashboard */
export default function TurtlebotLayout() {
    return (
        <div className="turtlebot-layout">
            <TurtlebotNavBar />
            <main className="turtlebot-content">
                <Outlet />
            </main>
        </div>
    );
}
