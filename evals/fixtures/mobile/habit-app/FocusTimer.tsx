import { useEffect } from 'react';
import { Pressable, Text, View, useColorScheme } from 'react-native';
import Animated, { useAnimatedStyle, useSharedValue, withRepeat, withTiming } from 'react-native-reanimated';
import { Ionicons } from '@expo/vector-icons';
import { color } from './tokens';

type Props = { secondsLeft: number; running: boolean; onToggle: () => void };

export function FocusTimer({ secondsLeft, running, onToggle }: Props) {
  const c = color[useColorScheme() === 'dark' ? 'dark' : 'light'];
  const scale = useSharedValue(1);
  useEffect(() => {
    scale.value = withRepeat(withTiming(1.08, { duration: 900 }), -1, true);
  }, []);
  const ring = useAnimatedStyle(() => ({ transform: [{ scale: scale.value }] }));
  const mm = String(Math.floor(secondsLeft / 60)).padStart(2, '0');
  const ss = String(secondsLeft % 60).padStart(2, '0');

  return (
    <View style={{ alignItems: 'center' }}>
      <Animated.View
        style={[{ width: 240, height: 240, borderRadius: 120, borderWidth: 6, borderColor: c.action, alignItems: 'center', justifyContent: 'center' }, ring]}
      >
        <Text style={{ fontSize: 48, fontWeight: '700', color: c.text }}>
          {mm}:{ss}
        </Text>
      </Animated.View>
      <Pressable
        onPress={onToggle}
        accessibilityRole="button"
        accessibilityLabel={running ? 'Pause' : 'Start'}
        hitSlop={12}
        style={{ marginTop: 24 }}
      >
        <Ionicons name={running ? 'pause' : 'play'} size={24} color={c.action} />
      </Pressable>
    </View>
  );
}
