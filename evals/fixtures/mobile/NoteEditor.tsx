import { useEffect, useState } from 'react';
import { BackHandler, ScrollView, Text, TextInput, View } from 'react-native';
import { Snackbar } from './Snackbar';

// Synthetic Android note editor. The app targets API 36 and runs edge-to-edge.
export function NoteEditor({ save }: { save: (text: string) => Promise<void> }) {
  const [text, setText] = useState('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Prevent accidental exits while editing.
    const sub = BackHandler.addEventListener('hardwareBackPress', () => true);
    return () => sub.remove();
  }, []);

  async function onSave() {
    try {
      await save(text);
    } catch {
      setError('Your note could not be saved. Data may be lost.');
    }
  }

  return (
    <View style={{ flex: 1 }}>
      <ScrollView contentContainerStyle={{ padding: 16 }}>
        <TextInput multiline value={text} onChangeText={setText} placeholder="Write a note" style={{ minHeight: 400, fontSize: 16 }} />
      </ScrollView>
      <View style={{ position: 'absolute', bottom: 0, left: 0, right: 0, height: 56, flexDirection: 'row', justifyContent: 'flex-end', padding: 8 }}>
        <Text onPress={onSave} style={{ fontSize: 14, padding: 8 }}>SAVE</Text>
      </View>
      {error ? <Snackbar message={error} duration={3000} /> : null}
    </View>
  );
}
