import { Text, View, useColorScheme } from 'react-native';
import { color, radius, type } from './tokens';

export function StatsCard({ completed, total }: { completed: number; total: number }) {
  const c = color[useColorScheme() === 'dark' ? 'dark' : 'light'];
  const pct = total ? completed / total : 0;
  return (
    <View
      style={{ padding: 12, borderRadius: radius.lg, backgroundColor: c.surfaceRaised, borderWidth: 1, borderColor: c.border, shadowOpacity: 0.1, shadowRadius: 8, elevation: 2 }}
    >
      <Text style={[type.label, { color: c.text }]}>This week</Text>
      <Text style={[type.caption, { color: c.textSecondary }]}>
        {completed} of {total} habits completed
      </Text>
      <View style={{ marginTop: 12, height: 8, borderRadius: 4, backgroundColor: c.surface }}>
        <View style={{ width: `${pct * 100}%`, height: 8, borderRadius: 4, backgroundColor: c.action }} />
      </View>
    </View>
  );
}
