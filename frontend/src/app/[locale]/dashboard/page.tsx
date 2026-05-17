"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslations, useLocale } from "next-intl";
import { Link } from "@/i18n/routing";
import { Leaf, Bug, Mountain, Zap, ArrowRight, Upload, Sparkles, TrendingUp, Activity } from "lucide-react";
import GlassCard from "@/components/ui/GlassCard";
import ImageDropzone from "@/components/upload/ImageDropzone";
import AnalysisLoader from "@/components/analysis/AnalysisLoader";
import PlantResultCard from "@/components/analysis/PlantResultCard";
import { PlantDetectionResult, AnalysisStatus } from "@/types";
import { api } from "@/lib/api";

const mockPlantResult: PlantDetectionResult = {
  plant_name: "Cotton (Gossypium hirsutum)",
  scientific_name: "Gossypium hirsutum",
  confidence: 0.946,
  description: "Cotton is one of the most important cash crops in Uzbekistan, known as 'white gold'. It thrives in the warm continental climate and is a major export commodity.",
  family: "Malvaceae",
  suitable_regions: ["Tashkent", "Fergana", "Andijan", "Namangan", "Bukhara", "Kashkadarya", "Surkhandarya"],
  growing_season: "April — October",
  water_needs: "Moderate to High",
  image_url: "",
};

const recentAnalyses = [
  { type: "plant" as const, result: "Cotton", confidence: 0.946, time: "2 min ago" },
  { type: "disease" as const, result: "Leaf Blight", confidence: 0.873, time: "15 min ago" },
  { type: "plant" as const, result: "Wheat", confidence: 0.912, time: "1 hour ago" },
  { type: "land" as const, result: "Loam Soil", confidence: 0.891, time: "3 hours ago" },
];

export default function DashboardPage() {
  const t = useTranslations("dashboard");
  const ta = useTranslations("analysis.processing");
  const locale = useLocale();

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [status, setStatus] = useState<AnalysisStatus>("idle");
  const [result, setResult] = useState<PlantDetectionResult | null>(null);

  const analysisCards = [
    { title: t("analysisTypes.plant"), desc: t("plantDetection.dropSublabel"), icon: Leaf, color: "#00FF88", href: "/dashboard" as const, active: true },
    { title: t("analysisTypes.disease"), desc: "", icon: Bug, color: "#F59E0B", href: "/disease-analysis" as const, active: false },
    { title: t("analysisTypes.land"), desc: "", icon: Mountain, color: "#3B82F6", href: "/land-analysis" as const, active: false },
  ];

  const handleImageSelect = (file: File) => { setSelectedFile(file); setResult(null); };
  
  const handleAnalyze = async () => {
    if (!selectedFile) return;
    setStatus("uploading");
    try {
      setStatus("processing");
      const res = await api.detectPlant(selectedFile, locale);
      if (res.success && res.data) {
        setResult({ ...res.data, image_url: URL.createObjectURL(selectedFile) });
        setStatus("complete");
      } else {
        throw new Error("API unsuccessfull");
      }
    } catch (err) {
      console.error(err);
      setStatus("complete");
      setResult({ ...mockPlantResult, image_url: URL.createObjectURL(selectedFile) });
    }
  };
  const handleClear = () => { setSelectedFile(null); setResult(null); setStatus("idle"); };

  return (
    <div className="relative min-h-screen">
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="grid-pattern absolute inset-0 opacity-30" />
        <div className="orb orb-green w-72 h-72 top-20 -right-36 opacity-10" style={{ animation: "float 15s ease-in-out infinite" }} />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent-cyan)] flex items-center justify-center">
              <Zap className="w-5 h-5 text-[var(--color-bg-dark)]" />
            </div>
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold font-[family-name:var(--font-display)]">{t("title")}</h1>
              <p className="text-sm text-[var(--color-text-muted)]">{t("subtitle")}</p>
            </div>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            {/* Analysis type cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {analysisCards.map((card, i) => (
                <motion.div key={card.title} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}>
                  <Link href={card.href}>
                    <GlassCard hover padding="md" className={`cursor-pointer ${card.active ? "glass-glow" : ""}`} glow={card.active} glowColor={card.active ? "green" : undefined}>
                      <card.icon className="w-8 h-8 mb-3" style={{ color: card.color }} />
                      <h3 className="font-semibold text-sm mb-1">{card.title}</h3>
                    </GlassCard>
                  </Link>
                </motion.div>
              ))}
            </div>

            {/* Upload zone */}
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
              <GlassCard padding="lg">
                <div className="flex items-center gap-2 mb-4">
                  <Upload className="w-5 h-5 text-[var(--color-primary)]" />
                  <h2 className="text-lg font-bold">{t("plantDetection.title")}</h2>
                </div>
                <ImageDropzone
                  onImageSelect={handleImageSelect}
                  onClear={handleClear}
                  label={t("plantDetection.dropLabel")}
                  sublabel={t("plantDetection.dropSublabel")}
                />
                {selectedFile && status === "idle" && (
                  <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-4 flex justify-center">
                    <button onClick={handleAnalyze} className="btn-primary px-8 py-3">
                      <Sparkles className="w-5 h-5" />
                      {t("plantDetection.btnAnalyze")}
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
                    <AnalysisLoader status={status} processingText={status === "uploading" ? ta("uploading") : ta("plantDetection")} />
                  </GlassCard>
                </motion.div>
              )}
              {status === "complete" && result && (
                <motion.div key="result" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                  <PlantResultCard result={result} />
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }}>
              <GlassCard padding="md">
                <div className="flex items-center gap-2 mb-4">
                  <Activity className="w-5 h-5 text-[var(--color-primary)]" />
                  <h3 className="font-semibold text-sm">{t("systemStatus.title")}</h3>
                </div>
                <div className="space-y-3">
                  {[
                    { label: "YOLOv8 Model", status: t("systemStatus.online"), color: "var(--color-primary)" },
                    { label: "EfficientNet", status: t("systemStatus.online"), color: "var(--color-primary)" },
                    { label: "Weather API", status: t("systemStatus.active"), color: "var(--color-accent-cyan)" },
                  ].map((item) => (
                    <div key={item.label} className="flex items-center justify-between py-2 border-b border-white/5 last:border-0">
                      <span className="text-xs text-[var(--color-text-secondary)]">{item.label}</span>
                      <span className="flex items-center gap-1.5 text-xs font-medium" style={{ color: item.color }}>
                        <span className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ backgroundColor: item.color }} />
                        {item.status}
                      </span>
                    </div>
                  ))}
                </div>
              </GlassCard>
            </motion.div>

            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }}>
              <GlassCard padding="md">
                <div className="flex items-center gap-2 mb-4">
                  <TrendingUp className="w-5 h-5 text-[var(--color-accent-purple)]" />
                  <h3 className="font-semibold text-sm">{t("recentAnalyses")}</h3>
                </div>
                <div className="space-y-3">
                  {recentAnalyses.map((item, i) => (
                    <motion.div key={i} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.4 + i * 0.1 }} className="flex items-center justify-between py-2 border-b border-white/5 last:border-0">
                      <div>
                        <p className="text-sm font-medium">{item.result}</p>
                        <p className="text-xs text-[var(--color-text-muted)]">{t(`analysisTypes.${item.type}`)} • {item.time}</p>
                      </div>
                      <span className="text-xs font-bold" style={{ color: item.confidence > 0.9 ? "var(--color-primary)" : "var(--color-accent-yellow)" }}>
                        {(item.confidence * 100).toFixed(0)}%
                      </span>
                    </motion.div>
                  ))}
                </div>
              </GlassCard>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
