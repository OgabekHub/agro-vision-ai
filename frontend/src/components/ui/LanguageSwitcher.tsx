"use client";

import { useLocale } from "next-intl";
import { usePathname, useRouter } from "@/i18n/routing";
import { useState, useRef, useEffect, useTransition } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Globe, Check, ChevronDown } from "lucide-react";

const locales = [
  { code: "en", label: "English", flag: "🇬🇧", shortLabel: "EN" },
  { code: "uz", label: "O'zbek", flag: "🇺🇿", shortLabel: "UZ" },
  { code: "ru", label: "Русский", flag: "🇷🇺", shortLabel: "RU" },
] as const;

type LocaleCode = "en" | "uz" | "ru";

export default function LanguageSwitcher() {
  const locale = useLocale() as LocaleCode;
  const pathname = usePathname();
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [isPending, startTransition] = useTransition();
  const ref = useRef<HTMLDivElement>(null);

  const current = locales.find((l) => l.code === locale) ?? locales[0];

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const switchLocale = (newLocale: LocaleCode) => {
    setIsOpen(false);
    startTransition(() => {
      router.replace(pathname, { locale: newLocale });
    });
  };

  return (
    <div ref={ref} className="relative">
      {/* Trigger Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        disabled={isPending}
        className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold transition-all duration-300 bg-white/3 hover:bg-white/8 border border-white/5 hover:border-white/15 text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] shadow-sm backdrop-blur-md group ${
          isPending ? "opacity-75 cursor-not-allowed" : ""
        }`}
        aria-label="Switch language"
        aria-expanded={isOpen}
      >
        {isPending ? (
          <div className="w-3.5 h-3.5 border-2 border-[var(--color-primary)] border-t-transparent rounded-full animate-spin" />
        ) : (
          <Globe className="w-3.5 h-3.5 text-[var(--color-primary)]" />
        )}
        <span className="hidden sm:inline text-xs leading-none">{current.flag}</span>
        <span className="font-bold tracking-wider">{current.shortLabel}</span>
        <motion.div
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
          className="text-[var(--color-text-muted)] group-hover:text-[var(--color-text-secondary)]"
        >
          <ChevronDown className="w-3.5 h-3.5 text-[var(--color-text-muted)]" />
        </motion.div>
      </button>

      {/* Dropdown */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 8, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 8, scale: 0.95 }}
            transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
            className="absolute right-0 top-full mt-2 w-48 bg-[var(--color-bg-dark)]/90 backdrop-blur-xl rounded-2xl border border-white/10 p-1.5 space-y-1 z-50 shadow-[0_20px_50px_rgba(0,0,0,0.6)]"
          >
            {locales.map((l, i) => {
              const isActive = l.code === locale;
              return (
                <motion.button
                  key={l.code}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.05 }}
                  onClick={() => switchLocale(l.code)}
                  className={`w-full flex items-center justify-between gap-3 px-3 py-2.5 rounded-xl text-xs font-semibold transition-all border ${
                    isActive
                      ? "bg-[var(--color-primary-subtle)] text-[var(--color-primary)] border-[var(--color-border-glow)]"
                      : "text-[var(--color-text-secondary)] hover:bg-white/5 hover:text-white border-transparent"
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    <span className="text-base leading-none">{l.flag}</span>
                    <div className="text-left">
                      <p className="font-semibold leading-none">{l.label}</p>
                      <p className="text-[9px] text-[var(--color-text-muted)] mt-0.5 uppercase tracking-wider font-medium">
                        {l.shortLabel}
                      </p>
                    </div>
                  </div>
                  {isActive && (
                    <Check className="w-3.5 h-3.5 text-[var(--color-primary)] flex-shrink-0" />
                  )}
                </motion.button>
              );
            })}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
