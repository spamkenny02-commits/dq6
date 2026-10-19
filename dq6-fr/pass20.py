"""Recreate the reviewed v0.20 input delta without replacing later local edits."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;O=P/'v0.20';B=P/'v0.19'
def read(p):return json.loads(p.read_text())
def save(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2))
O.mkdir(exist_ok=True)
for p in B.glob('*.json'):
 if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','progression-')):continue
 if not (O/p.name).exists():shutil.copy2(p,O/p.name)
reviews=read(O/'revue-lot-v020.json')
existing=read(O/'correspondances-revues.json');byid={r['id']:r for r in existing}
for r in reviews:
 if r['id'] in byid:assert byid[r['id']]==r
 else:existing.append(r)
save('correspondances-revues.json',existing)
adapt=read(O/'adaptations-francaises.json')
for r in reviews:
 if 'adaptation_body' not in r:continue
 row=dict(id=r['id'],file=r['file'],ids=r['ids'],original_body=r['original_body'],body=r['adaptation_body'],review=r['adaptation_review'])
 old=next((a for a in adapt if a['id']==r['id']),None)
 if old:assert old==row
 else:adapt.append(row)
save('adaptations-francaises.json',adapt)
print('v0.20 input delta ready:',len(reviews),'reviewed messages')
