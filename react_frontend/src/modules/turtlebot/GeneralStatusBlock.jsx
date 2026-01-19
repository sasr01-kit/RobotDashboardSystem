export default function GeneralStatusBlock({ icon, label, status, statusColor }) {
     return ( 
     <div className="general-status-block"> 
        <div className="status-icon">{icon}</div> 
        <div className="status-info"> 
            <div className="status-label">{label}</div> 
            <div className="status-value" style={{ color: statusColor }}>{status}</div> 
            </div> 
            </div> 
    ); 
}