import { I18nManager, Platform, Pressable, Text, useColorScheme } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { color, gap, inset, type } from './tokens';

type Props = { icon: keyof typeof Ionicons.glyphMap; title: string; value?: string; onPress: () => void };

// Synthetic settings row used across an Expo app's settings screens.
export function SettingsRow({ icon, title, value, onPress }: Props) {
  const c = color[useColorScheme() === 'dark' ? 'dark' : 'light'];
  return (
    <Pressable
      onPress={onPress}
      accessibilityRole="button"
      accessibilityLabel={value ? `${title}, ${value}` : title}
      android_ripple={{ color: c.border }}
      style={({ pressed }) => ({
        minHeight: 48,
        flexDirection: 'row',
        alignItems: 'center',
        gap: gap.inlineIcon,
        paddingHorizontal: inset.screen,
        paddingVertical: inset.control,
        backgroundColor: pressed && Platform.OS === 'ios' ? c.border : c.surface,
      })}
    >
      <Ionicons name={icon} size={22} color={c.textSecondary} accessibilityElementsHidden importantForAccessibility="no" />
      <Text style={[type.body, { flex: 1, color: c.text }]}>{title}</Text>
      {value ? (
        <Text numberOfLines={1} style={[type.body, { flexShrink: 1, maxWidth: '50%', color: c.textSecondary }]}>
          {value}
        </Text>
      ) : null}
      {Platform.OS === 'ios' ? (
        <Ionicons
          name="chevron-forward"
          size={17}
          color={c.textSecondary}
          style={{ transform: [{ scaleX: I18nManager.isRTL ? -1 : 1 }] }}
          accessibilityElementsHidden
          importantForAccessibility="no"
        />
      ) : null}
    </Pressable>
  );
}
