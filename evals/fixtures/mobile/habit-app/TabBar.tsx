import { Pressable, Text, View, useColorScheme } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { color, type } from './tokens';

const TABS = [
  { key: 'today', label: 'Today', icon: 'sunny-outline' },
  { key: 'focus', label: 'Focus', icon: 'timer-outline' },
  { key: 'stats', label: 'Stats', icon: 'stats-chart-outline' },
] as const;

export function TabBar({ active, onSelect }: { active: string; onSelect: (key: string) => void }) {
  const c = color[useColorScheme() === 'dark' ? 'dark' : 'light'];
  return (
    <View style={{ flexDirection: 'row', backgroundColor: c.surface, borderTopWidth: 1, borderColor: c.border, paddingTop: 8, paddingBottom: 8 }}>
      {TABS.map((t) => {
        const selected = t.key === active;
        return (
          <Pressable
            key={t.key}
            onPress={() => onSelect(t.key)}
            accessibilityRole="tab"
            accessibilityState={{ selected }}
            accessibilityLabel={t.label}
            style={{ flex: 1, minHeight: 48, alignItems: 'center', justifyContent: 'center' }}
          >
            <Ionicons name={t.icon} size={24} color={selected ? c.action : c.textSecondary} />
            <Text maxFontSizeMultiplier={1.5} style={[type.caption, { color: selected ? c.action : c.textSecondary }]}>
              {t.label}
            </Text>
          </Pressable>
        );
      })}
    </View>
  );
}
