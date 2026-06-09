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
        className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-sm font-medium transition-all border border-white/5 hover:border-[var(--color-border-glow)] hover:bg-[var(--color-primary-subtle)] text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] ${
          isPending ? "opacity-75 cursor-not-allowed" : ""
        }`}
        aria-label="Switch language"
        aria-expanded={isOpen}
      >
        {isPending ? (
          <div className="w-4 h-4 border-2 border-[var(--color-primary)] border-t-transparent rounded-full animate-spin" />
        ) : (
          <Globe className="w-4 h-4" />
        )}
        <span className="hidden sm:inline">{current.flag}</span>
        <span className="font-semibold">{current.shortLabel}</span>
        <motion.div
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
        >
          <ChevronDown className="w-3 h-3" />
        </motion.div>
      </button>

      {/* Dropdown */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -8, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -8, scale: 0.95 }}
            transition={{ duration: 0.15, ease: "easeOut" }}
            className="absolute right-0 top-full mt-2 w-44 glass rounded-xl border border-[var(--color-border-default)] overflow-hidden z-50"
            style={{
              boxShadow:
                "0 16px 48px rgba(0,0,0,0.4), 0 0 20px rgba(0,255,136,0.05)",
            }}
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
                  className={`w-full flex items-center justify-between gap-3 px-4 py-3 text-sm transition-all ${
                    isActive
                      ? "bg-[var(--color-primary-subtle)] text-[var(--color-primary)]"
                      : "text-[var(--color-text-secondary)] hover:bg-white/5 hover:text-[var(--color-text-primary)]"
                  } ${i !== 0 ? "border-t border-white/5" : ""}`}
                >
                  <div className="flex items-center gap-2.5">
                    <span className="text-lg leading-none">{l.flag}</span>
                    <div className="text-left">
                      <p className="font-medium leading-none">{l.label}</p>
                      <p className="text-[10px] text-[var(--color-text-muted)] mt-0.5 uppercase tracking-wider">
                        {l.shortLabel}
                      </p>
                    </div>
                  </div>
                  {isActive && (
                    <Check className="w-4 h-4 text-[var(--color-primary)] flex-shrink-0" />
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
