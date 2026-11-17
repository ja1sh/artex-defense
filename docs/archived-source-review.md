# Archived original ARTEX: source cross-check

Reviewed 2026-11-17. ARTEX Defense Lab now takes into account the original
`Autumn-27/ARTEX` source preserved in [Software Heritage](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/Autumn-27/ARTEX),
not only third-party reports. This is a defensive source comparison, not a fork
or redistribution of the original program.

## Version and provenance

The inspected archive visit is **2026-10-07 14:25:51 UTC**, with tip revision
`e6ec56999175509551a1e43a3ee3b053d0941bd9` (commit message identifies 0.3.15)
and directory `swh:1:dir:bcee5171ddb6ce4d8daacbd13b6b36d5f7601b2b`.
The two vendored Theori rules already reference this same revision through a
GitHub mirror. The archive independently supplies the original-origin context.

This pins the publicly archived version considered here. It does **not** prove
that every circulated copy, deployed binary or incident used identical bytes.
The mutable origin/HEAD link is for navigation; the content identifiers in
[the provenance manifest](archive-provenance.json) identify inspected files.

## What was checked against the code

| Archived file | Observed request behavior | Existing coverage |
|---|---|---|
| [`enrich/enrich.go`](https://archive.softwareheritage.org/browse/content/sha1_git:7c8fc13ee74d60790c880df49ed319854f7f3f0a/?origin_url=https://github.com/Autumn-27/ARTEX&path=bcee5171ddb6ce4d8daacbd13b6b36d5f7601b2b/enrich/enrich.go), L233 | `doHTTP` sends a GET to its supplied URL and sets `artex-enrich/1.0` | `web_artex_enrich_user_agent` |
| [`skills/api-recon/scripts/harvest_static.py`](https://archive.softwareheritage.org/browse/content/sha1_git:d1974c55007e8f5a36e7e8e85893a61eebc9b92c/?origin_url=https://github.com/Autumn-27/ARTEX&path=bcee5171ddb6ce4d8daacbd13b6b36d5f7601b2b/skills/api-recon/scripts/harvest_static.py), L23 | Static HTML/JavaScript retrieval sets `Mozilla/5.0 (spa-api-recon)` | `web_artex_api_recon_user_agent` |
| [`skills/api-recon/scripts/spider_mpa.py`](https://archive.softwareheritage.org/browse/content/sha1_git:d91f2f71a4df696f28bba3f65de726de3c1b6c7a/?origin_url=https://github.com/Autumn-27/ARTEX&path=bcee5171ddb6ce4d8daacbd13b6b36d5f7601b2b/skills/api-recon/scripts/spider_mpa.py), L22 | HTML crawling sets `Mozilla/5.0 (spa-api-recon spider)` | `web_artex_api_recon_user_agent` |

The existing prefix selections match all three exact strings, so the upstream
rules remain unmodified. New source-derived fixture checks exercise those values,
ordinary-browser and near-prefix controls, and attribution preservation. A fixture
match verifies our evaluator's logic, not a captured ARTEX run.

`enrich.go` takes a caller-supplied URL, has a per-asset cooldown, and disables
redirect following in its HTTP client. Do not read the vendored description's
“single GET to the root” as a proof of a once-only, root-only invariant across the
whole program. A copied header can also match; a changed header can evade these
rules. Preserve the upstream rule text for integrity, but apply these local
interpretation limits during triage.

## What this does not establish

The archived README describes planner/worker agents, asset and exploration graphs,
and shared task planning. Those design descriptions do not establish that this
pack's exact web/auth/data or Microsoft Graph/vault sequences occurred in a real
run. PT-01 through PT-05 remain report-motivated, generic behavioral hypotheses.
Their ten-minute windows and ten-secret threshold are not source-derived ARTEX
constants. No new high-confidence correlation is claimed from this inspection.

The review covered the three request-producing files above, the README and the
license, not all source, branches, dependencies, releases or runtime behavior.
No original ARTEX code was executed, imported, copied or deployed. No target was
contacted. Live SIEM validation and end-to-end telemetry remain outstanding.

## Attribution and license boundary

Credit the original ARTEX authors, including Autumn-27, and Software Heritage for
preservation. The archived root LICENSE contains GNU AGPL v3; its README identifies
AGPL-3.0 and also includes local-study-only use language. This repository links to
that material rather than incorporating the program. Its MIT license does not
relicense original ARTEX; the separately vendored Theori rules remain under DRL
1.1. Any future code import needs a separate license/notice review.
