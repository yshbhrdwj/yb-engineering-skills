import { useEffect, useState } from "react";
import { SafeAreaView, Text, TextInput, Pressable, BackHandler, StyleSheet, Platform } from "react-native";
import { useLocalSearchParams, router } from "expo-router";
import { theme } from "./theme";
import { saveNote } from "./data/orders";

const pressedFeedback = Platform.select({
  android: { android_ripple: { color: theme.color.border } },
  default: {},
});

export default function OrderDetail() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [note, setNote] = useState("");

  useEffect(() => {
    const subscription = BackHandler.addEventListener("hardwareBackPress", () => true);
    return () => subscription.remove();
  }, []);

  return (
    <SafeAreaView style={styles.screen}>
      <Pressable
        onPress={() => router.back()}
        accessibilityRole="button"
        accessibilityLabel="Close"
        hitSlop={6}
        style={({ pressed }) => [styles.close, Platform.OS === "ios" && pressed && styles.pressedIos]}
        {...pressedFeedback}
      >
        <Text>✕</Text>
      </Pressable>
      <Text style={styles.title} maxFontSizeMultiplier={1}>Order {id}</Text>

      <TextInput value={note} onChangeText={setNote} placeholder="Delivery note" style={styles.input} />
      <Pressable onPress={() => saveNote(id, note)} style={styles.save} {...pressedFeedback}>
        <Text style={styles.saveText}>Save note</Text>
      </Pressable>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: theme.color.surface },
  close: { width: 32, height: 32, alignItems: "center", justifyContent: "center", margin: theme.space.sm },
  pressedIos: { opacity: 0.6 },
  title: { ...theme.type.title, color: theme.color.text, paddingHorizontal: theme.space.lg },
  input: {
    position: "absolute", bottom: 72, left: theme.space.lg, right: theme.space.lg,
    height: 44, borderWidth: 1, borderColor: theme.color.border, borderRadius: theme.radius.sm, paddingHorizontal: theme.space.md,
  },
  save: {
    position: "absolute", bottom: 24, left: theme.space.lg, right: theme.space.lg,
    height: 30, borderRadius: theme.radius.sm, backgroundColor: theme.color.accent, alignItems: "center", justifyContent: "center",
  },
  saveText: { ...theme.type.label, color: theme.color.onAccent },
});
