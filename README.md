# ARTEX Defense Lab

**v0.1.0 • Experimental detection engineering • Synthetic validation**

A Sigma detection pack and offline purple-team test harness for ARTEX-relevant
behavior. Includes seven behavioral rules, five correlations and two upstream
Xint/Theori fingerprints, with fixtures, telemetry requirements and a validation
playbook.

![ARTEX Defense Lab workflow: normalize telemetry, apply seven behavioral rules and two upstream fingerprints, correlate five scenarios, and validate with positive, benign and known-false-positive fixtures. Synthetic tests are not attribution or production validation.](docs/assets/defense-workflow.svg)

## Original ARTEX source

We have cross-checked the existing fingerprints against the original
[ARTEX repository preserved by Software Heritage](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/Autumn-27/ARTEX),
pinned to revision `e6ec56999175509551a1e43a3ee3b053d0941bd9`.
See the [source mapping and limitations](docs/archived-source-review.md).
This is not a claim of complete attack-chain coverage or live validation.

The [fork comparison](docs/fork-review/README.md) checks three public ARTEX
variants against the pinned archive and outlines what to validate in your SIEM.

## Quick start

Python 3.10+ required. From this repository:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
make test
artex-replay fixtures/positive.jsonl --root .
artex-replay fixtures/benign.jsonl --root .
artex-replay fixtures/known_false_positive.jsonl --root .
```

Replay reads JSONL and emits JSON matches without executing event content or
contacting a target. Atomic matches provide context; filter on
`kind == "correlation"` for correlation alerts. The positive fixture produces five
alerts, the benign fixture produces none, and the approved credential-rotation
fixture produces one known false positive.

## Contents

- `vendor/theori/`: two unmodified Xint/Theori Sigma user-agent fingerprints.
- `rules/atomic/`: seven original, low-confidence context rules.
- `rules/correlation/`: ordered web/auth/data and cloud identity sequences;
  distinct secret-read threshold.
- `src/`: bounded offline reference evaluator, **not a general Sigma engine**.
- `tests/`, `fixtures/`: parser, reference, logic, scope, boundary and replay checks.
- [Purple-team playbook](docs/purple-team-playbook.md)
- [Telemetry contract and deployment](docs/telemetry.md)
- [Coverage and evidence](docs/coverage.md)
- [Sources and licensing](docs/sources.md)

## Testing and deployment

The test suite checks Sigma parsing and rule references, atomic matching,
correlation order and time windows, identity boundaries, distinct counts, upstream
file integrity and atomic Splunk query compilation. Synthetic fixtures cover
positive sequences, benign activity and an approved-automation false positive.

Live ARTEX execution and SIEM runtime behavior have not been validated. Matches
identify behavior or fingerprints, not attribution to ARTEX.

Map source telemetry to the documented normalized schema before deployment. The
offline evaluator supports this pack's selection, two-stage ordered and
distinct-count logic; it is not a general Sigma engine. Validate field mappings
and correlation semantics in your SIEM, then baseline in audit-only mode.

## Contributing and deployment readiness

Start with a reproducible fixture, expected matches and a clear telemetry mapping.
Include a benign counterexample and explain tuning tradeoffs when proposing rules.
Do not submit credentials, personal data or customer logs. See the
[deployment readiness checklist](docs/release-checklist.md) before operational use.
The offline evaluator has no outbound telemetry and never executes event content.

## License

Original code, documentation and original rules: MIT (`LICENSE`). Vendored rules:
Detection Rule License 1.1 (`vendor/theori/LICENSE`); preserve Xint attribution,
source links and license, including attribution in match output. See
`UPSTREAM.json` for pinned Git blob identifiers and byte checksums.
