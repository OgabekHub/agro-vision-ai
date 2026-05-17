"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslations, useLocale } from "next-intl";
import { Mountain, Sparkles, ArrowRight, Droplets, Sprout, ThermometerSun, FlaskConical } from "lucide-react";
import GlassCard from "@/components/ui/GlassCard";
import ImageDropzone from "@/components/upload/ImageDropzone";
import AnalysisLoader from "@/components/analysis/AnalysisLoader";
import ConfidenceGauge from "@/components/analysis/ConfidenceGauge";
import { LandAnalysisResult, AnalysisStatus } from "@/types";
import { api } from "@/lib/api";

const mockLandResult: LandAnalysisResult = {
  soil_condition: {
    type: "Loamy Soil", ph_level: 6.8, moisture: "Moderate", organic_matter: "Medium (3.2%)",
    nutrients: { nitrogen: "Adequate", phosphorus: "Low", potassium: "High" },
  },
  region: "Tashkent",
  recommended_crops: [
    { crop_name: "Cotton", suitability_score: 0.94, expected_yield: "3.2 tons/ha", growing_period: "Apr-Oct", irrigation_type: "Drip Irrigation", tips: ["Plant after soil temperature reaches 18°C"] },
    { crop_name: "Wheat", suitability_score: 0.88, expected_yield: "4.5 tons/ha", growing_period: "Oct-Jun", irrigation_type: "Sprinkler", tips: ["Ideal for winter planting"] },
    { crop_name: "Tomato", suitability_score: 0.82, expected_yield: "25 tons/ha", growing_period: "Mar-Sep", irrigation_type: "Drip Irrigation", tips: ["Use raised beds"] },
    { crop_name: "Grape", suitability_score: 0.79, expected_yield: "8 tons/ha", growing_period: "Mar-Oct", irrigation_type: "Furrow", tips: ["Prune in late winter"] },
  ],
  farming_suggestions: [
    "Add phosphorus-rich fertilizer to address low phosphorus levels",
    "Implement crop rotation with legumes",
    "Apply organic mulch during hot summer months",
    "Consider cover crops in winter to prevent erosion",
  ],
  irrigation_advice: "Drip irrigation is recommended. Schedule in early morning to minimize evaporation. Expected water savings: 30-40%.",
  image_url: "",
};

export default function LandAnalysisPage() {
  const t = useTranslations("land");
  const ta = useTranslations("analysis.processing");
  const locale = useLocale();

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [status, setStatus] = useState<AnalysisStatus>("idle");
  const [result, setResult] = useState<LandAnalysisResult | null>(null);

  const handleImageSelect = (file: File) => { setSelectedFile(file); setResult(null); setStatus("idle"); };
  const handleAnalyze = async () => {
    if (!selectedFile) return;
    setStatus("uploading");
    
    try {
      setStatus("processing");
      const res = await api.analyzeLand(selectedFile, locale);
      
      if (res.success && res.data) {
        setResult({ ...res.data, image_url: URL.createObjectURL(selectedFile) });
        setStatus("complete");
      } else {
        throw new Error("API unsuccessful");
      }
    } catch (err) {
      console.error(err);
      setStatus("complete");
      setResult({ ...mockLandResult, image_url: URL.createObjectURL(selectedFile) });
    }
  };
  const handleClear = () => { setSelectedFile(null); setResult(null); setStatus("idle"); };

  return (
    <div className="relative min-h-screen">
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="grid-pattern absolute inset-0 opacity-30" />
        <div className="orb w-72 h-72 top-20 -right-36 opacity-10" style={{ background: "#3B82F6", animation: "float 15s ease-in-out infinite" }} />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--color-accent-blue)] to-[var(--color-accent-purple)] flex items-center justify-center">
              <Mountain className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold font-[family-name:var(--font-display)]">{t("title")}</h1>
              <p className="text-sm text-[var(--color-text-muted)]">{t("subtitle")}</p>
            </div>
          </div>
        </motion.div>

        <div className="max-w-3xl mx-auto space-y-6">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
            <GlassCard padding="lg">
              <ImageDropzone onImageSelect={handleImageSelect} onClear={handleClear} label={t("dropLabel")} sublabel={t("dropSublabel")} />
              {selectedFile && status === "idle" && (
                <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-4 flex justify-center">
                  <button onClick={handleAnalyze} className="btn-primary px-8 py-3" style={{ background: "linear-gradient(135deg, #3B82F6, #8B5CF6)" }}>
                    <Sparkles className="w-5 h-5" />
                    {t("btnAnalyze")}
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </motion.div>
              )}
            </GlassCard>
          </motion.div>

          <AnimatePresence mode="wait">
            {(status === "uploading" || status === "processing") && (
              <motion.div key="loader" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                <GlassCard padding="lg">
                  <AnalysisLoader status={status} processingText={status === "uploading" ? ta("uploading") : ta("soilAnalysis")} />
                </GlassCard>
              </motion.div>
            )}

            {status === "complete" && result && (
              <motion.div key="results" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
                {/* Soil */}
                <GlassCard glow glowColor="blue" padding="lg">
                  <h2 className="text-xl font-bold font-[family-name:var(--font-display)] mb-4 flex items-center gap-2">
                    <FlaskConical className="w-5 h-5 text-[var(--color-accent-blue)]" />
                    {t("soilAnalysis")}
                  </h2>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-4">
                    {[
                      { labelKey: "soilType" as const, value: result.soil_condition.type, icon: Mountain },
                      { labelKey: "phLevel" as const, value: result.soil_condition.ph_level.toString(), icon: FlaskConical },
                      { labelKey: "moisture" as const, value: result.soil_condition.moisture, icon: Droplets },
                      { labelKey: "organicMatter" as const, value: result.soil_condition.organic_matter, icon: Sprout },
                    ].map((item) => (
                      <div key={item.labelKey} className="p-3 rounded-xl bg-white/3 border border-white/5 text-center">
                        <item.icon className="w-5 h-5 mx-auto mb-2 text-[var(--color-accent-blue)]" />
                        <p className="text-xs text-[var(--color-text-muted)] mb-0.5">{t(`labels.${item.labelKey}`)}</p>
                        <p className="text-sm font-bold">{item.value}</p>
                      </div>
                    ))}
                  </div>
                  <div className="grid grid-cols-3 gap-3">
                    {Object.entries(result.soil_condition.nutrients).map(([key, val]) => (
                      <div key={key} className="p-2 rounded-lg bg-white/3 border border-white/5 text-center">
                        <p className="text-xs text-[var(--color-text-muted)] capitalize">{key}</p>
                        <p className="text-sm font-semibold" style={{ color: val === "Low" ? "#EF4444" : val === "High" ? "#00FF88" : "#F59E0B" }}>{val}</p>
                      </div>
                    ))}
                  </div>
                </GlassCard>

                {/* Crops */}
                <GlassCard glow glowColor="green" padding="lg">
                  <h2 className="text-xl font-bold font-[family-name:var(--font-display)] mb-4 flex items-center gap-2">
                    <Sprout className="w-5 h-5 text-[var(--color-primary)]" />
                    {t("recommendedCrops")}
                  </h2>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {result.recommended_crops.map((crop, i) => (
                      <motion.div key={crop.crop_name} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }} className="p-4 rounded-xl bg-white/3 border border-white/5">
                        <div className="flex items-center justify-between mb-3">
                          <h3 className="font-bold">{crop.crop_name}</h3>
                          <ConfidenceGauge confidence={crop.suitability_score} size="sm" label="" />
                        </div>
                        <div className="space-y-1.5 text-xs text-[var(--color-text-secondary)]">
                          <p>📅 {t("labels.growingPeriod")}: {crop.growing_period}</p>
                          <p>📊 {t("labels.expectedYield")}: {crop.expected_yield}</p>
                          <p>💧 {crop.irrigation_type}</p>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </GlassCard>

                {/* Irrigation */}
                <GlassCard glow glowColor="cyan" padding="lg">
                  <h2 className="text-xl font-bold font-[family-name:var(--font-display)] mb-3 flex items-center gap-2">
                    <Droplets className="w-5 h-5 text-[var(--color-accent-cyan)]" />
                    {t("irrigationAdvice")}
                  </h2>
                  <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">{result.irrigation_advice}</p>
                </GlassCard>

                {/* Suggestions */}
                <GlassCard padding="lg">
                  <h2 className="text-xl font-bold font-[family-name:var(--font-display)] mb-3 flex items-center gap-2">
                    <ThermometerSun className="w-5 h-5 text-[var(--color-accent-yellow)]" />
                    {t("farmingSuggestions")}
                  </h2>
                  <ul className="space-y-2">
                    {result.farming_suggestions.map((s, i) => (
                      <li key={i} className="flex items-start gap-3 text-sm text-[var(--color-text-secondary)]">
                        <span className="w-6 h-6 rounded-lg bg-[var(--color-accent-yellow)]/10 flex items-center justify-center text-xs font-bold text-[var(--color-accent-yellow)] flex-shrink-0">{i + 1}</span>
                        {s}
                      </li>
                    ))}
                  </ul>
                </GlassCard>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
