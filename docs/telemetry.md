# Telemetry contract and deployment

## Common fields

Each JSONL record has unique `EventId` (string), timezone-qualified ISO-8601
`Timestamp` (event time), and the fields below. Keep identifiers as strings and
`Privileged` as a JSON Boolean. Normalize operations to the exact vocabulary.
Missing or empty correlation group keys are rejected rather than merged into an
unknown-user bucket. Identifiers must be stable, canonical and tenant scoped.
The evaluator compares selection strings case-insensitively; grouping identifiers
remain case-sensitive. Boolean `true` is not the string `"true"` or integer `1`.

| EventType | Required context and selection fields | Candidate raw sources |
|---|---|---|
| web | TenantId, ApplicationId, SessionId, AttackCategory=sqli/rce/path_traversal | WAF/access/application security logs |
| auth | same correlation keys, Outcome=success | application authentication audit |
| data_access | same keys, Outcome=success, Sensitivity=restricted | application/database audit plus data classification |
| graph | TenantId, ActorId, Operation=applications.list/servicePrincipals.list/roleAssignments.list, Outcome=success | Microsoft Graph activity logs |
| audit | TenantId, ActorId, Operation=application.credential.add or directory.role.assign, Outcome=success; Privileged=true for role event | Entra audit logs |
| vault | TenantId, ActorId, VaultId, ResourceId, Operation=SecretGet, Outcome=success | Key Vault data-plane diagnostic logs |

For upstream fingerprints, preserve `cs-user-agent` from reverse proxy/access
logs. A web fingerprint alone does not require custom EventType.

## Mapping is an engineering prerequisite

These are candidate sources, not certified parsers. Provision their audit logging
first. Map Graph URI/method into operation labels; distinguish successful server
results from attempted calls. Resolve the **initiating principal**, not the target
app/user, into ActorId. Resolve role privilege from an authoritative role catalog.
Use stable secret identity for ResourceId (not request ID; decide and document
whether versions count together). Deduplicate replicated events by EventId.

For web chains, SessionId must be a trusted application correlation identity
available at every stage. Never equate IP address or user-agent with a session.
If a malicious probe has no trustworthy session identifier, this pack intentionally
cannot correlate it to a later login. Preserve separate pre-auth and post-auth
session linkage in a verified enrichment step; do not guess it.

Normalize redacted samples and retain original event references securely. Test
tenant isolation, app boundaries, clocks, stale enrichments, late arrival and audit
gaps. False matches from a shared administrator/service principal are possible.

## Deploy progressively

1. Collect and normalize audit-only samples; confirm mandatory field completeness.
2. Parse with pySigma, then select a backend supporting the correlation types.
3. Convert using an explicit field/logsource pipeline for your SIEM. Without it,
   custom fields do not magically correspond to Microsoft/Splunk native fields.
4. Replay positive, benign and approved-automation cases in a test index. Compare
   event-time order, inclusive ten-minute boundaries and distinct-count behavior.
5. Measure 7–14 days of baseline and investigation yield; tune by tenant, workload,
   change ticket and approved identity. Do not blanket-allow all cloud admins.
6. Deduplicate/suppress repeated alerts in the SIEM with an investigation-aware key.
   The reference evaluator deliberately emits every qualifying terminal event.
7. Promote only after a documented analyst review. Keep automated response off.

No production-ready query or raw-log adapter is claimed in v0.1.0. The runnable
interface is the normalized JSONL contract; SIEM integration is a separate gate.

## Optional compiler smoke check

`python tools/compile_atomic.py` reproduces `queries/atomic-splunk.txt` with
pySigma-backend-splunk 1.1.3. Tests check those nine atomic filters compile and
match the checked-in output. They have **no index/sourcetype scoping or raw field
mapping** and do not implement the five correlations. Compilation is not runtime
validation; do not schedule these informational building blocks as alerts.
