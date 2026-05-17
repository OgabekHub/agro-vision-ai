"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useTranslations } from "next-intl";
import { MapPin, ThermometerSun, Droplets, Sprout, Cloud, ChevronRight } from "lucide-react";
import GlassCard from "@/components/ui/GlassCard";
import { RegionData } from "@/types";

const regionsData: RegionData[] = [
  { id: "tashkent", name: "Tashkent", name_uz: "Toshkent", capital: "Tashkent", coordinates: [41.299, 69.240], area_km2: 15300, climate: "Continental, Semi-arid", avg_temperature: { summer: 36, winter: -2 }, annual_rainfall_mm: 440, main_crops: ["Cotton", "Wheat", "Vegetables", "Grapes", "Fruits"], soil_types: ["Loamy", "Sierozem"], agricultural_area_hectares: 420000 },
  { id: "samarkand", name: "Samarkand", name_uz: "Samarqand", capital: "Samarkand", coordinates: [39.654, 66.959], area_km2: 16400, climate: "Continental", avg_temperature: { summer: 35, winter: -1 }, annual_rainfall_mm: 350, main_crops: ["Cotton", "Wheat", "Silk", "Grapes", "Melons"], soil_types: ["Sierozem", "Alluvial"], agricultural_area_hectares: 510000 },
  { id: "fergana", name: "Fergana", name_uz: "Farg'ona", capital: "Fergana", coordinates: [40.384, 71.789], area_km2: 6800, climate: "Continental, Fertile Valley", avg_temperature: { summer: 34, winter: -3 }, annual_rainfall_mm: 180, main_crops: ["Cotton", "Silk", "Rice", "Fruits", "Vegetables"], soil_types: ["Alluvial", "Meadow"], agricultural_area_hectares: 310000 },
  { id: "bukhara", name: "Bukhara", name_uz: "Buxoro", capital: "Bukhara", coordinates: [39.767, 64.421], area_km2: 39400, climate: "Arid, Desert", avg_temperature: { summer: 40, winter: 1 }, annual_rainfall_mm: 140, main_crops: ["Cotton", "Karakul Sheep", "Silkworm", "Wheat"], soil_types: ["Sandy", "Desert Sierozem"], agricultural_area_hectares: 280000 },
  { id: "andijan", name: "Andijan", name_uz: "Andijon", capital: "Andijan", coordinates: [40.783, 72.344], area_km2: 4200, climate: "Continental, Fertile", avg_temperature: { summer: 33, winter: -3 }, annual_rainfall_mm: 220, main_crops: ["Cotton", "Corn", "Vegetables", "Fruits", "Rice"], soil_types: ["Alluvial", "Meadow"], agricultural_area_hectares: 210000 },
  { id: "namangan", name: "Namangan", name_uz: "Namangan", capital: "Namangan", coordinates: [40.995, 71.672], area_km2: 7900, climate: "Continental", avg_temperature: { summer: 34, winter: -2 }, annual_rainfall_mm: 200, main_crops: ["Cotton", "Fruits", "Vegetables", "Grapes"], soil_types: ["Sierozem", "Alluvial"], agricultural_area_hectares: 280000 },
  { id: "kashkadarya", name: "Kashkadarya", name_uz: "Qashqadaryo", capital: "Karshi", coordinates: [38.860, 65.800], area_km2: 28400, climate: "Continental, Semi-arid", avg_temperature: { summer: 38, winter: 0 }, annual_rainfall_mm: 250, main_crops: ["Cotton", "Wheat", "Grain", "Livestock"], soil_types: ["Sierozem", "Brown"], agricultural_area_hectares: 580000 },
  { id: "surkhandarya", name: "Surkhandarya", name_uz: "Surxondaryo", capital: "Termez", coordinates: [37.224, 67.278], area_km2: 20800, climate: "Subtropical, Hot", avg_temperature: { summer: 42, winter: 3 }, annual_rainfall_mm: 300, main_crops: ["Cotton", "Citrus", "Rice", "Sugarcane", "Vegetables"], soil_types: ["Alluvial", "Sierozem"], agricultural_area_hectares: 370000 },
  { id: "khorezm", name: "Khorezm", name_uz: "Xorazm", capital: "Urgench", coordinates: [41.551, 60.631], area_km2: 6300, climate: "Continental, Irrigated", avg_temperature: { summer: 37, winter: -5 }, annual_rainfall_mm: 100, main_crops: ["Cotton", "Rice", "Wheat", "Melons"], soil_types: ["Alluvial", "Meadow"], agricultural_area_hectares: 260000 },
  { id: "jizzakh", name: "Jizzakh", name_uz: "Jizzax", capital: "Jizzakh", coordinates: [40.115, 67.842], area_km2: 20500, climate: "Continental", avg_temperature: { summer: 37, winter: -1 }, annual_rainfall_mm: 300, main_crops: ["Cotton", "Wheat", "Livestock", "Vegetables"], soil_types: ["Sierozem", "Brown"], agricultural_area_hectares: 410000 },
  { id: "navoi", name: "Navoi", name_uz: "Navoiy", capital: "Navoi", coordinates: [40.103, 65.379], area_km2: 110800, climate: "Arid, Desert", avg_temperature: { summer: 39, winter: -2 }, annual_rainfall_mm: 120, main_crops: ["Cotton", "Wheat", "Karakul"], soil_types: ["Desert", "Sandy"], agricultural_area_hectares: 190000 },
  { id: "syrdarya", name: "Syrdarya", name_uz: "Sirdaryo", capital: "Gulistan", coordinates: [40.486, 68.715], area_km2: 5100, climate: "Continental", avg_temperature: { summer: 36, winter: -1 }, annual_rainfall_mm: 300, main_crops: ["Cotton", "Wheat", "Rice", "Vegetables"], soil_types: ["Alluvial", "Meadow"], agricultural_area_hectares: 230000 },
  { id: "karakalpakstan", name: "Karakalpakstan", name_uz: "Qoraqalpog'iston", capital: "Nukus", coordinates: [42.461, 59.606], area_km2: 166600, climate: "Arid, Continental", avg_temperature: { summer: 35, winter: -7 }, annual_rainfall_mm: 90, main_crops: ["Cotton", "Rice", "Wheat", "Melons"], soil_types: ["Desert", "Alluvial"], agricultural_area_hectares: 480000 },
  { id: "tashkent_city", name: "Tashkent City", name_uz: "Toshkent shahri", capital: "Tashkent", coordinates: [41.311, 69.280], area_km2: 335, climate: "Continental Urban", avg_temperature: { summer: 35, winter: -1 }, annual_rainfall_mm: 440, main_crops: ["Urban Agriculture", "Greenhouses", "Vegetables"], soil_types: ["Urban", "Loamy"], agricultural_area_hectares: 5000 },
];

export default function RegionsPage() {
  const t = useTranslations("regions");
  const [selectedRegion, setSelectedRegion] = useState<RegionData | null>(null);

  return (
    <div className="relative min-h-screen">
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="grid-pattern absolute inset-0 opacity-30" />
        <div className="orb orb-purple w-72 h-72 top-20 -right-36 opacity-10" style={{ animation: "float 15s ease-in-out infinite" }} />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--color-accent-purple)] to-[var(--color-accent-cyan)] flex items-center justify-center">
              <MapPin className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold font-[family-name:var(--font-display)]">{t("title")}</h1>
              <p className="text-sm text-[var(--color-text-muted)]">{t("subtitle")}</p>
            </div>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Region List */}
          <div className="lg:col-span-1 space-y-3 max-h-[75vh] overflow-y-auto pr-2">
            {regionsData.map((region, i) => (
              <motion.div key={region.id} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.03 }}>
                <button onClick={() => setSelectedRegion(region)} className={`w-full text-left p-4 rounded-xl border transition-all ${selectedRegion?.id === region.id ? "bg-[var(--color-primary-subtle)] border-[var(--color-border-glow)] shadow-[0_0_20px_rgba(0,255,136,0.08)]" : "bg-[var(--color-bg-card)] border-white/5 hover:border-white/10 hover:bg-[var(--color-bg-card-hover)]"}`}>
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className={`font-semibold text-sm ${selectedRegion?.id === region.id ? "text-[var(--color-primary)]" : ""}`}>{region.name}</h3>
                      <p className="text-xs text-[var(--color-text-muted)]">{region.name_uz} • {region.main_crops.slice(0, 3).join(", ")}</p>
                    </div>
                    <ChevronRight className={`w-4 h-4 transition-transform ${selectedRegion?.id === region.id ? "text-[var(--color-primary)] rotate-90" : "text-[var(--color-text-muted)]"}`} />
                  </div>
                </button>
              </motion.div>
            ))}
          </div>

          {/* Region Detail */}
          <div className="lg:col-span-2">
            {selectedRegion ? (
              <motion.div key={selectedRegion.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
                <GlassCard glow glowColor="purple" padding="lg">
                  <div className="flex items-start justify-between mb-6">
                    <div>
                      <h2 className="text-2xl font-bold font-[family-name:var(--font-display)] gradient-text">{selectedRegion.name}</h2>
                      <p className="text-sm text-[var(--color-text-muted)]">{selectedRegion.name_uz} • {t("labels.capital")}: {selectedRegion.capital}</p>
                    </div>
                    <span className="px-3 py-1 rounded-full text-xs font-medium bg-[var(--color-accent-purple)]/10 text-[var(--color-accent-purple)] border border-[var(--color-accent-purple)]/20">
                      {selectedRegion.area_km2.toLocaleString()} km²
                    </span>
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-6">
                    <div className="p-3 rounded-xl bg-white/3 border border-white/5 text-center">
                      <ThermometerSun className="w-5 h-5 mx-auto mb-2 text-[var(--color-accent-red)]" />
                      <p className="text-xs text-[var(--color-text-muted)]">{t("labels.summer")}</p>
                      <p className="text-lg font-bold">{selectedRegion.avg_temperature.summer}°C</p>
                    </div>
                    <div className="p-3 rounded-xl bg-white/3 border border-white/5 text-center">
                      <Cloud className="w-5 h-5 mx-auto mb-2 text-[var(--color-accent-blue)]" />
                      <p className="text-xs text-[var(--color-text-muted)]">{t("labels.winter")}</p>
                      <p className="text-lg font-bold">{selectedRegion.avg_temperature.winter}°C</p>
                    </div>
                    <div className="p-3 rounded-xl bg-white/3 border border-white/5 text-center">
                      <Droplets className="w-5 h-5 mx-auto mb-2 text-[var(--color-accent-cyan)]" />
                      <p className="text-xs text-[var(--color-text-muted)]">{t("labels.rainfall")}</p>
                      <p className="text-lg font-bold">{selectedRegion.annual_rainfall_mm}mm</p>
                    </div>
                    <div className="p-3 rounded-xl bg-white/3 border border-white/5 text-center">
                      <Sprout className="w-5 h-5 mx-auto mb-2 text-[var(--color-primary)]" />
                      <p className="text-xs text-[var(--color-text-muted)]">{t("labels.agriArea")}</p>
                      <p className="text-lg font-bold">{(selectedRegion.agricultural_area_hectares / 1000).toFixed(0)}K ha</p>
                    </div>
                  </div>

                  <div className="mb-4">
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-2">{t("labels.climate")}</p>
                    <p className="text-sm text-[var(--color-text-secondary)]">{selectedRegion.climate}</p>
                  </div>
                  <div className="mb-4">
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-2">{t("labels.soilTypes")}</p>
                    <div className="flex flex-wrap gap-2">
                      {selectedRegion.soil_types.map((soil) => (
                        <span key={soil} className="px-3 py-1 rounded-full text-xs bg-[var(--color-accent-blue)]/10 text-[var(--color-accent-blue)] border border-[var(--color-accent-blue)]/20">{soil}</span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-2">{t("labels.mainCrops")}</p>
                    <div className="flex flex-wrap gap-2">
                      {selectedRegion.main_crops.map((crop) => (
                        <span key={crop} className="px-3 py-1 rounded-full text-xs bg-[var(--color-primary-subtle)] text-[var(--color-primary)] border border-[var(--color-border-glow)]">{crop}</span>
                      ))}
                    </div>
                  </div>
                </GlassCard>
              </motion.div>
            ) : (
              <GlassCard padding="xl" className="flex flex-col items-center justify-center min-h-[400px] text-center">
                <MapPin className="w-16 h-16 text-[var(--color-text-muted)] mb-4 opacity-30" />
                <h3 className="text-lg font-semibold mb-2">{t("selectRegion")}</h3>
                <p className="text-sm text-[var(--color-text-muted)] max-w-md">{t("selectHint")}</p>
              </GlassCard>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
