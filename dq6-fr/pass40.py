"""Idempotent batch v0.40, explicit native numeric/name bindings only."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;B=P/'v0.39';O=P/'v0.40';O.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text())
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2))
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
 if (O/name).exists():continue
 s=(B/name).read_text()
 if name not in ['names.py']:
  s=s.replace('v0.39','__NEW__').replace('v0.38','__BASE__').replace('__NEW__','v0.40').replace('__BASE__','v0.39').replace('v38','v39')
 if name=='prepare.py':
  s=s.replace('v039','v040').replace('correspondance_revue_v39','correspondance_revue_v40')
  s=s.replace('0xb2,0xc5};ALLOWED','0xb2,0xc5,0xb5};ALLOWED')
  s=s.replace('return sum(8 if ch','return sum(24 if ch==marker(0xb5) else 22 if ch==marker(0xb2) else 8 if ch')
  s=s.replace('for control in [0xbb,0xc1,0xb2,0xc5]:','for control in [0xbb,0xc1,0xb2,0xc5,0xb5]:')
  s=s.replace('def speaker_key(label,mid):',"SPECIFIC_SPEAKERS.update({6646:('司会','＊'),6647:('司会','＊')})\ndef speaker_key(label,mid):")
  s=s.replace("  body=change['body']","  body=change['body']\n  if 'speaker' in change:speaker=change['speaker']")
 if name=='verify.py':
  s=s.replace('len(checked)==22','len(checked)==40').replace('0xb3,0xb2,0xc5}', '0xb3,0xb2,0xc5,0xb5}')
 if name=='build.py':s=s.replace('5905','5927')
 (O/name).write_text(s)
if not (O/'spells.py').exists():shutil.copy2(B/'spells.py',O/'spells.py')
for p in B.glob('*.json'):
 if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','audit-noms','audit-tables','inventaire-','lieux-prepares')):continue
 if not (O/p.name).exists():shutil.copy2(p,O/p.name)
r=read(O/'revue-lot-v040.json');assert len(r)==40 and len({x['id'] for x in r})==40
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
print('v0.40 inputs ready:',len(r))

