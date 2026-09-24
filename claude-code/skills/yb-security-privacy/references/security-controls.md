# Security control paths

Use the sections relevant to the threat model and affected boundaries, not as finding quotas.

## Identity and isolation

Trace authentication separately from object, action, field, and tenant authorization. Check server-side ownership enforcement on individual/bulk endpoints, nested resources, exports, jobs, and alternate paths; client identifiers cannot establish permission.

Inspect sessions, token audience/validation/expiry/revocation, account recovery, privilege changes, role assignment, impersonation, support access, service accounts, default privileges, and confused-deputy paths. Check whether an audited actor can alter the evidence.

## Untrusted input

Trace input into queries, templates, commands, paths, URLs/redirects, parsers, interpreters, and rendered output. Assess safe APIs, parameterization, context-specific encoding, validation, and canonicalization at the actual boundary; a sanitizer's name proves nothing.

When present, inspect uploads, archive extraction, traversal, deserialization, cross-origin policy, request forgery, webhook authenticity/replay, and outbound request restrictions. AI-retrieved content and tool output must not grant action authority or bypass intended data boundaries.

## Secrets and infrastructure

Look for credential exposure in code/history within scope, artifacts, configuration, URLs, telemetry, errors, and client bundles. Inspect distribution, privilege, rotation, key access/lifecycle, transport/storage protection, backups/exports, and temporary files. Never expose values or test discovered credentials. Assess cryptography against its threat model using maintained facilities rather than demanding encryption without a purpose.

Review debug/admin endpoints, deployment defaults, public storage, network exposure, environment separation, and internal authentication. For supply-chain paths, inspect resolved versions, provenance, lockfiles, install/build hooks, untrusted pull-request inputs, CI permissions, and artifact publishing. Verify current advisories before specific vulnerability claims.

Check resource exhaustion, size/rate limits, costly operations, queue growth, concurrency races, retries/idempotency, and recovery for plausible security impact. Determine whether logs and alerts detect important abuse without leaking secrets, collecting excessive personal data, or permitting tampering.
