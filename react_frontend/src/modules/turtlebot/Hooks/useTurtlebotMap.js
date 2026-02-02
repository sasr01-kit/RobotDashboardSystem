import { useState, useEffect } from "react";
import { useWebSocketContext } from "../WebsocketUtil/WebsocketContext";

export function useTurtlebotMap() {
  const { subscribe } = useWebSocketContext();

  const [map, setMap] = useState(null);
  const [poseStamped, setPoseStamped] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!subscribe) return;

    return subscribe((data) => {
      try {
        if (data.type === "MAP_UPDATE") {
          setMap({
            mapUrl: data.mapUrl,
            resolution: data.resolution,
            width: data.width,
            height: data.height,
            origin: {
              x: data.origin.x,
              y: data.origin.y,
            },
          });
        }

        if (data.type === "POSE_UPDATE") {
          setPoseStamped({
            id: data.id,
            coordinate: {
              x: data.coordinate.x,
              y: data.coordinate.y,
              z: data.coordinate.z,
            },
            timestamp: data.timestamp,
            frame_id: data.frame_id,
          });
        }

        setIsLoading(false);
        setError(null);
      } catch {
        setError("Failed to parse Turtlebot map data");
        setIsLoading(false);
      }
    });
  }, [subscribe]);

  return { map, poseStamped, isLoading, error };
}