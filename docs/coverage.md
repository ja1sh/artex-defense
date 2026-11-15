# Coverage and evidence ledger

| Rule/group | Observation or hypothesis | Tested here | Important limitation |
|---|---|---|---|
| Xint api-recon UA | Upstream ARTEX-associated fingerprint | prefix match, missing field | Operator can change header; can be spoofed |
| Xint enrich UA | Upstream ARTEX-associated fingerprint | prefix match, missing field | Not proof of compromise |
| probe → successful auth | Suspicious same-session progression | positive, order/window/scope boundaries | Requires trustworthy session stitching; tests not exploitation evidence |
| auth → restricted read | Same-session access to classified content | synthetic sequence | Extremely common legitimate activity; enrich risk |
| Graph discovery → credential add | Identity discovery preceding persistence-capable change | synthetic sequence and approved CI collision | Admin automation triggers it; actor not necessarily attacker |
| Graph discovery → privileged role add | Discovery before privilege assignment | synthetic sequence | Onboarding and break-glass workflows |
| 10 distinct secret reads / 10m | Concentrated secret access | distinctness/identity/threshold fixtures | Deployment jobs and backup; slow reads evade threshold |

The seven atomics support these five behavior correlations. They are **not seven
independent high-fidelity detections**. Informational severity is intentional.

FBI/Microsoft reporting motivates phases and telemetry, not every literal
threshold or normalized label. Ten minutes and ten secrets are initial hypotheses,
not measured ARTEX constants. No precision/recall, runtime cost, malicious capture,
coverage percentage or attribution accuracy has been measured.

Existing ecosystem: Theori's aipt-detections already provides ARTEX indicators;
jiwoochris/artex-global also addresses correlations and synthetic validation. This
preview does not assert novelty over those projects. It adds a small inspectable
starter tailored to a normalized telemetry/playbook workflow.
