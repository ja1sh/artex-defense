"""Offline reference evaluator for this pack's documented Sigma subset.
Not a SIEM and not a general Sigma engine. Never executes event content.
"""
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
import yaml


def timestamp(value):
    t = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if t.tzinfo is None:
        raise ValueError('Timestamp must include a timezone')
    return t


def match(rule, event):
    detection = rule['detection']
    if detection['condition'] != 'selection':
        raise ValueError('Unsupported condition')
    for expression, expected in detection['selection'].items():
        field, *modifiers = expression.split('|')
        actual = event.get(field)
        if actual is None:
            return False
        values = expected if isinstance(expected, list) else [expected]
        if not modifiers:
            ok = any(type(actual) is type(v) and (actual.casefold() == v.casefold() if isinstance(v, str) else actual == v) for v in values)
        elif modifiers == ['startswith']:
            ok = isinstance(actual, str) and any(actual.casefold().startswith(v.casefold()) for v in values)
        else:
            raise ValueError('Unsupported modifier: ' + expression)
        if not ok:
            return False
    return True


def load_rules(root):
    if not (Path(root)/'rules').is_dir():
        raise ValueError('Rule directory missing; pass --root pointing to the repository')
    return [yaml.safe_load(p.read_text()) for folder in ('rules', 'vendor/theori')
            for p in sorted((Path(root)/folder).rglob('*.yml'))]


def evaluate(rules, events):
    atomic = {r['name']: r for r in rules if 'detection' in r}
    ordered = sorted(events, key=lambda e: (timestamp(e['Timestamp']), e['EventId']))
    if len({e['EventId'] for e in ordered}) != len(ordered):
        raise ValueError('Duplicate EventId')
    hits = {name: [e for e in ordered if match(rule, e)] for name, rule in atomic.items()}
    alerts = []
    # Atomic matches retain attribution. Context rules aren't actionable alerts on their own.
    for name, rows in hits.items():
        for e in rows:
            alerts.append({'rule':name,'kind':'atomic','author':atomic[name]['author'],
                           'events':[e['EventId']], 'Timestamp':e['Timestamp']})
    for rule in rules:
        if 'correlation' not in rule:
            continue
        c = rule['correlation']
        window = timedelta(minutes=int(c['timespan'].removesuffix('m')))
        def key(e):
            vals = tuple(e.get(k) for k in c['group-by'])
            return vals if all(v is not None and v != '' for v in vals) else None
        if c['type'] == 'temporal_ordered':
            if len(c['rules']) != 2:
                raise ValueError('Reference evaluator supports exactly two ordered stages')
            first, last = (hits[n] for n in c['rules'])
            for end in last:
                k = key(end)
                if k is None:
                    continue
                candidates = [start for start in first if key(start) == k and
                              timedelta(0) < timestamp(end['Timestamp'])-timestamp(start['Timestamp']) <= window]
                if candidates:
                    # One alert per final event; select most recent prior stage deterministically.
                    start = candidates[-1]
                    alerts.append({'rule':rule['name'],'kind':'correlation','author':rule['author'],
                                   'events':[start['EventId'],end['EventId']], 'Timestamp':end['Timestamp']})
        elif c['type'] == 'value_count':
            rows = hits[c['rules'][0]]
            field = c['condition']['field']
            threshold = c['condition']['gte']
            for end in rows:
                k = key(end)
                if k is None or not end.get(field):
                    continue
                bucket = [e for e in rows if key(e)==k and e.get(field) and
                          timedelta(0) <= timestamp(end['Timestamp'])-timestamp(e['Timestamp']) <= window]
                if len({e[field] for e in bucket}) >= threshold:
                    alerts.append({'rule':rule['name'],'kind':'correlation','author':rule['author'],
                                   'events':[e['EventId'] for e in bucket], 'Timestamp':end['Timestamp']})
        else:
            raise ValueError('Unsupported correlation')
    return alerts


def main():
    p = argparse.ArgumentParser()
    p.add_argument('input', type=Path)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    args = p.parse_args()
    events = [json.loads(line) for line in args.input.read_text().splitlines() if line.strip()]
    for alert in evaluate(load_rules(args.root), events):
        print(json.dumps(alert))

if __name__ == '__main__':
    main()
