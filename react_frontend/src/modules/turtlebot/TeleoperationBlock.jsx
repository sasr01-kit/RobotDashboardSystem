import { useModeContext } from "./ModeUtil/ModeContext";
import { motion } from "framer-motion";
import { useState } from 'react';
import TeleoperationButton from "./TeleoperationButton.jsx";
import { useRef, useEffect } from "react";
import teleopIcon from './assets/teleopIcon.svg';
import upIcon from './assets/upButton.svg';
import leftIcon from './assets/leftButton.svg';
import rightIcon from './assets/rightButton.svg';
import downIcon from './assets/downButton.svg';
import rotateLeftIcon from './assets/rotateLeftButton.svg';
import rotateRightIcon from './assets/rotateRightButton.svg';
import stopIcon from './assets/stopButton.svg';

export default function TeleoperationBlock() {
    const { mode } = useModeContext(); 
    const isTeleoperating = mode === 'Teleoperating';

    const ws = useRef(null);
    const [activeCommand, setActiveCommand] = useState(null);

    /* MOCK PLEASE DELETE !!!!! */
    const [messages, setMessages] = useState([]); 
    const mockSend = (commandArray) => { 
        const timestamp = new Date().toLocaleTimeString(); 
        const entry = `${timestamp} → ${JSON.stringify(commandArray)}`; setMessages(prev => [entry, ...prev]); 
    };
    /* END MOCK PLEASE DELETE !!!!! */

    useEffect(() => {
        //TODO: Establish WebSocket connection later
        ws.current = new WebSocket("ws://localhost:8000/ws/teleop")

        ws.current.onopen = () => console.log("[Teleop] WebSocket connected"); 
        ws.current.onclose = () => console.log("[Teleop] WebSocket disconnected"); 
        ws.current.onerror = (err) => console.error("[Teleop] WebSocket error:", err);

        return () => ws.current?.close();
    }, []);

    const handleInput = (direction) => { 
        const dir = direction.toUpperCase(); 
        let commandArray = [];

        switch (dir) { 
            case 'UP': 
                commandArray = ['FORWARD']; 
                break; 
            case 'DOWN': 
                commandArray = ['BACKWARD']; 
                break; 
            case 'LEFT': 
                commandArray = ['FORWARD', 'LEFT']; 
                break; 
            case 'RIGHT': 
                commandArray = ['FORWARD', 'RIGHT']; 
                break; 
            case 'ROTATE_CW': 
                commandArray = ['RIGHT']; 
                break; 
            case 'ROTATE_CCW': 
                commandArray = ['LEFT']; 
                break; 
            case 'STOP': 
                commandArray = ['STOP']; 
                break; 
            default: return; 
        }

        setActiveCommand(dir);

        /* MOCK PLEASE DELETE !!!!! */
        mockSend(commandArray);
        /* END MOCK PLEASE DELETE !!!!! */

        /* REAL CODE: USE THIS LATER
        if (process.env.NODE_ENV === 'development') { 
            console.log('[Teleop] Built command:', commandArray); 
        }

        sendCommand(commandArray); */
    
    };

    const sendCommand = (commandArray) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            const message = JSON.stringify({ commands: commandArray });
            ws.current.send(message);  
        } else {
            console.error('[Teleop] WebSocket is not connected.');
        }
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
            </div>
        </motion.div>
    );
}

/* Mock message log
            <div className="teleop-log">
                <h3>Sent Commands</h3>
                <ul>
                    {messages.map((msg, i) => (
                        <li key={i}>{msg}</li>
                    ))}
                </ul>
            </div> */
