// Synthetic Expo app theme used by mobile design evaluation cases.
export const space = { 1: 4, 2: 8, 3: 12, 4: 16, 5: 20, 6: 24, 8: 32, 10: 40 } as const;

export const inset = {
  screen: space[4],
  card: space[4],
  control: space[3],
} as const;

export const gap = {
  inlineIcon: space[2],
  stackRelated: space[2],
  section: space[6],
} as const;

export const radius = { sm: 8, md: 12, lg: 16, full: 999 } as const;

export const type = {
  title: { fontSize: 28, lineHeight: 34, fontWeight: '700' },
  heading: { fontSize: 20, lineHeight: 25, fontWeight: '600' },
  body: { fontSize: 17, lineHeight: 22, fontWeight: '400' },
  label: { fontSize: 15, lineHeight: 20, fontWeight: '600' },
  caption: { fontSize: 13, lineHeight: 18, fontWeight: '400' },
  metric: { fontSize: 34, lineHeight: 40, fontWeight: '700', fontVariant: ['tabular-nums'] },
} as const;

export const color = {
  light: {
    surface: '#FFFFFF',
    surfaceRaised: '#F4F6F5',
    text: '#14201C',
    textSecondary: '#5B6763',
    action: '#0F766E',
    onAction: '#FFFFFF',
    border: '#D5DBD8',
    danger: '#B42318',
    up: '#067647',
    down: '#B42318',
  },
  dark: {
    surface: '#0F1513',
    surfaceRaised: '#1A2320',
    text: '#EEF2F0',
    textSecondary: '#A3AFAA',
    action: '#5EEAD4',
    onAction: '#042F2B',
    border: '#2C3834',
    danger: '#F97066',
    up: '#47CD89',
    down: '#F97066',
  },
} as const;
