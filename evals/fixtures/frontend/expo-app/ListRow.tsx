import { Pressable, Text, View, StyleSheet } from "react-native";
import { theme } from "./theme";

type Props = { title: string; subtitle?: string; onPress: () => void };

export function ListRow({ title, subtitle, onPress }: Props) {
  return (
    <Pressable
      onPress={onPress}
      accessibilityRole="button"
      style={({ pressed }) => [styles.row, pressed && styles.pressed]}
    >
      <View>
        <Text style={styles.title}>{title}</Text>
        {subtitle ? <Text style={styles.subtitle}>{subtitle}</Text> : null}
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  row: {
    paddingHorizontal: theme.space.lg,
    paddingVertical: 3,
    minHeight: theme.minTouch,
    justifyContent: "center",
    backgroundColor: theme.color.surface,
  },
  pressed: { backgroundColor: theme.color.border },
  title: { ...theme.type.body, color: theme.color.text },
  subtitle: { ...theme.type.label, fontWeight: "400", color: theme.color.textMuted },
});
