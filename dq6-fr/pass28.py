"""Recreate 150 reviewed v0.28 dialogues, preserving the v0.27 selections."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;B=P/'v0.27';O=P/'v0.28'
def read(p):return json.loads(p.read_text())
def save(name,value):(O/name).write_text(json.dumps(value,ensure_ascii=False,indent=2))
O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
    if (O/name).exists():continue
    s=(B/name).read_text().replace('v0.27','v0.28')
    if name in ['prepare.py','verify.py']:s=s.replace('v0.26','v0.27').replace('v26','v27')
    if name=='prepare.py':s=s.replace('correspondance_revue_v27','correspondance_revue_v28')
    if name=='build.py':s=s.replace('len(rows)-5252','len(rows)-5402')
    if name=='prepare.py':s=s.replace("SPECIFIC_SPEAKERS={","SPECIFIC_SPEAKERS={6804:('カルベ','カルベ夫人'),")
    if name=='prepare.py':
        s=s.replace("baseline_by_id={r['id']:r for r in previous}","REVIEWED_NEW_IDS={r['id'] for r in read(O/'revue-lot-v028.json')}\nbaseline_by_id={r['id']:r for r in previous}")
        s=s.replace("mid=s['id']\n if mid in oldids", "mid=s['id']\n if mid not in oldids and mid not in REVIEWED_NEW_IDS:\n  review.append(dict(id=mid,reason='hors_lot_revu',sfc_jp=s['text']));continue\n if mid in oldids")
        # 3256 opens anonymously, then names Tulipe twice in both editions.
        s=s.replace("c['ja'][0])", "c['ja'][1] if mid==3256 else c['ja'][0])")
    (O/name).write_text(s)
for p in B.glob('*.json'):
    if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','progression-')):continue
    if not (O/p.name).exists():shutil.copy2(p,O/p.name)
reviews=read(O/'revue-lot-v028.json')
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
print('v0.28 reviewed input delta ready:',len(reviews),'messages')
