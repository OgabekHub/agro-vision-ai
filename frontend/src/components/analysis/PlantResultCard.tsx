"use client";

import { motion } from "framer-motion";
import { useTranslations } from "next-intl";
import GlassCard from "@/components/ui/GlassCard";
import ConfidenceGauge from "@/components/analysis/ConfidenceGauge";
import { PlantDetectionResult } from "@/types";
import { MapPin, Droplets, Sun } from "lucide-react";

interface PlantResultCardProps {
  result: PlantDetectionResult;
}

export default function PlantResultCard({ result }: PlantResultCardProps) {
  const t = useTranslations("analysis.plant");

  return (
    <GlassCard glow glowColor="green" padding="lg">
      <div className="flex flex-col lg:flex-row gap-8">
        {/* Left: image + gauge */}
        <div className="flex flex-col items-center gap-4">
          {result.image_url && (
            <div className="relative w-48 h-48 rounded-xl overflow-hidden border border-[var(--color-border-glow)] shadow-[0_0_24px_rgba(0,255,136,0.1)]">
              <img
                src={result.image_url}
                alt={result.plant_name}
                className="w-full h-full object-cover"
              />
            </div>
          )}
          <ConfidenceGauge confidence={result.confidence} size="md" label={t("confidence")} />
        </div>

        {/* Right: info */}
        <div className="flex-1 space-y-5">
          <div>
            <motion.h3
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="text-2xl font-bold font-[family-name:var(--font-display)] gradient-text"
            >
              {result.plant_name}
            </motion.h3>
            <p className="text-sm text-[var(--color-text-muted)] italic mt-1">
              {result.scientific_name}
            </p>
            <p className="text-sm text-[var(--color-text-secondary)] mt-1">
              <span className="text-[var(--color-text-muted)]">{t("family")}:</span>{" "}
              {result.family}
            </p>
          </div>

          <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">
            {result.description}
          </p>

          {/* Growing season + water needs */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="flex items-center gap-3 p-3 rounded-xl bg-white/3 border border-white/5">
              <Sun className="w-5 h-5 text-[var(--color-accent-yellow)] flex-shrink-0" />
              <div>
                <p className="text-xs text-[var(--color-text-muted)]">{t("growingSeason")}</p>
                <p className="text-sm font-medium">{result.growing_season}</p>
              </div>
            </div>
            <div className="flex items-center gap-3 p-3 rounded-xl bg-white/3 border border-white/5">
              <Droplets className="w-5 h-5 text-[var(--color-accent-blue)] flex-shrink-0" />
              <div>
                <p className="text-xs text-[var(--color-text-muted)]">{t("waterNeeds")}</p>
                <p className="text-sm font-medium">{result.water_needs}</p>
              </div>
            </div>
          </div>

          {/* Suitable regions */}
          <div>
            <div className="flex items-center gap-2 mb-2">
              <MapPin className="w-4 h-4 text-[var(--color-primary)]" />
              <span className="text-sm font-medium">{t("suitableRegions")}</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {result.suitable_regions.map((region) => (
                <span
                  key={region}
                  className="px-3 py-1 rounded-full text-xs font-medium bg-[var(--color-primary-subtle)] text-[var(--color-primary)] border border-[var(--color-border-glow)]"
                >
                  {region}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </GlassCard>
  );
}
