"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useTranslations, useLocale } from "next-intl";
import { MapPin, ThermometerSun, Droplets, Sprout, Cloud, ChevronRight } from "lucide-react";
import GlassCard from "@/components/ui/GlassCard";
import { RegionData } from "@/types";

// Regionlar uchun ko'p tilli ma'lumotlar
const regionsData = [
  {
    id: "tashkent", name: "Tashkent Region", name_uz: "Toshkent viloyati", name_ru: "Ташкентская область",
    capital: "Nurafshon", capital_uz: "Nurafshon", capital_ru: "Нурафшан",
    coordinates: [41.299, 69.240], area_km2: 15300,
    climate: "Continental, Semi-arid", climate_uz: "Kontinental, Yarim quruq", climate_ru: "Континентальный, полузасушливый",
    avg_temperature: { summer: 36, winter: -2 }, annual_rainfall_mm: 440,
    main_crops: ["Cotton", "Wheat", "Vegetables", "Grapes", "Fruits"],
    main_crops_uz: ["Paxta", "Bug'doy", "Sabzavotlar", "Uzum", "Mevalar"],
    main_crops_ru: ["Хлопок", "Пшеница", "Овощи", "Виноград", "Фрукты"],
    soil_types: ["Loamy", "Sierozem"],
    soil_types_uz: ["Qumoq", "Bo'z tuproq"],
    soil_types_ru: ["Суглинок", "Серозём"],
    agricultural_area_hectares: 395000,
  },
  {
    id: "samarkand", name: "Samarkand", name_uz: "Samarqand", name_ru: "Самарканд",
    capital: "Samarkand", capital_uz: "Samarqand", capital_ru: "Самарканд",
    coordinates: [39.654, 66.959], area_km2: 16773,
    climate: "Continental", climate_uz: "Kontinental", climate_ru: "Континентальный",
    avg_temperature: { summer: 35, winter: -1 }, annual_rainfall_mm: 350,
    main_crops: ["Cotton", "Wheat", "Silk", "Grapes", "Melons"],
    main_crops_uz: ["Paxta", "Bug'doy", "Ipak", "Uzum", "Qovun"],
    main_crops_ru: ["Хлопок", "Пшеница", "Шёлк", "Виноград", "Дыня"],
    soil_types: ["Sierozem", "Alluvial"],
    soil_types_uz: ["Bo'z tuproq", "Allyuvial"],
    soil_types_ru: ["Серозём", "Аллювиальный"],
    agricultural_area_hectares: 510000,
  },
  {
    id: "fergana", name: "Fergana", name_uz: "Farg'ona", name_ru: "Фергана",
    capital: "Fergana", capital_uz: "Farg'ona", capital_ru: "Фергана",
    coordinates: [40.384, 71.789], area_km2: 6800,
    climate: "Continental, Fertile Valley", climate_uz: "Kontinental, Unumdor vodiy", climate_ru: "Континентальный, плодородная долина",
    avg_temperature: { summer: 34, winter: -3 }, annual_rainfall_mm: 180,
    main_crops: ["Cotton", "Silk", "Rice", "Fruits", "Vegetables"],
    main_crops_uz: ["Paxta", "Ipak", "Sholi", "Mevalar", "Sabzavotlar"],
    main_crops_ru: ["Хлопок", "Шёлк", "Рис", "Фрукты", "Овощи"],
    soil_types: ["Alluvial", "Meadow"],
    soil_types_uz: ["Allyuvial", "O'tloq"],
    soil_types_ru: ["Аллювиальный", "Луговой"],
    agricultural_area_hectares: 310000,
  },
  {
    id: "bukhara", name: "Bukhara", name_uz: "Buxoro", name_ru: "Бухара",
    capital: "Bukhara", capital_uz: "Buxoro", capital_ru: "Бухара",
    coordinates: [39.767, 64.421], area_km2: 40300,
    climate: "Arid, Desert", climate_uz: "Quruq, Cho'l", climate_ru: "Засушливый, пустынный",
    avg_temperature: { summer: 40, winter: 1 }, annual_rainfall_mm: 140,
    main_crops: ["Cotton", "Karakul Sheep", "Silkworm", "Wheat"],
    main_crops_uz: ["Paxta", "Qorako'l qo'y", "Ipak qurti", "Bug'doy"],
    main_crops_ru: ["Хлопок", "Каракульские овцы", "Шелкопряд", "Пшеница"],
    soil_types: ["Sandy", "Desert Sierozem"],
    soil_types_uz: ["Qumloq", "Cho'l bo'z tuproq"],
    soil_types_ru: ["Песчаный", "Пустынный серозём"],
    agricultural_area_hectares: 280000,
  },
  {
    id: "andijan", name: "Andijan", name_uz: "Andijon", name_ru: "Андижан",
    capital: "Andijan", capital_uz: "Andijon", capital_ru: "Андижан",
    coordinates: [40.783, 72.344], area_km2: 4300,
    climate: "Continental, Fertile", climate_uz: "Kontinental, Unumdor", climate_ru: "Континентальный, плодородный",
    avg_temperature: { summer: 33, winter: -3 }, annual_rainfall_mm: 220,
    main_crops: ["Cotton", "Corn", "Vegetables", "Fruits", "Rice"],
    main_crops_uz: ["Paxta", "Makkajo'xori", "Sabzavotlar", "Mevalar", "Sholi"],
    main_crops_ru: ["Хлопок", "Кукуруза", "Овощи", "Фрукты", "Рис"],
    soil_types: ["Alluvial", "Meadow"],
    soil_types_uz: ["Allyuvial", "O'tloq"],
    soil_types_ru: ["Аллювиальный", "Луговой"],
    agricultural_area_hectares: 210000,
  },
  {
    id: "namangan", name: "Namangan", name_uz: "Namangan", name_ru: "Наманган",
    capital: "Namangan", capital_uz: "Namangan", capital_ru: "Наманган",
    coordinates: [40.995, 71.672], area_km2: 7900,
    climate: "Continental", climate_uz: "Kontinental", climate_ru: "Континентальный",
    avg_temperature: { summer: 34, winter: -2 }, annual_rainfall_mm: 200,
    main_crops: ["Cotton", "Fruits", "Vegetables", "Grapes"],
    main_crops_uz: ["Paxta", "Mevalar", "Sabzavotlar", "Uzum"],
    main_crops_ru: ["Хлопок", "Фрукты", "Овощи", "Виноград"],
    soil_types: ["Sierozem", "Alluvial"],
    soil_types_uz: ["Bo'z tuproq", "Allyuvial"],
    soil_types_ru: ["Серозём", "Аллювиальный"],
    agricultural_area_hectares: 280000,
  },
  {
    id: "kashkadarya", name: "Kashkadarya", name_uz: "Qashqadaryo", name_ru: "Кашкадарья",
    capital: "Karshi", capital_uz: "Qarshi", capital_ru: "Карши",
    coordinates: [38.860, 65.800], area_km2: 28568,
    climate: "Continental, Semi-arid", climate_uz: "Kontinental, Yarim quruq", climate_ru: "Континентальный, полузасушливый",
    avg_temperature: { summer: 38, winter: 0 }, annual_rainfall_mm: 250,
    main_crops: ["Cotton", "Wheat", "Grain", "Livestock"],
    main_crops_uz: ["Paxta", "Bug'doy", "Don", "Chorvachilik"],
    main_crops_ru: ["Хлопок", "Пшеница", "Зерно", "Животноводство"],
    soil_types: ["Sierozem", "Brown"],
    soil_types_uz: ["Bo'z tuproq", "Jigarrang"],
    soil_types_ru: ["Серозём", "Бурый"],
    agricultural_area_hectares: 580000,
  },
  {
    id: "surkhandarya", name: "Surkhandarya", name_uz: "Surxondaryo", name_ru: "Сурхандарья",
    capital: "Termez", capital_uz: "Termiz", capital_ru: "Термез",
    coordinates: [37.224, 67.278], area_km2: 20099,
    climate: "Subtropical, Hot", climate_uz: "Subtropik, Issiq", climate_ru: "Субтропический, жаркий",
    avg_temperature: { summer: 42, winter: 3 }, annual_rainfall_mm: 300,
    main_crops: ["Cotton", "Citrus", "Rice", "Sugarcane", "Vegetables"],
    main_crops_uz: ["Paxta", "Sitrus", "Sholi", "Shakarqamish", "Sabzavotlar"],
    main_crops_ru: ["Хлопок", "Цитрус", "Рис", "Сахарный тростник", "Овощи"],
    soil_types: ["Alluvial", "Sierozem"],
    soil_types_uz: ["Allyuvial", "Bo'z tuproq"],
    soil_types_ru: ["Аллювиальный", "Серозём"],
    agricultural_area_hectares: 370000,
  },
  {
    id: "khorezm", name: "Khorezm", name_uz: "Xorazm", name_ru: "Хорезм",
    capital: "Urgench", capital_uz: "Urganch", capital_ru: "Ургенч",
    coordinates: [41.551, 60.631], area_km2: 6300,
    climate: "Continental, Irrigated", climate_uz: "Kontinental, Sug'oriladigan", climate_ru: "Континентальный, орошаемый",
    avg_temperature: { summer: 37, winter: -5 }, annual_rainfall_mm: 100,
    main_crops: ["Cotton", "Rice", "Wheat", "Melons"],
    main_crops_uz: ["Paxta", "Sholi", "Bug'doy", "Qovun"],
    main_crops_ru: ["Хлопок", "Рис", "Пшеница", "Дыня"],
    soil_types: ["Alluvial", "Meadow"],
    soil_types_uz: ["Allyuvial", "O'tloq"],
    soil_types_ru: ["Аллювиальный", "Луговой"],
    agricultural_area_hectares: 260000,
  },
  {
    id: "jizzakh", name: "Jizzakh", name_uz: "Jizzax", name_ru: "Джизак",
    capital: "Jizzakh", capital_uz: "Jizzax", capital_ru: "Джизак",
    coordinates: [40.115, 67.842], area_km2: 21179,
    climate: "Continental", climate_uz: "Kontinental", climate_ru: "Континентальный",
    avg_temperature: { summer: 37, winter: -1 }, annual_rainfall_mm: 300,
    main_crops: ["Cotton", "Wheat", "Livestock", "Vegetables"],
    main_crops_uz: ["Paxta", "Bug'doy", "Chorvachilik", "Sabzavotlar"],
    main_crops_ru: ["Хлопок", "Пшеница", "Животноводство", "Овощи"],
    soil_types: ["Sierozem", "Brown"],
    soil_types_uz: ["Bo'z tuproq", "Jigarrang"],
    soil_types_ru: ["Серозём", "Бурый"],
    agricultural_area_hectares: 410000,
  },
  {
    id: "navoi", name: "Navoi", name_uz: "Navoiy", name_ru: "Навои",
    capital: "Navoi", capital_uz: "Navoiy", capital_ru: "Навои",
    coordinates: [40.103, 65.379], area_km2: 110800,
    climate: "Arid, Desert", climate_uz: "Quruq, Cho'l", climate_ru: "Засушливый, пустынный",
    avg_temperature: { summer: 39, winter: -2 }, annual_rainfall_mm: 120,
    main_crops: ["Cotton", "Wheat", "Karakul"],
    main_crops_uz: ["Paxta", "Bug'doy", "Qorako'l"],
    main_crops_ru: ["Хлопок", "Пшеница", "Каракуль"],
    soil_types: ["Desert", "Sandy"],
    soil_types_uz: ["Cho'l", "Qumloq"],
    soil_types_ru: ["Пустынный", "Песчаный"],
    agricultural_area_hectares: 190000,
  },
  {
    id: "syrdarya", name: "Syrdarya", name_uz: "Sirdaryo", name_ru: "Сырдарья",
    capital: "Gulistan", capital_uz: "Guliston", capital_ru: "Гулистан",
    coordinates: [40.486, 68.715], area_km2: 4276,
    climate: "Continental", climate_uz: "Kontinental", climate_ru: "Континентальный",
    avg_temperature: { summer: 36, winter: -1 }, annual_rainfall_mm: 300,
    main_crops: ["Cotton", "Wheat", "Rice", "Vegetables"],
    main_crops_uz: ["Paxta", "Bug'doy", "Sholi", "Sabzavotlar"],
    main_crops_ru: ["Хлопок", "Пшеница", "Рис", "Овощи"],
    soil_types: ["Alluvial", "Meadow"],
    soil_types_uz: ["Allyuvial", "O'tloq"],
    soil_types_ru: ["Аллювиальный", "Луговой"],
    agricultural_area_hectares: 230000,
  },
  {
    id: "karakalpakstan", name: "Karakalpakstan", name_uz: "Qoraqalpog'iston", name_ru: "Каракалпакстан",
    capital: "Nukus", capital_uz: "Nukus", capital_ru: "Нукус",
    coordinates: [42.461, 59.606], area_km2: 166600,
    climate: "Arid, Continental", climate_uz: "Quruq, Kontinental", climate_ru: "Засушливый, континентальный",
    avg_temperature: { summer: 35, winter: -8 }, annual_rainfall_mm: 90,
    main_crops: ["Cotton", "Rice", "Wheat", "Melons"],
    main_crops_uz: ["Paxta", "Sholi", "Bug'doy", "Qovun"],
    main_crops_ru: ["Хлопок", "Рис", "Пшеница", "Дыня"],
    soil_types: ["Desert", "Alluvial"],
    soil_types_uz: ["Cho'l", "Allyuvial"],
    soil_types_ru: ["Пустынный", "Аллювиальный"],
    agricultural_area_hectares: 480000,
  },
  {
    id: "tashkent_city", name: "Tashkent City", name_uz: "Toshkent shahri", name_ru: "Город Ташкент",
    capital: "Tashkent", capital_uz: "Toshkent", capital_ru: "Ташкент",
    coordinates: [41.311, 69.280], area_km2: 435,
    climate: "Continental Urban", climate_uz: "Kontinental shahar", climate_ru: "Континентальный городской",
    avg_temperature: { summer: 35, winter: -1 }, annual_rainfall_mm: 440,
    main_crops: ["Urban Agriculture", "Greenhouses", "Vegetables"],
    main_crops_uz: ["Shahar dehqonchiligi", "Issiqxonalar", "Sabzavotlar"],
    main_crops_ru: ["Городское земледелие", "Теплицы", "Овощи"],
    soil_types: ["Urban", "Loamy"],
    soil_types_uz: ["Shahar", "Qumoq"],
    soil_types_ru: ["Городской", "Суглинок"],
    agricultural_area_hectares: 5000,
  },
];

export default function RegionsPage() {
  const t = useTranslations("regions");
  const locale = useLocale();
  const [selectedRegion, setSelectedRegion] = useState<typeof regionsData[0] | null>(null);

  useEffect(() => {
    const handleHashChange = () => {
      const hash = decodeURIComponent(window.location.hash.replace("#", ""));
      if (hash) {
        const match = regionsData.find((r) => r.id === hash);
        if (match) {
          setSelectedRegion(match);
        }
      }
    };

    handleHashChange();

    window.addEventListener("hashchange", handleHashChange);
    return () => window.removeEventListener("hashchange", handleHashChange);
  }, []);

  // Locale bo'yicha viloyat nomini qaytarish
  const getLocaleName = (r: typeof regionsData[0]) => {
    if (locale === "uz") return r.name_uz;
    if (locale === "ru") return r.name_ru;
    return r.name;
  };

  const getLocaleClimate = (r: typeof regionsData[0]) => {
    if (locale === "uz") return r.climate_uz;
    if (locale === "ru") return r.climate_ru;
    return r.climate;
  };

  const getLocaleCrops = (r: typeof regionsData[0]) => {
    if (locale === "uz") return r.main_crops_uz;
    if (locale === "ru") return r.main_crops_ru;
    return r.main_crops;
  };

  const getLocaleSoils = (r: typeof regionsData[0]) => {
    if (locale === "uz") return r.soil_types_uz;
    if (locale === "ru") return r.soil_types_ru;
    return r.soil_types;
  };

  const getLocaleCapital = (r: typeof regionsData[0]) => {
    if (locale === "uz") return r.capital_uz;
    if (locale === "ru") return r.capital_ru;
    return r.capital;
  };

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
                      <h3 className={`font-semibold text-sm ${selectedRegion?.id === region.id ? "text-[var(--color-primary)]" : ""}`}>{getLocaleName(region)}</h3>
                      <p className="text-xs text-[var(--color-text-muted)]">{getLocaleCrops(region).slice(0, 3).join(", ")}</p>
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
                      <h2 className="text-2xl font-bold font-[family-name:var(--font-display)] gradient-text">{getLocaleName(selectedRegion)}</h2>
                      <p className="text-sm text-[var(--color-text-muted)]">{t("labels.capital")}: {getLocaleCapital(selectedRegion)}</p>
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
                    <p className="text-sm text-[var(--color-text-secondary)]">{getLocaleClimate(selectedRegion)}</p>
                  </div>
                  <div className="mb-4">
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-2">{t("labels.soilTypes")}</p>
                    <div className="flex flex-wrap gap-2">
                      {getLocaleSoils(selectedRegion).map((soil) => (
                        <span key={soil} className="px-3 py-1 rounded-full text-xs bg-[var(--color-accent-blue)]/10 text-[var(--color-accent-blue)] border border-[var(--color-accent-blue)]/20">{soil}</span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider mb-2">{t("labels.mainCrops")}</p>
                    <div className="flex flex-wrap gap-2">
                      {getLocaleCrops(selectedRegion).map((crop) => (
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
