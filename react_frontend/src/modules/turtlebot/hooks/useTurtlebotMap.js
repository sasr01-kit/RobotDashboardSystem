// Global state and listener management for Turtlebot map data, allowing 
// consistent map-related data across different components without prop drilling 
// or multiple WebSocket subscriptions

// Default state structure for map data
let globalMapState = {
  mapUrl: null,
  resolution: null,
  width: null,
  height: null,
  robotPose: null,
  humans: [],
  globalGoal: null,
  intermediateWaypoints: []
};

const listeners = new Set();

export function updateGlobalMapState(patch) {
  globalMapState = { ...globalMapState, ...patch };
  listeners.forEach(fn => fn(globalMapState));
}

import { useState, useEffect } from "react";
import { useWebSocketContext } from "../websocketUtil/WebsocketContext";

// Custom hook to provide Turtlebot map data to components
export function useTurtlebotMap() {
  const { subscribe } = useWebSocketContext();
  const [mapDTO, setMapDTO] = useState(globalMapState);

  useEffect(() => {
    // Hook is initialized, and subscribed to global map state updates for consistency across components and pages
    listeners.add(setMapDTO);
    setMapDTO(globalMapState);
    return () => listeners.delete(setMapDTO);
  }, []);

  useEffect(() => {
    if (!subscribe) return;

    return subscribe((data) => {
      // Debug log for incoming map-related messages from the backend
      console.log("[MAP HOOK] incoming:", data);

      if (data.type === "MAP_DATA") {
        const mapData = data.mapData;
        // Convert occupancy grid PNG from backend into data URL for frontend use
        updateGlobalMapState({
          mapUrl: mapData.occupancyGridPNG
            ? `data:image/png;base64,${mapData.occupancyGridPNG}`
            : globalMapState.mapUrl,
          resolution: mapData.resolution ?? globalMapState.resolution,
          width: mapData.width ?? globalMapState.width,
          height: mapData.height ?? globalMapState.height
        });

        return;
      }

      if (data.type === "POSE_DATA") {
        updateGlobalMapState({
          robotPose: data.robotPose ?? globalMapState.robotPose,
          humans: data.humans ?? globalMapState.humans,
          globalGoal: data.globalGoal ?? globalMapState.globalGoal,
          intermediateWaypoints:
            data.intermediateWaypoints ?? globalMapState.intermediateWaypoints
        });

        return;
      }
    });
  }, [subscribe]);

  return mapDTO;
}
