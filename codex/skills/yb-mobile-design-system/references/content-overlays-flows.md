# Content, overlays, and specialized flows

Apply the shared contract in `components.md` when specifying any component here. Read only the needed section.

## Content

- **Cards**: one idea per card; consistent internal padding by hierarchy (one token per card level); the whole card is a single target when it leads to one destination, with secondary actions as separate targets. Avoid cards inside cards and borders plus shadows plus tints on one surface. Group content for screen readers.
- **Feed items**: author, time, content, and actions in a stable order; media with reserved aspect ratio; truncated text with an accessible "more"; actions with counts announced; one primary target per item.
- **Expandable sections**: a clear disclosure indicator that rotates or changes with state; the whole header is the target; expanded state exposed to assistive technology; do not hide required information or errors inside collapsed sections.
- **Status displays**: current state in words plus icon and color; time of last change; next step or expected time when known.
- **Lists**: leading column (icon, avatar, thumbnail) aligned across rows; title, supporting text, trailing metadata or control; consistent row heights by line count; separators inset to the text column. Swipe actions have visible alternatives. Long lists virtualize and preserve scroll position.
- **Dashboards**: lead with the one or two numbers that answer the user's main question; group by decision, not by data source; show freshness ("Updated 2 min ago") and period; each tile links to detail. Avoid equal-weight tile grids.
- **Tables on mobile**: limit visible columns, pin the identifying column, right-align numbers with tabular figures, allow horizontal scroll with a visible affordance, or switch to stacked rows at compact widths and large text.
- **Charts**: title states the takeaway; axes labeled with units; direct labels; touch-and-hold scrubbing with a readout; accessible text summary. Sparkline trends need the current value and period beside them.
- **Progress**: determinate when measurable; steps for multistep flows; rings and bars expose value to assistive technology.
- **Badges and status chips**: short text, icon plus color for status, accessible description including count ("3 unread messages"); avoid badges for non-actionable information.
- **Avatars**: consistent sizes from the scale; initials fallback with accessible name; presence indicators not by color alone.
- **Media**: fixed aspect ratios; placeholders; captions and transcripts for video and audio content; controls with accessible names; no autoplay with sound.
- **Empty states**: explain what will appear and the next action; distinguish first-use, no-results, cleared, and error-empty.
- **Skeletons**: match the final layout closely; avoid shimmer under reduced motion; replace within the loading budget or switch to an explicit message.

## Overlays

- **Bottom sheets**: scoped tasks or details that keep context; drag handle when resizable; one sheet at a time; scrim for modal sheets; content scroll hands off to sheet drag at the top; dismissal never discards input silently. iOS sheet detents; Android modal sheets dismiss with back.
- **Modals and full-screen dialogs**: multistep or immersive tasks with explicit cancel and confirm; avoid stacking modals.
- **Menus and popovers**: related actions anchored to their trigger; destructive items last and styled; iPhone popovers become sheets.
- **Alerts and dialogs**: blocking decisions only; title states the question; buttons are verbs; destructive option styled and never the default.
- **Snackbars and toasts**: brief, non-critical confirmation with optional undo; announced to screen readers; persistent enough to read (and to act on for undo); never the only error channel for failures that block the task.
- **Tooltips and coach marks**: short, dismissible, shown once and in context; never the only place an essential instruction lives; reachable by assistive technology. Android tooltips appear on long press of icon buttons; iOS rarely uses them.
- **Confirmation surfaces**: name the action and its consequence ("Delete 3 photos? This can't be undone."); the confirming button repeats the verb; for high-stakes actions (payments, transfers, orders) show a review summary before the final action rather than a generic alert.

## Specialized flows

- **Onboarding**: show value through the product, not carousels; ask for permissions in context with a pre-permission explanation; let people skip and resume; keep account creation as late as the product allows.
- **Authentication**: passkeys and platform autofill first; sign-in and sign-up clearly distinguished; password visibility toggle; precise errors without account enumeration; biometric unlock as convenience with a fallback; account deletion discoverable in settings.
- **Workout tracking**: glanceable large numerals with tabular figures; controls usable with sweaty hands and in motion (large targets, minimal precision); lock-screen and widget surfaces; pause and resume prominent; avoid destructive actions near primary controls.
- **Health logging**: one-tap common entries, recent and favorite items, editable history, units and time zone clarity, non-judgmental language, privacy cues for sensitive data, clear distinction between user-entered and device-measured values.
- **Financial trading**: real-time values with tabular figures and stable layout; price change with sign, color, and arrow; order entry with explicit order type, quantity, estimated cost, and fees; review step and confirmation with a clear final action; status of pending, filled, and rejected orders; market hours and data delay disclosures.
- **Subscriptions and paywalls**: price, period, trial terms, and renewal shown before purchase; restore purchases; easy close; honest comparison of tiers; no disguised dismiss buttons.
- **Calendars and scheduling**: day/week/month appropriate to density; time zones explicit; drag to reschedule with a non-drag alternative; conflicts visible; accessible event summaries.
- **Messaging**: composer above keyboard with clear send state; delivery and read states not by color alone; timestamps on demand; failed messages with retry; media previews with sizes reserved; threads preserve position.
- **Meal logging**: search with recent and frequent foods first; barcode or photo capture where available; portion entry with sensible units; one-tap repeat of past meals; edits after the fact; neutral language about food choices.
- **Family dashboards and health summaries**: who and what needs attention now, then today, then trends; each member identified by name and avatar, never color alone; summaries in plain language with the period and data source; sensitive items visible only to permitted roles.
- **Media playback**: persistent mini player that expands to full player; scrubbing with time readout; captions, speed, and audio description controls; lock-screen and background controls; resume position.
- **Map interactions**: list and map views of the same results; selection syncs between them; map gestures do not conflict with sheet dragging; a non-map path to every result; location permission asked in context.
- **Checkout**: guest path where possible; platform wallets first; address autofill; full cost (items, delivery, fees, taxes) before the final action; final button states the amount; clear order confirmation and receipt.
- **Notifications**: in-app inbox for history; categories users can control; each notification leads to its specific content; permission requested after showing value.
- **Settings**: grouped by user mental model, not by code module; search for long settings; changes apply immediately for toggles and explain consequences; destructive account actions separated at the end.
- **Data visualization**: one question per chart; the takeaway in the title; tappable points with readouts; accessible summary or table.
- **Dashboards** (see Content): freshness, period selection, drill-down, and offline cached views.

Sources: Apple HIG; Material 3 components; App Review Guidelines on subscriptions and account deletion (see sources.md).
