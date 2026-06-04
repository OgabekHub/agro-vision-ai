"use client";

import { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { Link, useRouter } from "@/i18n/routing";
import { motion } from "framer-motion";
import { UserPlus, Mail, Lock, User, ArrowRight, CheckCircle } from "lucide-react";
import GlassCard from "@/components/ui/GlassCard";
import { useTranslations } from "next-intl";

export default function RegisterPage() {
  const { register, user } = useAuth();
  const router = useRouter();
  const t = useTranslations("auth.register");

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");
  const [loading, setLoading] = useState(false);

  // If already logged in, redirect
  if (user) {
    router.replace(user.role === "admin" ? "/admin" : "/dashboard");
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg("");
    setSuccessMsg("");
    setLoading(true);

    try {
      const res = await register(email, password, fullName);
      if (res.success) {
        setSuccessMsg(t("successMsg"));
        setTimeout(() => {
          router.push("/login");
        }, 3000);
      }
    } catch (err: any) {
      console.error(err);
      setErrorMsg(err.message || t("errorMsg"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-[85vh] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 overflow-hidden bg-[var(--color-bg-dark)]">
      {/* Background glow effects */}
      <div className="absolute top-1/4 left-1/4 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full bg-[var(--color-primary)]/10 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 translate-x-1/2 translate-y-1/2 w-96 h-96 rounded-full bg-[var(--color-accent-cyan)]/10 blur-[120px] pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-md relative z-10"
      >
        <GlassCard className="p-8 border border-white/5 shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-[var(--color-primary)] to-transparent" />

          <div className="text-center mb-8">
            <div className="mx-auto w-12 h-12 rounded-xl bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent-cyan)] flex items-center justify-center shadow-[0_0_20px_rgba(0,255,136,0.15)] mb-4">
              <UserPlus className="w-6 h-6 text-[var(--color-bg-dark)]" />
            </div>
            <h2 className="text-2xl font-bold font-[family-name:var(--font-display)] text-white tracking-tight">
              {t("title")}
            </h2>
            <p className="text-sm text-[var(--color-text-secondary)] mt-2">
              {t("subtitle")}
            </p>
          </div>

          {errorMsg && (
            <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-xs leading-relaxed">
              ⚠️ {errorMsg}
            </div>
          )}

          {successMsg && (
            <div className="mb-6 p-4 rounded-xl bg-green-500/10 border border-green-500/20 text-green-400 text-xs leading-relaxed flex items-start gap-2.5">
              <CheckCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
              <span>{successMsg}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-xs font-semibold text-[var(--color-text-secondary)] uppercase tracking-wider mb-2">
                {t("fullNameLabel")}
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-white/40">
                  <User className="w-4 h-4" />
                </div>
                <input
                  type="text"
                  required
                  placeholder={t("fullNamePlaceholder")}
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="block w-full pl-10 pr-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-white/30 text-sm focus:outline-none focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-[var(--color-text-secondary)] uppercase tracking-wider mb-2">
                {t("emailLabel")}
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-white/40">
                  <Mail className="w-4 h-4" />
                </div>
                <input
                  type="email"
                  required
                  placeholder={t("emailPlaceholder")}
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="block w-full pl-10 pr-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-white/30 text-sm focus:outline-none focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-[var(--color-text-secondary)] uppercase tracking-wider mb-2">
                {t("passwordLabel")}
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-white/40">
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  type="password"
                  required
                  placeholder={t("passwordPlaceholder")}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full pl-10 pr-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-white/30 text-sm focus:outline-none focus:border-[var(--color-primary)] focus:ring-1 focus:ring-[var(--color-primary)] transition-all"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary py-3 rounded-xl text-sm font-semibold flex items-center justify-center gap-2 mt-2 shadow-[0_4px_20px_rgba(0,255,136,0.15)] disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span>{t("btnLoading")}</span>
              ) : (
                <>
                  <UserPlus className="w-4 h-4" />
                  <span>{t("btnSubmit")}</span>
                </>
              )}
            </button>
          </form>

          <div className="mt-8 pt-6 border-t border-white/5 text-center">
            <p className="text-xs text-[var(--color-text-secondary)]">
              {t("hasAccount")}{" "}
              <Link
                href="/login"
                className="text-[var(--color-primary)] hover:underline inline-flex items-center gap-0.5 font-medium ml-1"
              >
                {t("loginLink")} <ArrowRight className="w-3 h-3" />
              </Link>
            </p>
          </div>
        </GlassCard>
      </motion.div>
    </div>
  );
}
