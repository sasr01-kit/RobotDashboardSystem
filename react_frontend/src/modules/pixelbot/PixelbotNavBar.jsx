import { useNavigate, useLocation, useParams } from 'react-router-dom';
import './Pixelbot.css';
import chevron from './assets/chevron.svg';
import { useEffect, useRef, useState } from 'react';
import { usePixelbotChildren } from './hooks/usePixelbotChildren';

export default function PixelbotNavBar() {
    // Comes from URL params
    const { childId, sessionId } = useParams();
    const navigate = useNavigate();
    const location = useLocation();

    const { children, isLoading } = usePixelbotChildren(); // Custom hook to fetch children and their sessions

    const [isChildDropDownOpen, toggleChildMenu] = useState(false);
    const [selectedChildId, setSelectedChildId] = useState(null);
    const dropdownRef = useRef(null);

    // Sync selectedChildId with URL param childId
    useEffect(() => {
        if (childId) {
            if (children) {
                const child = children.find(c => c.childId == childId);
                if (child) {
                    setSelectedChildId(child.childId);
                }
            }
        } else {
            // Clear selection when navigating to summary or other non-child pages
            setSelectedChildId(null);
        }
    }, [childId, children]);

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                toggleChildMenu(false);
                // Only reset selectedChildId if no session was actually navigated to
                if (!childId && !sessionId) {
                    setSelectedChildId(null);
                }
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [childId, sessionId]);

    // Navigation handlers
    function navigateToSection(section) {
        navigate(`/pixelbot/${section}`);
        toggleChildMenu(false);
    }

    function handleChildSelect(childId) {
        setSelectedChildId(childId);
    }

    function handleSessionSelect(sessionId) {
        if (selectedChildId) {
            toggleChildMenu(false);
            if (sessionId === 'recap') {
                navigate(`/pixelbot/session/${selectedChildId}`);
            }
            else {
                navigate(`/pixelbot/session/${selectedChildId}/${sessionId}`);
            }
        }
    }

    const isSummaryActive = location.pathname.includes('summary') || location.pathname === '/pixelbot';
    const isChildActive = !isSummaryActive;

    return (
        <div className="pixelbot-navbar">
            <button
                className={`nav-button ${isSummaryActive ? 'active' : ''}`}
                onClick={() => navigateToSection('summary')}
            >
                Summary
            </button>

            <div className="nav-dropdown-wrapper" ref={dropdownRef}>
                <button
                    className={`nav-button ${isChildActive ? 'active' : ''}`}
                    onClick={() => toggleChildMenu(!isChildDropDownOpen)}
                >
                    Child
                    <img src={chevron} alt="chevron" className={`chevron-icon ${isChildDropDownOpen ? 'open' : ''}`} />
                </button>

                    {isChildDropDownOpen && (
                        <div className="dropdown-container">
                            <div className="dropdown-panel">
                                {(isLoading || !children) ? (
                                    <div>Loading...</div>
                                ) : (
                                    <div className="dropdown-items-grid">
                                        {children.map((child, index) => (
                                            <div
                                                key={index}
                                                className={`dropdown-item ${selectedChildId === child.childId ? 'selected' : ''}`}
                                                onClick={() => handleChildSelect(child.childId)}
                                            >
                                                {child.name}
                                            </div>
                                        ))}
                                 </div>
                                )}
                            </div>

                            {selectedChildId && (
                                <div className="dropdown-panel sessions-panel">
                                    <div className="dropdown-items-grid">
                                        <div
                                            className={`dropdown-item ${childId && sessionId == null ? 'session-selected' : ''}`}
                                            onClick={() => handleSessionSelect('recap')}
                                        >
                                            Recap
                                        </div>
                                        {children.find(c => c.childId == selectedChildId).sessions.map((session, index) => (
                                            <div
                                                key={index}
                                                className={`dropdown-item ${sessionId === session.sessionId ? 'session-selected' : ''}`}
                                                onClick={() => handleSessionSelect(session.sessionId)}
                                            >
                                                {session.sessionId}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    )
                }
            </div>
        </div>
       ) 
}


