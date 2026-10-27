"use client";

import { ACCENTS, type Mode } from "@/lib/theme";
import { useTheme } from "@/lib/theme-store";
import { t } from "@/i18n";

const MODES: Mode[] = ["auto", "dark", "light"];

export function ThemePanel({ onClose }: { onClose: () => void }) {
  const { theme, update, reset } = useTheme();

  return (
    <section className="panel glass" role="dialog" aria-label={t("theme.title")}>
      <header className="panel-head">
        <h2>{t("theme.title")}</h2>
        <button type="button" className="ghost" onClick={onClose}>{t("theme.close")}</button>
      </header>

      <div className="field">
        <span className="label">{t("theme.mode")}</span>
        <div className="seg" role="group" aria-label={t("theme.mode")}>
          {MODES.map((m) => (
            <button key={m} type="button" aria-pressed={theme.mode === m} onClick={() => update({ mode: m })}>
              {t(`theme.mode.${m}`)}
            </button>
          ))}
        </div>
      </div>

      <div className="field">
        <span className="label">{t("theme.accent")}</span>
        <div className="swatches">
          {ACCENTS.map((a) => (
            <button
              key={a.id}
              type="button"
              className="swatch"
              style={{ background: a.value }}
              aria-label={t(`accent.${a.id}`)}
              aria-pressed={theme.accent.toLowerCase() === a.value.toLowerCase()}
              onClick={() => update({ accent: a.value })}
            />
          ))}
          <label className="swatch custom" aria-label={t("theme.accent.custom")}>
            <input type="color" value={theme.accent} onChange={(e) => update({ accent: e.target.value })} />
          </label>
        </div>
      </div>

      <div className="field">
        <label className="label" htmlFor="blur">{t("theme.blur")}</label>
        <input id="blur" className="range" type="range" min={8} max={40} value={theme.blur}
          onChange={(e) => update({ blur: Number(e.target.value) })} />
      </div>

      <div className="field">
        <label className="switch">
          <span>{t("theme.animations")}</span>
          <input type="checkbox" checked={theme.animations} onChange={(e) => update({ animations: e.target.checked })} />
        </label>
      </div>

      <div className="field">
        <button type="button" className="ghost" onClick={reset}>{t("theme.reset")}</button>
      </div>
    </section>
  );
}