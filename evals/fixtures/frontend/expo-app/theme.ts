// Parcel theme (synthetic fixture). Components consume these values only.
export const theme = {
  space: { xs: 4, sm: 8, md: 12, lg: 16, xl: 24 },
  radius: { sm: 6, md: 12 },
  minTouch: 44,
  color: {
    text: "#111827",
    textMuted: "#4B5563",
    surface: "#FFFFFF",
    border: "#E5E7EB",
    accent: "#1D4ED8",
    onAccent: "#FFFFFF",
    danger: "#B91C1C",
  },
  type: {
    body: { fontSize: 16, lineHeight: 22 },
    label: { fontSize: 14, lineHeight: 20, fontWeight: "600" },
    title: { fontSize: 22, lineHeight: 28, fontWeight: "700" },
  },
} as const;
