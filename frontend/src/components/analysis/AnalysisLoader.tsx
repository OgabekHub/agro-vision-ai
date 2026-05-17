"use client";

import { motion } from "framer-motion";
import { useTranslations } from "next-intl";
import { Cpu, ScanLine, BarChart3, CheckCircle2 } from "lucide-react";

interface AnalysisLoaderProps {
  status: "uploading" | "processing" | "complete";
  processingText?: string;
}

export default function AnalysisLoader({
  status,
  processingText = "Analyzing with neural network...",
}: AnalysisLoaderProps) {
  const t = useTranslations("analysis.processing.steps");

  const steps = [
    { id: "uploading", label: t("uploading"), icon: ScanLine },
    { id: "aiAnalysis", label: t("aiAnalysis"), icon: Cpu },
    { id: "generatingResults", label: t("generatingResults"), icon: BarChart3 },
  ];

  // Map status to step index
  const statusToIndex: Record<string, number> = {
    uploading: 0,
    processing: 1,
    complete: 2,
  };
  const currentStep = statusToIndex[status] ?? 0;

  return (
    <div className="flex flex-col items-center py-12">
      {/* Neural network animation */}
      <div className="relative w-32 h-32 mb-8">
        {/* Orbiting dots */}
        {[0, 1, 2, 3, 4, 5].map((i) => (
          <motion.div
            key={i}
            className="absolute w-3 h-3 rounded-full bg-[var(--color-primary)]"
            style={{
              top: "50%",
              left: "50%",
              marginTop: -6,
              marginLeft: -6,
            }}
            animate={{
              x: [0, Math.cos((i * Math.PI * 2) / 6) * 45],
              y: [0, Math.sin((i * Math.PI * 2) / 6) * 45],
              scale: [0.5, 1, 0.5],
              opacity: [0.3, 1, 0.3],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              delay: i * 0.15,
              ease: "easeInOut",
            }}
          />
        ))}

        {/* Center icon */}
        <motion.div
          className="absolute inset-0 flex items-center justify-center"
          animate={{ rotate: 360 }}
          transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
        >
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent-cyan)] flex items-center justify-center shadow-[0_0_30px_rgba(0,255,136,0.3)]">
            <Cpu className="w-7 h-7 text-[var(--color-bg-dark)]" />
          </div>
        </motion.div>

        {/* Pulse rings */}
        {[1, 2, 3].map((i) => (
          <motion.div
            key={`ring-${i}`}
            className="absolute inset-0 rounded-full border border-[var(--color-primary)]"
            animate={{
              scale: [1, 1.5 + i * 0.3],
              opacity: [0.3, 0],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              delay: i * 0.5,
              ease: "easeOut",
            }}
          />
        ))}
      </div>

      {/* Status text */}
      <motion.p
        key={status}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-lg font-medium text-[var(--color-text-primary)] mb-2"
      >
        {processingText}
      </motion.p>

      {/* Steps */}
      <div className="flex items-center gap-3 mt-6">
        {steps.map((step, i) => {
          const Icon = step.icon;
          const isActive = i === currentStep;
          const isDone = i < currentStep;

          return (
            <div key={step.id} className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                <div
                  className={`w-8 h-8 rounded-lg flex items-center justify-center transition-all ${
                    isDone
                      ? "bg-[var(--color-primary)] text-[var(--color-bg-dark)]"
                      : isActive
                      ? "bg-[var(--color-primary-subtle)] border border-[var(--color-border-glow)] text-[var(--color-primary)]"
                      : "bg-white/5 text-[var(--color-text-muted)]"
                  }`}
                >
                  {isDone ? (
                    <CheckCircle2 className="w-4 h-4" />
                  ) : (
                    <Icon className="w-4 h-4" />
                  )}
                </div>
                <span
                  className={`text-xs font-medium hidden sm:block ${
                    isActive
                      ? "text-[var(--color-primary)]"
                      : isDone
                      ? "text-[var(--color-text-primary)]"
                      : "text-[var(--color-text-muted)]"
                  }`}
                >
                  {step.label}
                </span>
              </div>

              {i < steps.length - 1 && (
                <div
                  className={`w-8 h-px ${
                    isDone ? "bg-[var(--color-primary)]" : "bg-white/10"
                  }`}
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
