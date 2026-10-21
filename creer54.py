"""Fresh explicit review; minimally extend compiler after native handler audit."""
from pathlib import Path
import json,subprocess,sys
from plans54 import PLANS
R=Path(__file__).resolve().parent;D=R/'dq6-fr';B=D/'v0.53';O=D/'v0.54';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());jp=read(D/'clean-base/sfc-jp.json');vf=read(D/'clean-base/sfc-vf.json');ja={(x['file'],x['id']):x for x in read(D/'clean-base/ds-ja.json')};fr={(x['file'].replace('/FR/','/JA/'),x['id']):x for x in read(D/'clean-base/ds-fr.json')}
refs={3727:[('0009.p',542)],6716:[('0074.p',109)],6718:[('0074.p',109)],6922:[('0098.p',29)],6923:[('0098.p',30)],6924:[('0098.p',31)],6925:[('0098.p',32)]}
notes={3727:'E0 imprime vous ou vous tous selon le compte natif, pas un nom. Svetlana correspond à ジーナ ; les autres non nommés restent non nommés. AF source conservé. La phrase DS de542 prouve seulement le nom Svetlana, pas un alignement complet.',6548:'D4/DE/E1/BB/D5 gardés. E1 ne consomme pas de paramètre du script : modifie59A8 si16. Aucune transaction réelle ni équivalence sémantique de ce drapeau inventée.',6716:'Calvin confirmé DS0074:109. Numéro5 conservé. B5 lit5A2A, C7 lit5A2C via la même fonction de nom ; deux objets séparés et deux pauses sources conservés. Aucun article imposé aux noms variables.',6718:'Même locuteur Calvin et deux objets natifs distincts B5/C7. Pause terminale AF conservée ; ne pas consolider avec6716.',6922:'DS0098:29 relu ; DC et CC gardés. CC reste variable et locuteur, pas Laura littérale.',6923:'DS0098:30 confirme éclosion. SFC Homme gardé plutôt que Gardien ajouté par DS ; répétition conservée.',6924:'DS0098:31 relu, nom Seigneur Zénith confirmé. SFC notre avenir a grandi, sans ajouter la nouvelle ère du texte DS.',6925:'DS0098:32 relu. CC reste variable ; B0 natif entre la question et l’exclamation gardé. Pas de suppression de pause ni nom figé.'}
r=[]
for mid,plan in PLANS.items():
 rr=[]
 for file,i in refs.get(mid,[]):
  key=('data/MESS6/JA/'+file,i);rr.append(dict(scope='FRAGMENT_DS_A_ADAPTER_OU_LEXIQUE_EXPLICITE',file=key[0],id=i,ja=ja[key]['text'],fr=fr[key]['text']))
 r.append(dict(id=mid,file='SFC_NATIVE_REVIEW',ids=[],status='RELU',compile_mode='NATIVE_PLAN_REVIEWED',sfc_jp=jp[mid]['text'],sfc_vf_secondaire=vf[mid]['text'],native_plan=plan,original_body=plan,adaptation_body=plan,adaptation_speaker='',adaptation_review=notes[mid],review=notes[mid],ds_references=rr,native_bindings={f'native_{t:02X}':t for t in jp[mid]['tokens'] if t<0x200 and t not in [0xad,0xaf,0xac,0xae]},sfc_context=[dict(id=i,text=jp[i]['text']) for i in range(mid-2,mid+3)]))
(O/'revue-lot-v054.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));(O/'nouveaux-prepares-v054.json').write_text('[]')
for name in ['init.py','prepare.py','build.py','verify.py','names.py','spells.py','native_helpers.py','native_plan.py','test_render.py','render_fixtures.py']:
 s=(B/name).read_text()
 if name not in ['names.py','spells.py','native_helpers.py','native_plan.py']:s=s.replace('v0.53','v0.54').replace('v0.52','v0.53').replace('v053','v054').replace('v052','v053').replace('v52','v53')
 if name=='build.py':s=s.replace('len(rows)-6883','len(rows)-6895')
 if name=='verify.py':s=s.replace('len(checked)==12','len(checked)==8')
 if name=='native_plan.py':s=s.replace('}|set(range(0xc9,0xd4))','}|{0xc7,0xdc,0xe0,0xe1}|set(range(0xc9,0xd4))',1).replace('0xdf:0})','0xdf:0,0xc7:24,0xe0:9,0xdc:0,0xe1:0})')
 if name=='test_render.py':s=s.replace("'0x5a2a':[1,0]","'0x5a2a':[1,0],'0x5a2c':[2,0]")
 (O/name).write_text(s)
s=(D/'pass53.py').read_text().replace('v0.53','v0.54').replace('v0.52','v0.53').replace('v053','v054').replace('v052','v053');s=s.replace(".replace('v0.51','v0.53')",".replace('v0.52','v0.53')");(D/'pass54.py').write_text(s)
subprocess.run([sys.executable,str(D/'pass54.py')],check=True)
s=(D/'audit_reliquat_v053.py').read_text().replace('v0.53','v0.54').replace('len(done)==6895 and len(rows)==62','len(done)==6903 and len(rows)==54');(D/'audit_reliquat_v054.py').write_text(s)
print('8 fresh reviews; native handlers preserved')
