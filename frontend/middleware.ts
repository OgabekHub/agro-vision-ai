import createMiddleware from "next-intl/middleware";
import { routing } from "./src/i18n/routing";
import { NextRequest, NextResponse } from "next/server";

const intlMiddleware = createMiddleware(routing);

export default function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Root "/" → "/uz" ga redirect
  if (pathname === "/") {
    return NextResponse.redirect(new URL("/uz", request.url));
  }

  return intlMiddleware(request);
}

export const config = {
  // Match all pathnames except Next.js internals and static files
  matcher: "/((?!_next|_vercel|.*\\..*).*)",
};
