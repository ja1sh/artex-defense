# ARTEX Defense Diff
**Defender-focused source comparison · 25 November 2026**

**Bottom line:** Keep ARTEX User-Agent matches as triage leads, not as the primary control or proof of attribution. Prioritize behavior tied together by identity, resource, and time. Confirm visibility in the SIEM before interpreting a non-match as an absence of activity.

## Scope and provenance

Baseline: Autumn-27/ARTEX 0.3.15, revision `e6ec56999175509551a1e43a3ee3b053d0941bd9`, directory `swh:1:dir:bcee5171ddb6ce4d8daacbd13b6b36d5f7601b2b`, original archive visit 7 October 2026 14:25:51 UTC, per the [ARTEX Defense source review](../archived-source-review.md). The [Software Heritage revision page](https://archive.softwareheritage.org/browse/revision/e6ec56999175509551a1e43a3ee3b053d0941bd9/) did not return readable contents on this pass; the seven selected baseline paths were checked at the same Git revision via RuoJi6, not against a newly downloaded archive. This pins a public snapshot, not the build used in any incident. Public availability is not evidence of adoption or malicious use.

| Comparison target | Pinned source | What Git history establishes |
|---|---|---|
| BaaRai/ARTEX | [3cb0638](https://github.com/BaaRai/ARTEX/commit/3cb06383fd99ffe7686abe1d375de11da7cfad54) | Diverged: 1,437 commits ahead / 444 behind, with an older merge base (`ad9f14f`). Its three-dot diff starts at that merge base, not at the archived tip. Use the selected exact blob comparisons for baseline-vs-head statements. |
| RuoJi6/ARTEX | [253a8ee](https://github.com/RuoJi6/ARTEX/commit/253a8eeac3b278cd4ff383674a31a0edcc34e143) | The archived tip is an ancestor; 310 commits ahead and 0 behind at review time. This verifies lineage, not the maintainer’s identity or authorization claims. |
| jiwoochris/artex-global | [06b36d7](https://github.com/jiwoochris/artex-global/commit/06b36d7219244c5e2b6467394f60eca160c785cf) | The compare endpoint returned 404. Its changelog describes a 0.3.15-derived edition, but ancestry was not established here. Selected file contents can still be compared against the baseline. |

GitHub returned 300 changed-file rows for each successful compare, the endpoint's documented cap; those counts are not total churn. The three-dot result is for ancestry; the CSV compares selected file blobs directly. The seven paths per fork cover docs and packaging, not an exhaustive source diff. SHA differences show changed bytes, not which behavior changed. This study did not execute any fork or verify any release binary, live detection, or attacker technique.

## What changed, piece by piece

| Surface | BaaRai | RuoJi6 | artex-global | What changes for defense |
|---|---|---|---|---|
| HTTP fingerprint confidence | Documents a recognizable scanner marker for approved assessments as optional. | Documents variable User-Agent behavior in supported HTTP components. | No pinned evidence in this review that the archived marker is reliable across this fork. | A match is one lead. Absence is not clearance. Validate coverage using application, identity, cloud, and endpoint records; do not try to attribute a fork from the header alone. |
| Product-side audit and access | Changelog describes added fact provenance and clearer approval/audit outcomes. The two-graph shape itself is not counted as new. | Documents an optional MCP service with a separate token boundary and call audit, plus backups that omit operational server logs. | Changelog documents failed login/initialization logging and session invalidation on password change. These are maintainer-described, not runtime-verified. | For an **authorized internal instance** collect independent identity and access decisions, and send audit evidence off-host where appropriate. Restore and audit retention are separate checks. A targeted organization ordinarily sees its own telemetry, not an external operator’s console. |
| Human-readable outputs | Changelog adds UI localization; no claim of normalized event changes. | No reviewed evidence establishes a multilingual output guarantee. | English default with Korean, Chinese, Spanish and Japanese options. Maintainer distinguishes localized reports/UI from server console logs and notes that runtime values can retain their own language. | Parse stable event fields; don't build rules around exact wording or assume all sources follow the display language. Test missing or mixed-language fields separately. |
| Packaging and provenance | Compose uses a locally tagged application image; release workflow contains SBOM generation and GitHub build attestation steps. A configured workflow is not proof of an attestation for any specific artifact. | Compose references the maintainer’s image rather than the original; the release workflow and Dockerfile blob both changed. | Compose references the edition’s GHCR image; the pinned head updates the release source. | For sanctioned tooling, inventory the repository, build revision, registry and image digest. Check attestations for the artifact in hand. Neither a mutable tag nor a repository name is runtime identity. |

Evidence: pinned [BaaRai README](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/README.md), [BaaRai changelog](https://github.com/BaaRai/ARTEX/blob/3cb06383fd99ffe7686abe1d375de11da7cfad54/CHANGELOG.md), [RuoJi6 README](https://github.com/RuoJi6/ARTEX/blob/253a8eeac3b278cd4ff383674a31a0edcc34e143/README.md), [RuoJi6 changelog](https://github.com/RuoJi6/ARTEX/blob/253a8eeac3b278cd4ff383674a31a0edcc34e143/CHANGELOG.md), [artex-global changelog](https://github.com/jiwoochris/artex-global/blob/06b36d7219244c5e2b6467394f60eca160c785cf/CHANGELOG.en.md), and the per-file links in the [file evidence table](file-evidence.csv). The defensive emphasis on correlating logs is also consistent with [UK NCSC's November 24 guidance](https://www.ncsc.gov.uk/blogs/familiar-weaknesses-exploited-faster-defending-against-agentic-cyber-attacks).

## What matters to a detection team

1. **Check the joins first.** For the [existing ARTEX Defense pack](https://github.com/ja1sh/artex-defense), the archive cross-check supports its original fingerprints. Carry the behavioral rules and correlations forward as candidates, not certified fork coverage. Verify that gateway, identity and control-plane logs preserve consistent principals and resource IDs; make missing join fields visible as a coverage gap.
2. **Separate a lead from attribution.** Report behavior matches as suspicious activity, or compatible with ARTEX-style behavior if warranted. Require corroborating evidence before assigning a tool or version. Keep the approved-automation false-positive fixture as a baseline; investigate the account’s expected role and change record rather than suppressing everything from that account.
3. **Verify in audit-only mode.** Run the [companion validation plan](validation-plan.md) using generated logs, not the forks. Scope the first rollout to sources with reliable normalization. Compare expected results with the actual SIEM backend's ordered joins and negative controls. No live or production results are claimed here.
4. **For a researcher, preserve two kinds of evidence.** Re-pin each revision on update, check ancestry separately from file content, and label claims as source-verified, maintainer-described, or not checked. Prioritize new logging, schema, custody, and artifact-provenance changes before prose or branding differences.

## Files

- [revisions.json](revisions.json): pinned heads, archive identifiers and comparison status.
- [file-evidence.csv](file-evidence.csv): 21 path comparisons (seven per fork), with exact blob IDs and links where present.
- [validation-plan.md](validation-plan.md): defender-side acceptance checks to apply to the existing detection pack.

The review includes no fork source, payloads or instructions for operating the frameworks. It changes no detection rules.
