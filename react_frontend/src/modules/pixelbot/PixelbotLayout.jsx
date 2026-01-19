import { Outlet } from 'react-router-dom';
import Header from '../global/Header';
import PixelbotNavBar from './PixelbotNavBar.jsx';

export default function PixelbotLayout() {
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
