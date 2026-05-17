// ===========================
// AgroVision AI — Utility Functions
// ===========================

import { SeverityLevel } from "@/types";

export function cn(...classes: (string | undefined | null | false)[]) {
  return classes.filter(Boolean).join(" ");
}

export function formatConfidence(confidence: number): string {
  return `${(confidence * 100).toFixed(1)}%`;
}

export function getConfidenceColor(confidence: number): string {
  if (confidence >= 0.8) return "var(--color-primary)";
  if (confidence >= 0.6) return "var(--color-accent-yellow)";
  return "var(--color-accent-red)";
}

export function getSeverityColor(severity: SeverityLevel): string {
  const colors: Record<SeverityLevel, string> = {
    low: "var(--color-severity-low)",
    medium: "var(--color-severity-medium)",
    high: "var(--color-severity-high)",
    critical: "var(--color-severity-critical)",
  };
  return colors[severity];
}

export function getSeverityLabel(severity: SeverityLevel): string {
  const labels: Record<SeverityLevel, string> = {
    low: "Low Risk",
    medium: "Medium Risk",
    high: "High Risk",
    critical: "Critical",
  };
  return labels[severity];
}

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + "...";
}

export function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function generateId(): string {
  return Math.random().toString(36).substring(2) + Date.now().toString(36);
}
