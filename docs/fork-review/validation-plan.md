# Defensive validation plan

Use synthetic, normalized events and the current ARTEX Defense [telemetry contract](../telemetry.md). Derive event types and expected rule IDs from the consumer's pinned pack, not from attacker source. The cases below are proposed tests, not executed SIEM validations.

| Case | Change to synthetic input | Expected result |
|---|---|---|
| V01: Fingerprint present | Existing archive-positive offline fixture | Legacy fingerprint can be a lead. Do not label it proof of tool or variant. |
| V02: Fingerprint absent | Use a generic header, then omit the header; keep identity, timestamps, and behavior events fixed | Legacy marker may stop matching; selected behavior correlation still has evidence if required fields are mapped. |
| V03: Localization | Change only human-facing report text, keeping event type and joins fixed | The normalized correlation result stays the same. |
| V04: Wrong actor and time | Split expected evidence across two actors, then put it outside the correlation window in a separate replay | No same-actor ordered correlation under the rule's contract. |
| V05: Approved change | Existing synthetic approved credential rotation | A match can be expected. Triage records verify owner and change context independently. |
| V06: Incomplete logging | Omit the required identity or resource join key in a separate run | Treat any non-match as a measured coverage gap; do not report “no activity.” |
| V07: Authorized deployment audit | Use synthetic success, denial and missing-log records | The ingest pipeline distinguishes decisions, tracks collection gaps and enforces retention/redaction policy. Not external tool attribution. |

Record backend and rule version, data sources and fields, fixture ID, expected versus observed rule ID, the result and any exceptions. Keep test data free of credentials and production identifiers. Start with behavior alerts in audit-only mode and review approved change patterns with the team operating those identities before tuning thresholds or adding exclusions.
