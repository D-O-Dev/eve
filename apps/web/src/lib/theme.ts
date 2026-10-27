export type Mode = "auto" | "dark" | "light";

export interface ThemeSettings {
  mode: Mode;
  accent: string; // « #rrggbb »
  blur: number; // 8 à 40 px
  animations: boolean;
}

export const DEFAULT_THEME: ThemeSettings = { mode: "auto", accent: "#D9B25A", blur: 22, animations: true };

export const ACCENTS = [
  { id: "or", value: "#D9B25A" },
  { id: "emeraude", value: "#3FB68B" },
  { id: "saphir", value: "#5B8DEF" },
  { id: "rubis", value: "#E0566B" },
  { id: "amethyste", value: "#9B6BDF" },
] as const;

export const STORAGE_KEY = "eve.theme.v1";

/** Seule porte d’entrée des réglages : tout ce qui est inconnu ou invalide est remplacé par la valeur par défaut. */
export function sanitize(input: unknown): ThemeSettings {
  const o = (typeof input === "object" && input !== null ? input : {}) as Record<string, unknown>;
  const m = o.mode;
  const a = o.accent;
  const b = o.blur;
  const n = o.animations;
  return {
    mode: m === "auto" || m === "dark" || m === "light" ? m : DEFAULT_THEME.mode,
    accent: typeof a === "string" && /^#[0-9a-fA-F]{6}$/.test(a) ? a : DEFAULT_THEME.accent,
    blur: typeof b === "number" && Number.isFinite(b) ? Math.min(40, Math.max(8, Math.round(b))) : DEFAULT_THEME.blur,
    animations: typeof n === "boolean" ? n : DEFAULT_THEME.animations,
  };
}

export function loadTheme(): ThemeSettings {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? sanitize(JSON.parse(raw)) : DEFAULT_THEME;
  } catch {
    return DEFAULT_THEME;
  }
}

export function saveTheme(theme: ThemeSettings): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(theme));
  } catch {
    // stockage indisponible : le thème reste actif pour la session
  }
}

export function resolveMode(mode: Mode): "dark" | "light" {
  if (mode !== "auto") return mode;
  return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
}

export function applyTheme(theme: ThemeSettings): void {
  const root = document.documentElement;
  root.dataset.theme = resolveMode(theme.mode);
  root.dataset.motion = theme.animations ? "on" : "off";
  root.style.setProperty("--accent", theme.accent);
  root.style.setProperty("--glass-blur", `${theme.blur}px`);
}