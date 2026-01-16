import { useState, useEffect, useRef } from 'react';


// TEMPORARY MOCK — replace later with real WebSocket version
function useTurtlebotStatus() {


     return { statusDTO: {
        battery: 90,
        wifi: true,
        raspberryPi: true,
        comms: true,
        mode: 'Teleoperating',
        docking: false, },
        isLoading: false,
        error: null,
        connectWebSocket: () => {},
        disconnectWebSocket: () => {},
    };
}


export { useTurtlebotStatus };


/* REAL VERSION
export function useTurtlebotStatus() {
    const [statusDTO, setStatusDTO] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const socketRef = useRef(null);


    const connectWebSocket = () => {
        if (socketRef.current) return;
        //TODO : Replace with actual Turtlebot WebSocket endpoint
        socketRef.current = new WebSocket('ws://your-turtlebot-endpoint/status');


        socketRef.current.onopen = () => {
            setIsLoading(true);
            setError(null);
        };


        socketRef.current.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);


                // Mapping received data
                const status = {
                    battery: data.battery,
                    wifi: data.wifi,
                    raspberryPi: data.raspberryPi,
                    comms: data.comms,
                    mode: data.mode,
                    docking: data.docking,
                };
                setStatusDTO(status);
                setIsLoading(false);
            } catch (err) {
                setError('Error: Failed to parse status data');
                setIsLoading(false);
            };


            socketRef.current.onerror = () => {
                setError('WebSocket error occurred');
                setIsLoading(false);
            };


            socketRef.current.onclose = () => {
                socketRef.current = null;
            };
        };


        const disconnectWebSocket = () => {
            if (socketRef.current) {
                socketRef.current.close();
                socketRef.current = null;
            }
        };


        useEffect(() => {
            connectWebSocket();
            return () => {
                disconnectWebSocket();
            };
        }, []);


        return { statusDTO, isLoading, error, connectWebSocket, disconnectWebSocket };
    };
} */
