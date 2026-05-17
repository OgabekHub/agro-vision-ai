"use client";

import { motion } from "framer-motion";
import { getConfidenceColor, formatConfidence } from "@/lib/utils";

interface ConfidenceGaugeProps {
  confidence: number;
  size?: "sm" | "md" | "lg";
  label?: string;
  showPercentage?: boolean;
  animated?: boolean;
}

const sizes = {
  sm: { width: 80, stroke: 6, fontSize: 14, labelSize: 9 },
  md: { width: 120, stroke: 8, fontSize: 22, labelSize: 11 },
  lg: { width: 160, stroke: 10, fontSize: 28, labelSize: 13 },
};

export default function ConfidenceGauge({
  confidence,
  size = "md",
  label = "Confidence",
  showPercentage = true,
  animated = true,
}: ConfidenceGaugeProps) {
  const { width, stroke, fontSize, labelSize } = sizes[size];
  const radius = (width - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = confidence * circumference;
  const color = getConfidenceColor(confidence);

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width, height: width }}>
        <svg
          width={width}
          height={width}
          className="transform -rotate-90"
        >
          {/* Background circle */}
          <circle
            cx={width / 2}
            cy={width / 2}
            r={radius}
            fill="none"
            stroke="rgba(255,255,255,0.05)"
            strokeWidth={stroke}
          />
          {/* Progress circle */}
          <motion.circle
            cx={width / 2}
            cy={width / 2}
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth={stroke}
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={animated ? { strokeDashoffset: circumference } : {}}
            animate={{ strokeDashoffset: circumference - progress }}
            transition={{ duration: 1.5, ease: [0.4, 0, 0.2, 1], delay: 0.3 }}
            style={{
              filter: `drop-shadow(0 0 6px ${color})`,
            }}
          />
        </svg>

        {/* Center text */}
        {showPercentage && (
          <div
            className="absolute inset-0 flex flex-col items-center justify-center"
          >
            <motion.span
              initial={animated ? { opacity: 0 } : {}}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8 }}
              className="font-bold font-[family-name:var(--font-display)]"
              style={{ fontSize, color }}
            >
              {formatConfidence(confidence)}
            </motion.span>
          </div>
        )}
      </div>

      {label && (
        <span
          className="uppercase tracking-wider text-[var(--color-text-muted)] font-medium"
          style={{ fontSize: labelSize }}
        >
          {label}
        </span>
      )}
    </div>
  );
}
