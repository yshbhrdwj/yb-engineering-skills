---
name: yb-release-operator
description: "Plan or execute authorized releases, migrations, incidents, recovery, maintenance, and retirement. Use for operational work with explicit targets, readiness evidence, and stop conditions."
argument-hint: "[plan, prepare, execute, diagnose, or retire] [service and target]"
---

# YB Release Operator

Achieve the requested operational outcome using the established pipeline or runbook. Match care to blast radius. Preserve existing authorization; readiness, passing checks, permission to act, and actual deployment are separate facts.

## Procedure

1. Pick the requested mode: plan (steps), prepare (authorized artifact changes), execute (through verification), diagnose (investigate), or retire. Read the relevant delivery config, runbooks, recent changes, and evidence. Batch independent inspection; do not build a parallel process.
2. Before mutation, pin service, immutable revision/artifact, configuration, environment/account/region, affected data, and outcome from authoritative evidence. A working directory or successful login does not establish the target. Resolve a consequential ambiguity before acting.
3. Establish readiness for this artifact: changed behavior, tests, compatibility when old/new versions and data coexist, rollout order, health baseline and success/abort criteria, justified observation window, and recovery path. Label proposed thresholds. Use [release-recovery.md](references/release-recovery.md) for delivery, migrations, or restore; [operations-retirement.md](references/operations-retirement.md) for incidents, maintenance, capacity, or retirement.
4. Inspect the actual plan/diff for replacements, deletions, permission/secrets changes, and costs. Promote the same immutable artifact when possible; run dependent steps in order. Stop on an unexpected target, destructive surprise, failed criterion, or unexplained partial state. Inspect committed state before retrying; do not repeat a side effect blindly.
5. Verify deployed revision/configuration, affected user behavior, significant data invariants, and health with designated test data. Command success or liveness alone is insufficient. Observe for the justified window; execute recovery only within existing authority and verify its result. Code rollback does not restore data, and backup success does not prove recoverability.
6. For diagnosis, separate observation, hypothesis, experiment, and conclusion. Prefer read-only evidence and isolated reproduction. For authorized mitigation, choose a bounded change with expected signal and stop/recovery conditions, then record its result before another change. Service restoration and root-cause certainty differ.
7. Record revision/digest, run/job IDs, relevant times/config/migrations, results, and deviations without sensitive data. Verify current vendor limits/prices/advisories from primary sources when they affect the decision. For PR landing, apply the separate merge workflow rather than treating release intent as blanket merge authority.

## Boundaries

Do not invent credentials, targets, owners, job results, or health. Do not create unrequested monitors/schedules or treat idle/prepared work as released. Interpret authorization from the user's actual scope: resolve unspecified destructive, external messaging, access, or spending actions before execution; do not re-ask for actions already authorized. Retirement must account for consumers, retained data/backups, resources, and resulting billing state.

## Deliver

State the operational outcome, exact target/revision, actual checks, remaining risk, and recovery status or next step. Deliver complete requested plans and runbooks. Report what remains unresolved rather than claiming completion from a successful command.

## Claude Code integration

Follow applicable `CLAUDE.md`, the active planning mode, and permissions. Use available tools; delegate bounded independent work only when useful. Load each applicable named skill; for delegated work, pass the relevant skill path or instructions with the requirements and raw artifacts. The skill does not change host configuration.
