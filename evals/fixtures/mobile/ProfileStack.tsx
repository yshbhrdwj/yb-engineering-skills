import { createStackNavigator } from '@react-navigation/stack';
import { Pressable, Text } from 'react-native';
import { ProfileScreen, EditProfileScreen, SettingsScreen } from './screens';

const Stack = createStackNavigator();

// Synthetic profile stack. Users report that "swiping back doesn't work" on iPhone.
export function ProfileStack() {
  return (
    <Stack.Navigator screenOptions={{ gestureEnabled: false }}>
      <Stack.Screen name="Profile" component={ProfileScreen} options={{ title: 'Profile' }} />
      <Stack.Screen
        name="Settings"
        component={SettingsScreen}
        options={({ navigation }) => ({
          title: 'Settings',
          headerLargeTitle: true,
          headerLeft: () => (
            <Pressable onPress={() => navigation.goBack()}>
              <Text style={{ fontSize: 15, color: '#0F766E', marginLeft: 8 }}>Back</Text>
            </Pressable>
          ),
        })}
      />
      <Stack.Screen name="EditProfile" component={EditProfileScreen} options={{ title: 'Edit profile', presentation: 'modal' }} />
    </Stack.Navigator>
  );
}
