export default function PowerStatus({ isOn }) { 
    const color = isOn ? '#5AAE61' : '#dc3545'; 

    return ( 
        <div className="power-status"> 
            <div 
                className="power-icon" 
                style={{ backgroundColor: color }} 
            /> 
            <span className="power-label">{isOn ? 'ON' : 'OFF'}</span> 
        </div> 
    );
}