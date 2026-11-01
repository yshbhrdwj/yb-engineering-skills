# Frameworks and feasibility

How design decisions are usually expressed per stack, and what they cost. These are constraints to name in a specification, not measurements: never state a performance number you did not measure. Detect the stack from the project (`package.json`, config files) before advising; never assume one. Check the project's installed versions against current documentation when an API is version-sensitive (versions in source-registry).

## Expressing tokens by stack

| Stack | Tokens and theming | Dark mode | Variants and responsive |
| --- | --- | --- | --- |
| Plain CSS | Custom properties at `:root`; roles overridden under a mode selector | `prefers-color-scheme` plus a `[data-theme]` override | Class or attribute variants; media and container queries |
| Tailwind CSS v4 | `@theme { --color-*; --font-*; --breakpoint-* }` in CSS generates utilities and exposes CSS variables; a single `--spacing` base scales spacing utilities | Media-query `dark:` by default; `@custom-variant dark (...)` for class or attribute control | Responsive prefixes from `--breakpoint-*`; `@container` variants; component variants usually via a class-composition helper already in the project |
| React | No styling opinion: follows the project's CSS approach (CSS modules, Tailwind, CSS-in-JS). Tokens stay in CSS variables so they work across approaches | Theme attribute on `<html>`, set before paint to avoid a flash | Variant props mapped to classes; avoid runtime style computation per render |
| Next.js | As React; `next/font` self-hosts fonts and avoids layout shift; `next/image` needs `width`/`height` (or `fill` with a sized parent) to reserve space. In Next.js 16, `priority` is deprecated in favor of `preload`, and the docs prefer `loading="eager"` or `fetchPriority="high"` for the main image | Server-rendered theme needs a cookie or an inline pre-paint script to avoid mismatch and flash | Server components cannot hold interactive state; interactive variants live in client components |
| Vue | `<style scoped>`; `v-bind()` in `<style>` binds reactive values to CSS variables | Class on root, CSS variables | Props to classes; `:class` bindings |
| Nuxt | As Vue; official modules provide font and image optimization (check `nuxt.config` for what is installed) | A color-mode module if installed; otherwise as Vue | As Vue |
| Svelte | Component styles scoped by default; CSS variables passed as `--prop` on components | Class or attribute on root | `class:` directives and props |
| Angular | Component styles use emulated encapsulation by default; tokens as CSS variables in global styles; Angular CDK and Material theming if present. `NgOptimizedImage` requires dimensions (or `fill`) and offers `priority` for the main image | Class on `<html>` or body; Material theme if used | Host bindings and inputs mapped to classes |

## What a decision costs

- **Layout stability:** anything that loads late (images, embeds, fonts, ads, async panels) must have reserved space or it shifts the page; Cumulative Layout Shift is a Core Web Vital. Specify dimensions or aspect ratios in the design.
- **Fonts:** each family, weight, and style is a file; a variable font may replace several. Metric-matched fallbacks reduce swap shift. A display face used only in the hero may not justify a blocking load.
- **Images:** hero imagery affects Largest Contentful Paint. Specify responsive sizes (`srcset`/`sizes`), modern formats, eager loading for the main image and lazy loading below the fold. Background images in CSS are discovered late.
- **Animation:** animate `transform` and `opacity`. Blur, `backdrop-filter`, large shadows, and filters on big or many elements are expensive to paint, especially on low-end devices. Scroll-linked effects driven by script compete with input responsiveness (Interaction to Next Paint).
- **DOM size:** decorative wrappers, duplicated mobile and desktop markup, and large hidden menus add nodes, style recalculation, and accessibility-tree noise. Prefer one responsive structure over two hidden copies.
- **Long lists and grids:** beyond a few hundred rows, specify pagination or virtualization; virtualization breaks find-in-page, can confuse screen readers, and needs stable row heights. Say which the design assumes.
- **Compatibility:** check Baseline status on MDN for newer CSS before relying on it. As checked for the registry, container size queries, `color-mix()`, `oklch()`, `popover`, `text-wrap`, and `<dialog>` are widely available; `light-dark()`, same-document view transitions, and anchor positioning are newly available; the `closedby` dialog attribute has limited availability. Provide a fallback or progressive enhancement for anything not widely available.
- **SEO and structure:** marketing pages need server-rendered content, one `h1`, meaningful heading order, real text (not text in images), descriptive link text, and stable URLs. Client-only rendering of essential content and infinite scroll without paginated URLs harm discoverability.

## Core Web Vitals, for naming constraints

Current thresholds for "good" (web.dev): Largest Contentful Paint at most 2.5s, Interaction to Next Paint at most 200ms, Cumulative Layout Shift at most 0.1, assessed at the 75th percentile of page loads. INP replaced First Input Delay in 2024. A design can make these easier or harder; only measurement on the built product establishes them, and that belongs to the engineer and QA.
