"use client";
import { useState } from "react";
import { useSearchParams } from "next/navigation";

// PR 412 replaced <Link href="?tab=..."> with local state for faster switching.
const TABS = ["profile", "billing", "security"] as const;
type Tab = (typeof TABS)[number];

export function SettingsTabs() {
  const params = useSearchParams();
  const requested = params.get("tab");
  const initial: Tab = TABS.includes(requested as Tab) ? (requested as Tab) : "profile";
  const [tab, setTab] = useState<Tab>(initial);

  return (
    <div>
      <div role="tablist" aria-label="Settings">
        {TABS.map((t) => (
          <button key={t} role="tab" id={`tab-${t}`} aria-selected={tab === t} aria-controls="settings-panel" onClick={() => setTab(t)}>
            {t}
          </button>
        ))}
      </div>
      <section role="tabpanel" id="settings-panel" aria-labelledby={`tab-${tab}`}>
        {tab}
      </section>
    </div>
  );
}
