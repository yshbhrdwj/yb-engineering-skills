import { Pressable, ScrollView, Text, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

type Stat = { label: string; value: string };
type Props = { title: string; date: string; stats: Stat[]; notes: string; onShare: () => void };

// Synthetic post-workout summary screen for a fitness app.
export function WorkoutSummary({ title, date, stats, notes, onShare }: Props) {
  return (
    <ScrollView style={{ backgroundColor: '#fff' }} contentContainerStyle={{ padding: 14 }}>
      <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
        <Text style={{ fontSize: 18, fontWeight: '400', color: '#222' }}>{title}</Text>
        <Pressable onPress={onShare} style={{ padding: 4 }}>
          <Ionicons name="share-outline" size={22} color="#222" />
        </Pressable>
      </View>
      <Text style={{ fontSize: 13, color: '#999', marginTop: 2 }}>{date}</Text>

      <Text style={{ fontSize: 17, fontWeight: '400', color: '#222', marginTop: 16 }}>Stats</Text>
      <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginTop: 10 }}>
        {stats.map((s) => (
          <View key={s.label} style={{ width: '48%', height: 72, padding: 12, borderRadius: 10, backgroundColor: '#F2F2F2' }}>
            <Text allowFontScaling={false} style={{ fontSize: 16, color: '#222' }}>{s.value}</Text>
            <Text style={{ fontSize: 12, color: '#AAA' }}>{s.label}</Text>
          </View>
        ))}
      </View>

      <Text style={{ fontSize: 17, fontWeight: '400', color: '#222', marginTop: 20 }}>Notes</Text>
      <View style={{ marginTop: 8, padding: 16, borderRadius: 16, backgroundColor: '#F2F2F2', borderWidth: 1, borderColor: '#E0E0E0' }}>
        <Text numberOfLines={2} style={{ fontSize: 15, color: '#444' }}>{notes}</Text>
      </View>
    </ScrollView>
  );
}
