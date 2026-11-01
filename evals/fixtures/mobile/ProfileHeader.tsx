import { Image, Pressable, Text, View } from 'react-native';
import { Ionicons, MaterialIcons, Feather } from '@expo/vector-icons';
import { color, inset, type } from './tokens';

type Props = { name: string; avatarUrl: string; location: string; bio: string; followers: string; onEdit: () => void };

// Synthetic profile header for a creator app.
export function ProfileHeader({ name, avatarUrl, location, bio, followers, onEdit }: Props) {
  const c = color.light;
  return (
    <View style={{ padding: inset.screen, backgroundColor: c.surface }}>
      <View style={{ flexDirection: 'row', alignItems: 'center' }}>
        <View style={{ width: 72, height: 72, padding: 4, borderRadius: 20, backgroundColor: c.action }}>
          <Image source={{ uri: avatarUrl }} style={{ width: 64, height: 64, borderRadius: 20 }} />
        </View>
        <View style={{ flex: 1, marginLeft: 12 }}>
          <View style={{ flexDirection: 'row', alignItems: 'center' }}>
            <Text style={[type.heading, { color: c.text }]}>{name}</Text>
            <MaterialIcons name="verified" size={20} color={c.action} style={{ marginLeft: 4 }} />
          </View>
          <View style={{ flexDirection: 'row', alignItems: 'center', marginTop: 2 }}>
            <Feather name="map-pin" size={12} color={c.textSecondary} />
            <Text style={{ fontSize: 10, color: c.textSecondary, marginLeft: 4 }}>{location}</Text>
          </View>
        </View>
        <Pressable onPress={onEdit}>
          <Feather name="edit-2" size={18} color={c.text} />
        </Pressable>
      </View>

      <Text style={[type.body, { color: c.text, letterSpacing: 0.8, marginTop: 12 }]}>{bio}</Text>

      <View style={{ flexDirection: 'row', alignItems: 'center', marginTop: 12 }}>
        <Text style={{ fontSize: 20, fontWeight: '700', color: c.text }}>{followers}</Text>
        <Text style={[type.caption, { color: c.textSecondary, marginLeft: 4 }]}>followers</Text>
      </View>

      <Pressable style={{ flexDirection: 'row', alignItems: 'center', marginTop: 12 }}>
        <Text style={[type.label, { color: c.action }]}>View public profile</Text>
        <Ionicons name="chevron-forward" size={16} color={c.action} />
      </Pressable>
    </View>
  );
}
