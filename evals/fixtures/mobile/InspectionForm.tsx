import { useState } from 'react';
import { Pressable, ScrollView, Text, TextInput } from 'react-native';

const FIELDS = [
  'Site ID', 'Inspector name', 'Date', 'Weather', 'Equipment serial', 'Hours meter',
  'Hydraulic pressure (psi)', 'Fluid level (%)', 'Tire tread (mm)', 'Damage observed', 'Photos taken (count)', 'Notes',
];

// Synthetic field-inspection form for an operations app.
export function InspectionForm({ submit }: { submit: (v: Record<string, string>) => Promise<void> }) {
  const [values, setValues] = useState<Record<string, string>>({});
  const [errors, setErrors] = useState<string[]>([]);

  async function onSubmit() {
    const missing = FIELDS.filter((f) => !values[f]);
    if (missing.length) return setErrors(missing.map((f) => `${f} is required`));
    try {
      await submit(values);
    } catch {
      setErrors(['Something went wrong']);
    } finally {
      setValues({});
    }
  }

  return (
    <ScrollView contentContainerStyle={{ padding: 16 }}>
      {errors.length ? <Text style={{ color: 'red', fontSize: 12 }}>{errors.join(', ')}</Text> : null}
      {FIELDS.map((f) => (
        <TextInput
          key={f}
          placeholder={f}
          value={values[f] ?? ''}
          onChangeText={(t) => setValues({ ...values, [f]: t })}
          style={{ borderBottomWidth: 1, borderColor: '#ddd', paddingVertical: 8, fontSize: 14 }}
        />
      ))}
      <Pressable onPress={onSubmit} style={{ alignSelf: 'flex-end', padding: 6, marginTop: 12 }}>
        <Text style={{ fontSize: 12, color: '#0F766E' }}>Submit</Text>
      </Pressable>
    </ScrollView>
  );
}
