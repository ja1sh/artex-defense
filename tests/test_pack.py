import copy
import json
from pathlib import Path
import pytest
from sigma.collection import SigmaCollection
from artex_defense.engine import evaluate, load_rules, match

ROOT = Path(__file__).resolve().parents[1]
RULES = load_rules(ROOT)
ATOMIC = [r for r in RULES if 'detection' in r]

def event(i, **kw):
    return dict(EventId=str(i), Timestamp=f'2026-11-15T00:{i:02}:00Z', TenantId='lab',
                ApplicationId='demo', SessionId='session-a', ActorId='actor-a', **kw)

def corr(events):
    return [a for a in evaluate(RULES, events) if a['kind']=='correlation']

def test_sigma_parser():
    docs = '\n---\n'.join(p.read_text() for base in ['rules','vendor/theori'] for p in sorted((ROOT/base).rglob('*.yml')))
    parsed = SigmaCollection.from_yaml(docs)
    assert len(parsed.rules) == len(RULES)
    parsed.resolve_rule_references()

@pytest.mark.parametrize('rule', ATOMIC, ids=lambda r:r['name'])
def test_atomic_witness_and_each_missing_field(rule):
    e = {}
    for key, value in rule['detection']['selection'].items():
        e[key.split('|')[0]] = value[0] if isinstance(value,list) else value
    assert match(rule,e)
    for field in e:
        missing = dict(e); del missing[field]
        assert not match(rule,missing)
    assert not match(rule,{})

def test_order_scope_window_and_empty_keys():
    a = event(1, EventType='web', AttackCategory='sqli')
    b = event(2, EventType='auth', Outcome='success')
    assert len(corr([b,a]))==1  # ingestion order independent
    assert not corr([dict(a,Timestamp=b['Timestamp']),dict(b,Timestamp=a['Timestamp'])])
    assert not corr([a,dict(b,Timestamp='2026-11-15T00:12:00Z')])
    assert corr([a,dict(b,Timestamp='2026-11-15T00:11:00Z')])
    assert not corr([a,dict(b,Timestamp=a['Timestamp'])])
    for key in ['TenantId','ApplicationId','SessionId']:
        assert not corr([a,dict(b,**{key:'other'})])
        assert not corr([dict(a,**{key:''}),dict(b,**{key:''})])
        x=dict(a); y=dict(b); del x[key]; del y[key]
        assert not corr([x,y])

def test_distinct_secrets_and_actor_separation():
    events=[event(i,EventType='vault',Operation='SecretGet',Outcome='success',VaultId='vault-a',ResourceId=f'secret-{i}') for i in range(10)]
    assert len(corr(events))==1
    assert not corr(events[:9])
    assert not corr([dict(e,ResourceId='same') for e in events])
    assert not corr([dict(e,ActorId=str(i)) for i,e in enumerate(events)])
    assert not corr([dict(e,ResourceId='') for e in events])
    assert not corr([dict(e,VaultId='') for e in events])

def test_bad_input_rejected():
    e=event(1,EventType='auth',Outcome='success')
    with pytest.raises(ValueError,match='Duplicate'):
        evaluate(RULES,[e,e])
    with pytest.raises(ValueError,match='timezone'):
        evaluate(RULES,[dict(e,Timestamp='2026-11-15T00:00:00')])

@pytest.mark.parametrize('filename',['positive','benign','known_false_positive'])
def test_fixture_contract(filename):
    events=[json.loads(s) for s in (ROOT/'fixtures'/f'{filename}.jsonl').read_text().splitlines()]
    expected=json.loads((ROOT/'fixtures/expected.json').read_text())[filename]
    actual=sorted(a['rule'] for a in corr(events))
    assert actual==sorted(expected)

def test_unsupported_sigma_fails():
    r=copy.deepcopy(ATOMIC[0]); r['detection']['condition']='not selection'
    with pytest.raises(ValueError): match(r,{})

@pytest.mark.parametrize('rule',[r for r in RULES if r.get('correlation',{}).get('type')=='temporal_ordered'],ids=lambda r:r['name'])
def test_every_sequence_is_scoped_and_ordered(rule):
    c=rule['correlation']; atoms={r['name']:r for r in ATOMIC}
    rows=[]
    for i,name in enumerate(c['rules'],1):
        fields={k:(v[0] if isinstance(v,list) else v) for k,v in atoms[name]['detection']['selection'].items()}
        rows.append(event(i,**fields))
    def found(es): return [a for a in corr(es) if a['rule']==rule['name']]
    assert len(found(rows))==1
    assert not found([dict(rows[0],Timestamp=rows[1]['Timestamp']),dict(rows[1],Timestamp=rows[0]['Timestamp'])])
    assert not found([rows[0],dict(rows[1],Timestamp='2026-11-15T00:12:00Z')])
    for key in c['group-by']:
        assert not found([rows[0],dict(rows[1],**{key:'other'})])
        assert not found([dict(e,**{key:''}) for e in rows])

def test_upstream_bytes_and_credits():
    import hashlib
    for item in json.loads((ROOT/'UPSTREAM.json').read_text()):
        data=(ROOT/item['file']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==item['sha256']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['git_blob_sha']
    e=event(1,**{'cs-user-agent':'ARTEX-ENRICH/fixture'})
    a=evaluate(RULES,[e])
    assert len(a)==1 and a[0]['author']=='Xint'

def test_boolean_types_and_case():
    r=next(r for r in ATOMIC if r['name']=='ad_role_added')
    base=dict(r['detection']['selection'])
    assert match(r,dict(base,Outcome='SUCCESS'))
    assert not match(r,dict(base,Privileged='true'))
    assert not match(r,dict(base,Privileged=1))

def test_missing_repository_fails():
    with pytest.raises(ValueError,match='Rule directory missing'):
        load_rules(ROOT/'nonexistent')

def test_atomic_splunk_compilation_matches_checked_in():
    from sigma.backends.splunk import SplunkBackend
    output=(ROOT/'queries/atomic-splunk.txt').read_text()
    for base in ['rules/atomic','vendor/theori']:
        for p in sorted((ROOT/base).glob('*.yml')):
            queries=SplunkBackend().convert(SigmaCollection.from_yaml(p.read_text()))
            assert len(queries)==1 and queries[0] in output
