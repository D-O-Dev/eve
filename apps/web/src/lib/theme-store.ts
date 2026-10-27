"use client";

import { useSyncExternalStore } from "react";
import { DEFAULT_THEME, loadTheme, sanitize, saveTheme, type ThemeSettings } from "./theme";

const listeners = new Set<() => void>();
let current: ThemeSettings = DEFAULT_THEME;
let loaded = false;

function getSnapshot(): ThemeSettings {
  if (!loaded && typeof window !== "undefined") {
    current = loadTheme();
    loaded = true;
  }
  return current;
}

function getServerSnapshot(): ThemeSettings {
  return DEFAULT_THEME;
}

function subscribe(callback: () => void) {
  listeners.add(callback);
  return () => listeners.delete(callback);
}

function setTheme(next: ThemeSettings) {
  current = next;
  loaded = true;
  saveTheme(next);
  listeners.forEach((listener) => listener());
}

export function useTheme() {
  const theme = useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot);
  return {
    theme,
    update: (patch: Partial<ThemeSettings>) => setTheme(sanitize({ ...getSnapshot(), ...patch })),
    reset: () => setTheme(DEFAULT_THEME),
  };
}