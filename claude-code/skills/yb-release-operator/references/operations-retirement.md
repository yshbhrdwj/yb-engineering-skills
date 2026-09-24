# Operations, incidents, maintenance, and retirement

Read only the section matching the operational task. Apply the core skill's target, authorization, evidence, and compact-report rules.

## Operability

Connect logs, metrics, and traces to user outcomes and consequential dependencies. Include revision/environment and useful correlation without exposing secrets or excessive personal data. Alert on actionable conditions with an actual destination, runbook, and known owner; mark unknown ownership openly. Use supplied service indicators/objectives or label proposals.

Inspect relevant resource limits, queues, backpressure, dependency timeouts, retry budgets, overload behavior, and graceful degradation. Do not describe accepting work that cannot be preserved as safe degradation. Keep configuration changes reviewable and commands reproducible. Hazardous runbook steps need prerequisites, expected results, stop conditions, and recovery.

## Incidents

Establish symptom, time window, affected users/environment, blast radius, last known good state, and recent changes. Separate observations, hypotheses, experiments, and conclusions. Use logs, metrics, traces, configuration, and dependency evidence to test likely causes; preserve useful evidence with sensitive content minimized. Prefer read-only inspection and isolated synthetic reproduction over worsening live impact.

For authorized mitigation, choose one bounded change with an expected signal and stop/recovery condition; record the result before another speculative change. Service restoration and root-cause certainty are separate. Summarize supported impact, timeline, contributing factors, uncertainty, and prevention/detection/recovery work. Do not invent contacts, communicate externally, or assign blame as a substitute for evidence.

## Maintenance and capacity

Use observed inventory, support timelines, and applicable advisories for dependency, runtime, OS, certificate, or credential maintenance. Verify compatibility with staged checks; avoid unrelated blanket upgrades. Update runbooks when evidence exposes errors.

For capacity/cost decisions, state workload, units, baseline period, consumption, pricing source/date, exclusions, and uncertainty. Separate forecasts from measurements. Scale or optimize for a demonstrated constraint or explicit forecast, not a generic checklist.

## Retirement

Identify active consumers, data, integrations, jobs, domains, credentials, resources, and owners. Define the requested end state, supplied notice/compatibility obligations, export and retention needs, and evidence that required consumers are accounted for.

Sequence replacement/export, validation, traffic/access changes, job shutdown, retention handling, and resource removal by dependency. Distinguish reversible disablement from irreversible deletion. Account for backups and restored data reappearing; preserve required records and audit evidence.

Execute only authorized retirement actions. “Unused” is not permission to delete, notify customers, revoke credentials, or terminate paid resources. Verify resulting endpoint, resource, and billing state through available evidence. Record what remains, why, its known owner, and next action. Do not claim shutdown complete while unresolved consumers or resources remain.
