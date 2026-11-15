# Purple-team playbook: safe first validation

## Objective and authorization

Determine whether telemetry can expose suspicious web-to-access and cloud identity
chains without claiming ARTEX attribution. First pass is **offline only**. No
scanner, exploit, persistence, secret extraction or ARTEX execution is included.
Use synthetic values; never insert real credentials or restricted customer data.

For a later live lab, obtain written scope, tenant/hosts, owner, test identities,
change window, rollback and stop conditions. Use an isolated non-production tenant,
nonprivileged test accounts and dummy secrets. This document is not authorization
to perform those actions. Operator and defender must agree on every state change.

## Roles and setup

- Operator: prepares approved event fixtures and records timestamps/EventIds.
- Defender: owns normalization, correlation deployment, alert/triage evidence.
- Observer: checks expected outcomes, privacy, noise and teardown.

Run the README installation and `make test` first. Record Python/dependency
versions and git commit. Start with `fixtures/positive.jsonl`; no target needed.

## Offline scenarios

| ID | Sequence | Expected correlation | Defender evidence |
|---|---|---|---|
| PT-01 | classified WAF probe, later successful auth, same trusted session | ad_probe_then_login | both EventIds, app/session/tenant, event times |
| PT-02 | successful auth, later restricted data access | ad_login_then_sensitive_read | classification source and access outcome |
| PT-03 | Graph discovery then app credential addition by same actor | ad_discovery_then_credential | initiator vs target app; change approval |
| PT-04 | Graph discovery then privileged role assignment | ad_discovery_then_role | authoritative role privilege enrichment |
| PT-05 | ten distinct successful dummy secret reads in ten minutes | ad_bulk_secrets | actor/vault/tenant and distinct secret identities |

```sh
artex-replay fixtures/positive.jsonl --root . > /tmp/artex-positive.jsonl
artex-replay fixtures/benign.jsonl --root . > /tmp/artex-benign.jsonl
artex-replay fixtures/known_false_positive.jsonl --root . > /tmp/artex-ci.jsonl
python -m pytest -q
```

Positive pass: each expected correlation in `fixtures/expected.json` occurs once.
Benign pass: no correlations (atomic context matches are expected). CI collision
pass: approved rotation **does alert**; analyst recognizes it using the change
ticket, not by pretending the detector is perfectly precise.

## Required negative controls

Use the automated tests to vary time ordering, exactly ten minutes vs just outside,
missing grouping identity, different session/tenant/actor, repeated reads of one
secret, nine vs ten distinct secrets and duplicate EventIds. Add a new fixture
whenever an analyst finds a real false positive or normalization failure. Never
modify expected results merely to make tests green; explain the behavioral change.

## Analyst triage

1. Confirm logging/enrichment correctness and original event references.
2. Establish initiator, tenant, affected app/vault and successful vs attempted action.
3. Check authorized activity and change window. Validate with owner out of band.
4. Review adjacent sign-ins/audit events and affected resources under local policy.
5. Escalate through the incident process if unexplained. Do not label the actor
   ARTEX solely from speed, an LLM endpoint, a matching UA or these correlations.

## Evidence and exit criteria

Store redacted fixture, commit, expected vs actual alerts, field completeness,
clock skew, known false positives, analyst decision and rule-tuning rationale.
An offline pass means logical consistency only. A deployment pass additionally
requires real test-index mapping and backend semantics validation, an agreed noise
budget, logging-gap monitoring and an owner. No live validation is claimed here.
Teardown any later lab changes and revoke test access under the approved plan.
