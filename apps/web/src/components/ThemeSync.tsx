"use client";

import { useEffect } from "react";
import { applyTheme } from "@/lib/theme";
import { useTheme } from "@/lib/theme-store";

export function ThemeSync() {
  const { theme } = useTheme();

  useEffect(() => {
    applyTheme(theme);
    if (theme.mode !== "auto") return;
    const query = window.matchMedia("(prefers-color-scheme: light)");
    const onChange = () => applyTheme(theme);
    query.addEventListener("change", onChange);
    return () => query.removeEventListener("change", onChange);
  }, [theme]);

  return null;
}