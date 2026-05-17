"use client";

import { useState, useEffect } from "react";
import { usePathname } from "@/i18n/routing";
import { Link } from "@/i18n/routing";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslations } from "next-intl";
import {
  Leaf,
  LayoutDashboard,
  Bug,
  Mountain,
  MapPin,
  Shield,
  Menu,
  X,
  Zap,
  Send,
} from "lucide-react";

import LanguageSwitcher from "@/components/ui/LanguageSwitcher";

export default function Navbar() {
  const t = useTranslations("nav");
  const pathname = usePathname();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileOpen, setIsMobileOpen] = useState(false);

  const navLinks = [
    { href: "/" as const, label: t("home"), icon: Leaf },
    { href: "/dashboard" as const, label: t("dashboard"), icon: LayoutDashboard },
    { href: "/disease-analysis" as const, label: t("diseaseAnalysis"), icon: Bug },
    { href: "/land-analysis" as const, label: t("landAnalysis"), icon: Mountain },
    { href: "/regions" as const, label: t("regions"), icon: MapPin },
    { href: "/admin" as const, label: t("admin"), icon: Shield },
  ];

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    setIsMobileOpen(false);
  }, [pathname]);

  return (
    <>
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.6, ease: [0.4, 0, 0.2, 1] }}
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          isScrolled ? "glass border-b border-white/5" : "bg-transparent"
        }`}
        style={
          isScrolled
            ? {
                borderRadius: 0,
                backdropFilter: "blur(20px) saturate(150%)",
                background: "rgba(5, 10, 24, 0.85)",
              }
            : {}
        }
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link href="/" className="flex items-center gap-2 group flex-shrink-0">
              <div className="relative">
                <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent-cyan)] flex items-center justify-center group-hover:shadow-[0_0_20px_rgba(0,255,136,0.3)] transition-shadow duration-300">
                  <Zap className="w-5 h-5 text-[var(--color-bg-dark)]" />
                </div>
                <div className="absolute -inset-1 rounded-lg bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent-cyan)] opacity-0 group-hover:opacity-20 blur-md transition-opacity duration-300" />
              </div>
              <div className="flex flex-col">
                <span className="text-base font-bold tracking-tight font-[family-name:var(--font-display)] leading-tight">
                  Agro<span className="text-[var(--color-primary)]">Vision</span>
                </span>
                <span className="text-[9px] uppercase tracking-[0.15em] text-[var(--color-text-muted)]">
                  AI Platform
                </span>
              </div>
            </Link>

            {/* Desktop Nav — always single row */}
            <div className="hidden lg:flex items-center gap-0.5 min-w-0">
              {navLinks.map((link) => {
                const isActive = pathname === link.href;
                const Icon = link.icon;
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    title={link.label}
                    className={`relative flex items-center gap-1.5 px-2.5 py-2 rounded-lg text-xs font-medium transition-all duration-200 whitespace-nowrap flex-shrink-0 ${
                      isActive
                        ? "text-[var(--color-primary)]"
                        : "text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-white/5"
                    }`}
                  >
                    <Icon className="w-3.5 h-3.5 flex-shrink-0" />
                    <span className="hidden xl:inline">{link.label}</span>
                    {isActive && (
                      <motion.div
                        layoutId="navbar-indicator"
                        className="absolute inset-0 rounded-lg border border-[var(--color-border-glow)] bg-[var(--color-primary-subtle)]"
                        style={{ zIndex: -1 }}
                        transition={{ type: "spring", stiffness: 350, damping: 30 }}
                      />
                    )}
                  </Link>
                );
              })}
            </div>

            {/* Right side: Language Switcher + Telegram + CTA */}
            <div className="hidden lg:flex items-center gap-2 flex-shrink-0">
              <LanguageSwitcher />
              {/* Telegram Bot tugmasi */}
              <a
                href="https://t.me/agro_visionai_bot"
                target="_blank"
                rel="noopener noreferrer"
                title="Telegram Bot"
                className="flex items-center gap-1.5 px-2.5 py-2 rounded-lg text-xs font-medium whitespace-nowrap text-[var(--color-text-secondary)] hover:text-[#29B6F6] hover:bg-[#29B6F6]/10 transition-all duration-200 border border-transparent hover:border-[#29B6F6]/20"
              >
                <Send className="w-3.5 h-3.5 flex-shrink-0" />
                <span className="hidden xl:inline">Telegram</span>
              </a>
              <Link
                href="/dashboard"
                className="btn-primary text-xs py-2 px-3 whitespace-nowrap xl:text-sm xl:py-2.5 xl:px-5"
              >
                <Zap className="w-4 h-4 flex-shrink-0" />
                <span className="hidden xl:inline">{t("startAnalysis")}</span>
              </Link>
            </div>

            {/* Mobile Toggle */}
            <div className="lg:hidden flex items-center gap-2">
              <LanguageSwitcher />
              <button
                onClick={() => setIsMobileOpen(!isMobileOpen)}
                className="p-2 rounded-lg hover:bg-white/5 transition-colors"
                aria-label="Toggle menu"
              >
                {isMobileOpen ? (
                  <X className="w-5 h-5" />
                ) : (
                  <Menu className="w-5 h-5" />
                )}
              </button>
            </div>
          </div>
        </div>
      </motion.nav>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMobileOpen && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 z-40 lg:hidden"
          >
            <div
              className="absolute inset-0 bg-black/60 backdrop-blur-sm"
              onClick={() => setIsMobileOpen(false)}
            />
            <motion.div
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", damping: 25, stiffness: 200 }}
              className="absolute right-0 top-0 bottom-0 w-72 bg-[var(--color-bg-deeper)] border-l border-white/5 p-6 pt-20"
            >
              <div className="flex flex-col gap-2">
                {navLinks.map((link) => {
                  const isActive = pathname === link.href;
                  const Icon = link.icon;
                  return (
                    <Link
                      key={link.href}
                      href={link.href}
                      className={`flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                        isActive
                          ? "text-[var(--color-primary)] bg-[var(--color-primary-subtle)] border border-[var(--color-border-glow)]"
                          : "text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-white/5"
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      {link.label}
                    </Link>
                  );
                })}
              </div>
              <div className="mt-6 pt-6 border-t border-white/5 flex flex-col gap-3">
                <Link href="/dashboard" className="btn-primary w-full text-sm py-3" onClick={() => setIsMobileOpen(false)}>
                  <Zap className="w-4 h-4" />
                  {t("startAnalysis")}
                </Link>
                <a
                  href="https://t.me/agro_visionai_bot"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center justify-center gap-2 w-full py-3 px-4 rounded-xl text-sm font-medium border border-[#29B6F6]/30 text-[#29B6F6] bg-[#29B6F6]/10 hover:bg-[#29B6F6]/20 transition-all"
                >
                  <Send className="w-4 h-4" />
                  Telegram Bot
                </a>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Spacer */}
      <div className="h-16" />
    </>
  );
}
