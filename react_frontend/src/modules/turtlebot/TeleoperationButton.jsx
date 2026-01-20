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
            whileTap={{ scale: 0.90 }} 
            transition={{ type: "spring", stiffness: 300, damping: 10 }} 
        >
            {icon}
        </motion.button>
    ); 
}