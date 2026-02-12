import {motion} from "framer-motion";

export default function GeneralStatusBlock({ icon, label, status, statusColor }) {
    const isMissing = status === null || status === undefined || status === "null%" || status === ""; 
    
    const displayValue = isMissing ? "N/A" : status;


    return ( 
     <motion.div className="general-status-block" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
        <div className="status-icon">{icon}</div> 
        <div className="status-info"> 
            <div className="status-label">{label}</div> 
            <div className="status-value" style={{ color: statusColor }}>{displayValue}</div> 
            </div> 
    </motion.div> 
    ); 
}