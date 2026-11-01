# Source registry

External sources this skill relies on, what each was used for, and when it was checked. Recheck version-sensitive entries before relying on them for a specific project; the project's installed versions win over this table.

| Source | Used for | Checked |
| --- | --- | --- |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Success criteria, levels, contrast, reflow, text spacing, target size; current version dated 12 December 2024; 4.1.1 Parsing obsolete | 2026-11-01 |
| [What's new in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/) | The nine new criteria and their levels | 2026-11-01 |
| [Understanding Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) | 320 CSS px equals 1280px at 400% zoom | 2026-11-01 |
| [WCAG 3 introduction](https://www.w3.org/WAI/standards-guidelines/wcag/wcag3-intro/) | WCAG 3 remains a Working Draft | 2026-11-01 |
| [ARIA APG patterns](https://www.w3.org/WAI/ARIA/apg/patterns/) | Grid, combobox, disclosure, menu patterns exist | 2026-11-01 |
| [APG dialog (modal)](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) | Focus entry, Tab containment, Escape, focus return, labelling | 2026-11-01 |
| [APG disclosure navigation](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/) | Site navigation without the menu role | 2026-11-01 |
| [APG read me first](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/) | "No ARIA is better than bad ARIA" | 2026-11-01 |
| [MDN dialog](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog) | `showModal()` inertness and Escape; widely available | 2026-11-01 |
| [MDN closedBy](https://developer.mozilla.org/en-US/docs/Web/API/HTMLDialogElement/closedBy) | Limited availability | 2026-11-01 |
| [MDN popover](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/popover) | Widely available since April 2024 | 2026-11-01 |
| [MDN anchor-name](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/anchor-name) | Anchor positioning newly available (2026) | 2026-11-01 |
| [MDN container-type](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/container-type) | Container size queries widely available | 2026-11-01 |
| [MDN length units](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/length) | `cqi`, `svh`, `dvh`, `lvh` definitions | 2026-11-01 |
| [MDN oklch()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/oklch) | Components and ranges; widely available since May 2023 | 2026-11-01 |
| [MDN color-mix()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/color-mix) | Widely available | 2026-11-01 |
| [MDN light-dark()](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/color_value/light-dark) | Newly available (2024) | 2026-11-01 |
| [MDN text-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-wrap) | `balance` and `pretty` behavior and line limits; widely available | 2026-11-01 |
| [MDN prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion) | Values; widely available | 2026-11-01 |
| [MDN startViewTransition](https://developer.mozilla.org/en-US/docs/Web/API/Document/startViewTransition) | Same-document view transitions newly available (2025) | 2026-11-01 |
| [web.dev Web Vitals](https://web.dev/articles/vitals) | LCP, INP, CLS thresholds at the 75th percentile; INP replaced FID in 2024 | 2026-11-01 |
| [Tailwind theme variables](https://tailwindcss.com/docs/theme) | v4 `@theme`, namespaces, CSS variable exposure | 2026-11-01 |
| [Tailwind dark mode](https://tailwindcss.com/docs/dark-mode) | Media-query default, `@custom-variant`; docs at v4.3 | 2026-11-01 |
| [Next.js fonts](https://nextjs.org/docs/app/getting-started/fonts) | `next/font` self-hosting without layout shift | 2026-11-01 |
| [Next.js Image](https://nextjs.org/docs/app/api-reference/components/image) | Dimensions reserve space; `priority` deprecated for `preload` in v16 | 2026-11-01 |
| [Next.js blog](https://nextjs.org/blog) | Current major 16 | 2026-11-01 |
| [Nuxt blog](https://nuxt.com/blog) | Current major 4 | 2026-11-01 |
| [Vue SFC CSS features](https://vuejs.org/api/sfc-css-features.html) | Scoped styles, `v-bind()` in CSS | 2026-11-01 |
| [Svelte scoped styles](https://svelte.dev/docs/svelte/scoped-styles) | Styles scoped by default; Svelte 5 runes | 2026-11-01 |
| [Angular component styling](https://angular.dev/guide/components/styling) | Emulated encapsulation default; docs at v22 | 2026-11-01 |
| [Angular image optimization](https://angular.dev/guide/image-optimization) | `NgOptimizedImage` dimensions, `fill`, `priority` | 2026-11-01 |
| [React versions](https://react.dev/versions) | React 19 current | 2026-11-01 |

Not verified at a primary source in this pass, so stated without version claims: Nuxt font and image module details, the Svelte `class:` directive, `@starting-style`, `font-optical-sizing`, and the `@font-face` metric-override descriptors. Check MDN or the framework docs before relying on their exact behavior.

## UI/UX Pro Max

[UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), v2.15.0 as installed locally, MIT License, copyright 2024 Next Level Builder (license file read 2026-11-01). It was studied for approach only: master-plus-page-override persistence that refuses to overwrite without explicit force, a one-intent query contract, and per-product reasoning profiles. No code, CSV data, palettes, or font pairings were copied, so its MIT notice requirement is not triggered; if any of its material is ever copied, include its copyright and permission notice. This skill works without it. In one local design-system query for an enterprise analytics dashboard (2026-11-01), it returned a marketing landing pattern (hero video, client logos, contact-sales CTA) and fixed device breakpoints; treat its output as a candidate to examine, not a decision.
