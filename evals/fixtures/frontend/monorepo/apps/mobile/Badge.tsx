import { Text, StyleSheet } from "react-native";
import { tokens } from "@tally/ui/tokens";

export function Badge({ label }: { label: string }) {
  return <Text style={styles.badge}>{label}</Text>;
}

const styles = StyleSheet.create({
  badge: {
    color: tokens.badge.light.text,
    backgroundColor: tokens.badge.light.background,
    fontSize: 12,
    lineHeight: 16,
    fontWeight: "600",
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 999,
    overflow: "hidden",
  },
});
