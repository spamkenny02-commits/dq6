"""Idempotent v0.49 delta: independently reviewed SFC text and explicit DS fragments."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;B=P/'v0.48';O=P/'v0.49';O.mkdir(exist_ok=True);read=lambda p:json.loads(p.read_text())
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2))
r=read(O/'revue-lot-v049.json');n=len(r)
for name in ['init.py','prepare.py','build.py','verify.py','names.py','spells.py','native_helpers.py']:
 if (O/name).exists():continue
 s=(B/name).read_text()
 if name not in ['names.py','spells.py','native_helpers.py']:s=s.replace('v0.48','v0.49').replace('v0.47','v0.48').replace('v048','v049').replace('v47','v47')
 if name=='build.py':s=s.replace('len(rows)-6529','len(rows)-6529')
 if name=='verify.py':s=s.replace('len(checked)==143',f'len(checked)=={n}')
 (O/name).write_text(s)
for p in B.glob('*.json'):
 if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','audit-noms','audit-tables','inventaire-','lieux-prepares','layout-engine','render-progress','blocages-')):continue
 if not (O/p.name).exists():shutil.copy2(p,O/p.name)
ids={x['id'] for x in r};old={x['id'] for x in read(B/'insertion-candidates.json')};assert len(ids)==n and not ids&old
jp=read(P/'clean-base/sfc-jp.json')
for x in r:assert x['status']=='RELU' and x['sfc_jp']==jp[x['id']]['text']
oldr=read(B/'correspondances-revues.json');save('revues-preparatoires-remplacees.json',[x for x in oldr if x['id'] in ids]);save('correspondances-revues.json',sorted([x for x in oldr if x['id'] not in ids]+r,key=lambda x:x['id']))
ad=[x for x in read(B/'adaptations-francaises.json') if x['id'] not in ids];bindings=read(B/'liaisons-variables-natives.json')
for x in r:
 ad.append(dict(id=x['id'],file=x['file'],ids=x['ids'],original_body=x['original_body'],body=x['adaptation_body'],speaker=x['adaptation_speaker'],review=x['adaptation_review']));bindings[str(x['id'])]=x['native_bindings']
save('adaptations-francaises.json',sorted(ad,key=lambda x:x['id']));save('liaisons-variables-natives.json',bindings);print(n,'v0.49 inputs ready')
