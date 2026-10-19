"""Recreate 150 reviewed v0.27 dialogues, preserving the v0.26 selections."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;B=P/'v0.26';O=P/'v0.27'
def read(p):return json.loads(p.read_text())
def save(name,value):(O/name).write_text(json.dumps(value,ensure_ascii=False,indent=2))
O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
    if (O/name).exists():continue
    s=(B/name).read_text().replace('v0.26','v0.27')
    if name in ['prepare.py','verify.py']:s=s.replace('v0.25','v0.26').replace('v25','v26')
    if name=='prepare.py':s=s.replace('correspondance_revue_v26','correspondance_revue_v27')
    if name=='build.py':s=s.replace('len(rows)-5152','len(rows)-5252')
    (O/name).write_text(s)
for p in B.glob('*.json'):
    if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','progression-')):continue
    if not (O/p.name).exists():shutil.copy2(p,O/p.name)
reviews=read(O/'revue-lot-v027.json')
assert len(reviews)==150 and len({r['id'] for r in reviews})==150
oldids={r['id'] for r in read(B/'insertion-candidates.json')}
assert not oldids&{r['id'] for r in reviews}
jp={r['id']:r for r in read(P/'clean-base/sfc-jp.json')}
for r in reviews:assert r['sfc_jp']==jp[r['id']]['text'] and r['status']=='RELU'
reviewids={r['id'] for r in reviews}
base_reviews=read(B/'correspondances-revues.json')
save('revues-preparatoires-remplacees.json',[r for r in base_reviews if r['id'] in reviewids])
existing=[r for r in base_reviews if r['id'] not in reviewids]+reviews
save('correspondances-revues.json',sorted(existing,key=lambda r:r['id']))
adapted={r['id'] for r in reviews if 'adaptation_body' in r}
adapt=[r for r in read(B/'adaptations-francaises.json') if r['id'] not in adapted]
for r in reviews:
    if 'adaptation_body' in r:
        adapt.append(dict(id=r['id'],file=r['file'],ids=r['ids'],original_body=r['original_body'],body=r['adaptation_body'],review=r['adaptation_review']))
save('adaptations-francaises.json',sorted(adapt,key=lambda r:r['id']))
print('v0.27 reviewed input delta ready:',len(reviews),'messages')
