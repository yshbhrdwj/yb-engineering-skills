# Release, migration, and recovery details

Read relevant sections for deployment execution, delivery infrastructure, migration, or restore work. Apply only to affected risks; the core skill supplies authority and evidence rules.

## Delivery mechanism

Inspect existing CI/CD, infrastructure definitions, protected-environment controls, and manual configuration drift. Use the established route unless it cannot meet the requirement. Validate changed configuration with proportionate static checks, tests, builds, or infrastructure previews; inspect actual additions, replacements, deletions, permissions, secret handling, and costs before applying.

Choose direct, rolling, canary, or blue/green delivery for compatibility and failure risk. Explain meaningful downtime, resource, reversibility, and confidence tradeoffs. Record the known-good artifact/configuration and required dependencies. Prefer promoting an immutable artifact; record and verify any rebuilt artifact as distinct. Use established least-privilege credentials without exposing their values.

Health criteria should cover the affected user journey and significant dependencies, not merely process survival. Include a relevant baseline, success/abort criteria, observation window, and recovery trigger. Use supplied service targets or explicitly proposed ones. Verify the actual deployed revision and configuration before interpreting results. Record whether traffic expanded, remained limited, or was restored.

## Migration compatibility

Check coexistence across application versions, clients, workers, schemas, events, and configuration. When needed, sequence additive schema changes, compatible deployment, bounded/resumable backfill, data verification, and later cleanup. Account for locking, transaction duration, idempotency, interruptions, and mixed-version behavior.

State what each irreversible step changes and which recovery options remain. An old binary can be unsafe against a new schema or rewritten data. Distinguish rollback, forward repair, restore, and reconciliation; do not promise zero loss from the existence of a backup. Before retrying a partial migration or infrastructure operation, inspect what committed and resume safely.

## Recovery evidence

Map recoverable state: data, files, configuration, required versions, secret references, and external dependencies. Check backup scope, access separation, protection, retention, and failure detection for the actual risks. A completed backup job is evidence of a job result, not proof of recovery.

Use authorized isolated restore exercises with controlled data. Verify integrity, business invariants, downstream reconciliation, pending work, possible duplicate side effects, restored deletions, and cutover criteria. Measure actual elapsed recovery time and recoverable data point against supplied targets; label unprovided targets proposed. Keep restore evidence tied to the tested backup, software/configuration versions, environment, and time.

Clean up exercise resources within scope and record retained sensitive copies or cost. After real recovery, verify important behavior and data before declaring restoration. Update incorrect runbooks using observed evidence; avoid ceremonial additions.
