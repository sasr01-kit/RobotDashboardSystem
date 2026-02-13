import '../styles/MapView.css';
import { useEffect, useRef } from "react";
import { useTurtlebotMap } from "../hooks/useTurtlebotMap";

// Component to display the map view, including canvas rendering of the map, robot position, 
// human positions with proxemic zones, global goal, and intermediate waypoints

// onMapResize notifies the parent component on how tall the map image is so the layout can adjust accordingly
export default function MapView({ onMapResize }) {
  const canvasRef = useRef(null);
  const map = useTurtlebotMap();

  useEffect(() => {
  if (!map.mapUrl) return;

  const canvas = canvasRef.current;
  const ctx = canvas.getContext("2d");

  const img = new Image();
  img.src = map.mapUrl;

  // Ensure canvas size is correct
  img.onload = () => {
    canvas.width = img.width;
    canvas.height = img.height;
    if (onMapResize) onMapResize(img.height);
    draw();
  };

  // Draw every time map or pose changes
  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0);

    // Human drawing with proxemic zones
    if (map.humans) {
      map.humans.forEach(h => {
        // Adjust the coordinates according to map resolution
        const px = h.position.x / map.resolution;
        const py = h.position.y / map.resolution;

        const zones = h.proxemicDistances || {};

        const drawZone = (radiusMeters, color) => {
          const r = radiusMeters / map.resolution;
          ctx.beginPath();
          ctx.arc(px, py, r, 0, Math.PI * 2);
          ctx.fillStyle = color;
          ctx.fill();
        };

        // Public (7.6 m)
        drawZone(zones.public, "rgba(0, 255, 0, 0.10)");

        // Social (3.6 m)
        drawZone(zones.social, "rgba(255, 255, 0, 0.26)");

        // Personal (1.2 m)
        drawZone(zones.personal, "rgba(255, 166, 0, 0.53)");

        // Intimate (0.45 m)
        drawZone(zones.intimate, "rgba(255, 0, 0, 0.32)");

        // Draw human dot on top
        ctx.fillStyle = "blue";
        ctx.beginPath();
        ctx.arc(px, py, 5, 0, Math.PI * 2);
        ctx.fill();
      });
    }

    // Global goal drawing
    if (map.globalGoal) {
      const gx = map.globalGoal.position.x / map.resolution;
      const gy = map.globalGoal.position.y / map.resolution;

      ctx.fillStyle = "rgba(0, 255, 0, 0.8)";
      ctx.beginPath();
      ctx.arc(gx, gy, 7, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = "black";
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    // Intermediate waypoints drawing
    if (map.intermediateWaypoints && map.intermediateWaypoints.length > 0) {
      map.intermediateWaypoints.forEach(wp => {
        const wx = wp.position.x / map.resolution;
        const wy = wp.position.y / map.resolution;

        ctx.fillStyle = "rgb(246, 255, 0)";
        ctx.beginPath();
        ctx.arc(wx, wy, 7, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = "black";
        ctx.lineWidth = 1.5;
        ctx.stroke();
      });
    }

    // Robot drawing
    if (map.robotPose) {
      const { x, y } = map.robotPose.position;
      const px = x / map.resolution;
      const py = y / map.resolution;

      ctx.fillStyle = "red";
      ctx.beginPath();
      ctx.arc(px, py, 8, 0, Math.PI * 2);
      ctx.fill();
    }
  }
}, [map]);


  return (
    <div className="map-container">
      <canvas ref={canvasRef} />
      <div className="map-legend">
        <div className="legend-item">
          <span className="legend-color public"></span>
          <span>Public Zone (7.6m)</span>
        </div>

        <div className="legend-item">
          <span className="legend-color social"></span>
          <span>Social Zone (3.6m)</span>
        </div>

        <div className="legend-item">
          <span className="legend-color personal"></span>
          <span>Personal Zone (1.2m)</span>
        </div>

        <div className="legend-item">
          <span className="legend-color intimate"></span>
          <span>Intimate Zone (0.45m)</span>
        </div>

        <div className="legend-item">
          <span className="legend-color human"></span>
          <span>Human Position</span>
        </div>

        <div className="legend-item">
          <span className="legend-color global-goal"></span>
          <span>Global Goal</span>
        </div>

        <div className="legend-item">
          <span className="legend-color waypoint"></span>
          <span>Intermediate Waypoint</span>
        </div>

        <div className="legend-item">
          <span className="legend-color robot"></span>
          <span>Robot Position</span>
        </div>
      </div>
    </div>
  );

}
