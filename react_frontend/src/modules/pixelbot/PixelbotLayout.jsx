import { Outlet, useLocation, useNavigate, useParams } from 'react-router-dom';
import Header from '../global/Header';
import PixelbotNavBar from './PixelbotNavBar.jsx';

/* Provides the navigation bar layout for the pixelbot dashboard */
export default function PixelbotLayout() {
    const { childId, sessionId } = useParams();

    const viewMode = childId || sessionId ? 'Child' : 'Summary';
    const selectedChildId = childId || null;
    const activeSessionId = sessionId || null;

    return (
        <div className="page pixelbot-layout">
            <Header
                title="Pixelbot Dashboard"
            />
            <PixelbotNavBar />
            <main className="pixelbot-content">
                <Outlet />
            </main>
        </div>
    );
}

