import { tokens } from "@tally/ui/tokens";

export function Badge({ label }: { label: string }) {
  const { badge } = tokens;
  return (
    <span style={{ color: badge.light.text, background: badge.light.background, font: "600 12px/16px system-ui", padding: "4px 8px", borderRadius: 999 }}>
      {label}
    </span>
  );
}
