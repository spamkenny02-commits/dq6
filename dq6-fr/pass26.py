"""Recreate 100 reviewed v0.26 dialogues, preserving the v0.25 selections."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;B=P/'v0.25';O=P/'v0.26'
def read(p):return json.loads(p.read_text())
def save(name,value):(O/name).write_text(json.dumps(value,ensure_ascii=False,indent=2))
O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
    if (O/name).exists():continue
    s=(B/name).read_text().replace('v0.25','v0.26')
    if name in ['prepare.py','verify.py']:s=s.replace('v0.24','v0.25').replace('v24','v25')
    if name=='prepare.py':s=s.replace('correspondance_revue_v25','correspondance_revue_v26')
    if name=='build.py':s=s.replace('len(rows)-5140','len(rows)-5152')
    (O/name).write_text(s)
for p in B.glob('*.json'):
    if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','progression-')):continue
    if not (O/p.name).exists():shutil.copy2(p,O/p.name)
reviews=read(O/'revue-lot-v026.json')
assert len(reviews)==100 and len({r['id'] for r in reviews})==100
oldids={r['id'] for r in read(B/'insertion-candidates.json')}
assert not oldids&{r['id'] for r in reviews}
jp={r['id']:r for r in read(P/'clean-base/sfc-jp.json')}
for r in reviews:assert r['sfc_jp']==jp[r['id']]['text'] and r['status']=='RELU'
existing=read(O/'correspondances-revues.json');byid={r['id']:r for r in existing}
for r in reviews:
    if r['id'] in byid:assert byid[r['id']]==r
    else:existing.append(r)
save('correspondances-revues.json',sorted(existing,key=lambda r:r['id']))
adapt=read(O/'adaptations-francaises.json')
for r in reviews:
    if 'adaptation_body' not in r:continue
    row=dict(id=r['id'],file=r['file'],ids=r['ids'],original_body=r['original_body'],body=r['adaptation_body'],review=r['adaptation_review'])
    prior=next((a for a in adapt if a['id']==r['id']),None)
    if prior:assert prior==row
    else:adapt.append(row)
save('adaptations-francaises.json',sorted(adapt,key=lambda r:r['id']))
print('v0.26 reviewed input delta ready:',len(reviews),'messages')
