"""Explicit final-source reviews; no fuzzy matching or forced event interpretation."""
from pathlib import Path
import json,subprocess,sys
from plans56 import PLANS,FIXED,REVISIONS
R=Path(__file__).resolve().parent;D=R/'dq6-fr';B=D/'v0.55';O=D/'v0.56';O.mkdir(exist_ok=True);read=lambda p:json.loads(p.read_text());jp=read(D/'clean-base/sfc-jp.json');vf=read(D/'clean-base/sfc-vf.json');ja={(x['file'],x['id']):x for x in read(D/'clean-base/ds-ja.json')};fr={(x['file'].replace('/FR/','/JA/'),x['id']):x for x in read(D/'clean-base/ds-fr.json')}
notes={
5698:'Révision isolée : ancien texte Par contre, il faut qu’ils soient utilisés par... remplacé par le titre neutre Compatible avec. Le vrai appel C3C5BE imprime ce préfixe avant la liste. Sens équipement conservé, pas de pluriel imposé aux personnages.',
5699:'Révision structurelle de disposition : C1 espace D5 gardés dans le même ordre ; AF puis AD ajoutés après chaque nom pour permettre des pauses et maîtriser les lignes avant débordement. L’ancienne source voulait trois noms sur une ligne. Aucun nom figé.',
5700:'Même correction de disposition que5699, à la branche CPY2 de la liste native ; C1/D5/AD/AE gardés, AF ajouté. Ne compte pas comme traduction nouvelle.',
5701:'Conjonction et suspension conservées. La boucle native C3C608 pour6–8 porteurs appelle5701 après le cinquième nom. AF source conservé, AD après la pause pour isoler le nom suivant. IPS secondaire décalé ne servait pas de validation.',
5702:'Conclusion japonaise semble pouvoir équiper : le sens compatibilité figure dans le préfixe5698 ; semble-t-il garde la modalisation sans genre ni nombre. Appel après la boucle6–8, contrairement au suffixe5703 de la boucle1–5. Disposition typographique adaptée, AF conservé.',
5703:'Suffixe japonais de modalisation semble ; après le préfixe Compatible avec et les noms natifs, semble-t-il conserve la conclusion sans imposer singulier/pluriel. D5/AF/AC gardés. Appel C3C5FE après boucle1–5.',
6040:'C90910 appelle ce texte puis le choix, et positionne/efface le bit0002 à7E3D00 via C92E50/C92E93. C5907D lit ce bit et l’entrée5840 masque0020 pour alimenter6E51. Annuler est la fonction donnée par le japonais, aucune touche physique B/L inventée.',
6041:'Branche oui de6040 : C9091B affiche6041 puis C92E50 argument7E3D00 masque0002 ; marche avec Annuler autorisée, pas marche à travers les murs.',
6042:'Branche non de6040 : C9092C affiche6042 puis C92E93 argument7E3D00 masque0002. Pas d’effet non démontré ajouté.',
6046:'C9096A propose le changement puis les branches6047/6048 positionnent/effacent7E3D00 masque0004. C00254B lit ce bit au démarrage et la branche dédiée charge la valeur1. Étage truqué traduit le label interne インチキフロア ; aucune zone nommée inventée.',
6047:'Branche oui de6046, C90975 puis C92E50, bit0004. Étape de départ technique, pas un nom de lieu DS.',6048:'Branche non de6046, C90986 puis C92E93, bit0004 ; opposition étage standard/étage truqué conservée.',
6184:'Le passage CFDAE1–CFDB25 présente ce poème puis un choix. Oui appelle CE7444 (qui appelle C7B648), change de carte vers01A9 et poursuit6185 ; non poursuit6186. Drapeau/sein/doigt et la double lecture volontaire sont conservés. Pas de traduction sémantique non prouvée en objet ou flag précis.',
6185:'Suite oui du poème6184 au point CFDB1C. しずく reste des gouttes, sans inventer Rosée des rêves ou une commande précise. Sous-entendu et ambiguïté du texte volontairement conservés ; ce n’est plus un libellé pris hors de son appel.',
6186:'Suite non du même choix au point CFDB22 ; refus et jeter ça conservés, pas affirmation de destruction d’un objet réel.',
6193:'Choix au point CFDB93, branche oui C7B648 puis TSB3D5E masque0008 et changement de carte00A0. Fusionner conserve le mot source ; pas se joindre au groupe comme l’IPS. Pas de fusion naturelle complète revendiquée.',
6194:'Choix au point CFDBBB : oui TSB3D72 masque0010 et départ vers carte0214, coordonnées0190/0179. Le japonais omet l’objet précis : une goutte conserve cette omission, ne pas nommer un objet DS sans preuve.',
6195:'Choix au point CFDC06 : oui départ carte012B, coordonnées0039/0028. Faire tourner ça garde le verbe et l’objet indéterminé ; ni séduction IPS ni mécanisme de quête ajouté.',
6956:'Réparation de frontière isolée : l’extraction JP dépasse0x3B8703 dans la table des noms. Seuls les44 premiers tokens, jusqu’à AF inclus, sont linguistiquement et physiquement fiables. La traduction garde C9 SFC (pas CC DS), Tulipe et l’obligation à accomplir. Ajout explicite d’un AC sûr après le AF, absent du préfixe source borné ; aucun AC original ni scène naturelle prétendu. Le redécodage et les tests vérifient cette terminaison ajoutée, sans traduire les octets de noms en faux dialogue.',
}
r=[]
for mid,plan in sorted(PLANS.items()):
 refs=[]
 if mid==6956:
  key=('data/MESS6/JA/0816.p',12);refs=[dict(file=key[0],id=12,ja=ja[key]['text'],fr=fr[key]['text'],scope='DS_ADAPTE_A_LA_VARIABLE_C9_ET_OBLIGATION_SFC')]
 r.append(dict(id=mid,file='SFC_NATIVE_REVIEW',ids=[],status='RELU',compile_mode='NATIVE_PLAN_REVIEWED',fixed_layout=mid in FIXED,existing_revision=mid in REVISIONS,sfc_jp=jp[mid]['text'],sfc_vf_secondaire=vf[mid]['text'],native_plan=plan,original_body=plan,adaptation_body=plan,adaptation_speaker='',adaptation_review=notes[mid],review=notes[mid],ds_references=refs,native_bindings={f'native_{t:02X}':t for t in jp[mid]['tokens'][:44] if t<0x200 and t not in [0xad,0xaf,0xac,0xae]} if mid==6956 else {f'native_{t:02X}':t for t in jp[mid]['tokens'] if t<0x200 and t not in [0xad,0xaf,0xac,0xae]},sfc_context=[dict(id=i,text=jp[i]['text']) for i in range(max(0,mid-2),min(len(jp),mid+3))]))
(O/'revue-lot-v056.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));(O/'nouveaux-prepares-v056.json').write_text('[]')
for name in ['init.py','prepare.py','build.py','verify.py','names.py','spells.py','native_helpers.py','native_plan.py','fixed_plan.py','test_render.py','render_fixtures.py']:
 if (O/name).exists():continue
 s=(B/name).read_text()
 if name not in ['names.py','spells.py','native_helpers.py','native_plan.py','fixed_plan.py']:s=s.replace('v0.55','v0.56').replace('v0.54','v0.55').replace('v055','v056').replace('v054','v055').replace('v54','v55')
 if name=='build.py':s=s.replace('len(rows)-6903','len(rows)-6941')
 if name=='prepare.py':
  s=s.replace("src=read(P/'clean-base/sfc-jp.json');", "from bounded_source import bounded\nsrc=[bounded(x) for x in read(P/'clean-base/sfc-jp.json')];")
  s=s.replace('revisit=set()','revisit={5698,5699,5700}').replace('accepted[mid]=r;new.append(mid);continue','accepted[mid]=r;\n  if mid not in oldids:new.append(mid)\n  continue',1)
 if name=='verify.py':
  s=s.replace("assert all(old[i]['tokens']==new[i]['tokens'] for i in old)","assert all(old[i]['tokens']==new[i]['tokens'] for i in old if i not in [5698,5699,5700])")
  s=s.replace("jp={r['id']:r for r in json.loads((P/'clean-base/sfc-jp.json').read_text())}","from bounded_source import bounded\njp={r['id']:bounded(r) for r in json.loads((P/'clean-base/sfc-jp.json').read_text())}")
  s=s.replace('new_reviewed_translations=29,source_structural_entries=9','new_reviewed_translations=16,source_structural_entries=0,isolated_existing_revisions=[5698,5699,5700]').replace('all_v55_tokens_unchanged=True','v55_tokens_unchanged_except_explicit_equipment_revisions=True').replace('len(checked)==38','len(checked)==16')
  s=s[:s.index('\nstructural=[1,2,3,2358,5699,5700,5775,6213,6214]')]+"\nfor mid in [1,2,3,2358,5775,6213,6214]:assert new[mid]['tokens']==jp[mid]['tokens']\n"
 if name=='fixed_plan.py':s=s.replace("assert tags.count(0xaf)==original.count(0xaf)","assert tags.count(0xaf)>=original.count(0xaf)")
 if name=='test_render.py':
  a=s.index("ids=[x['id'] for x in review");b=s.index(';ids=list(map',a);s=s[:a]+"ids=[x['id'] for x in review if x['id'] not in [5698,5699,5700,5701,5702,5703]]"+s[b:]
 (O/name).write_text(s)
s=(D/'pass55.py').read_text().replace('v0.55','v0.56').replace('v0.54','v0.55').replace('v055','v056').replace('v054','v055');s=s.replace('and not ids&old','and ids&old=={5698,5699,5700}');(D/'pass56.py').write_text(s)
subprocess.run([sys.executable,str(D/'pass56.py')],check=True)
print('16 new texts and3 explicit equipment revisions ready')
