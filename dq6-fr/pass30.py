"""Idempotent reviewed v0.30 delta, based on published v0.29."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;B=P/'v0.29';O=P/'v0.30'
def read(p):return json.loads(p.read_text())
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2))
O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
 if(O/name).exists():continue
 s=(B/name).read_text().replace('v0.29','VERSION_NEW').replace('v0.28','VERSION_BASE').replace('VERSION_NEW','v0.30').replace('VERSION_BASE','v0.29').replace('v029','v030').replace('v28','v29')
 if name=='build.py':s=s.replace('len(rows)-5552','len(rows)-5616')
 if name=='prepare.py':
  s=s.replace('correspondance_revue_v29','correspondance_revue_v30')
  s=s.replace('SPECIFIC_SPEAKERS={',"SPECIFIC_SPEAKERS={6748:('司会','＊'),6751:('司会','＊'),")
  s=s.replace("{1111:'Le frère'","{6748:'Présentateur',6751:'Présentateur',1111:'Le frère'")
 (O/name).write_text(s)
for p in B.glob('*.json'):
 if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','progression-','audit-noms','audit-tables','inventaire-','lieux-prepares','blocages-restants')):continue
 if not(O/p.name).exists():shutil.copy2(p,O/p.name)
r=read(O/'revue-lot-v030.json');assert len(r)==114 and len({x['id'] for x in r})==114
old={x['id'] for x in read(B/'insertion-candidates.json')};assert not old&{x['id'] for x in r}
jp=read(P/'clean-base/sfc-jp.json')
for x in r:assert x['status']=='RELU' and x['sfc_jp']==jp[x['id']]['text']
ids={x['id'] for x in r};oldr=read(B/'correspondances-revues.json');save('revues-preparatoires-remplacees.json',[x for x in oldr if x['id'] in ids]);save('correspondances-revues.json',sorted([x for x in oldr if x['id'] not in ids]+r,key=lambda x:x['id']))
ids={x['id'] for x in r if 'adaptation_body'in x};ad=[x for x in read(B/'adaptations-francaises.json') if x['id'] not in ids]
for x in r:
 if 'adaptation_body'in x:ad.append(dict(id=x['id'],file=x['file'],ids=x['ids'],original_body=x['original_body'],body=x['adaptation_body'],review=x['adaptation_review']))
save('adaptations-francaises.json',sorted(ad,key=lambda x:x['id']))
print('v0.30 inputs ready',len(r))
