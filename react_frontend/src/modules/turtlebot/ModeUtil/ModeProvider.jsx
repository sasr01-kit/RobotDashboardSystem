import { useState, useEffect } from 'react';
import ModeContext from './ModeContext.js';
import { useTurtlebotStatus } from '../Hooks/useTurtlebotStatus.js';


export const ModeProvider = ({ children }) => {
  const { statusDTO } = useTurtlebotStatus();
  //The mode provider starts with null until the first statusDTO is received
  const [mode, setMode] = useState(null);


  useEffect(() => {
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
