# Product brief and delivery handoff

Use for a final brief or a substantial revision. Scale depth to the product. Default to one Markdown document with distinct architect and engineer sections. If split, link one authoritative requirements register rather than copying conflicting versions.

State each policy and open decision once, then refer to its ID in journeys and handoffs. Avoid repeating the same uncertainty in every section. Separate an accepted capability from proposed detailed behavior or acceptance thresholds; user approval of a feature does not approve every design choice. Keep a narrow product brief compact while retaining material requirements and unresolved decisions.

## 1. Decision summary

Record title, version/date, scope, sources, known owner, and proposal/accepted status. Explain the user problem, proposed experience, value, first-release boundary, main uncertainty, and recommended next step in plain language. Final writing does not imply accepted policy.

## 2. Opportunity and evidence

Describe users and context, buyer/payer differences, desired outcomes, existing alternatives, pain frequency/severity, and the differentiator being tested. Summarize concepts considered, choice, tradeoffs, and disconfirming evidence.

For material assumptions use: **ID | claim | source/evidence | confidence/limits | consequence if wrong | validation**. Use `ASM-` and `EXP-` or existing project IDs. Keep user assertions, observations, and experiment plans distinct. Cite external evidence and relevant dates; never fabricate research.

## 3. Experience and scope

Trace primary and consequential secondary journeys: trigger, action/input, state/result, permission, error, and recovery. Describe surfaces/navigation, content hierarchy, relevant microcopy, accessibility/device/language needs, consent, notifications, and failure states. Link actual designs; label textual proposals.

Specify domain invariants and decision policies. Separate first-release inclusions, deferred work, non-goals, hard constraints, and preferences. Preserve a coherent end-to-end experience.

## 4. Authoritative requirements

Use stable `FR-` behavior, `NFR-` quality, `UX-` experience, `MET-` metric, and `RISK-` identifiers, or preserve project IDs. Never silently repurpose an ID.

| ID | Observable requirement | Source | Decision status | Priority/slice | Acceptance example | Dependencies |
| --- | --- | --- | --- | --- | --- | --- |

Decision status: **accepted**, **proposed**, **assumed**, **deferred**, or **unknown**. Accepted requires explicit user intent or an authoritative requirement. Track **verified/partial/unverified/not applicable** separately when actual evidence exists. Agreement on a target does not verify it.

Acceptance examples state initial condition, action, expected result, and significant failure outcome. Quality targets need relevant units, percentile, workload, environment, or time bounds. Missing thresholds remain unknown/proposed. Include consequential security, privacy, accessibility, operability, and compatibility requirements here, not just in prose.

## 5. Business, metrics, and experiments

Describe adoption/distribution, activation, retention, and applicable monetization or internal value. Label pricing and financial scenarios. Define metric formula, cohort, time window, baseline, target status, data source, guardrails, and decision use. Minimize analytics data collection.

For each important experiment state hypothesis, method, audience/sample limits, signal, justified decision threshold, effort assumptions, and next action for negative as well as positive results. A plan is not authorization for outreach or spending.

## 6. Architect handoff

Link requirements to actors/roles, system boundary, journeys, invariants, known data/ownership/sensitivity/lifecycle, integrations, and hard versus preferred quality/technology/team constraints. Identify feasibility questions, tradeoffs, bounded spikes, and decisions left to architecture. Architecture later links design elements and `ADR-` decisions back to these IDs.

State ready, ready with assumptions, or blocked for specific decisions, with scope and reason. Readiness does not create an approval ritual.

## 7. Engineer and QA handoff

Order slices by value, risk, and dependency. Each slice includes user outcome, requirement/UX IDs, acceptance and boundary examples, role rules, failure/recovery states, actual design links, synthetic data needs, and unresolved questions. Link required architecture contracts/decisions when available; never invent them.

Identify prototype-ready, implementation-ready, or blocked slices. Include appropriate proposed verification: functional, integration, UX/accessibility, security, performance, or resilience. Product-definition completeness is not technical readiness. Avoid fabricated dates, effort estimates, APIs, or repository paths.

## 8. Launch, learning, and open decisions

Describe initial cohort, onboarding/support, metrics, quality/harm guardrails, feedback, and expansion evidence. Hand technical rollout/recovery to operations. Record ownership, maintenance/learning triggers, and relevant retirement/export/deletion needs; unknown owners stay unassigned.

An open decision records question, affected IDs, assumption, impact, next action, and latest responsible decision point. On updates summarize changed intent and affected journeys, metrics, architecture, code, tests, and release plans. Preserve IDs and flag superseded decisions.
