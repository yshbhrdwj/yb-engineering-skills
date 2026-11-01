import { Pressable, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { color, inset, radius, type } from './tokens';

type Props = { label: string; icon?: keyof typeof Ionicons.glyphMap; onPress: () => void; disabled?: boolean };

export function PrimaryButton({ label, icon, onPress, disabled }: Props) {
  const c = color.light;
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityState={{ disabled }}
      disabled={disabled}
      onPress={onPress}
      hitSlop={4}
      style={({ pressed }) => ({
        minHeight: 48,
        paddingHorizontal: inset.card,
        paddingVertical: inset.control,
        borderRadius: radius.md,
        backgroundColor: c.action,
        opacity: disabled ? 0.4 : pressed ? 0.85 : 1,
        justifyContent: 'center',
      })}
    >
      <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'center' }}>
        {icon ? <Ionicons name={icon} size={20} color={c.onAction} style={{ marginRight: 3 }} /> : null}
        <Text style={[type.label, { color: c.onAction }]}>{label}</Text>
      </View>
    </Pressable>
  );
}
