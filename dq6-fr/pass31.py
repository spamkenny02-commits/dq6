"""Restore the carpet correction against an exact v0.30 baseline, idempotently."""
from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent;B=P/'v0.30';O=P/'v0.31'
def read(p):return json.loads(p.read_text())
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2))
O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
 if(O/name).exists():continue
 s=(B/name).read_text().replace('v0.30','VERSION_NEW').replace('v0.29','VERSION_BASE').replace('VERSION_NEW','v0.31').replace('VERSION_BASE','v0.30').replace('v030','v031').replace('v29','v30')
 if name=='build.py':s=s.replace('len(rows)-5616','len(rows)-5730')
 if name=='prepare.py':
  s=s.replace('correspondance_revue_v30','correspondance_revue_v31').replace('revisit=set()','revisit={323}')
 if name=='verify.py':
  s=s.replace("assert all(old[i]['tokens']==new[i]['tokens'] for i in old)","revisions=json.loads((O/'revisions-autorisees.json').read_text());approved={r['id'] for r in revisions};assert approved=={323}\nfor proof in revisions:\n assert hashlib.sha256(json.dumps(old[proof['id']]['tokens'],separators=(',',':')).encode()).hexdigest()==proof['old_tokens_sha256']\n assert old[proof['id']]['text']==proof['old_text']\nassert all(old[i]['tokens']==new[i]['tokens'] for i in old if i not in approved)\nassert all(old[i]['tokens']!=new[i]['tokens'] for i in approved)")
  s=s.replace("if i not in old:assert", "if i not in old or i in approved:assert")
  s=s.replace("if mid in old:continue", "if mid in old and mid not in approved:continue")
  s=s.replace('v30_messages_retained=len(old)','v30_messages_retained=len(old)-len(approved)').replace('all_v30_tokens_unchanged=True','all_v30_tokens_unchanged_except_approved=True,approved_revised_ids=sorted(approved)')
 (O/name).write_text(s)
for p in B.glob('*.json'):
 if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','progression-','audit-noms','audit-tables','inventaire-','lieux-prepares','blocages-restants','nouveaux-cas-differes')):continue
 if not(O/p.name).exists():shutil.copy2(p,O/p.name)
r=read(O/'revue-lot-v031.json');assert {x['id'] for x in r}=={322,323}
old={x['id']:x for x in read(B/'insertion-candidates.json')};assert 322 not in old and 323 in old
proof=read(O/'revisions-autorisees.json');assert len(proof)==1 and proof[0]['id']==323
assert hashlib.sha256(json.dumps(old[323]['tokens'],separators=(',',':')).encode()).hexdigest()==proof[0]['old_tokens_sha256']
assert old[323]['text']==proof[0]['old_text']
jp=read(P/'clean-base/sfc-jp.json')
for x in r:assert x['status']=='RELU' and x['sfc_jp']==jp[x['id']]['text']
ids={322,323};oldr=read(B/'correspondances-revues.json');save('revues-remplacees.json',[x for x in oldr if x['id'] in ids]);save('correspondances-revues.json',sorted([x for x in oldr if x['id'] not in ids]+r,key=lambda x:x['id']))
ad=[x for x in read(B/'adaptations-francaises.json') if x['id'] not in ids]
for x in r:ad.append(dict(id=x['id'],file=x['file'],ids=x['ids'],original_body=x['original_body'],body=x['adaptation_body'],review=x['adaptation_review']))
save('adaptations-francaises.json',sorted(ad,key=lambda x:x['id']))
print('v0.31 inputs ready: 1 new + 1 explicitly revised')
