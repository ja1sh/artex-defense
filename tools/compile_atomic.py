"""Compile atomic filters only; requires deployment index/field pipeline before use."""
from pathlib import Path
from sigma.collection import SigmaCollection
from sigma.backends.splunk import SplunkBackend
root=Path(__file__).resolve().parents[1]
lines=['# Generated atomic Splunk filters; not scheduled detections.',
       '# No index/sourcetype pipeline; normalize and scope before use.',
       '# Correlations are NOT included. Never treat these as attributable ARTEX alerts.']
for base in ['rules/atomic','vendor/theori']:
    for path in sorted((root/base).glob('*.yml')):
        rules=SigmaCollection.from_yaml(path.read_text())
        lines.append('\n# '+str(path.relative_to(root)))
        lines.extend(SplunkBackend().convert(rules))
output=root/'queries/atomic-splunk.txt'
output.write_text('\n'.join(lines)+'\n')
print(output)
