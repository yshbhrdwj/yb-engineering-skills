import { Text, View } from 'react-native';
import { color, type } from './tokens';

const c = color.light;

// Three card components found in different feature folders of the same synthetic app.
export function ActivityCard({ title, detail }: { title: string; detail: string }) {
  return (
    <View style={{ padding: 12, borderRadius: 12, backgroundColor: c.surfaceRaised, borderWidth: 1, borderColor: c.border }}>
      <Text style={type.label}>{title}</Text>
      <Text style={[type.caption, { color: c.textSecondary }]}>{detail}</Text>
    </View>
  );
}

export function GoalCard({ title, progress }: { title: string; progress: string }) {
  return (
    <View style={{ padding: 16, borderRadius: 16, backgroundColor: '#F5F7F6', shadowOpacity: 0.12, shadowRadius: 6, elevation: 3 }}>
      <Text style={{ fontSize: 16, fontWeight: '600' }}>{title}</Text>
      <Text style={{ fontSize: 13, color: '#6B7280' }}>{progress}</Text>
    </View>
  );
}

export function MealCard({ title, time }: { title: string; time: string }) {
  return (
    <View style={{ padding: 14, borderRadius: 10, backgroundColor: c.surfaceRaised }}>
      <View style={{ padding: 4, borderRadius: 10, backgroundColor: c.surface }}>
        <Text style={type.label}>{title}</Text>
      </View>
      <Text style={[type.caption, { color: c.textSecondary }]}>{time}</Text>
    </View>
  );
}
