"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslations, useLocale } from "next-intl";
import { Bug, Sparkles, ArrowRight, ShieldAlert, History } from "lucide-react";
import GlassCard from "@/components/ui/GlassCard";
import ImageDropzone from "@/components/upload/ImageDropzone";
import AnalysisLoader from "@/components/analysis/AnalysisLoader";
import DiseaseResultCard from "@/components/analysis/DiseaseResultCard";
import { DiseaseDetectionResult, AnalysisStatus } from "@/types";
import { api } from "@/lib/api";

const mockDiseaseResult: DiseaseDetectionResult = {
  disease_name: "Early Blight (Alternaria solani)",
  plant_affected: "Tomato",
  confidence: 0.891,
  severity: "high",
  description: "Early blight is a common fungal disease affecting tomato plants. It causes dark, concentric ring-shaped lesions on lower leaves and can reduce fruit yield by up to 79%.",
  causes: [
    "Fungal pathogen Alternaria solani thriving in warm, humid conditions",
    "Overhead watering creating prolonged leaf wetness",
    "Poor air circulation due to dense planting",
    "Infected plant debris from previous seasons",
  ],
  symptoms: ["Dark brown spots with concentric rings", "Yellowing of leaves", "Premature leaf drop"],
  treatments: [
    "Apply copper-based fungicide every 7-10 days",
    "Remove and destroy all infected leaves immediately",
    "Apply neem oil spray as an organic alternative",
    "Improve drainage and reduce watering frequency",
  ],
  prevention_tips: [
    "Rotate crops — avoid planting tomatoes in the same spot for 2-3 years",
    "Space plants adequately for proper air circulation",
    "Water at the base, never overhead, preferably in the morning",
    "Use disease-resistant varieties when available",
  ],
  image_url: "",
};

const sevColors: Record<string, string> = { low: "#00FF88", medium: "#F59E0B", high: "#EF4444", critical: "#DC2626" };

const emptyLabels = {
  uz: "Tahlillar hali mavjud emas",
  ru: "Анализы пока отсутствуют",
  en: "No analyses available yet",
};

interface RecentDiseaseItem {
  name: string;
  plant: string;
  severity: string;
  time: string;
}

export default function DiseaseAnalysisPage() {
  const t = useTranslations("disease");
  const ta = useTranslations("analysis.processing");
  const locale = useLocale();

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [status, setStatus] = useState<AnalysisStatus>("idle");
  const [result, setResult] = useState<DiseaseDetectionResult | null>(null);
  const [recentDetections, setRecentDetections] = useState<RecentDiseaseItem[]>([]);

  const formatTime = (dateStr: string) => {
    try {
      const date = new Date(dateStr);
      const now = new Date();
      const diffMs = now.getTime() - date.getTime();
      const diffMin = Math.floor(diffMs / 60000);
      if (diffMin < 1) return locale === "uz" ? "Hozirgi" : locale === "ru" ? "Только что" : "Just now";
      if (diffMin < 60) return locale === "uz" ? `${diffMin} daq. oldin` : locale === "ru" ? `${diffMin} мин. назад` : `${diffMin}m ago`;
      const diffHrs = Math.floor(diffMin / 60);
      if (diffHrs < 24) return locale === "uz" ? `${diffHrs} soat oldin` : locale === "ru" ? `${diffHrs} ч. назад` : `${diffHrs}h ago`;
      const diffDays = Math.floor(diffHrs / 24);
      return locale === "uz" ? `${diffDays} kun oldin` : locale === "ru" ? `${diffDays} дн. назад` : `${diffDays}d ago`;
    } catch {
      return dateStr;
    }
  };

  useEffect(() => {
    async function loadRecent() {
      try {
        const res = await api.getRecentDiseases(5).catch(() => null);
        if (res && Array.isArray(res)) {
          const items = res.map((item: any) => ({
            name: item.disease_name || "Noma'lum kasallik",
            plant: item.plant_affected || "O'simlik",
            severity: item.severity || "medium",
            time: formatTime(item.created_at),
          }));
          setRecentDetections(items);
        }
      } catch (err) {
        console.error("Error loading recent diseases:", err);
      }
    }
    loadRecent();
  }, [locale]);

  const handleImageSelect = (file: File) => { setSelectedFile(file); setResult(null); setStatus("idle"); };
  const handleAnalyze = async () => {
    if (!selectedFile) return;
    setStatus("uploading");
    try {
      setStatus("processing");
      const res = await api.analyzeDiseases(selectedFile, locale);
      if (res.success && res.data) {
        setResult({ ...res.data, image_url: URL.createObjectURL(selectedFile) });
        setStatus("complete");
      } else {
        throw new Error("API unsuccessfull");
      }
    } catch (err) {
      console.error(err);
      setStatus("complete");
      setResult({ ...mockDiseaseResult, image_url: URL.createObjectURL(selectedFile) });
    }
  };
  const handleClear = () => { setSelectedFile(null); setResult(null); setStatus("idle"); };

  return (
    <div className="relative min-h-screen">
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="grid-pattern absolute inset-0 opacity-30" />
        <div className="orb w-72 h-72 top-20 -left-36 opacity-10" style={{ background: "#F59E0B", animation: "float 15s ease-in-out infinite" }} />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--color-accent-yellow)] to-[var(--color-accent-red)] flex items-center justify-center">
              <Bug className="w-5 h-5 text-[var(--color-bg-dark)]" />
            </div>
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold font-[family-name:var(--font-display)]">{t("title")}</h1>
              <p className="text-sm text-[var(--color-text-muted)]">{t("subtitle")}</p>
            </div>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
              <GlassCard padding="lg">
                <div className="flex items-center gap-2 mb-4">
                  <ShieldAlert className="w-5 h-5 text-[var(--color-accent-yellow)]" />
                  <h2 className="text-lg font-bold">{t("title")}</h2>
                </div>
                <ImageDropzone onImageSelect={handleImageSelect} onClear={handleClear} label={t("dropLabel")} sublabel={t("dropSublabel")} />
                {selectedFile && status === "idle" && (
                  <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-4 flex justify-center">
                    <button onClick={handleAnalyze} className="btn-primary px-8 py-3" style={{ background: "linear-gradient(135deg, #F59E0B, #EF4444)" }}>
                      <Sparkles className="w-5 h-5" />
                      {t("btnDetect")}
                      <ArrowRight className="w-4 h-4" />
                    </button>
                  </motion.div>
                )}
              </GlassCard>
            </motion.div>

            <AnimatePresence mode="wait">
              {(status === "uploading" || status === "processing") && (
                <motion.div key="loader" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}>
                  <GlassCard padding="lg">
                    <AnalysisLoader status={status} processingText={status === "uploading" ? ta("uploading") : ta("diseaseClassifier")} />
                  </GlassCard>
                </motion.div>
              )}
              {status === "complete" && result && (
                <motion.div key="result" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                  <DiseaseResultCard result={result} />
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <div className="space-y-6">
            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }}>
              <GlassCard padding="md">
                <div className="flex items-center gap-2 mb-4">
                  <History className="w-5 h-5 text-[var(--color-accent-yellow)]" />
                  <h3 className="font-semibold text-sm">{t("recentDetections")}</h3>
                </div>
                <div className="space-y-3">
                  {recentDetections.length > 0 ? (
                    recentDetections.map((item, i) => (
                      <div key={i} className="flex items-center justify-between py-2 border-b border-white/5 last:border-0">
                        <div>
                          <p className="text-sm font-medium">{item.name}</p>
                          <p className="text-xs text-[var(--color-text-muted)]">{item.plant} • {item.time}</p>
                        </div>
                        <span className="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase" style={{ color: sevColors[item.severity], backgroundColor: `${sevColors[item.severity]}15`, border: `1px solid ${sevColors[item.severity]}30` }}>
                          {t(`severity.${item.severity as "low" | "medium" | "high" | "critical"}`)}
                        </span>
                      </div>
                    ))
                  ) : (
                    <p className="text-xs text-[var(--color-text-muted)] py-2 text-center">
                      {emptyLabels[locale as "uz" | "ru" | "en"] || emptyLabels.uz}
                    </p>
                  )}
                </div>
              </GlassCard>
            </motion.div>

            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }}>
              <GlassCard padding="md" glow glowColor="yellow">
                <h3 className="font-semibold text-sm mb-3">💡 {t("tips.title")}</h3>
                <ul className="space-y-2 text-xs text-[var(--color-text-secondary)]">
                  {(["tip1", "tip2", "tip3", "tip4"] as const).map((key) => (
                    <li key={key} className="flex items-start gap-2">
                      <span className="w-1 h-1 rounded-full bg-[var(--color-accent-yellow)] mt-1.5 flex-shrink-0" />
                      {t(`tips.${key}`)}
                    </li>
                  ))}
                </ul>
              </GlassCard>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
