"use client";

import { motion, HTMLMotionProps } from "framer-motion";
import { cn } from "@/lib/utils";
import { ReactNode } from "react";

interface GlassCardProps extends Omit<HTMLMotionProps<"div">, "children"> {
  children: ReactNode;
  className?: string;
  glowColor?: "green" | "blue" | "purple" | "red" | "yellow" | "cyan";
  hover?: boolean;
  glow?: boolean;
  padding?: "sm" | "md" | "lg" | "xl";
}

const glowColors = {
  green: "rgba(0, 255, 136, 0.25)",
  blue: "rgba(59, 130, 246, 0.25)",
  purple: "rgba(139, 92, 246, 0.25)",
  red: "rgba(239, 68, 68, 0.25)",
  yellow: "rgba(245, 158, 11, 0.25)",
  cyan: "rgba(6, 182, 212, 0.25)",
};

const paddings = {
  sm: "p-4",
  md: "p-6",
  lg: "p-8",
  xl: "p-10",
};

export default function GlassCard({
  children,
  className,
  glowColor = "green",
  hover = true,
  glow = false,
  padding = "md",
  ...motionProps
}: GlassCardProps) {
  return (
    <motion.div
      className={cn(
        "glass rounded-2xl",
        paddings[padding],
        hover && "glass-hover",
        glow && "glass-glow",
        className
      )}
      style={
        glow
          ? {
              borderColor: glowColors[glowColor],
              boxShadow: `0 0 20px ${glowColors[glowColor].replace("0.25", "0.08")}, inset 0 0 20px ${glowColors[glowColor].replace("0.25", "0.02")}`,
            }
          : {}
      }
      {...motionProps}
    >
      {children}
    </motion.div>
  );
}
