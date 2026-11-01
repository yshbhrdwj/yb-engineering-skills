import { useState } from "react";
import { saveSettings } from "./api";

export function SettingsForm({ initial }: { initial: { displayName: string } }) {
  const [displayName, setDisplayName] = useState(initial.displayName);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (saving) return;
    setSaving(true);
    setError(null);
    try {
      await saveSettings({ displayName });
      setSaving(false);
    } catch {
      setError("Could not save. Try again.");
    }
  }

  return (
    <form onSubmit={onSubmit} className="settings-form">
      <label htmlFor="display-name">Display name</label>
      <input
        id="display-name"
        value={displayName}
        onChange={(e) => setDisplayName(e.target.value)}
        aria-describedby={error ? "settings-error" : undefined}
      />
      {error && <p id="settings-error" role="alert">{error}</p>}
      <button type="submit" disabled={saving}>{saving ? "Saving…" : "Save"}</button>
    </form>
  );
}
