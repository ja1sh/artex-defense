# Release checklist

- [x] Original/vendored material separated, license and source identities retained.
- [x] Synthetic positive, benign and known-false-positive fixtures supplied.
- [x] Offline validation and Sigma parser/reference tests supplied.
- [ ] Real normalized telemetry adapter reviewed by source owner.
- [ ] SIEM backend query compilation and execution validated.
- [ ] Live authorized lab validation and baseline noise measurement.
- [ ] Detection engineering peer review and identity/threshold tuning.
- [ ] User explicitly approves public release and accompanying social claims.

Keep repository visibility private until that final approval. Do not advertise
"detects ARTEX" or publish efficacy numbers from synthetic replay. A defensible
future description: “An experimental Sigma/purple-team starter for validating
ARTEX-relevant behavior hypotheses, with upstream fingerprints and honest
false-positive fixtures.”
