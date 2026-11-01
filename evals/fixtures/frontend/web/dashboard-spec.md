# Usage dashboard (accepted 2026-10-20)

Synthetic fixture. Replaces the draft `UsageDashboard.tsx`.

- FR-1: Show total requests this month and a per-project table with name, requests, and status.
- FR-2: While loading, show a loading state; never show zero as a placeholder.
- FR-3: With no projects, explain that usage appears after the first project and offer "Create project".
- FR-4: On fetch failure, keep previously loaded data visible and show an error with Retry.
- FR-5: Status reads "Within quota" or "Over quota" and is understandable without color.
- FR-6: Works from 320 px to wide desktop; the table may scroll horizontally inside its own region, but the page must not.

Data comes from `useUsage()` in `./useUsage`, which returns `{ data, error, isLoading, refetch }`. Use `tokens.css`; add no dependencies.
