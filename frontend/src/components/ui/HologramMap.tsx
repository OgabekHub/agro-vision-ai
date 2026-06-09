"use client";

import { motion } from "framer-motion";
import HologramParticles from "./HologramParticles";

export default function HologramMap() {
  return (
    <div className="relative w-full max-w-[280px] aspect-square flex items-center justify-center mx-auto">
      {/* Outer rotating HUD ring */}
      <motion.div
        className="absolute w-full h-full rounded-full border border-dashed border-[var(--color-primary)]/10 pointer-events-none"
        animate={{ rotate: 360 }}
        transition={{ duration: 40, repeat: Infinity, ease: "linear" }}
      />
      
      {/* Inner scanning ring */}
      <motion.div
        className="absolute w-[85%] h-[85%] rounded-full border border-dotted border-[var(--color-primary)]/15 pointer-events-none"
        animate={{ rotate: -360 }}
        transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
      />

      {/* Floating container */}
      <motion.div
        className="relative z-20 w-[90%] h-[90%] flex items-center justify-center"
        animate={{ y: [-8, 8, -8] }}
        transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
      >
        {/* Radial green glow behind map */}
        <div className="absolute w-[70%] h-[70%] rounded-full bg-[var(--color-primary)]/10 blur-3xl" />
        
        {/* Hologram map image */}
        <img
          src="/images/uzbekistan_hologram_map.png"
          alt="Uzbekistan Hologram Map"
          className="w-full h-full object-contain filter drop-shadow-[0_0_20px_rgba(0,255,136,0.4)] select-none pointer-events-none"
        />
      </motion.div>

      {/* Floating blue dot particles */}
      <HologramParticles count={14} />
    </div>
  );
}
