"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";

interface Particle {
  id: number;
  x: number;
  y: number;
  size: number;
  duration: number;
  delay: number;
  rangeX: number;
  rangeY: number;
}

export default function HologramParticles({ count = 12 }: { count?: number }) {
  const [particles, setParticles] = useState<Particle[]>([]);

  useEffect(() => {
    const newParticles = Array.from({ length: count }).map((_, i) => ({
      id: i,
      x: Math.random() * 80 + 10, // keep away from absolute edges
      y: Math.random() * 80 + 10,
      size: Math.random() * 3 + 2, // 2px to 5px
      duration: Math.random() * 5 + 6, // 6s to 11s (slower, silliq drift)
      delay: Math.random() * 3,
      rangeX: Math.random() * 40 - 20, // drift up to 20px horizontally
      rangeY: Math.random() * 40 - 20, // drift up to 20px vertically
    }));
    setParticles(newParticles);
  }, [count]);

  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden z-10">
      {particles.map((p) => (
        <motion.div
          key={p.id}
          className="absolute rounded-full"
          style={{
            left: `${p.x}%`,
            top: `${p.y}%`,
            width: p.size,
            height: p.size,
            background: "radial-gradient(circle, #3B82F6 0%, #06B6D4 100%)",
            boxShadow: "0 0 8px rgba(59, 130, 246, 0.8), 0 0 16px rgba(6, 182, 212, 0.4)",
          }}
          animate={{
            x: [0, p.rangeX, -p.rangeX, 0],
            y: [0, p.rangeY, -p.rangeY, 0],
            opacity: [0.15, 0.7, 0.3, 0.7, 0.15],
            scale: [1, 1.3, 0.7, 1.3, 1],
          }}
          transition={{
            duration: p.duration,
            repeat: Infinity,
            delay: p.delay,
            ease: "easeInOut",
          }}
        />
      ))}
    </div>
  );
}
