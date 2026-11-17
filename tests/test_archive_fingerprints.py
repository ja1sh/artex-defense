"""Offline compatibility checks, not execution of archived ARTEX."""
import json
from pathlib import Path
import pytest
from artex_defense.engine import evaluate, load_rules, match

ROOT = Path(__file__).resolve().parents[1]
RULES = load_rules(ROOT)
MANIFEST = json.loads((ROOT / 'docs/archive-provenance.json').read_text())

@pytest.mark.parametrize('item', MANIFEST['files'], ids=lambda x: x['path'])
def test_archived_exact_header(item):
    rule = next(r for r in RULES if r['name'] == item['matching_rule'])
    assert match(rule, {'cs-user-agent': item['observed_user_agent']})
    assert not match(rule, {})

@pytest.mark.parametrize('ua', ['Mozilla/5.0', 'Mozilla/5.0 (spa-api-reco)',
                               'artex-enric/1.0', 'prefix artex-enrich/1.0'])
def test_nonmatching_header_controls(ua):
    rules = [r for r in RULES if r['name'].startswith('web_artex_')]
    assert not any(match(r, {'cs-user-agent': ua}) for r in rules)

def test_archived_fixture_is_atomic_only_with_credit():
    events = [json.loads(s) for s in (ROOT / 'fixtures/archive_fingerprints.jsonl').read_text().splitlines()]
    assert [e['cs-user-agent'] for e in events] == [f['observed_user_agent'] for f in MANIFEST['files']]
    alerts = evaluate(RULES, events)
    assert len(alerts) == 3
    assert sorted(a['rule'] for a in alerts) == sorted(f['matching_rule'] for f in MANIFEST['files'])
    assert all(a['kind'] == 'atomic' and a['author'] == 'Xint' for a in alerts)
