import { createContext, useContext } from 'react';

// Context to hold the current mode of the Turtlebot to avoid prop drilling
// and allow consistent mode data across different components and pages
const ModeContext = createContext(null);

export default ModeContext;

// Custom hook for components to access the ModeContext, ensuring it is used within a ModeProvider
export const useModeContext = () => {
    const context = useContext(ModeContext);

    if (!context) {
        throw new Error('useModeContext must be used within a ModeProvider');
    }

    return context;
};
