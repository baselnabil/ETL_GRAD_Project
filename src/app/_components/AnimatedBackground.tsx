"use client";
import React, { useEffect, useState } from "react";

const AnimatedBackground: React.FC = () => {
  const [blobs, setBlobs] = useState<{ id: number; x: number; y: number; color: string; offsetX: number; offsetY: number }[]>([]);
  const [target, setTarget] = useState<{ x: number; y: number } | null>(null);

  useEffect(() => {
    const generateBlobs = (count: number) => {
      const colors = ["bg-blue-300", "bg-pink-300", "bg-yellow-300"];
      const newBlobs = Array.from({ length: count }, (_, i) => ({
        id: i,
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        color: colors[i % colors.length],
        offsetX: (Math.random() * 0.08 + 0.02) * window.innerWidth, // 2-10% of window width
        offsetY: (Math.random() * 0.08 + 0.02) * window.innerHeight, // 2-10% of window height
      }));
      setBlobs(newBlobs);
    };

    const handleMouseClick = (event: MouseEvent) => {
      const { clientX, clientY } = event;
      setTarget({ x: clientX, y: clientY });
    };

    const handleMouseUp = () => {
      setTarget(null);
    };

    const moveBlobs = () => {
      setBlobs((prevBlobs) =>
        prevBlobs.map((blob) => {
          if (target) {
            const targetX = target.x + blob.offsetX;
            const targetY = target.y + blob.offsetY;
            const angle = Math.atan2(targetY - blob.y, targetX - blob.x);
            const distance = Math.hypot(targetX - blob.x, targetY - blob.y);
            const speed = Math.min(distance / 20, 5); // Adjust speed as needed
            return {
              ...blob,
              x: blob.x + Math.cos(angle) * speed,
              y: blob.y + Math.sin(angle) * speed,
            };
          }
          return blob;
        })
      );
    };

    const animationInterval = setInterval(moveBlobs, 20);

    const updateBlobCount = () => {
      const isMobile = window.innerWidth <= 768;
      generateBlobs(isMobile ? 5 : 8);
    };

    updateBlobCount();
    window.addEventListener("resize", updateBlobCount);
    window.addEventListener("mousedown", handleMouseClick);
    window.addEventListener("mouseup", handleMouseUp);

    return () => {
      clearInterval(animationInterval);
      window.removeEventListener("resize", updateBlobCount);
      window.removeEventListener("mousedown", handleMouseClick);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [target]);

  return (
    <div className="absolute inset-0 z-0">
      {blobs.map((blob) => (
        <div
          key={blob.id}
          className={`absolute w-64 h-64 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob ${blob.color}`}
          style={{ top: blob.y, left: blob.x, transition: 'top 0.2s, left 0.2s' }}
        ></div>
      ))}
    </div>
  );
};

export default AnimatedBackground;