"""Fresh native review; exact DS fragments are references, not fuzzy approvals."""
from pathlib import Path
import json,subprocess,sys
from plans53 import PLANS
R=Path(__file__).resolve().parent;D=R/'dq6-fr';B=D/'v0.52';O=D/'v0.53';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());jp=read(D/'clean-base/sfc-jp.json');vf=read(D/'clean-base/sfc-vf.json');ja={(x['file'],x['id']):x for x in read(D/'clean-base/ds-ja.json')};fr={(x['file'].replace('/FR/','/JA/'),x['id']):x for x in read(D/'clean-base/ds-fr.json')}
notes={0:'Libellé technique non vide ノーメッセージ : Aucun message. DE natif conservé ; aucune entrée vide comptée comme traduction.',74:'DS0824:0 confirme machine à sous et coût en jetons. SFC garde deux BB distincts dans le même ordre : dénomination ドル et coût en pièces まい. Localisation casino en jetons sans conversion numérique. Aucune partie réelle ni débit testé.',1716:'Deux X sont littéraux dans le japonais SFC, sans BB. D3 puis B5 conservés. Ancien IPS reprend une autre variante à BB : rejeté. Texte probablement technique, ne pas prétendre valider un compteur réel.',4854:'C9 qualifie le prince ; C4 qualifie son escorte/destinataire. Ne pas accoler et Cie au prince. Nom natif conservé ; forme vous compatible avec une personne vouvoyée ou le groupe.',6169:'Parodie japonaise : vie de cinquante ans / droits d’auteur de cinquante yens. Nombres, yen et AF conservés. Glyphes de chant rendus avec les notes déjà disponibles, sans modification de police.',6171:'ダンチョネ transcrit phonétiquement Danchoné. Aucun sens français, nom propre de personnage ou effet de jeu inventé.',6207:'ハイロー est gardé comme titre High-Low ; question de poker traduite sans inventer de règles ni établir une identité avec le poker DS. Ancien blocage de terminologie résolu par conservation explicite du titre, pas par validation d’une partie.'}
r=[]
for mid,plan in PLANS.items():
 rr=[]
 if mid==74:
  key=('data/MESS6/JA/0824.p',0);rr=[dict(scope='FRAGMENT_DS_ADAPTE_AU_SFC',file=key[0],id=0,ja=ja[key]['text'],fr=fr[key]['text'])]
 note=notes.get(mid,'Japonais SFC et voisins relus directement. C4 natif conditionnel conservé après vous : accord compatible avec une personne vouvoyée ou un groupe, sans figer les compagnons. C9 et D4 gardés dans leur ordre. Aucun équivalent DS complet établi ; IPS secondaire lacunaire ou décalé non admis comme validation. Deux branches C4 à tester en diagnostic, scène naturelle encore ouverte.')
 r.append(dict(id=mid,file='SFC_NATIVE_REVIEW',ids=[],status='RELU',compile_mode='NATIVE_PLAN_REVIEWED',sfc_jp=jp[mid]['text'],sfc_vf_secondaire=vf[mid]['text'],native_plan=plan,original_body=plan,adaptation_body=plan,adaptation_speaker='',adaptation_review=note,review=note,ds_references=rr,native_bindings={f'native_{t:02X}':t for t in jp[mid]['tokens'] if t<0x200 and t not in [0xad,0xaf,0xac,0xae]},sfc_context=[dict(id=i,text=jp[i]['text']) for i in range(max(0,mid-2),mid+3)]))
(O/'revue-lot-v053.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));(O/'nouveaux-prepares-v053.json').write_text('[]')
for name in ['init.py','prepare.py','build.py','verify.py','names.py','spells.py','native_helpers.py','native_plan.py','test_render.py','render_fixtures.py','test_runtime.py']:
 s=(B/name).read_text()
 if name not in ['names.py','spells.py','native_helpers.py','native_plan.py']:s=s.replace('v0.52','v0.53').replace('v0.51','v0.52').replace('v052','v053').replace('v051','v052').replace('v51','v52')
 if name=='build.py':s=s.replace('len(rows)-6880','len(rows)-6883')
 if name=='verify.py':s=s.replace('len(checked)==3','len(checked)==12')
 (O/name).write_text(s)
s=(D/'pass52.py').read_text().replace('v0.52','v0.53').replace('v0.51','v0.52').replace('v052','v053').replace('v051','v052');s=s.replace(".replace('v0.50','v0.52')",".replace('v0.51','v0.52')");(D/'pass53.py').write_text(s)
subprocess.run([sys.executable,str(D/'pass53.py')],check=True)
s=(D/'audit_reliquat_v052.py').read_text().replace('v0.52','v0.53').replace('len(done)==6883 and len(rows)==74','len(done)==6895 and len(rows)==62').replace('prepared_main=26','prepared_main=25').replace('prepared_main_drafts=14','prepared_main_drafts=13');s=s.replace("'v0.53/revue-lot-v052.json : texte SFC", "'v0.52/revue-lot-v052.json : texte SFC");(D/'audit_reliquat_v053.py').write_text(s)
print('12 fresh reviews')
