# ARTEX Defense Lab

**Private preview • v0.1.0 • experimental detections, not verified attribution**

A small, runnable purple-team starter that builds on existing Sigma work rather
than claiming every agent-assisted intrusion needs a new signature. Two attributed
upstream fingerprints complement seven new normalized telemetry building blocks
and five correlations. The contribution is a reproducible validation/playbook
layer, not a claim to be the first ARTEX detection repository.

## Run in five minutes

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

Replay reads JSONL and prints JSON matches; **it never executes event content or
contacts a target**. Atomic context matches are not actionable alerts. Filter on
`kind == "correlation"` to see the five positive scenario alerts. Benign has no
correlation alerts. Approved credential rotation deliberately produces one alert
in `known_false_positive`, showing why tuning and human investigation matter.

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

## What is and isn't validated

All shipped YAML parses with pySigma and correlation references resolve. Tests
exercise synthetic normalized records only. No ARTEX binary, real intrusion,
customer telemetry, endpoint lab or SIEM execution was used. These rules are
**hypotheses for behavior detection**, not evidence of ARTEX attribution. The
upstream strings are changeable fingerprints; absence of matches proves nothing.

The custom logsource requires your own normalization. Do not deploy directly
against raw Entra, Graph, WAF or Key Vault logs. The fixture evaluator intentionally
supports only this pack's selection + two-stage ordered/value-count subset;
backend correlation/window semantics must be validated before enabling alerts.
Start in audit-only mode. No destructive playbooks or automated response.

## Privacy and release

Keep this preview private. No public release, publishing workflow, outbound
telemetry or credentials are included. See `docs/release-checklist.md` before any
future public release. This repository does not create or authorize a public post.

## License

Original code, documentation and original rules: MIT (`LICENSE`). Vendored rules:
Detection Rule License 1.1 (`vendor/theori/LICENSE`); preserve Xint attribution,
source links and license, including attribution in match output. See
`UPSTREAM.json` for pinned Git blob identifiers and byte checksums.
