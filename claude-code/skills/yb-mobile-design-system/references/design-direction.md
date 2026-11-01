# Design direction

A direction is a small set of decisions that makes every later choice predictable. It comes from the product's context, not from a style catalog.

## Derive it

1. **Context line.** Who uses it, for which task, where (glance or focus, one hand or two, indoors or outdoors, calm or stressed), how often, and what is at stake when they make a mistake.
2. **Primary qualities.** Choose two or three from calm, trust, speed, precision, confidence, readability, discovery, delight, immersion, focus. Name what each choice costs: precision costs warmth, immersion costs density, delight costs speed.
3. **Translate into dials.** Decide each one explicitly:
   - Typography approach: system or custom; contrast between levels; numeric treatment.
   - Color system: neutral temperature, brand hue role, accent proportion, theme stance.
   - Geometry: radius family, border versus fill versus elevation, one shape motif at most.
   - Spacing and density: base rhythm, gutter, rows per screen.
   - Interaction language: native or branded feedback, gesture vocabulary, haptic use.
   - Motion: purpose, tempo, signature moments.
   - Brand expression: where identity appears (display type, signature color, illustration, motion, copy voice).
4. **Check constraints.** Platform conventions, accessibility at the largest text and in dark theme, implementation cost in the actual stack, existing brand assets.
5. **Name the boundary.** One sentence on what the product must not feel like.

## Direction brief

Use for Mode 4 and for any exploration. Keep it to one screen of text.

| Field | Content |
| --- | --- |
| Context | The context line |
| Qualities | Two or three, with their costs |
| Character | Visual character in one or two sentences |
| Dials | Type, color, geometry, density, interaction, motion, brand expression |
| Platform stance | What is shared; what follows iOS and Android |
| Not | What it must not feel like |
| Tradeoffs | What this direction gives up |

## Explore alternatives only when undecided

Two or three directions that differ on at least three dials, applied to the same one or two key screens and judged against the qualities. A palette swap is not an alternative. Recommend one and say why; do not produce concepts nobody will evaluate.

## Judgment pairs

- **Minimal or empty.** Minimal: every remaining element earns its place and the primary task is still obvious. Empty: hierarchy and affordances were removed with the decoration.
- **Simple or incapable.** Simple: advanced capability is one clear step away. Incapable: it was deleted or hidden without a path.
- **Elegant or decorated.** Elegance comes from proportion, type, and restraint; decoration adds layers that carry no meaning.
- **Premium or luxurious.** Premium is precision, fewer and stronger moves, excellent type, and quiet confidence. Luxury styling (gold, heavy serif, dark gradients) is one possible expression and often reads as costume.
- **Playful or childish.** Playful lives in motion, illustration, and voice over a solid structure. Childish enlarges and saturates everything and talks down to people.
- **Consistent or monotonous.** Consistency means shared rules; composition should still vary by screen purpose so a dashboard, a detail view, and a form do not look interchangeable.
- **Dense or cluttered.** Density is organized by alignment, type, and grouping with one clear emphasis. Clutter is competing emphasis.

## Generic patterns to challenge

These often signal unconsidered or machine-generated design. Each may be right; each needs a product reason to stay. Do not report them as defects without a concrete effect on users.

- The same large-radius card for every kind of content.
- Gradients, glass, or blur as default decoration, especially on content.
- Pastel palettes without semantic roles; one accent color applied to everything.
- Oversized hero headers on utility screens, pushing the task below the fold.
- Illustrations or emoji that carry no meaning; icons on every row and label.
- Floating action buttons for secondary actions; shadows on everything.
- Dashboards made of equal tiles; every screen built from the same template.
- Centered text and layouts where scanning needs a strong leading edge.

## Distinctive without being unfamiliar

Spend distinctiveness on display typography, a signature color and its proportion, one shape motif, imagery and illustration style, motion at key moments, and copy voice. Keep familiar what people operate by habit: navigation, back, system controls, gestures, form patterns, and text input.
