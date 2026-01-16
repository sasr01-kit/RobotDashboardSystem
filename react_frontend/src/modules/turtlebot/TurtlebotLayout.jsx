import { Outlet } from 'react-router-dom';
import TurtlebotNavBar from './TurtlebotNavBar';


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
