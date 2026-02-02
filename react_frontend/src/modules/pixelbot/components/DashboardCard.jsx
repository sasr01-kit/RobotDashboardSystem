import '../Pixelbot.css';
import '../styles/DashboardCard.css';

// A reusable dashboard card component with optional print functionality and icon support.
export default function DashboardCard({ id, title, subtitle, children, onPrint, icon, className = '' }) {
    return (
        <div id={id} className={`dashboard-card ${className}`}>
            <div className="dashboard-card-header">
                <div className="dashboard-card-header-left">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                        {icon && <div className="dashboard-card-icon">{icon}</div>}
                        <h3 className="dashboard-card-title">{title}</h3>
                    </div>
                    {subtitle && <div className="dashboard-card-subtitle-header">{subtitle}</div>}
                </div>
                {onPrint && (
                    <svg onClick={onPrint} aria-label="Print" className="print-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="6 9 6 2 18 2 18 9"></polyline>
                        <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
                        <rect x="6" y="14" width="12" height="8"></rect>
                    </svg>
                )}
            </div>
            <div className="dashboard-card-content">
                {children}
            </div>
        </div>
    );
}