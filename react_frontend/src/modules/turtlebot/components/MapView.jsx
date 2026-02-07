import { useEffect, useRef } from "react";
import { useTurtlebotMap } from "../Hooks/useTurtlebotMap";

export default function MapView({ onMapResize }) {
  const canvasRef = useRef(null);
  const map = useTurtlebotMap();

  useEffect(() => {
    if (!map.mapUrl) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    const img = new Image();
    img.src = map.mapUrl;

    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;

      // Draw map
      ctx.drawImage(img, 0, 0);

      // Draw robot pose
      if (map.robotPose) {
        const { x, y } = map.robotPose.position;

        const px = x / map.resolution;
        const py = y / map.resolution;

        ctx.fillStyle = "red";
        ctx.beginPath();
        ctx.arc(px, py, 6, 0, Math.PI * 2);
        ctx.fill();
      }

      // Draw humans
      if (map.humans) {
        ctx.fillStyle = "blue";
        map.humans.forEach(h => {
          const px = h.position.x / map.resolution;
          const py = h.position.y / map.resolution;

          ctx.beginPath();
          ctx.arc(px, py, 5, 0, Math.PI * 2);
          ctx.fill();
        });
      }
        if (onMapResize) { 
            onMapResize(img.height); // <— report height to parent, to make sure log panel height matches map height
        }
    };
  }, [map]);

  return (
    <div className="map-container">
      <canvas ref={canvasRef} />
    </div>
  );
}
