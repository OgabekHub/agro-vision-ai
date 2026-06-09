"use client";

import { motion, type Variants } from "framer-motion";
import { Link } from "@/i18n/routing";
import { useTranslations } from "next-intl";
import { Zap, ArrowRight, Leaf, Bug, Mountain, MapPin, BarChart3, Shield, Sparkles, ChevronRight, Cpu } from "lucide-react";
import GlassCard from "@/components/ui/GlassCard";

import HologramMap from "@/components/ui/HologramMap";
import HologramPlant from "@/components/ui/HologramPlant";

const fadeUp: Variants = {
  initial: { opacity: 0, y: 30 },
  animate: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.7, ease: [0.4, 0, 0.2, 1] as [number, number, number, number] },
  },
};
const stagger: Variants = { animate: { transition: { staggerChildren: 0.1 } } };

export default function LandingPage() {
  const t = useTranslations("landing");

  const features = [
    { icon: Leaf, key: "plantDetection", color: "#00FF88", href: "/dashboard" as const },
    { icon: Bug, key: "diseaseAnalysis", color: "#F59E0B", href: "/disease-analysis" as const },
    { icon: Mountain, key: "landAnalysis", color: "#3B82F6", href: "/land-analysis" as const },
    { icon: MapPin, key: "regionIntelligence", color: "#8B5CF6", href: "/regions" as const },
    { icon: BarChart3, key: "smartRecommendations", color: "#06B6D4", href: "/dashboard" as const },
    { icon: Shield, key: "adminDashboard", color: "#EF4444", href: "/admin" as const },
  ] as const;

  const stats = [
    { value: "14", labelKey: "regions" as const },
    { value: "200+", labelKey: "plants" as const },
    { value: "50+", labelKey: "diseases" as const },
    { value: "95%", labelKey: "accuracy" as const },
  ];

  return (
    <div className="relative">
      {/* Background */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="orb orb-green w-96 h-96 -top-48 -right-48" style={{ animation: "float 15s ease-in-out infinite" }} />
        <div className="orb orb-blue w-80 h-80 top-1/3 -left-40" style={{ animation: "float 20s ease-in-out infinite reverse" }} />
        <div className="orb orb-purple w-72 h-72 bottom-1/4 right-1/4" style={{ animation: "float 18s ease-in-out infinite" }} />
        <div className="grid-pattern absolute inset-0 opacity-40" />
      </div>

      {/* HERO */}
      <section className="relative min-h-[80vh] lg:min-h-[85vh] flex items-center justify-center px-4 overflow-hidden pt-12 lg:pt-0">
        <div className="w-full max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between gap-6 relative z-20">
          
          {/* Left Hologram Map */}
          <div className="hidden lg:block w-[180px] xl:w-[240px] 2xl:w-[300px] flex-shrink-0">
            <HologramMap />
          </div>

          {/* Center Hero Text Content */}
          <div className="flex-grow max-w-xl xl:max-w-2xl 2xl:max-w-3xl text-center pointer-events-auto">
            <motion.div {...stagger} initial="initial" animate="animate" className="space-y-8">
              <motion.div {...fadeUp} className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-[var(--color-border-glow)] text-sm">
                <Sparkles className="w-4 h-4 text-[var(--color-primary)]" />
                <span className="text-[var(--color-text-secondary)]">{t("badge")}</span>
                <span className="text-[var(--color-primary)] font-semibold">{t("badgeModel")}</span>
              </motion.div>

              <motion.h1 {...fadeUp} transition={{ delay: 0.1, duration: 0.8 }} className="text-[42px] sm:text-[56px] lg:text-6xl xl:text-7xl 2xl:text-8xl font-bold font-[family-name:var(--font-display)] leading-[1.05] tracking-tight">
                <span className="text-[var(--color-text-primary)]">{t("headline1")}</span>
                <br />
                <span className="gradient-text">{t("headline2")}</span>
                <br />
                <span className="text-[var(--color-text-primary)]">{t("headline3")}</span>
              </motion.h1>
            
              <motion.p {...fadeUp} transition={{ delay: 0.2 }} className="text-lg sm:text-xl text-[var(--color-text-secondary)] max-w-xl mx-auto leading-relaxed">
                {t("subtitle")}
              </motion.p>

              <motion.div {...fadeUp} transition={{ delay: 0.3 }} className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <Link href="/dashboard" className="btn-primary text-base px-8 py-4 rounded-xl">
                  <Zap className="w-5 h-5" />
                  {t("ctaPrimary")}
                  <ArrowRight className="w-4 h-4" />
                </Link>
                <Link href="/regions" className="btn-secondary text-base px-8 py-4 rounded-xl">
                  <MapPin className="w-5 h-5" />
                  {t("ctaSecondary")}
                </Link>
              </motion.div>

              <motion.div {...fadeUp} transition={{ delay: 0.4 }} className="flex flex-wrap items-center justify-center gap-8 sm:gap-12 pt-8">
                {stats.map((stat) => (
                  <div key={stat.labelKey} className="text-center">
                    <div className="text-3xl sm:text-4xl font-bold gradient-text font-[family-name:var(--font-display)]">{stat.value}</div>
                    <div className="text-xs sm:text-sm text-[var(--color-text-muted)] mt-1">{t(`stats.${stat.labelKey}`)}</div>
                  </div>
                ))}
              </motion.div>
            </motion.div>
          </div>

          {/* Right Hologram Plant */}
          <div className="hidden lg:block w-[180px] xl:w-[240px] 2xl:w-[300px] flex-shrink-0">
            <HologramPlant />
          </div>
        </div>
      </section>

      {/* FEATURES */}
      <section className="relative py-24 px-4" id="features">
        <div className="max-w-7xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-center mb-16">
            <span className="text-sm font-semibold text-[var(--color-primary)] uppercase tracking-widest">Features</span>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-[family-name:var(--font-display)] mt-3 mb-4">
              {t("features.title")} <span className="gradient-text">{t("features.titleHighlight")}</span>
            </h2>
            <p className="text-[var(--color-text-secondary)] max-w-xl mx-auto">{t("features.subtitle")}</p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, i) => (
              <motion.div key={feature.key} initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.08 }}>
                <Link href={feature.href}>
                  <GlassCard hover padding="lg" className="h-full group cursor-pointer">
                    <div className="w-12 h-12 rounded-xl flex items-center justify-center mb-4" style={{ backgroundColor: `${feature.color}15` }}>
                      <feature.icon className="w-6 h-6" style={{ color: feature.color }} />
                    </div>
                    <h3 className="text-lg font-bold mb-2 group-hover:text-[var(--color-primary)] transition-colors">
                      {t(`features.${feature.key}.title`)}
                    </h3>
                    <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed mb-4">
                      {t(`features.${feature.key}.desc`)}
                    </p>
                    <div className="flex items-center gap-1 text-sm text-[var(--color-primary)] font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                      {t("features.learnMore")} <ChevronRight className="w-4 h-4" />
                    </div>
                  </GlassCard>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="relative py-24 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-center mb-16">
            <span className="text-sm font-semibold text-[var(--color-accent-purple)] uppercase tracking-widest">{t("howItWorks.tag")}</span>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-[family-name:var(--font-display)] mt-3">
              {t("howItWorks.title")} <span className="gradient-text">{t("howItWorks.titleHighlight")}</span>
            </h2>
          </motion.div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {(["upload", "processing", "results"] as const).map((step, i) => (
              <motion.div key={step} initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.15 }}>
                <GlassCard glow glowColor={i === 0 ? "green" : i === 1 ? "purple" : "cyan"} padding="lg" className="text-center relative overflow-hidden h-full">
                  <div className="absolute top-4 right-4 text-6xl font-bold text-white/3 font-[family-name:var(--font-display)]">{t(`howItWorks.steps.${step}.step`)}</div>
                  <div className="text-5xl mb-4">{["📸", "🧠", "📊"][i]}</div>
                  <h3 className="text-xl font-bold mb-3 font-[family-name:var(--font-display)]">{t(`howItWorks.steps.${step}.title`)}</h3>
                  <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">{t(`howItWorks.steps.${step}.desc`)}</p>
                </GlassCard>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="relative py-24 px-4">
        <div className="max-w-4xl mx-auto">
          <motion.div initial={{ opacity: 0, scale: 0.95 }} whileInView={{ opacity: 1, scale: 1 }} viewport={{ once: true }}>
            <GlassCard glow glowColor="green" padding="xl" className="text-center relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-[var(--color-primary-subtle)] to-transparent opacity-50" />
              <div className="relative z-10">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent-cyan)] flex items-center justify-center mx-auto mb-6 shadow-[0_0_40px_rgba(0,255,136,0.3)]">
                  <Cpu className="w-8 h-8 text-[var(--color-bg-dark)]" />
                </div>
                <h2 className="text-3xl sm:text-4xl font-bold font-[family-name:var(--font-display)] mb-4">
                  {t("cta.title")} <span className="gradient-text">{t("cta.titleHighlight")}</span>
                </h2>
                <p className="text-[var(--color-text-secondary)] max-w-lg mx-auto mb-8">{t("cta.subtitle")}</p>
                <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                  <Link href="/dashboard" className="btn-primary text-base px-8 py-4 rounded-xl">
                    <Zap className="w-5 h-5" />
                    {t("cta.btnLaunch")}
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                  <Link href="/disease-analysis" className="btn-secondary text-base px-8 py-4 rounded-xl">
                    <Bug className="w-5 h-5" />
                    {t("cta.btnDisease")}
                  </Link>
                </div>
              </div>
            </GlassCard>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
