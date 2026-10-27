import { t } from "@/i18n";
import { Icon, type IconName } from "./icons";

export type SectorStatus = "available" | "coming_soon" | "premium";

interface Props {
  label: string;
  icon: IconName;
  status: SectorStatus;
  selected: boolean;
  onSelect: () => void;
}

export function SectorTile({ label, icon, status, selected, onSelect }: Props) {
  const locked = status !== "available";
  return (
    <button type="button" className="sector" aria-pressed={selected} disabled={locked} onClick={onSelect}>
      <span className="sq glass">
        {locked && (
          <span className="lock"><Icon name="lock" /></span>
        )}
        <span className="ic"><Icon name={icon} /></span>
      </span>
      <span>
        <b>{label}</b>
        <small>{t(`status.${status}`)}</small>
      </span>
    </button>
  );
}