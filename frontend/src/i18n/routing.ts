import { defineRouting } from "next-intl/routing";
import { createNavigation } from "next-intl/navigation";

export const routing = defineRouting({
  locales: ["uz", "en", "ru"],
  defaultLocale: "uz",
  localePrefix: "always",
});

export type Locale = (typeof routing.locales)[number];

// Locale-aware navigation helpers
// Use these instead of next/link and next/navigation throughout the app
export const { Link, redirect, usePathname, useRouter } =
  createNavigation(routing);
