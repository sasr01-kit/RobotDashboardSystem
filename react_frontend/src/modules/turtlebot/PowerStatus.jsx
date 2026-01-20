import {motion} from "framer-motion";

export default function PowerStatus({ isOn }) { 
    const color = isOn ? '#5AAE61' : '#dc3545'; 

    return ( 
        <motion.div className="power-status" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
            <div 
                className="power-icon" 
                style={{ backgroundColor: color }} 
            /> 
            <span className="power-label">{isOn ? 'ON' : 'OFF'}</span> 
        </motion.div> 
    );
}