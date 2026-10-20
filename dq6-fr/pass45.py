"""v0.45: reviewed system messages and native bag/new-name bindings."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;B=P/'v0.44';O=P/'v0.45';O.mkdir(exist_ok=True);read=lambda p:json.loads(p.read_text())
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2))
r=read(O/'revue-lot-v045.json');n=len(r)
for name in ['init.py','prepare.py','build.py','verify.py','names.py','spells.py','native_helpers.py']:
 if (O/name).exists():continue
 s=(B/name).read_text()
 if name not in ['names.py','spells.py','native_helpers.py']:s=s.replace('v0.44','__NEW__').replace('v0.43','__BASE__').replace('__NEW__','v0.45').replace('__BASE__','v0.44').replace('v43','v44')
 if name=='prepare.py':
  s=s.replace('v044','v045').replace('correspondance_revue_v44','correspondance_revue_v45').replace('0xc5,0xb5}', '0xc5,0xb5,0xc3,0xd8}').replace('for control in [0xbb,0xc1,0xb2,0xc5,0xb5]', 'for control in [0xbb,0xc1,0xb2,0xc5,0xb5,0xc3,0xd8]')
  s=s.replace("accepted={r['id']:r.copy() for r in previous};review=[];new=[]", "DIRECT={x['id']:x for x in read(O/'revue-lot-v045.json') if x.get('compile_mode')=='SFC_REVIEWED_ADAPTATION'}\naccepted={r['id']:r.copy() for r in previous};review=[];new=[]")
  direct=""" if mid in DIRECT:
  d=DIRECT[mid];assert d['sfc_jp']==s['text'] and d['status']=='RELU'
  c=dict(body=d['original_body'],speaker=d.get('adaptation_speaker',''))
  try:r=convert(c,s)
  except ValueError as e:review.append(dict(id=mid,reason=str(e)));continue
  r.update(id=mid,ds_file=None,ds_id=[],method='adaptation_SFC_revue_avec_references_DS_explicites',source_japanese=s['text'],sfc_previous=vf[mid]['text'],ds_references=d.get('ds_references',[]))
  accepted[mid]=r;new.append(mid);continue
"""
  s=s.replace(' if str(mid) in MULTI:',direct+' if str(mid) in MULTI:')
 if name=='verify.py':s=s.replace('len(checked)==0',f'len(checked)=={n}').replace('0xc5,0xb5}:','0xc5,0xb5,0xc3,0xd8}:').replace('new_ds_validations=','new_reviewed_translations=')
 (O/name).write_text(s)
for p in B.glob('*.json'):
 if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','audit-noms','audit-tables','inventaire-','lieux-prepares','layout-engine')):continue
 if not (O/p.name).exists():shutil.copy2(p,O/p.name)
ids={x['id'] for x in r};old={x['id'] for x in read(B/'insertion-candidates.json')};assert len(ids)==n and not ids&old
jp=read(P/'clean-base/sfc-jp.json')
for x in r:assert x['status']=='RELU' and x['sfc_jp']==jp[x['id']]['text']
oldr=read(B/'correspondances-revues.json');save('revues-preparatoires-remplacees.json',[x for x in oldr if x['id'] in ids]);save('correspondances-revues.json',sorted([x for x in oldr if x['id'] not in ids]+r,key=lambda x:x['id']))
ad=[x for x in read(B/'adaptations-francaises.json') if x['id'] not in ids];bindings=read(B/'liaisons-variables-natives.json')
for x in r:
 ad.append(dict(id=x['id'],file=x['file'],ids=x['ids'],original_body=x['original_body'],body=x['adaptation_body'],speaker=x['adaptation_speaker'],review=x['adaptation_review']));bindings[str(x['id'])]=x['native_bindings']
save('adaptations-francaises.json',sorted(ad,key=lambda x:x['id']));save('liaisons-variables-natives.json',bindings)
print('v0.45',n)
