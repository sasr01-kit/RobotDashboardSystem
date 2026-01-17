import { useState } from 'react';
import { motion } from 'framer-motion';

export default function TeleoperationButton({ direction, icon, onClick }) { 
    const [clicked, setClicked] = useState(false); 

    const handleClick = () => { 
        setClicked(true); 
        setTimeout(() => setClicked(false), 150); 
        onClick(direction); 
    }; 
    
    return ( 
        <motion.button 
            className={`teleop-button ${direction} ${clicked ? 'clicked' : ''}`} 
            onClick={handleClick} 
            whileTap={{ scale: 0.94 }} 
            transition={{ type: "spring", stiffness: 400, damping: 20 }} 
        >
            {icon}
        </motion.button>
    ); 
}