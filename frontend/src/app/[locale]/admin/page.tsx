"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useTranslations } from "next-intl";
import { Shield, BarChart3, Image, Users, FileText, Activity, Leaf, Bug, Mountain, Eye, Trash2, Search } from "lucide-react";
import GlassCard from "@/components/ui/GlassCard";
import { api } from "@/lib/api";

const logs = [
  { id: "1", type: "plant" as const, result: "Cotton detected", confidence: 0.946, time: "2 min ago", processing: 234, model: "YOLOv8n" },
  { id: "2", type: "disease" as const, result: "Early Blight found", confidence: 0.891, time: "15 min ago", processing: 456, model: "EfficientNet-B0" },
  { id: "3", type: "plant" as const, result: "Wheat detected", confidence: 0.912, time: "1h ago", processing: 198, model: "YOLOv8n" },
  { id: "4", type: "land" as const, result: "Loamy soil analyzed", confidence: 0.873, time: "3h ago", processing: 521, model: "OpenCV+ML" },
  { id: "5", type: "disease" as const, result: "Powdery Mildew", confidence: 0.834, time: "5h ago", processing: 389, model: "EfficientNet-B0" },
  { id: "6", type: "plant" as const, result: "Grape vine detected", confidence: 0.967, time: "6h ago", processing: 167, model: "YOLOv8n" },
];

const users = [
  { id: "1", name: "Abdulaziz Karimov", email: "abdulaziz@mail.uz", role: "admin", analyses: 156, joined: "2025-01-15" },
  { id: "2", name: "Nilufar Rashidova", email: "nilufar@mail.uz", role: "user", analyses: 89, joined: "2025-03-22" },
  { id: "3", name: "Sardor Alimov", email: "sardor@mail.uz", role: "user", analyses: 234, joined: "2025-02-10" },
  { id: "4", name: "Gulnora Yusupova", email: "gulnora@mail.uz", role: "user", analyses: 67, joined: "2025-04-05" },
];

type Tab = "overview" | "logs" | "images" | "users";
const typeIcons = { plant: Leaf, disease: Bug, land: Mountain };
const typeColors = { plant: "#00FF88", disease: "#F59E0B", land: "#3B82F6" };

export default function AdminPage() {
  const t = useTranslations("admin");
  const [activeTab, setActiveTab] = useState<Tab>("overview");
  const [searchQuery, setSearchQuery] = useState("");

  const [stats, setStats] = useState<any>(null);
  const [logsList, setLogsList] = useState<any[]>([]);
  const [usersList, setUsersList] = useState<any[]>([]);

  useEffect(() => {
    async function loadData() {
      try {
        const [statsRes, logsRes, usersRes] = await Promise.all([
          api.getAdminStats().catch(() => null),
          api.getAdminLogs(1, 50).catch(() => null),
          api.getAdminUsers(1, 50).catch(() => null),
        ]);

        if (statsRes?.success && statsRes.data) {
          setStats(statsRes.data);
        }
        if (logsRes?.success && logsRes.data) {
          setLogsList(logsRes.data);
        }
        if (usersRes?.success && usersRes.data) {
          setUsersList(usersRes.data);
        }
      } catch (err) {
        console.error("Admin data load error", err);
      }
    }
    loadData();
  }, []);

  const tabs: { id: Tab; icon: typeof Shield }[] = [
    { id: "overview", icon: BarChart3 },
    { id: "logs", icon: FileText },
    { id: "images", icon: Image },
    { id: "users", icon: Users },
  ];

  const statsData = [
    { labelKey: "totalAnalyses" as const, value: "0", change: "0%", icon: BarChart3, color: "#00FF88" },
    { labelKey: "imagesUploaded" as const, value: "0", change: "0%", icon: Image, color: "#3B82F6" },
    { labelKey: "activeUsers" as const, value: "0", change: "0%", icon: Users, color: "#8B5CF6" },
    { labelKey: "aiAccuracy" as const, value: "0%", change: "0%", icon: Activity, color: "#06B6D4" },
  ];

  const displayStats = stats ? [
    { labelKey: "totalAnalyses" as const, value: stats.total_analyses.toLocaleString(), change: `+${stats.analyses_this_week || 0} this wk`, icon: BarChart3, color: "#00FF88" },
    { labelKey: "imagesUploaded" as const, value: stats.images_uploaded.toLocaleString(), change: `+${stats.analyses_today || 0} today`, icon: Image, color: "#3B82F6" },
    { labelKey: "activeUsers" as const, value: stats.active_users.toLocaleString(), change: "Active", icon: Users, color: "#8B5CF6" },
    { labelKey: "aiAccuracy" as const, value: `${stats.ai_accuracy}%`, change: "Target: 95%", icon: Activity, color: "#06B6D4" },
  ] : statsData;

  const displayLogs = logsList.length > 0 ? logsList : logs;

  const displayUsers = usersList.length > 0 ? usersList.map(u => ({
    id: u.id,
    name: u.full_name || "Foydalanuvchi",
    email: u.email || "",
    role: u.role || "user",
    analyses: u.analyses_count || 0,
    joined: u.created_at ? u.created_at.split("T")[0] : "2026-05-20",
  })) : users;

  return (
    <div className="relative min-h-screen">
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="grid-pattern absolute inset-0 opacity-20" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--color-accent-red)] to-[var(--color-accent-yellow)] flex items-center justify-center">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold font-[family-name:var(--font-display)]">{t("title")}</h1>
              <p className="text-sm text-[var(--color-text-muted)]">{t("subtitle")}</p>
            </div>
          </div>
        </motion.div>

        {/* Tabs */}
        <div className="flex gap-2 mb-8 overflow-x-auto pb-2">
          {tabs.map((tab) => (
            <button key={tab.id} onClick={() => setActiveTab(tab.id)} className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all whitespace-nowrap ${activeTab === tab.id ? "bg-[var(--color-primary-subtle)] text-[var(--color-primary)] border border-[var(--color-border-glow)]" : "text-[var(--color-text-secondary)] hover:bg-white/5 border border-transparent"}`}>
              <tab.icon className="w-4 h-4" />
              {t(`tabs.${tab.id}`)}
            </button>
          ))}
        </div>

        {/* Overview */}
        {activeTab === "overview" && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {displayStats.map((stat, i) => (
                <motion.div key={stat.labelKey} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}>
                  <GlassCard hover padding="md">
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="text-xs text-[var(--color-text-muted)] mb-1">{t(`stats.${stat.labelKey}`)}</p>
                        <p className="text-2xl font-bold font-[family-name:var(--font-display)]">{stat.value}</p>
                        <p className="text-xs font-medium mt-1" style={{ color: stat.color }}>{stat.change}</p>
                      </div>
                      <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ backgroundColor: `${stat.color}15` }}>
                        <stat.icon className="w-5 h-5" style={{ color: stat.color }} />
                      </div>
                    </div>
                  </GlassCard>
                </motion.div>
              ))}
            </div>
            <GlassCard padding="lg">
              <h3 className="font-bold mb-4">{t("recentActivity")}</h3>
              <div className="space-y-3">
                {displayLogs.slice(0, 5).map((log) => {
                  const logType = log.type || log.analysis_type || "plant";
                  const Icon = typeIcons[logType as "plant" | "disease" | "land"] || Leaf;
                  const logColor = typeColors[logType as "plant" | "disease" | "land"] || "#00FF88";
                  const model = log.model || log.model_version || "YOLOv8";
                  const processing = log.processing || log.processing_time_ms || 250;
                  const time = log.time || (log.created_at ? new Date(log.created_at).toLocaleTimeString() : "Just now");
                  return (
                    <div key={log.id} className="flex items-center justify-between py-2 border-b border-white/5 last:border-0">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: `${logColor}15` }}>
                          <Icon className="w-4 h-4" style={{ color: logColor }} />
                        </div>
                        <div>
                          <p className="text-sm font-medium">{log.result}</p>
                          <p className="text-xs text-[var(--color-text-muted)]">{model} • {processing}ms • {time}</p>
                        </div>
                      </div>
                      <span className="text-xs font-bold" style={{ color: log.confidence > 0.9 ? "#00FF88" : "#F59E0B" }}>
                        {(log.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                  );
                })}
              </div>
            </GlassCard>
          </motion.div>
        )}

        {/* Logs */}
        {activeTab === "logs" && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <GlassCard padding="lg">
              <div className="flex items-center justify-between mb-6">
                <h3 className="font-bold">{t("tabs.logs")}</h3>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--color-text-muted)]" />
                  <input type="text" placeholder={t("searchLogs")} value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} className="pl-9 pr-4 py-2 rounded-lg bg-white/5 border border-white/10 text-sm focus:outline-none focus:border-[var(--color-border-glow)] transition-colors w-48" />
                </div>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-white/5">
                      {(["type", "result", "confidence", "model", "time", "speed", "actions"] as const).map((col) => (
                        <th key={col} className={`py-3 px-2 text-xs text-[var(--color-text-muted)] uppercase tracking-wider ${col === "actions" ? "text-right" : "text-left"}`}>
                          {t(`columns.${col}`)}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {displayLogs.filter(l => (l.result || "").toLowerCase().includes(searchQuery.toLowerCase())).map((log) => {
                      const logType = log.type || log.analysis_type || "plant";
                      const Icon = typeIcons[logType as "plant" | "disease" | "land"] || Leaf;
                      const logColor = typeColors[logType as "plant" | "disease" | "land"] || "#00FF88";
                      const model = log.model || log.model_version || "YOLOv8";
                      const processing = log.processing || log.processing_time_ms || 250;
                      const time = log.time || (log.created_at ? new Date(log.created_at).toLocaleDateString() : "Just now");
                      return (
                        <tr key={log.id} className="border-b border-white/3 hover:bg-white/3 transition-colors">
                          <td className="py-3 px-2"><div className="flex items-center gap-2"><Icon className="w-4 h-4" style={{ color: logColor }} /><span className="capitalize text-xs">{logType}</span></div></td>
                          <td className="py-3 px-2 font-medium">{log.result}</td>
                          <td className="py-3 px-2"><span style={{ color: log.confidence > 0.9 ? "#00FF88" : "#F59E0B" }}>{(log.confidence * 100).toFixed(1)}%</span></td>
                          <td className="py-3 px-2 text-[var(--color-text-muted)]">{model}</td>
                          <td className="py-3 px-2 text-[var(--color-text-muted)]">{time}</td>
                          <td className="py-3 px-2 text-[var(--color-text-muted)]">{processing}ms</td>
                          <td className="py-3 px-2 text-right"><div className="flex items-center justify-end gap-1"><button className="p-1.5 rounded-lg hover:bg-white/5"><Eye className="w-3.5 h-3.5" /></button><button className="p-1.5 rounded-lg hover:bg-white/5 text-[var(--color-accent-red)]"><Trash2 className="w-3.5 h-3.5" /></button></div></td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </GlassCard>
          </motion.div>
        )}

        {/* Images */}
        {activeTab === "images" && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <GlassCard padding="lg">
              <h3 className="font-bold mb-6">{t("uploadedImages")}</h3>
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
                {displayLogs.map((log, i) => {
                  const logType = log.type || log.analysis_type || "plant";
                  const Icon = typeIcons[logType as "plant" | "disease" | "land"] || Leaf;
                  const logColor = typeColors[logType as "plant" | "disease" | "land"] || "#00FF88";
                  const time = log.time || (log.created_at ? new Date(log.created_at).toLocaleDateString() : "Just now");
                  return (
                    <motion.div key={log.id} initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: i * 0.05 }} className="group relative aspect-square rounded-xl bg-gradient-to-br from-white/5 to-white/2 border border-white/5 overflow-hidden hover:border-[var(--color-border-glow)] transition-all cursor-pointer">
                      <div className="absolute inset-0 flex items-center justify-center"><Icon className="w-10 h-10 opacity-20" style={{ color: logColor }} /></div>
                      <div className="absolute bottom-0 left-0 right-0 p-3 bg-gradient-to-t from-black/60 to-transparent">
                        <p className="text-xs font-medium truncate">{log.result}</p>
                        <p className="text-[10px] text-[var(--color-text-muted)]">{time}</p>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </GlassCard>
          </motion.div>
        )}

        {/* Users */}
        {activeTab === "users" && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <GlassCard padding="lg">
              <h3 className="font-bold mb-6">{t("registeredUsers")}</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-white/5">
                      {(["name", "email", "role", "analyses", "joined"] as const).map((col) => (
                        <th key={col} className="text-left py-3 px-2 text-xs text-[var(--color-text-muted)] uppercase tracking-wider">{t(`columns.${col}`)}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {displayUsers.map((user) => (
                      <tr key={user.id} className="border-b border-white/3 hover:bg-white/3 transition-colors">
                        <td className="py-3 px-2">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-accent-cyan)] flex items-center justify-center text-xs font-bold text-[var(--color-bg-dark)]">
                              {user.name.split(" ").map((n: string) => n[0]).join("")}
                            </div>
                            <span className="font-medium">{user.name}</span>
                          </div>
                        </td>
                        <td className="py-3 px-2 text-[var(--color-text-muted)]">{user.email}</td>
                        <td className="py-3 px-2">
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase ${user.role === "admin" ? "bg-[var(--color-accent-red)]/10 text-[var(--color-accent-red)] border border-[var(--color-accent-red)]/20" : "bg-white/5 text-[var(--color-text-secondary)] border border-white/10"}`}>{user.role}</span>
                        </td>
                        <td className="py-3 px-2">{user.analyses}</td>
                        <td className="py-3 px-2 text-[var(--color-text-muted)]">{user.joined}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </GlassCard>
          </motion.div>
        )}
      </div>
    </div>
  );
}
