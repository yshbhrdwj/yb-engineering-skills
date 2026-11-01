# Websites versus web applications

Classify the surface before composing it. A product often has both: a marketing site that persuades and an application that is used daily. They need different priorities and frequently different density, type scale, and motion, under one shared identity (logo, accent, type family, voice).

| Type | Primary job | Usage | Optimize for | Signals of the wrong mode |
| --- | --- | --- | --- | --- |
| Marketing site | Explain and persuade | Once or occasionally | Story, clarity, trust, one action | Dense tables, app chrome, many competing CTAs |
| SaaS application | Complete repeated tasks | Daily, for hours | Efficiency, predictability, state | Hero banners, oversized headings, scroll-reveal animation |
| Dashboard | Monitor and decide | Glanced often | Scannability, comparison, anomalies | Decorative cards, giant numbers without context, 3D charts |
| E-commerce | Find, evaluate, buy | Episodic | Product imagery, filters, price clarity, checkout | Hidden costs, slow galleries, navigation changes mid-checkout |
| Editorial | Read | Sessions of minutes | Measure, type, pacing, wayfinding | Narrow measure, ads that shift text, sticky clutter |

## Landing-page composition

A landing page answers, in order: what is it, who is it for, why believe it, what does it cost or require, and what do I do now. Typical sequence: a hero with a specific value proposition (an outcome, not a category name) and one primary action; proof close to the claim (named customers, real metrics, testimonials with attribution, product imagery); how it works in a few concrete steps; objections answered (pricing, security, integration, migration); a final action.

- The hero needs a real product view or a concrete image of the outcome; abstract gradients carry no information.
- Use one primary CTA label throughout; a secondary action (demo, docs) is visually subordinate.
- Proof must be real. Never invent logos, testimonials, ratings, user counts, or metrics; leave clearly marked placeholders for content the client must supply.
- Vary section composition by content (a comparison wants a table, a workflow wants steps, a story wants an image and text); a page of identical three-column icon grids reads as a template.

**Conversion without dark patterns.** Do not use fake scarcity or countdowns that reset, pre-checked upsells or consent, confirmshaming ("No, I don't want to save money"), hidden fees revealed at the last step, disguised ads, obstructed cancellation, or forced account creation that the business does not need. Flag such requests as defects with the honest alternative (real deadlines, clear pricing, easy cancellation) and their trust and legal risk; do not design them silently.

## Application information architecture

- Structure navigation around objects and tasks users name ("Shipments", "Invoices"), not around internal teams. Keep the number of top-level destinations small and stable.
- Every object has a predictable home: a list view (search, filter, sort, bulk actions), a detail view (status, key facts, actions, history), and create and edit flows. Deep links and back behave as users expect; filters and tabs persist in the URL.
- Workflow continuity: preserve unsaved work and state across navigation, show where the user is in multi-step work, return users to where they were after an interruption, and make the next step obvious after completion.
- Status is first-class: loading, saving, saved, failed, stale, and permission states are designed, not left to defaults.

## Data readability

- Tables over cards for comparison; consistent units and precision; tabular numerals right-aligned; meaningful empty and null values ("—" with an explanation, not 0).
- Dashboards lead with the few metrics tied to decisions, each with comparison and timeframe; drill-down replaces cramming. Alerts and anomalies get the accent; everything else stays neutral.
- Density follows frequency: experts in daily tools want more on screen and keyboard paths; occasional users want guidance and fewer choices. Offer density as a setting when both exist.
