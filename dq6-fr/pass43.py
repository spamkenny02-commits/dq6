"""Idempotent batch v0.43, reviewed item and contextual-name bindings."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;B=P/'v0.42';O=P/'v0.43';O.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text())
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2))
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
 if (O/name).exists():continue
 s=(B/name).read_text()
 if name!='names.py':s=s.replace('v0.42','__NEW__').replace('v0.41','__BASE__').replace('__NEW__','v0.43').replace('__BASE__','v0.42').replace('v41','v42')
 if name=='prepare.py':s=s.replace('v042','v043').replace('correspondance_revue_v42','correspondance_revue_v43')
 if name=='verify.py':s=s.replace('len(checked)==71','len(checked)==63')
 if name=='build.py':s=s.replace('6031','6102')
 (O/name).write_text(s)
if not (O/'spells.py').exists():shutil.copy2(B/'spells.py',O/'spells.py')
for p in B.glob('*.json'):
 if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','audit-noms','audit-tables','inventaire-','lieux-prepares')):continue
 if not (O/p.name).exists():shutil.copy2(p,O/p.name)
r=read(O/'revue-lot-v043.json');assert len(r)==63 and len({x['id'] for x in r})==63
old={x['id'] for x in read(B/'insertion-candidates.json')};assert not old&{x['id'] for x in r}
jp=read(P/'clean-base/sfc-jp.json')
for x in r:assert x['status']=='RELU' and x['sfc_jp']==jp[x['id']]['text']
ids={x['id'] for x in r};oldr=read(B/'correspondances-revues.json')
save('revues-preparatoires-remplacees.json',[x for x in oldr if x['id'] in ids])
save('correspondances-revues.json',sorted([x for x in oldr if x['id'] not in ids]+r,key=lambda x:x['id']))
ad=[x for x in read(B/'adaptations-francaises.json') if x['id'] not in ids]
bindings=read(B/'liaisons-variables-natives.json')
for x in r:
 change=dict(id=x['id'],file=x['file'],ids=x['ids'],original_body=x['original_body'],body=x['adaptation_body'],review=x['adaptation_review'])
 if 'adaptation_speaker' in x:change['speaker']=x['adaptation_speaker']
 ad.append(change)
 if 'native_bindings' in x:
  assert str(x['id']) not in bindings or bindings[str(x['id'])]==x['native_bindings']
  bindings[str(x['id'])]=x['native_bindings']
save('adaptations-francaises.json',sorted(ad,key=lambda x:x['id']));save('liaisons-variables-natives.json',bindings)
print('v0.43 inputs ready:',len(r))
