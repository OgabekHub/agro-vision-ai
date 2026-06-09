"use client";

import { motion } from "framer-motion";
import HologramParticles from "./HologramParticles";

export default function HologramPlant() {
  return (
    <div className="relative w-full max-w-[280px] aspect-square flex items-center justify-center mx-auto">
      {/* Outer rotating HUD ring */}
      <motion.div
        className="absolute w-full h-full rounded-full border border-dashed border-[var(--color-primary)]/10 pointer-events-none"
        animate={{ rotate: -360 }}
        transition={{ duration: 35, repeat: Infinity, ease: "linear" }}
      />
      
      {/* Inner scanning ring */}
      <motion.div
        className="absolute w-[85%] h-[85%] rounded-full border border-dotted border-[var(--color-primary)]/15 pointer-events-none"
        animate={{ rotate: 300 }}
        transition={{ duration: 22, repeat: Infinity, ease: "linear" }}
      />

      {/* Floating container */}
      <motion.div
        className="relative z-20 w-[90%] h-[90%] flex items-center justify-center"
        animate={{ y: [8, -8, 8] }} // Offset float timing from the map
        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
      >
        {/* Radial green glow behind plant */}
        <div className="absolute w-[70%] h-[70%] rounded-full bg-[var(--color-primary)]/10 blur-3xl pointer-events-none" />
        
        {/* Hologram plant image */}
        <img
          src="/images/hologram_plant.png"
          alt="Hologram Plant Sprout"
          className="w-full h-full object-contain mix-blend-screen filter drop-shadow-[0_0_20px_rgba(0,255,136,0.4)] select-none pointer-events-none"
        />
      </motion.div>

      {/* Floating blue dot particles */}
      <HologramParticles count={14} />
    </div>
  );
}

