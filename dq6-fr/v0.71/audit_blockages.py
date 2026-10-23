"""Document exact-JA DS alternatives for unresolved positions; never approve them."""
from common import *
ledger=read(O/'registre-positions-0800-1199.json');fr={(x['file'].replace('/FR/','/JA/'),x['id']):x for x in read(R/'dq6-fr/clean-base/ds-fr.json')};ja=read(R/'dq6-fr/clean-base/ds-ja.json');index={}
for j in ja:
 if '/MENULIST6/JA/' in j['file'] and field(j['text']):index.setdefault(field(j['text']),[]).append(j)
rows=[]
for x in ledger:
 if not (x['status'].startswith('DIFFERE') or x['status']=='PREPARE_NON_INSERE'):continue
 candidates=[]
 for j in index.get(x['sfc_jp'],[]):
  f=fr.get((j['file'],j['id']))
  if f:candidates.append(dict(JA_file=j['file'],FR_file=f['file'],id=j['id'],JA_text=j['text'],FR_text=f['text'],extracted_label=field(f['text'])))
 rows.append(dict(position=x['position'],sids=x['sids'],current=x['current'],sfc_jp=x['sfc_jp'],status=x['status'],blocker=x['reason'],exact_JA_DS_alternatives=candidates,approved=False))
q=dict(release='v0.71',positions=rows,source='Restored Git JA/FR extractions; full Japanese label equality only, no fuzzy match.',limits='Alternative source records are context evidence, not approvals. Direct ROM field checks for insertion/proposals are counted separately in qa-lot400.json. No extra translation or review count from this report.')
(O/'blocages-v071.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(len(rows),'unresolved positions documented')
