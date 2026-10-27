import { describe, expect, it } from "vitest";
import { DEFAULT_THEME, sanitize } from "./theme";

describe("sanitize", () => {
  it("garde des réglages valides", () => {
    const t = { mode: "dark", accent: "#3FB68B", blur: 30, animations: false };
    expect(sanitize(t)).toEqual(t);
  });

  it("refuse une couleur qui n’est pas #rrggbb", () => {
    for (const bad of ["red", "#12345", "url(javascript:alert(1))", "#12345g", "#D9B25A; background:red", 42, null]) {
      expect(sanitize({ accent: bad }).accent).toBe(DEFAULT_THEME.accent);
    }
  });

  it("borne le flou entre 8 et 40", () => {
    expect(sanitize({ blur: 9999 }).blur).toBe(40);
    expect(sanitize({ blur: -5 }).blur).toBe(8);
    expect(sanitize({ blur: Number.NaN }).blur).toBe(DEFAULT_THEME.blur);
    expect(sanitize({ blur: "30" }).blur).toBe(DEFAULT_THEME.blur);
  });

  it("refuse un mode inconnu", () => {
    expect(sanitize({ mode: "neon" }).mode).toBe("auto");
  });

  it("ignore les entrées qui ne sont pas des objets et les clés inconnues", () => {
    expect(sanitize(null)).toEqual(DEFAULT_THEME);
    expect(sanitize("n’importe quoi")).toEqual(DEFAULT_THEME);
    expect(Object.keys(sanitize({ evil: "<script>" })).sort()).toEqual(["accent", "animations", "blur", "mode"]);
  });
});