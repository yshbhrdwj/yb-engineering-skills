import { View, Text, ScrollView, StyleSheet } from "react-native";
import { tokens } from "@tally/ui/tokens";

export function OrderSummary({ lines, total }: { lines: { label: string; amount: string }[]; total: string }) {
  return (
    <View style={styles.screen}>
      <ScrollView contentContainerStyle={styles.content}>
        {lines.map((line) => (
          <View key={line.label} style={styles.line}>
            <Text>{line.label}</Text>
            <Text>{line.amount}</Text>
          </View>
        ))}
      </ScrollView>
      <View style={styles.totalBar}>
        <Text style={styles.total}>Total {total}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: tokens.surface },
  content: { padding: tokens.space.md, paddingBottom: 72 },
  line: { flexDirection: "row", justifyContent: "space-between", paddingVertical: tokens.space.sm },
  totalBar: {
    position: "absolute", left: 0, right: 0, bottom: 0,
    paddingHorizontal: tokens.space.md, paddingTop: tokens.space.sm, paddingBottom: tokens.space.sm,
    backgroundColor: tokens.surface, borderTopWidth: 1, borderTopColor: tokens.border,
  },
  total: { fontSize: 17, fontWeight: "600", textAlign: "right" },
});
