"""Idempotent reviewed v0.32 delta, based on published v0.31."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;B=P/'v0.31';O=P/'v0.32'
def read(p):return json.loads(p.read_text())
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2))
O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
 if(O/name).exists():continue
 s=(P/'v0.30'/name).read_text().replace('v0.30','VERSION_NEW').replace('v0.29','VERSION_BASE').replace('VERSION_NEW','v0.32').replace('VERSION_BASE','v0.31').replace('v030','v032').replace('v29','v31')
 if name=='build.py':s=s.replace('len(rows)-5616','len(rows)-5731')
 if name=='prepare.py':s=s.replace('correspondance_revue_v30','correspondance_revue_v32')
 (O/name).write_text(s)
for p in B.glob('*.json'):
 if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','progression-','audit-noms','audit-tables','inventaire-','lieux-prepares','blocages-restants')):continue
 if not(O/p.name).exists():shutil.copy2(p,O/p.name)
r=read(O/'revue-lot-v032.json');assert len(r)==1 and len({x['id'] for x in r})==1
old={x['id'] for x in read(B/'insertion-candidates.json')};assert not old&{x['id'] for x in r}
jp=read(P/'clean-base/sfc-jp.json')
for x in r:assert x['status']=='RELU' and x['sfc_jp']==jp[x['id']]['text']
ids={x['id'] for x in r};oldr=read(B/'correspondances-revues.json');save('revues-preparatoires-remplacees.json',[x for x in oldr if x['id'] in ids]);save('correspondances-revues.json',sorted([x for x in oldr if x['id'] not in ids]+r,key=lambda x:x['id']))
ids={x['id'] for x in r if 'adaptation_body'in x};ad=[x for x in read(B/'adaptations-francaises.json') if x['id'] not in ids]
for x in r:
 if 'adaptation_body'in x:ad.append(dict(id=x['id'],file=x['file'],ids=x['ids'],original_body=x['original_body'],body=x['adaptation_body'],review=x['adaptation_review']))
save('adaptations-francaises.json',sorted(ad,key=lambda x:x['id']))
bindings=read(B/'liaisons-variables-natives.json');bindings['1836']={'%a002240':0xb2,'%a000140':0xd3};save('liaisons-variables-natives.json',bindings)
print('v0.32 inputs ready',len(r))
