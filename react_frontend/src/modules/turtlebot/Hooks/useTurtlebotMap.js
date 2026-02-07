// -------------------------------------------------------------
// GLOBAL STORE (persists across page changes)
// -------------------------------------------------------------

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

// All hook instances subscribe here
const listeners = new Set();

// Called by WebSocket callback to update global state
export function updateGlobalMapState(patch) {
  globalMapState = { ...globalMapState, ...patch };
  listeners.forEach(fn => fn(globalMapState));
}



// -------------------------------------------------------------
// HOOK
// -------------------------------------------------------------

import { useState, useEffect } from "react";
import { useWebSocketContext } from "../WebsocketUtil/WebsocketContext";

export function useTurtlebotMap() {
  const { subscribe } = useWebSocketContext();

  // Initialize from global state (not defaults)
  const [mapDTO, setMapDTO] = useState(globalMapState);

  // Subscribe this hook instance to global store updates
  useEffect(() => {
    listeners.add(setMapDTO);

    // Immediately sync with latest global state
    setMapDTO(globalMapState);

    return () => listeners.delete(setMapDTO);
  }, []);

  // Subscribe to WebSocket messages
  useEffect(() => {
    if (!subscribe) return;

    return subscribe((data) => {
      console.log("[MAP HOOK] incoming:", data);

      if (data.type === "MAP_DATA") {
        const mapData = data.mapData;

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
