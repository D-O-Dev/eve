"use client";

import { useState, type CSSProperties } from "react";
import { Icon, type IconName } from "@/components/icons";
import { SectorTile, type SectorStatus } from "@/components/SectorTile";
import { ThemePanel } from "@/components/ThemePanel";
import { t, type MessageKey } from "@/i18n";

interface Sector {
  code: string;
  icon: IconName;
  status: SectorStatus;
}

// Provisoire : viendra de l’API (/api/sectors) à l’étape suivante.
const SECTORS: Sector[] = [
  { code: "commerce", icon: "commerce", status: "available" },
  { code: "restauration", icon: "food", status: "coming_soon" },
  { code: "services", icon: "services", status: "coming_soon" },
  { code: "transport", icon: "transport", status: "coming_soon" },
  { code: "numerique", icon: "digital", status: "coming_soon" },
  { code: "more", icon: "plus", status: "coming_soon" },
];

export default function Home() {
  const [selected, setSelected] = useState<string | null>(null);
  const [panelOpen, setPanelOpen] = useState(false);

  return (
    <main className="shell">
      <div className="top">
        <div className="steps">
          <span>{t("onboarding.step", { n: 3, total: 7 })}</span>
          <div className="bar"><i style={{ width: "43%" }} /></div>
        </div>
        <button type="button" className="icon-btn glass" aria-label={t("theme.open")} onClick={() => setPanelOpen(true)}>
          <Icon name="palette" />
        </button>
      </div>

      <h1>{t("onboarding.title")}</h1>
      <p className="sub">{t("onboarding.subtitle")}</p>

      <ul className="sectors">
        {SECTORS.map((s, i) => (
          <li key={s.code} style={{ "--i": i } as CSSProperties}>
            <SectorTile
              label={t(`sector.${s.code}` as MessageKey)}
              icon={s.icon}
              status={s.status}
              selected={selected === s.code}
              onSelect={() => setSelected(selected === s.code ? null : s.code)}
            />
          </li>
        ))}
      </ul>

      <p className="hint">{selected ? t("onboarding.picked") : t("onboarding.hint")}</p>
      <button type="button" className="cta" disabled={!selected}>{t("cta.continue")}</button>

      {panelOpen && <ThemePanel onClose={() => setPanelOpen(false)} />}
    </main>
  );
}