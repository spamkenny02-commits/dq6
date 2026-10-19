"""Idempotent SFC-aware review delta v0.29, retaining v0.28 accepted tokens."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;B=P/'v0.28';O=P/'v0.29'
def read(p):return json.loads(p.read_text())
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2))
O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
 if (O/name).exists():continue
 s=(B/name).read_text().replace('v0.28','VERSION_NEW').replace('v0.27','VERSION_BASE').replace('VERSION_NEW','v0.29').replace('VERSION_BASE','v0.28').replace('v028','v029').replace('v27','v28')
 if name=='build.py':s=s.replace('len(rows)-5402','len(rows)-5552')
 if name=='prepare.py':
  s=s.replace("assert body==change['original_body']","assert body==change['original_body'],s['id']")
  s=s.replace('correspondance_revue_v28','correspondance_revue_v29')
  s=s.replace('SPECIFIC_SPEAKERS={',"SPECIFIC_SPEAKERS={1111:('弟','＊'),6749:('司会','＊'),5252:('神父','＊'),")
  s=s.replace("c['ja'][1] if mid==3256 else c['ja'][0]", "c['ja'][{3256:1,1203:2,5036:2,5040:1}.get(mid,0)]")
  s=s.replace("speaker=c['speaker'];body=c['body']", "if s['id']==2300:actor=None # Anonymous opening before her name is spoken.\n speaker={1111:'Le frère',6749:'Présentateur',5252:'Prêtre'}.get(s['id'],c['speaker']);body=c['body']")
 (O/name).write_text(s)
for p in B.glob('*.json'):
 if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','progression-','audit-noms','audit-tables','inventaire-','lieux-prepares')):continue
 if not(O/p.name).exists():shutil.copy2(p,O/p.name)
r=read(O/'revue-lot-v029.json');assert len(r)==64 and len({x['id'] for x in r})==64
old={x['id'] for x in read(B/'insertion-candidates.json')};assert not old&{x['id'] for x in r}
jp=read(P/'clean-base/sfc-jp.json')
for x in r:assert x['status']=='RELU' and x['sfc_jp']==jp[x['id']]['text']
ids={x['id'] for x in r};oldr=read(B/'correspondances-revues.json');save('revues-preparatoires-remplacees.json',[x for x in oldr if x['id'] in ids]);save('correspondances-revues.json',sorted([x for x in oldr if x['id'] not in ids]+r,key=lambda x:x['id']))
ids={x['id'] for x in r if 'adaptation_body'in x};ad=[x for x in read(B/'adaptations-francaises.json') if x['id'] not in ids]
for x in r:
 if 'adaptation_body'in x:ad.append(dict(id=x['id'],file=x['file'],ids=x['ids'],original_body=x['original_body'],body=x['adaptation_body'],review=x['adaptation_review']))
save('adaptations-francaises.json',sorted(ad,key=lambda x:x['id']))
save('audit-candidats-differes.json',[x for x in read(B/'audit-candidats-differes.json') if x['id'] not in {y['id'] for y in r}])
print('v0.29 inputs ready:',len(r))
