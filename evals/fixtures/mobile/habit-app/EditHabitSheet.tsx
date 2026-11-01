import { useState } from 'react';
import { Modal, Pressable, Text, TextInput, View, useColorScheme } from 'react-native';
import { color, inset, radius, type } from './tokens';

type Props = { visible: boolean; initialName: string; onSave: (name: string) => void; onClose: () => void };

export function EditHabitSheet({ visible, initialName, onSave, onClose }: Props) {
  const c = color[useColorScheme() === 'dark' ? 'dark' : 'light'];
  const [name, setName] = useState(initialName);
  return (
    <Modal visible={visible} transparent animationType="slide" onRequestClose={onClose}>
      <Pressable style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.4)' }} onPress={onClose} />
      <View style={{ padding: inset.screen, borderTopLeftRadius: radius.lg, borderTopRightRadius: radius.lg, backgroundColor: c.surface }}>
        <TextInput
          value={name}
          onChangeText={setName}
          placeholder="Habit name"
          style={[type.body, { color: c.text, borderBottomWidth: 1, borderColor: c.border, paddingVertical: 12 }]}
        />
        <Pressable
          onPress={() => onSave(name)}
          accessibilityRole="button"
          style={({ pressed }) => ({ minHeight: 48, marginTop: 16, borderRadius: radius.md, backgroundColor: c.action, opacity: pressed ? 0.85 : 1, alignItems: 'center', justifyContent: 'center' })}
        >
          <Text style={[type.label, { color: c.onAction }]}>Save habit</Text>
        </Pressable>
      </View>
    </Modal>
  );
}
