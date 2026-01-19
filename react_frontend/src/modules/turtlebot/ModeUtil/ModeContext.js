import { createContext, useContext } from 'react';


const ModeContext = createContext(null);


export default ModeContext;


export const useModeContext = () => {
    const context = useContext(ModeContext);


    if (!context) {
        throw new Error('useModeContext must be used within a ModeProvider');
    }


    return context;
};
