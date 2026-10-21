"""Create a fresh review from explicit source fragments; no fuzzy approval."""
from pathlib import Path
import json,subprocess,sys
from plans52 import PLANS
R=Path(__file__).resolve().parent;D=R/'dq6-fr';B=D/'v0.51';O=D/'v0.52';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());jp=read(D/'clean-base/sfc-jp.json');vf=read(D/'clean-base/sfc-vf.json');ja={(x['file'],x['id']):x for x in read(D/'clean-base/ds-ja.json')};fr={(x['file'].replace('/FR/','/JA/'),x['id']):x for x in read(D/'clean-base/ds-fr.json')}
refs={1135:('0089.p',[634,635,636]),2404:('0056.p',list(range(8))),5341:('0060.p',[677,678,679])}
notes={1135:'SFC はなてば : lancer/relâcher. DS かざせば : lever ; conserver l’action SFC, ne pas importer la DS. Aucun point cardinal dans cette phrase SFC. DS FR nord-est contredit DS JP nord-ouest : aucun ajouté. Blaise/orbe/cap/mer attestés dans les références. Texte relu, usage naturel de l’objet toujours non vérifié.',2404:'Huit paragraphes SFC conservés. DS0056:4 confirme trois niveaux vers le bas puis deux vers le haut. Pas d’inversion. Trois indices au total et un seul connu de Poséidon. Noms Poséidon/Gracos confirmés DS0056:0/1. Parcours naturel de la salle non vérifié.',5341:'SFC : depuis la mer remonter la rivière, puis grotte profonde. DS ajoute est, absent du SFC, donc non importé. Brigandia confirmé DS0060:679. IPS parle d’un cuisinier sans rapport : décalage rejeté. Route naturelle non vérifiée.'}
r=[]
for mid,plan in PLANS.items():
 name,ids=refs[mid];rr=[]
 for i in ids:
  key=('data/MESS6/JA/'+name,i);rr.append(dict(scope='FRAGMENT_DS_RELIS_ET_ADAPTE_AU_SFC',file=key[0],id=i,ja=ja[key]['text'],fr=fr[key]['text']))
 r.append(dict(id=mid,file='SFC_NATIVE_REVIEW',ids=[],status='RELU',compile_mode='NATIVE_PLAN_REVIEWED',sfc_jp=jp[mid]['text'],sfc_vf_secondaire=vf[mid]['text'],native_plan=plan,original_body=plan,adaptation_body=plan,adaptation_speaker='',adaptation_review=notes[mid],review=notes[mid],ds_references=rr,native_bindings={f'native_{t:02X}':t for t in jp[mid]['tokens'] if t<0x200 and t not in [0xad,0xaf,0xac,0xae]},sfc_context=[dict(id=i,text=jp[i]['text']) for i in range(mid-2,mid+3)]))
(O/'revue-lot-v052.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));(O/'nouveaux-prepares-v052.json').write_text('[]')
for name in ['init.py','prepare.py','build.py','verify.py','names.py','spells.py','native_helpers.py','native_plan.py','test_render.py','render_fixtures.py','test_runtime.py']:
 s=(B/name).read_text()
 if name not in ['names.py','spells.py','native_helpers.py','native_plan.py']:s=s.replace('v0.51','v0.52').replace('v0.50','v0.51').replace('v051','v052').replace('v050','v051').replace('v50','v51')
 if name=='build.py':s=s.replace('len(rows)-6864','len(rows)-6880')
 if name=='verify.py':s=s.replace('len(checked)==16','len(checked)==3')
 (O/name).write_text(s)
s=(D/'pass51.py').read_text().replace('v0.51','v0.52').replace('v0.50','v0.51').replace('v051','v052').replace('v050','v051');s=s.replace(".replace('v0.49','v0.51')",".replace('v0.50','v0.51')");(D/'pass52.py').write_text(s)
subprocess.run([sys.executable,str(D/'pass52.py')],check=True)
s=(D/'audit_reliquat_v051.py').read_text().replace('v0.51','v0.52').replace('len(done)==6880 and len(rows)==77','len(done)==6883 and len(rows)==74');(D/'audit_reliquat_v052.py').write_text(s)
print('3 fresh reviews')
