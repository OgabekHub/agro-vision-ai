"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useTranslations } from "next-intl";
import GlassCard from "@/components/ui/GlassCard";
import ConfidenceGauge from "@/components/analysis/ConfidenceGauge";
import { DiseaseDetectionResult, SeverityLevel } from "@/types";
import { getSeverityColor } from "@/lib/utils";
import {
  AlertTriangle,
  Stethoscope,
  ShieldCheck,
  ChevronDown,
} from "lucide-react";

interface DiseaseResultCardProps {
  result: DiseaseDetectionResult;
}

const severityGlow: Record<SeverityLevel, "green" | "yellow" | "red"> = {
  low: "green",
  medium: "yellow",
  high: "red",
  critical: "red",
};

export default function DiseaseResultCard({ result }: DiseaseResultCardProps) {
  const t = useTranslations("disease");
  const ta = useTranslations("analysis.plant");

  const [expandedSection, setExpandedSection] = useState<string | null>(
    "treatments"
  );

  const toggle = (section: string) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  const severityColor = getSeverityColor(result.severity);
  const severityLabel = t(`severity.${result.severity as "low" | "medium" | "high" | "critical"}`);

  const sections = [
    {
      key: "causes",
      title: t("sections.causes"),
      icon: AlertTriangle,
      items: result.causes,
      color: "var(--color-accent-yellow)",
    },
    {
      key: "treatments",
      title: t("sections.treatments"),
      icon: Stethoscope,
      items: result.treatments,
      color: "var(--color-primary)",
    },
    {
      key: "prevention",
      title: t("sections.prevention"),
      icon: ShieldCheck,
      items: result.prevention_tips,
      color: "var(--color-accent-cyan)",
    },
  ];

  return (
    <GlassCard glow glowColor={severityGlow[result.severity]} padding="lg">
      <div className="flex flex-col gap-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div
              className="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0"
              style={{ backgroundColor: `${severityColor}20` }}
            >
              <AlertTriangle
                className="w-6 h-6"
                style={{ color: severityColor }}
              />
            </div>
            <div>
              <h3 className="text-xl font-bold font-[family-name:var(--font-display)]">
                {result.disease_name}
              </h3>
              <p className="text-sm text-[var(--color-text-muted)]">
                <span className="text-[var(--color-text-secondary)]">
                  {t("affects")}:
                </span>{" "}
                {result.plant_affected}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <span
              className="px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider border"
              style={{
                color: severityColor,
                borderColor: `${severityColor}40`,
                backgroundColor: `${severityColor}10`,
              }}
            >
              {severityLabel}
            </span>
            <ConfidenceGauge
              confidence={result.confidence}
              size="sm"
              label={ta("confidence")}
            />
          </div>
        </div>

        {/* Description */}
        <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">
          {result.description}
        </p>

        {/* Expandable sections */}
        {sections.map((section) => (
          <div
            key={section.key}
            className="border border-white/5 rounded-xl overflow-hidden"
          >
            <button
              onClick={() => toggle(section.key)}
              className="w-full flex items-center justify-between p-4 hover:bg-white/3 transition-colors"
            >
              <div className="flex items-center gap-3">
                <section.icon
                  className="w-5 h-5"
                  style={{ color: section.color }}
                />
                <span className="font-medium text-sm">{section.title}</span>
                <span className="text-xs text-[var(--color-text-muted)]">
                  ({section.items.length})
                </span>
              </div>
              <motion.div
                animate={{ rotate: expandedSection === section.key ? 180 : 0 }}
                transition={{ duration: 0.2 }}
              >
                <ChevronDown className="w-4 h-4 text-[var(--color-text-muted)]" />
              </motion.div>
            </button>

            {expandedSection === section.key && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                transition={{ duration: 0.2 }}
                className="px-4 pb-4"
              >
                <ul className="space-y-2">
                  {section.items.map((item, i) => (
                    <motion.li
                      key={i}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="flex items-start gap-3 text-sm text-[var(--color-text-secondary)]"
                    >
                      <span
                        className="w-1.5 h-1.5 rounded-full mt-2 flex-shrink-0"
                        style={{ backgroundColor: section.color }}
                      />
                      {item}
                    </motion.li>
                  ))}
                </ul>
              </motion.div>
            )}
          </div>
        ))}
      </div>
    </GlassCard>
  );
}
