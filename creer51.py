"""New explicit review and v0.51 recipe; does not mutate old releases."""
from pathlib import Path
import json,shutil,subprocess,sys,importlib.util,hashlib
from plans51 import PLANS
R=Path(__file__).resolve().parent;D=R/'dq6-fr';B=D/'v0.50';O=D/'v0.51';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
jp=read(D/'clean-base/sfc-jp.json');vf=read(D/'clean-base/sfc-vf.json');ja=read(D/'clean-base/ds-ja.json');fr={(x['file'].replace('/FR/','/JA/'),x['id']):x for x in read(D/'clean-base/ds-fr.json')};ji={(x['file'],x['id']):x for x in ja}
skills={6020:[133,132],6021:[146,131],6022:[4,5],6023:[50,55,37,25],6024:[90],6025:[],6026:[],6027:[],6028:[60,154],6029:[138,123,140],6030:[142,144,141,2],6031:[76,129,57,124],6032:[56,14,8,150],6033:[93,117,80],6034:[86],6035:[104]}
notes={6024:'ラストダンス est décrit littéralement comme dernière danse qui scelle la danse ennemie. DS90 Antidanse est une comparaison de fonction, pas une identité de nom ou de SID imposée.',6025:'Le second paragraphe SFC concerne le nombre de trésors proches ; ne pas reprendre les chances de butin inventées par IPS.',6026:'まものつかい SFC et まものマスター DS : nom DS Maître monstres, mais recrutement SFC après combat conservé ; ne pas importer la suppression de cette mécanique sur DS.',6033:'Prérequis SFC exacts : Voleur, Maître monstres, Marchand. IPS remplace à tort Marchand par Soldat. Riposte renvoie ici le souffle de feu, pas toute attaque inventée.',6034:'Les quatre paragraphes et la plaisanterie du narrateur entraîné dans la danse sont gardés ; pas seulement le résumé IPS.',6035:'Le SFC ne dit pas de maîtriser toutes les autres classes ni absence de PM : ne pas importer ces ajouts IPS. Conserver diverses vocations sans inventer de prérequis précis.'}
review=[]
for mid,plan in PLANS.items():
 refs=[]
 keys=[('data/MENULIST6/JA/b1006000.mpt',mid-6020)]+[('data/MENULIST6/JA/b1003000.mpt',i) for i in skills[mid]]
 # Include prerequisite job labels independently, so no old IPS wording decides them.
 keys += [('data/MENULIST6/JA/b1006000.mpt',i) for i in {6029:[0,1],6030:[0,2],6031:[1,3],6032:[2,3],6033:[5,6,7],6034:[4,8]}.get(mid,[])]
 for key in keys:refs.append(dict(scope='LEXIQUE_DS_SEULEMENT_SFC_RELU',file=key[0],id=key[1],ja=ji[key]['text'],fr=fr[key]['text']))
 note='Description et contexte séquentiel des vocations SFC relus. Noms DS établis par entrées explicites ; aucun équivalent DS complet déclaré. Toutes les pauses AF et DE gardées. '+notes.get(mid,'Ne pas reprendre les omissions et généralités de l’ancien IPS ; techniques et prérequis japonais conservés.')
 review.append(dict(id=mid,file='SFC_NATIVE_REVIEW',ids=[],status='RELU',compile_mode='NATIVE_PLAN_REVIEWED',sfc_jp=jp[mid]['text'],sfc_vf_secondaire=vf[mid]['text'],native_plan=plan,original_body=plan,adaptation_body=plan,adaptation_speaker='',adaptation_review=note,review=note,ds_references=refs,native_bindings={f'native_{t:02X}':t for t in jp[mid]['tokens'] if t<0x200 and t not in [0xad,0xaf,0xac,0xae]},sfc_context=[dict(id=i,text=jp[i]['text']) for i in range(mid-2,mid+3)]))
save(O/'revue-lot-v051.json',review);save(O/'nouveaux-prepares-v051.json',[])
for name in ['init.py','prepare.py','build.py','verify.py','names.py','spells.py','native_helpers.py','native_plan.py','test_render.py','render_fixtures.py']:
 s=(B/name).read_text()
 if name not in ['names.py','spells.py','native_helpers.py','native_plan.py']:
  s=s.replace('v0.50','v0.51').replace('v0.49','v0.50').replace('v050','v051').replace('v049','v050').replace('v49','v50')
 if name=='build.py':s=s.replace('len(rows)-6729','len(rows)-6864')
 if name=='verify.py':s=s.replace('len(checked)==135','len(checked)==16')
 (O/name).write_text(s)
s=(D/'pass50.py').read_text().replace('v0.50','v0.51').replace('v0.49','v0.50').replace('v0.48','v0.49').replace('v050','v051').replace('v049','v050');(D/'pass51.py').write_text(s)
subprocess.run([sys.executable,str(D/'pass51.py')],check=True)
s=(D/'audit_reliquat_v050.py').read_text().replace('v0.50','v0.51').replace('len(done)==6864 and len(rows)==93','len(done)==6880 and len(rows)==77');(D/'audit_reliquat_v051.py').write_text(s)
print('16 descriptions reviewed; no new preparations')
