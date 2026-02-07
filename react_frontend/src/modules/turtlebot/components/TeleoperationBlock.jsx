import { motion } from "framer-motion";
import { useState } from 'react';
import { useModeContext } from "../ModeUtil/ModeContext.js";
import { useWebSocketContext } from "../WebsocketUtil/WebsocketContext.js";

import TeleoperationButton from "./TeleoperationButton.jsx";
import teleopIcon from '../assets/teleopIcon.svg';
import upIcon from '../assets/upButton.svg';
import leftIcon from '../assets/leftButton.svg';
import rightIcon from '../assets/rightButton.svg';
import downIcon from '../assets/downButton.svg';
import rotateLeftIcon from '../assets/rotateLeftButton.svg';
import rotateRightIcon from '../assets/rotateRightButton.svg';
import stopIcon from '../assets/stopButton.svg';

export default function TeleoperationBlock() {
    const { mode } = useModeContext(); 
    const isTeleoperating = mode === 'Teleoperating';

    const { send } = useWebSocketContext();
    const [activeCommand, setActiveCommand] = useState(null);
    const [messages, setMessages] = useState([]);
    
    const handleInput = (direction) => { 
    const dir = direction.toUpperCase(); 
    let command = null;

    switch (dir) { 
        case 'UP': 
            command = 'FORWARD'; 
            break; 
        case 'DOWN': 
            command = 'BACKWARD'; 
            break; 
        case 'LEFT': 
            command = 'LEFT'; 
            break; 
        case 'RIGHT': 
            command = 'RIGHT'; 
            break; 
        case 'ROTATE_CW': 
            command = 'ROTATE_RIGHT'; 
            break; 
        case 'ROTATE_CCW': 
            command = 'ROTATE_LEFT'; 
            break; 
        case 'STOP': 
            command = 'STOP'; 
            break; 
        default:
            return; 
    }

    setActiveCommand(dir);
    setMessages(prev => [...prev, `Sent: ${command}`]);
    send({ command });
};


    return (
        <motion.div 
            className={`teleoperation-block ${isTeleoperating ? '' : 'disabled'}`}
            initial={{ opacity: 0, y: 10 }}
            animate={{
                opacity: isTeleoperating ? 1 : 0.4, y: 0,
            }}
            transition={{ duration: 0.2 }}
        >
            <div className="top-left-logo"> 
                <img src={teleopIcon} alt="Teleoperation Logo" className="teleop-logo" /> 
            </div> 
            <div className="control-zone">
                <div className="direction-pad">
                    <TeleoperationButton 
                        direction="UP" 
                        onClick={handleInput} 
                        icon={<img src={upIcon} alt="up" className="teleop-icon" />}
                    />
                    <div className="horizontal-row">
                        <TeleoperationButton 
                            direction="LEFT" 
                            onClick={handleInput} 
                            icon={<img src={leftIcon} alt="left" className="teleop-icon" />}
                        />
                        <TeleoperationButton 
                            direction="RIGHT" 
                            onClick={handleInput} 
                            icon={<img src={rightIcon} alt="right" className="teleop-icon" />}
                        />
                    </div>
                    <TeleoperationButton 
                        direction="DOWN" 
                        onClick={handleInput} 
                        icon={<img src={downIcon} alt="down" className="teleop-icon down" />}
                    />
                </div>
                <div className="action-buttons">
                    <TeleoperationButton 
                        direction="ROTATE_CCW" 
                        onClick={handleInput} 
                        icon={<img src={rotateLeftIcon} alt="rotate left" className="teleop-icon" />} 
                    />
                    <TeleoperationButton 
                        direction="ROTATE_CW" 
                        onClick={handleInput} 
                        icon={<img src={rotateRightIcon} alt="rotate right" className="teleop-icon" />} 
                    />
                    <TeleoperationButton 
                        direction="STOP" 
                        onClick={handleInput} 
                        icon={<img src={stopIcon} alt="stop" className="teleop-icon" />} 
                    />
                </div>
                   <div className="teleop-log">
                <h3>Sent Commands</h3>
                <ul>
                    {messages.map((msg, i) => (
                        <li key={i}>{msg}</li>
                    ))}
                </ul>
            </div> 
            </div>
        </motion.div>
    );
}