"use client";

import { motion } from "framer-motion";
import { useState } from "react";
import { useLocale } from "next-intl";
import { Link } from "@/i18n/routing";
import HologramParticles from "./HologramParticles";
import { uzbekistanMapRegions, MapRegion } from "@/data/uzbekistanMapData";

export default function HologramMap() {
  const locale = useLocale();
  const [hoveredRegion, setHoveredRegion] = useState<MapRegion | null>(null);

  return (
    <div className="relative w-full max-w-[280px] aspect-square flex flex-col items-center justify-center mx-auto">
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
      <Link href="/regions" className="w-[90%] h-[90%] flex items-center justify-center group relative z-20">
        <motion.div
          className="relative w-full h-full flex flex-col items-center justify-center"
          animate={{ y: [-8, 8, -8] }}
          transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
        >
          {/* Radial green glow behind map */}
          <div className="absolute w-[70%] h-[70%] rounded-full bg-[var(--color-primary)]/5 blur-3xl pointer-events-none" />
          
          {/* Interactive SVG Map */}
          <svg
            viewBox="0 0 793 517"
            className="w-full h-auto filter drop-shadow-[0_0_15px_rgba(0,255,136,0.3)] transition-all duration-500 group-hover:drop-shadow-[0_0_20px_rgba(0,255,136,0.5)] select-none pointer-events-auto"
            xmlns="http://www.w3.org/2000/svg"
          >
            {uzbekistanMapRegions.map((region, idx) => {
              const isHovered = hoveredRegion?.id === region.id;
              return (
                <motion.path
                  key={`${region.id}-${idx}`}
                  d={region.d}
                  initial={{ pathLength: 0, opacity: 0 }}
                  animate={{ pathLength: 1, opacity: 1 }}
                  transition={{
                    duration: 1.5,
                    ease: "easeInOut",
                    delay: idx * 0.03
                  }}
                  fill={
                    region.isWater
                      ? isHovered
                        ? "rgba(59, 130, 246, 0.15)"
                        : "rgba(59, 130, 246, 0.05)"
                      : isHovered
                      ? "rgba(0, 255, 136, 0.12)"
                      : "rgba(0, 255, 136, 0.02)"
                  }
                  stroke={
                    region.isWater
                      ? isHovered
                        ? "#60a5fa"
                        : "rgba(59, 130, 246, 0.4)"
                      : isHovered
                      ? "#00ff88"
                      : "rgba(0, 255, 136, 0.35)"
                  }
                  strokeWidth={isHovered ? 2 : 1.2}
                  strokeDasharray={region.isWater ? "4 4" : undefined}
                  className="transition-all duration-300 ease-out cursor-pointer"
                  onMouseEnter={() => setHoveredRegion(region)}
                  onMouseLeave={() => setHoveredRegion(null)}
                />
              );
            })}
          </svg>

          {/* Active region HUD display */}
          <div className="absolute -bottom-6 left-0 right-0 text-center font-mono text-[10px] tracking-wider text-[var(--color-primary)]/80 pointer-events-none h-5">
            {hoveredRegion ? (
              <motion.span
                initial={{ opacity: 0, y: 5 }}
                animate={{ opacity: 1, y: 0 }}
                className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-black/80 border border-[var(--color-primary)]/30 backdrop-blur-sm"
              >
                <span className="w-1 h-1 rounded-full bg-[var(--color-primary)] animate-pulse" />
                {hoveredRegion.name[locale as "uz" | "ru" | "en"] || hoveredRegion.name.en}
              </motion.span>
            ) : (
              <span className="text-[var(--color-text-muted)] text-[8px] uppercase tracking-widest animate-pulse">
                {locale === "uz" ? "Batafsil ko'rish" : locale === "ru" ? "Подробнее" : "View Details"}
              </span>
            )}
          </div>
        </motion.div>
      </Link>

      {/* Floating blue dot particles */}
      <HologramParticles count={12} />
    </div>
  );
}

