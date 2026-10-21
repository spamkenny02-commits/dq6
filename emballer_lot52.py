"""Explicit public source/report/BPS allowlist for v0.52; no ROM or game saves."""
from pathlib import Path
import json,hashlib,shutil,sys
R=Path(__file__).resolve().parent;D=R/'dq6-fr';O=D/'v0.52';B=D/'v0.51'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
r=read(O/'revue-lot-v052.json');new=read(O/'insertion-candidates.json');old=read(B/'insertion-candidates.json');by={x['id']:x for x in new}
assert len(r)==3 and len(old)==6880 and len(new)==6883 and all(by[x['id']]['tokens']==x['tokens'] for x in old)
digest=sha(O/'result.sfc');pages=read(O/'qa-render-fixtures.json');visual=read(O/'qa-relecture-visuelle.json');bus=read(O/'qa-script-name-engine-bus.json');reg=read(O/'qa-regression-variables.json')
for x in [pages,visual,bus,reg,read(O/'qa-runtime.json')]:assert x['result_sha256']==digest
assert visual['all_final_captures_reviewed'] and visual['accepted_final_pages']==len(pages['rows']) and {x['id'] for x in r}=={x['id'] for x in pages['rows']}
assert bus['groups_checked']==880 and bus['all_rom_bus_reads_match']
proof=O/'qa-restauration-propre.json'
if '--provisional' in sys.argv and not proof.exists():save(proof,dict(pending=True,result_sha256=digest))
if '--provisional' not in sys.argv:assert read(proof)['fresh_destination'] and read(proof)['result_sha256']==digest
# Isolated name/frame/font/engine equality checks, in both ROM mappings.
a=(O/'result.sfc').read_bytes();b=(B/'result.sfc').read_bytes()
for c in [0,0x400000]:
 for lo,hi in [(0x58366,0x58374),(0x4b,0x4e),(0x2b7e,0x2bfd),(0x165e7,0x1785e),(0x3b8703,0x3bc712),(0x159d2,0x15ad1),(71270,71305)]:assert a[c+lo:c+hi]==b[c+lo:c+hi],hex(lo)
save(O/'qa-noms-moteur-inchanges.json',dict(old_tokens_unchanged=6880,name_sids_unchanged=2512,native_engine_tree_vectors_loader_and_name_frame_unchanged=True,baseline='v0.51 public BPS',result_sha256=digest))
state=read(R/'etat-projet.json');state.update(release='v0.52',baseline='v0.51',main_script=dict(validated=6883,visible_total=6957,new_this_pass=3,remaining=74),notes='Trois indices relus : orbe1135, salle à répétition2404, bouclier5341. Écarts SFC/DS explicitement conservés ; parcours naturels encore ouverts.',next='Continuer les74 entrées, dont26 préparées non insérées, puis les tables, recherche des oublis et relecture complète.');state['separate_tables']['inventory_version']='v0.52'
q=read(O/'qa-reliquat.json');state.update(deferred_remaining_from_v034=q['historical_v034']['remaining_count'],resolved_from_v034_ids=q['historical_v034']['resolved_ids'])
for p in [R/'etat-projet.json',O/'etat-projet.json']:save(p,state)
text=f'''# DQVI FR v0.52 partielle

6883/6957 messages intégrés :3 ajouts,74 restants dont26 préparés non insérés (12 fragments,14 brouillons), aucun préparé nouveau. ROM8 Mio. Projet non finalisé.

1135 : Blaise demande de lancer l’orbe depuis le cap de la Mort dans la mer du Néant, conformément au SFC. Ne pas importer lever de la DS ni le point cardinal DS FR erroné et absent de cette phrase SFC.2404 : huit paragraphes de Poséidon, trois étages vers le bas puis deux vers le haut, trois indices au total et un seul connu.5341 : depuis la mer remonter la rivière vers une grotte profonde, sans ajouter l’est de la DS. Brigandia confirmé. L’ancien IPS5341 décrit un cuisinier sans rapport et n’est pas admis comme validation.

Ces trois textes sont intégrés, leurs parcours naturels restent ouverts.610 est le seul des26 différés historiques v0.34 encore non intégré ; cela ne ferme pas les audits globaux. Les autres textes envisagés n’ont pas été insérés ni comptés sans validation terminée.

6880 anciens tokens et2512 noms inchangés. Aucun changement moteur, commandes, polices, Journal/Options, crédits retirés ni cadre du nom. prepare.py/build.py/verify.py :6960 entrées redécodées, BPS/IPS réappliqués, mauvaises sources et zones protégées contrôlées. Recette pass52.py idempotente, restauration neuve et reconstruction identiques.

Snes9x :{len(pages['rows'])} pages pour les3 indices, toutes relues, et{len(reg['rows'])} pages de régression784/6939/752 pour noms, objet, nombre et DF, également relues. Démarrage et Journal vérifiés. Bus880 plages/{bus['bytes_checked']} octets. Redirections du message100 au camp ; aucune utilisation naturelle de l’orbe, résolution du labyrinthe, route de la grotte, transaction ou écriture SRAM validées.

Tables séparées réinventoriées, inchangées :2512 SID/2048 entrées physiques/464 alias ;37 libellés FR confirmés et4 aides grammaticales,25 lieux préparés.1558 autres textes,346 identifiants,83 vides à qualifier,23 identités DS à vérifier et1 crédit retiré.0 japonais détecté ne signifie pas tables traduites. Audits610/5351, fragments assemblés, commandes rares,6956, scènes322/323/1836/4095 et routes1135/2404/5341 encore ouverts. Relecture exhaustive non encore commencée.

SHA256 résultat :{digest}. BPS pour JP sans en-tête SHA25690ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Sources, revues, rapports et patch seulement ; aucune ROM, SRAM ou état d’émulateur.
'''
for p in [R/'LISEZ-MOI.md',O/'LISEZ-MOI.md']:p.write_text(text)
(R/'README.md').write_text('# Dragon Quest VI — traduction française Super Famicom\n\nv0.52 partielle : **6883/6957 messages intégrés**,74 restants dont26 préparés non insérés. Trois indices relus et testés en diagnostic ; parcours naturels et tables encore ouverts.\n\nPatch dans patches/. Lire LISEZ-MOI.md et REPRISE-AUTOMATIQUE.md. Restaurer par python restore_sources.py. Aucune ROM ou sauvegarde publiée.\n')
p=R/'REPRISE-AUTOMATIQUE.md';head='# Reprise v0.52\n\n'+state['notes']+' '+state['next']+' Ne pas recycler la revue de ce lot.\n\n';s=p.read_text();p.write_text(s if s.startswith(head) else head+s)
patch=R/'patches/DQVI-FR-DS-v0.52-BASE-JP-PARTIEL.bps';shutil.copy2(O/patch.name,patch)
files=[R/'plans52.py',R/'creer52.py',D/'pass52.py',D/'audit_reliquat_v052.py',Path(__file__).resolve(),R/'reconstruire_propre52.py',patch]
allowed={'revue-lot-v052.json','prepares-non-inseres.json','revues-preparatoires-remplacees.json','nouveaux-messages.json','nouveaux-prepares-v052.json','validation.json','couverture-preparation.json','etat-projet.json','LISEZ-MOI.md','inventaire-tables.json','layout-engine-check.json'}
for p in sorted(O.iterdir()):
 if p.suffix=='.py' or p.name in allowed or p.name.startswith('qa-') and p.suffix=='.json':files.append(p)
assert all(p.suffix in {'.py','.json','.md','.bps'} for p in files)
spec=dict(kind='readable_translation_delta',version='v0.52',baseline='v0.51',baseline_count=6880,new_count=3,recipe='dq6-fr/pass52.py',merged_selection_sha256=sha(O/'insertion-candidates.json'),generated_inputs={n:sha(O/n) for n in ['correspondances-revues.json','adaptations-francaises.json','liaisons-variables-natives.json','charset.json','prepares-non-inseres.json']},files=[dict(path=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size) for p in files]);save(R/'sources/lots/v0.52.json',spec);save(R/'publish-v052-files.json',[str(p.relative_to(R)) for p in files]+['sources/lots/v0.52.json','README.md','LISEZ-MOI.md','REPRISE-AUTOMATIQUE.md','etat-projet.json']);print(len(files),'authorized files')
