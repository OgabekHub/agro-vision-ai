"use client";

import { Link } from "@/i18n/routing";
import { useTranslations } from "next-intl";
import {
  Zap,
  Github,
  Twitter,
  Linkedin,
  Mail,
  MapPin,
  Leaf,
  Bug,
  Mountain,
} from "lucide-react";

export default function Footer() {
  const t = useTranslations("footer");
  const tc = useTranslations("common");

  return (
    <footer className="relative border-t border-white/5 bg-[var(--color-bg-deeper)]">
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-1/2 h-px bg-gradient-to-r from-transparent via-[var(--color-primary)] to-transparent opacity-30" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
          {/* Brand */}
          <div className="lg:col-span-1">
            <Link href="/" className="flex items-center gap-2.5 mb-4">
              <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent-cyan)] flex items-center justify-center">
                <Zap className="w-5 h-5 text-[var(--color-bg-dark)]" />
              </div>
              <div className="flex flex-col">
                <span className="text-lg font-bold tracking-tight font-[family-name:var(--font-display)]">
                  Agro<span className="text-[var(--color-primary)]">Vision</span>
                </span>
                <span className="text-[10px] uppercase tracking-[0.2em] text-[var(--color-text-muted)] -mt-1">
                  {tc("aiPlatform")}
                </span>
              </div>
            </Link>
            <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed mb-6 max-w-xs">
              {t("description")}
            </p>
            <div className="flex items-center gap-3">
              {[Github, Twitter, Linkedin, Mail].map((Icon, i) => (
                <a
                  key={i}
                  href="#"
                  className="w-9 h-9 rounded-lg border border-white/5 flex items-center justify-center text-[var(--color-text-muted)] hover:text-[var(--color-primary)] hover:border-[var(--color-border-glow)] hover:bg-[var(--color-primary-subtle)] transition-all duration-200"
                >
                  <Icon className="w-4 h-4" />
                </a>
              ))}
            </div>
          </div>

          {/* Platform Links */}
          <div>
            <h4 className="text-sm font-semibold text-[var(--color-text-primary)] mb-4 uppercase tracking-wider">
              {t("platform")}
            </h4>
            <ul className="space-y-2.5">
              {[
                { label: t("links.plantDetection"), href: "/dashboard", Icon: Leaf },
                { label: t("links.diseaseAnalysis"), href: "/disease-analysis", Icon: Bug },
                { label: t("links.landAnalysis"), href: "/land-analysis", Icon: Mountain },
                { label: t("links.regionMap"), href: "/regions", Icon: MapPin },
              ].map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href as "/dashboard" | "/disease-analysis" | "/land-analysis" | "/regions"}
                    className="text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] transition-colors flex items-center gap-2"
                  >
                    <link.Icon className="w-3.5 h-3.5" />
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="text-sm font-semibold text-[var(--color-text-primary)] mb-4 uppercase tracking-wider">
              {t("resources")}
            </h4>
            <ul className="space-y-2.5">
              {[
                t("documentation"),
                t("apiReference"),
                t("modelAccuracy"),
                t("dataSources"),
              ].map((label) => (
                <li key={label}>
                  <a
                    href="#"
                    className="text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] transition-colors"
                  >
                    {label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h4 className="text-sm font-semibold text-[var(--color-text-primary)] mb-4 uppercase tracking-wider">
              {t("company")}
            </h4>
            <ul className="space-y-2.5">
              {[t("about"), t("contact"), t("privacy"), t("terms")].map(
                (label) => (
                  <li key={label}>
                    <a
                      href="#"
                      className="text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-primary)] transition-colors"
                    >
                      {label}
                    </a>
                  </li>
                )
              )}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-[var(--color-text-muted)]">
            © {new Date().getFullYear()} {t("copyright")}
          </p>
          <div className="flex items-center gap-2 text-xs text-[var(--color-text-muted)]">
            <span className="w-2 h-2 rounded-full bg-[var(--color-primary)] animate-pulse" />
            {tc("operational")}
          </div>
        </div>
      </div>
    </footer>
  );
}
