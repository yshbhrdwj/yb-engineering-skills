import { Text, View } from 'react-native';

type Position = { symbol: string; name: string; qty: number; price: number; changePct: number; value: number };

// Synthetic row in an active trader's positions list (rendered about 30 times per screen).
export function PositionRow({ p }: { p: Position }) {
  const up = p.changePct >= 0;
  return (
    <View style={{ flexDirection: 'row', alignItems: 'center', paddingVertical: 18, paddingHorizontal: 16, borderBottomWidth: 1, borderColor: '#EEE' }}>
      <View style={{ flex: 1 }}>
        <Text style={{ fontSize: 16, fontWeight: '700' }}>{p.symbol}</Text>
        <Text numberOfLines={1} style={{ fontSize: 13, color: '#888' }}>{p.name}</Text>
      </View>
      <View style={{ alignItems: 'center', width: 90 }}>
        <Text style={{ fontSize: 15 }}>{p.price.toFixed(2)}</Text>
        <Text style={{ fontSize: 13, color: up ? '#16A34A' : '#DC2626' }}>{Math.abs(p.changePct).toFixed(2)}%</Text>
      </View>
      <Text style={{ width: 100, textAlign: 'center', fontSize: 15 }}>${p.value.toLocaleString()}</Text>
    </View>
  );
}
