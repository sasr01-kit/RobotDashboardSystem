export function useTurtlebotMap() {
  const { socket } = useWebSocketContext();

  const [map, setMap] = useState(null);
  const [poseStamped, setPoseStamped] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!socket) return;

    const handleMessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === "MAP_UPDATE") {
          setMap({
            mapUrl: data.mapUrl,
            resolution: data.resolution,
            width: data.width,
            height: data.height,
            origin: { x: data.origin.x, y: data.origin.y },
          });
        }

        if (data.type === "POSE_UPDATE") {
          setPoseStamped({
            id: data.id,
            coordinate: { x: data.coordinate.x, y: data.coordinate.y, z: data.coordinate.z },
            timestamp: data.timestamp,
            frame_id: data.frame_id,
          });
        }

        setIsLoading(false);
        setError(null);
      } catch (err) {
        setError("Failed to parse Turtlebot data");
        setIsLoading(false);
      }
    };

    socket.addEventListener("message", handleMessage);
    return () => socket.removeEventListener("message", handleMessage);
  }, [socket]);

  return { map, poseStamped, goalLogs, isLoading, error };
}
