import '../Pixelbot.css';
import '../styles/MetricCard.css';

// A reusable card component to display a metric with title, value, unit, icon, and trend information.
// props: title, value, unit, icon, trendValue
export default function MetricCard({ title, value, unit, icon, trendValue }) {
    return (
        <div className="metric-card">
            <div className="metric-card-header">
                <span className="metric-card-title">{title}</span>
                {icon && <span className="metric-card-icon">{icon}</span>}
            </div>
            <div className="metric-card-value">{value}{unit}</div>
            {trendValue && <div className="metric-card-subtitle">{trendValue}{unit} than last month</div>}
        </div>
    );
}