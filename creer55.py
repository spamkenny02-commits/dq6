"""Idempotent explicit review: no automatic fuzzy or debug-literal approval."""
from pathlib import Path
import json,subprocess,sys
from plans55 import PLANS,FIXED,STRUCTURAL
R=Path(__file__).resolve().parent;D=R/'dq6-fr';B=D/'v0.54';O=D/'v0.55';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());jp=read(D/'clean-base/sfc-jp.json');vf=read(D/'clean-base/sfc-vf.json');ja={(x['file'],x['id']):x for x in read(D/'clean-base/ds-ja.json')};fr={(x['file'].replace('/FR/','/JA/'),x['id']):x for x in read(D/'clean-base/ds-fr.json')}
refs={610:[('MESS6','0072.p',i) for i in range(53,63)],4952:[('MESS6','0043.p',i) for i in [523,525,526,529,530,531]],6157:[('MESS6','0626.p',293),('MESS6','0632.p',8)]}
for ids,start in [([1313,1314,1315],307),([1318,1319,1320],310),([1323,1324,1325],313)]:
 for mid,i in zip(ids,range(start,start+3)):refs[mid]=[('MENULIST6','b1005000.mpt',i)]
for mid,echoes in [(1312,[1313,1314,1315]),(1317,[1318,1319,1320]),(1322,[1323,1324,1325])]:refs[mid]=[x for e in echoes for x in refs[e]]
notes={610:'Adaptation linguistique de l’énigme relue contre DS0072:53–62 et choix MENULIST307–315. Les jeux phonétiques japonais deviennent les indices français DS vérité/lame et galets/sortir de la glace. Mot Frizzam DS, trois phrases et dix tours D4/neuf AF conservés. Nord SFC conservé. Les positions natives 1/3/2 ne changent pas. La porte naturelle reste à tester.',4952:'Les huit symboles chiffrés sont identiques dans les versions JP/FR DS0043:526 : aucune signification à inventer. Caption éditoriale explicite (Paroles indéchiffrables...) à la place des glyphes JP incompatibles avec la police VF. Roi Louis confirmé par la séquence DS. Aucun décodage du sort prétendu.',5351:'Instructions SFC gardées : statue Goyle (translittération du nom opaque ゴイル), sud, main GAUCHE au mur, PREMIER buisson. Ne pas importer le dragon d’or ou la géographie modifiée DS. Traduction du parcours, pas preuve de son exécution naturelle ; audit5351 reste ouvert.',6157:'Nom du château confirmé DS0626:293 (château tombé à terre) et0632:8 (Mortamor). Libellé technique après la chute, aucun événement de chute exécuté.',6019:'Confirmation isolée DE, contexte6017/6018 d’identification d’objets relu ; formulation neutre ne fige aucun nom ni objet. Rendu diagnostic, composition naturelle non revendiquée.'}
r=[]
for mid in sorted(set(PLANS)|set(STRUCTURAL)):
 plan=PLANS.get(mid,'');rr=[]
 for kind,f,i in refs.get(mid,[]):
  key=(f'data/{kind}/JA/{f}',i);assert key in ja and key in fr,key;rr.append(dict(scope='SOURCE_DS_EXPLICITE_ADAPTEE_AU_SFC',file=key[0],id=i,ja=ja[key]['text'],fr=fr[key]['text']))
 note=notes.get(mid,'Choix SFC conservé dans sa position native ; comparaison JP/FR DS explicite. Prévisualisation1317 abrégée avec points de suspension, écho1318 complet. 1319 corrige le faux sens IPS Ne me combats pas. Trois lignes fixes sans pagination.' if 1312<=mid<=1325 else 'Fragments natifs AE/AC relus dans leur contexte. D5, BB et limites de retour gardés. Direction est/ouest puis nord/sud, nombres variables. Pour5832–5839, le qualificatif itinérant est déplacé dans chacun des sept suffixes, sans perte ni ajout de service.')
 if mid in STRUCTURAL:note='STRUCTURE SANS TEXTE À TRADUIRE : restauration exacte de tous les tokens japonais, y compris espaces, nom C1 et terminator. Comparaison VF explicite ;5700/5775 sont décalés dans IPS. Ne compte pas comme nouvelle traduction française.'
 r.append(dict(id=mid,file='SFC_NATIVE_REVIEW',ids=[],status='RELU',compile_mode='NATIVE_PLAN_REVIEWED',structural_only=mid in STRUCTURAL,fixed_layout=mid in FIXED,sfc_jp=jp[mid]['text'],sfc_vf_secondaire=vf[mid]['text'],native_plan=plan,original_body=plan,adaptation_body=plan,adaptation_speaker='',adaptation_review=note,review=note,ds_references=rr,native_bindings={f'native_{t:02X}':t for t in jp[mid]['tokens'] if t<0x200 and t not in [0xad,0xaf,0xac,0xae]},sfc_context=[dict(id=i,text=jp[i]['text']) for i in range(max(0,mid-2),min(len(jp),mid+3))]))
(O/'revue-lot-v055.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));
if not (O/'nouveaux-prepares-v055.json').exists():(O/'nouveaux-prepares-v055.json').write_text('[]')
for name in ['init.py','prepare.py','build.py','verify.py','names.py','spells.py','native_helpers.py','native_plan.py','test_render.py','render_fixtures.py']:
 if (O/name).exists():continue
 s=(B/name).read_text()
 if name not in ['names.py','spells.py','native_helpers.py','native_plan.py']:s=s.replace('v0.54','v0.55').replace('v0.53','v0.54').replace('v054','v055').replace('v053','v054').replace('v53','v54')
 if name=='build.py':s=s.replace('len(rows)-6895','len(rows)-6903')
 if name=='verify.py':s=s.replace('len(checked)==8','len(checked)==38');s=s.replace("if r.get('method')=='native_plan_reviewed':","if r.get('method') in ['native_plan_reviewed','native_fixed_layout_reviewed','native_source_structure_restored']:")
 if name=='test_render.py':s=s.replace("ids=[x['id'] for x in review]","ids=[x['id'] for x in review if not x.get('structural_only') and x['id'] not in [1313,1314,1315,1318,1319,1320,1323,1324,1325,5820,5821,5822,5823,5832,5833,5834,5835,5836,5837,5838,5839]]")
 if name=='native_plan.py':
  s=s.replace("original=source['tokens'];plan=d['native_plan']","original=source['tokens'];plan=d['native_plan']\n if d.get('structural_only'):\n  assert not any(t>=0x200 and t!=0x200 for t in original)\n  return dict(id=source['id'],tokens=original[:],text='',lines=[],method='native_source_structure_restored',source_terminator=original[-1])\n if d.get('fixed_layout'):\n  from fixed_plan import compile_fixed\n  return compile_fixed(d,source,rev,punct,ALLOWED,WIDTH)")
 (O/name).write_text(s)
s=(D/'pass54.py').read_text().replace('v0.54','v0.55').replace('v0.53','v0.54').replace('v054','v055').replace('v053','v054');(D/'pass55.py').write_text(s)
subprocess.run([sys.executable,str(D/'pass55.py')],check=True)
print(len(PLANS),'linguistic reviews;',len(STRUCTURAL),'exact source structures')
