"""Extend the unchanged v0.35 inventory tool with reviewed v0.38 actions.
The old, hashed inventory implementation is never modified.
"""
from pathlib import Path
import runpy,json,collections
P=Path(__file__).resolve().parent
# Reuse all existing independent pointer, pool, width and place diagnostics.
g=runpy.run_path(str(P/'inventaire_tables_v035.py'))
O=g['O'];v=g['v'];key=g['version_key'];confirmed=g['confirmed'];out=g['out'];summary=g['summary'];regions=g['regions']
for p in P.glob('v*/revue-sorts-v*.json'):
 if key(p.parent.name)>key(v):continue
 for r in json.loads(p.read_text()):
  row=next(x for x in out if x['position']==r['position'])
  assert row['current']==r['french'] and row['sids']==r['runtime_sids']
  row['status']='FR_CONFIRME_PROJET';confirmed.add(r['position'])
summary['counts']=dict(collections.Counter(x['status'] for x in out));summary['counts'].setdefault('JAPONAIS_DETECTE',0)
summary['by_region']={t:dict(entries=sum(x['region']==t for x in out),statuses=dict(collections.Counter(x['status'] for x in out if x['region']==t))) for t,_,_ in regions}
summary['review_extension']='revue-sorts-v*.json, versions antérieures ou égales à la cible'
for t,_,_ in regions:(O/('inventaire-'+t+'.json')).write_text(json.dumps([x for x in out if x['region']==t],ensure_ascii=False,indent=2))
(O/'inventaire-tables.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print('Inventaire avec sorts relus:',summary['counts'])
