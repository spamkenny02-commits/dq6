"""Idempotent reviewed main-script batch v0.37; no table or engine changes."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;B=P/'v0.36';O=P/'v0.37'
def read(p):return json.loads(p.read_text())
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2))
O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
 if (O/name).exists():continue
 s=(B/name).read_text()
 if name!='names.py':
  s=s.replace('v0.36','__NEW__').replace('v0.35','__BASE__').replace('__NEW__','v0.37').replace('__BASE__','v0.36')
  s=s.replace('v036','v037').replace('correspondance_revue_v36','correspondance_revue_v37').replace('v35','v36')
 if name=='build.py':s=s.replace('5853','5854')
 (O/name).write_text(s)
for p in B.glob('*.json'):
 if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','audit-noms','audit-tables','inventaire-','lieux-prepares','nouveaux-cas-differes')):continue
 if not (O/p.name).exists():shutil.copy2(p,O/p.name)
r=read(O/'revue-lot-v037.json');assert len(r)==51 and len({x['id'] for x in r})==51
old={x['id'] for x in read(B/'insertion-candidates.json')};assert not old&{x['id'] for x in r}
jp=read(P/'clean-base/sfc-jp.json')
for x in r:assert x['status']=='RELU' and x['sfc_jp']==jp[x['id']]['text']
ids={x['id'] for x in r};oldr=read(B/'correspondances-revues.json')
save('revues-preparatoires-remplacees.json',[x for x in oldr if x['id'] in ids])
save('correspondances-revues.json',sorted([x for x in oldr if x['id'] not in ids]+r,key=lambda x:x['id']))
changed={x['id'] for x in r if 'adaptation_body' in x}
ad=[x for x in read(B/'adaptations-francaises.json') if x['id'] not in changed]
for x in r:
 if 'adaptation_body' in x:ad.append(dict(id=x['id'],file=x['file'],ids=x['ids'],original_body=x['original_body'],body=x['adaptation_body'],review=x['adaptation_review']))
save('adaptations-francaises.json',sorted(ad,key=lambda x:x['id']))
print('v0.37 inputs ready:',len(r))
