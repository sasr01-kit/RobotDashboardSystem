import { useNavigate, useLocation } from 'react-router-dom';
import { useModeContext } from './ModeUtil/ModeContext.js';
import NavBar from '../global/NavBar.jsx';

const tabs = [
    { label: 'Status', value: 'status' },
    { label: 'Map', value: 'map' },
    { label: 'Feedback', value: 'feedback' },
];

export default function TurtlebotNavBar() {
    const navigate = useNavigate();
    const location = useLocation();
    const { mode } = useModeContext();

    const active = tabs.find(t => location.pathname.endsWith(t.value))?.value || 'status';

    const isDisabled = (value) => (
        mode === 'Teleoperating' && (value === 'map' || value === 'feedback')
    );

    const onSelect = (value) => {
        if (isDisabled(value)) return;
        navigate(`/turtlebot/${value}`);
    };

    return (
        <NavBar tabs={tabs} active={active} onSelect={onSelect} isDisabled={isDisabled} />
    );
}
