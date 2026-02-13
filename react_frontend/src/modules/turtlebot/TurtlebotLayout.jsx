import { Outlet } from 'react-router-dom';
import Header from '../global/Header';
import TurtlebotNavBar from './TurtlebotNavBar';

// Provides the navigation bar layout for the turtlebot4 dashboard for consistency between pages
export default function TurtlebotLayout() {
    return (
        <div className="page turtlebot-layout">
            <Header
                title="Turtlebot4 Dashboard"
            />
            <TurtlebotNavBar />
            <main className="turtlebot-content">
                <Outlet />
            </main>
        </div>
    );
}
