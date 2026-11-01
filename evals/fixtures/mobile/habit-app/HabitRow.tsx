import { Pressable, Text, View, useColorScheme } from 'react-native';
import { Swipeable } from 'react-native-gesture-handler';
import { Ionicons } from '@expo/vector-icons';
import { color, gap, inset, type } from './tokens';

type Props = { name: string; streak: number; done: boolean; onToggle: () => void; onDelete: () => void };

export function HabitRow({ name, streak, done, onToggle, onDelete }: Props) {
  const c = color[useColorScheme() === 'dark' ? 'dark' : 'light'];
  return (
    <Swipeable
      renderRightActions={() => (
        <Pressable
          onPress={onDelete}
          accessibilityRole="button"
          accessibilityLabel={`Delete ${name}`}
          style={{ width: 88, backgroundColor: c.danger, alignItems: 'center', justifyContent: 'center' }}
        >
          <Ionicons name="trash-outline" size={24} color={c.onAction} />
        </Pressable>
      )}
    >
      <View style={{ flexDirection: 'row', alignItems: 'center', gap: gap.inlineIcon, paddingHorizontal: inset.screen, paddingVertical: inset.control, backgroundColor: c.surface }}>
        <Pressable onPress={onToggle} accessibilityRole="checkbox" accessibilityLabel={name} hitSlop={10}>
          <Ionicons name={done ? 'checkmark-circle' : 'ellipse-outline'} size={28} color={done ? c.action : c.textSecondary} />
        </Pressable>
        <View style={{ flex: 1 }}>
          <Text style={[type.body, { color: c.text }]}>{name}</Text>
          <Text style={[type.caption, { color: '#7C8188' }]}>{streak}-day streak</Text>
        </View>
      </View>
    </Swipeable>
  );
}
