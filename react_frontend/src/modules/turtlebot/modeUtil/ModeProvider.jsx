import { useState, useEffect } from 'react';
import ModeContext from './ModeContext.js';
import { useTurtlebotStatus } from '../hooks/useTurtlebotStatus.js';

// Provider component to wrap around parts of the app that need access to the Turtlebot's current mode
export const ModeProvider = ({ children }) => {
  const { statusDTO } = useTurtlebotStatus();
  //The mode provider starts with Teleoperating as default until the first statusDTO is received
  const [mode, setMode] = useState('Teleoperating');

  useEffect(() => {
    // Update mode state whenever the Turtlebot status changes
    if (statusDTO?.mode) {
      setMode(statusDTO.mode);
    }
  }, [statusDTO]);

  return (
    <ModeContext.Provider value={{ mode, setMode }}>
      {children}
    </ModeContext.Provider>
  );
};
