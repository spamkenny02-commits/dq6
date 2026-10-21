"""Package the explicit v0.50 source/report/BPS allowlist; never ROM or state."""
from pathlib import Path
import json,hashlib,shutil,sys
R=Path(__file__).resolve().parent;D=R/'dq6-fr';O=D/'v0.50';B=D/'v0.49'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
review=read(O/'revue-lot-v050.json');qa=read(O/'qa-render-fixtures.json');runtime=read(O/'qa-runtime.json');bus=read(O/'qa-script-name-engine-bus.json');visual=read(O/'qa-relecture-visuelle.json')
digest=sha(O/'result.sfc');assert digest==qa['result_sha256']==runtime['result_sha256']==bus['result_sha256']==visual['result_sha256']
assert len(review)==135 and len(qa['rows'])==visual['accepted_final_pages']
assert visual['all_final_captures_reviewed'] and visual['stress_pages_reviewed']==len(runtime['probes'])
assert {x['id'] for x in review}=={x['id'] for x in qa['rows']}
assert bus['groups_checked']==880 and bus['all_rom_bus_reads_match']
proof=O/'qa-restauration-propre.json'
if '--provisional' in sys.argv and not proof.exists():save(proof,dict(pending=True,result_sha256=digest))
if '--provisional' not in sys.argv:assert read(proof)['fresh_destination'] and read(proof)['result_sha256']==digest
old=read(B/'insertion-candidates.json');now=read(O/'insertion-candidates.json');by={x['id']:x for x in now}
assert len(old)==6729 and len(now)==6864 and all(x['tokens']==by[x['id']]['tokens'] for x in old)
a=(O/'result.sfc').read_bytes();b=(B/'result.sfc').read_bytes()
for copy in [0,0x400000]:
 for lo,hi in [(0x58366,0x58374),(0x4b,0x4e),(0x2b7e,0x2bfd),(0x165e7,0x1785e),(0x3b8703,0x3bc712),(0x159d2,0x15ad1),(71270,71305)]:assert a[copy+lo:copy+hi]==b[copy+lo:copy+hi],hex(lo)
save(O/'qa-noms-moteur-inchanges.json',dict(old_tokens_unchanged=6729,name_sids_unchanged=2512,native_engine_tree_vectors_loader_and_name_frame_unchanged=True,source='v0.49/result.sfc reconstructed from public BPS',result_sha256=digest))
reliquat=read(O/'qa-reliquat.json');assert reliquat['remaining']==93
state=read(R/'etat-projet.json');state.update(release='v0.50',baseline='v0.49',main_script=dict(validated=6864,visible_total=6957,new_this_pass=135,remaining=93),notes='135 dialogues, récits, retrouvailles et conversations finales relus. Plans explicites : ordre de tous les contrôles hors mise en lignes conservé, pauses sources gardées, locuteurs et noms non consolidés. DS prioritaire pour les références explicites, écarts SFC conservés ; IPS secondaire non admis comme validation de ses décalages.',next='Continuer les 93 messages, dont26 préparés non insérés, les tables et les audits naturels. Les commandes rares C7/DC/E0/E1, les fragments assemblés et les choix couplés exigent encore une revue spécifique.',deferred_remaining_from_v034=reliquat['historical_v034']['remaining_count'],resolved_from_v034_ids=reliquat['historical_v034']['resolved_ids'])
state['separate_tables']['inventory_version']='v0.50';state['prepared_not_inserted'].update(main=26,reviewed_fragments=12,draft_main=14)
for p in [R/'etat-projet.json',O/'etat-projet.json']:save(p,state)
pages=len(qa['rows']);stress=len(runtime['probes']);refs=sum(bool(x['ds_references']) for x in review)
text=f'''# DQVI FR v0.50 partielle

6864/6957 messages intégrés, 135 ajouts, 93 restants. 26 préparés non insérés : 12 fragments à assembler et14 brouillons contextuels. Les7 nouveaux préparés sont6019 et6184/6185/6186/6193/6194/6195 ; aucun n’est dans le lot inséré. Tables et audits naturels ouverts. ROM8 Mio.

Dialogues à plusieurs locuteurs, origine de CC à Sorcéria, mondes réels/rêvés, retrouvailles et fin du jeu. {refs} entrées avec références DS explicites de lexique ou de fragments. Chaque entrée garde JP, IPS secondaire, voisins et plans des commandes. Les importants décalages de l’IPS ne servent pas de validation. Les rôles D4/variables et AF ne sont pas consolidés. Les noms sont revus : Dragore, Zénithia, Pierrebrute, Monsieur Soren, Tulipe, Boss, Colin, Sergueï, Brad/Ivan et les autres correspondances DS. 2432 est une exclamation affirmative reprise de2431, C’est un grand honneur (DS0000:601), pas la négation de l’ancien IPS.

6729 anciens tokens,2512 noms, arbre, moteur, cadres et polices inchangés ; Journal/Options et crédits retirés conservés. prepare.py/build.py/verify.py,6960 entrées redécodées, BPS/IPS réappliqués, mauvaises sources et zones protégées vérifiés. Recette pass50.py idempotente ; restauration et reconstruction neuves identiques.

Snes9x : {pages} pages finales pour135 textes, toutes relues ; {stress} pages supplémentaires de stress et menu Journal relus. Bus courant880 plages/{bus['bytes_checked']} octets. C4 affiché seul/pluriel sur4745/6576, objets de24 cellules sur784/5688, BB=16777215 et B2 long. Audit du handler DF : il produit un suffixe011C, vide en français ; Vous reste littéral dans752. E0, non DF, imprime vous/vous tous. Deux branches DF forcées en diagnostic ; le lot complet a été recapturé après correction, moteur inchangé. Redirections du message100 au camp : aucune scène naturelle, transaction ou écriture SRAM validée.

Tables inchangées :2512 SID/2048 entrées physiques/464 alias ;37 libellés FR confirmés et4 aides grammaticales,25 lieux préparés. Les1558 autres textes,346 identifiants,83 vides à qualifier et23 identités DS non contrôlées en contexte restent au registre. Pointeurs, taille et fenêtres natives sont à traiter séparément.

Restent notamment les choix/indices couplés610/1135/2404/5341/5351, fragments natifs et commandes rares, texte6956 à auditer, ainsi que les scènes322/323/1836/4095 et les tables. Quatre différés historiques encore ouverts. Aucun achèvement global annoncé.

SHA256 résultat :{digest}. BPS pour JP sans en-tête SHA25690ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Ni ROM, ni SRAM, ni état, ni archive de ROM publiés.
'''
for p in [R/'LISEZ-MOI.md',O/'LISEZ-MOI.md']:p.write_text(text)
(R/'README.md').write_text('# Dragon Quest VI — traduction française Super Famicom\n\nv0.50 partielle : **6864/6957 messages intégrés**, 93 restants dont26 préparés non insérés. 135 ajouts relus et vérifiés. Tables et audits ouverts ; projet non finalisé.\n\nPatch BPS dans patches/. Lire LISEZ-MOI.md et REPRISE-AUTOMATIQUE.md. Restaurer par python restore_sources.py. Aucune ROM ou sauvegarde publiée.\n')
f=R/'REPRISE-AUTOMATIQUE.md';head='# Reprise v0.50\n\n'+state['notes']+' '+state['next']+' Lire native_plan.py et les plans du lot, ne pas recycler cette revue pour le prochain lot.\n\n';s=f.read_text();f.write_text(s if s.startswith(head) else head+s)
patch=R/'patches/DQVI-FR-DS-v0.50-BASE-JP-PARTIEL.bps';shutil.copy2(O/patch.name,patch)
files=[R/'plans50.py',R/'creer50.py',R/'finaliser_rendu50.py',D/'pass50.py',D/'audit_reliquat_v050.py',Path(__file__).resolve(),R/'reconstruire_propre50.py',patch]
allowed={'revue-lot-v050.json','prepares-non-inseres.json','revues-preparatoires-remplacees.json','nouveaux-messages.json','nouveaux-prepares-v050.json','validation.json','couverture-preparation.json','etat-projet.json','LISEZ-MOI.md','inventaire-tables.json','layout-engine-check.json'}
for p in sorted(O.iterdir()):
 if p.suffix=='.py' or p.name in allowed or p.name.startswith('qa-') and p.suffix=='.json':files.append(p)
assert all(p.suffix in {'.py','.json','.md','.bps'} for p in files)
spec=dict(kind='readable_translation_delta',version='v0.50',baseline='v0.49',baseline_count=6729,new_count=135,recipe='dq6-fr/pass50.py',merged_selection_sha256=sha(O/'insertion-candidates.json'),generated_inputs={n:sha(O/n) for n in ['correspondances-revues.json','adaptations-francaises.json','liaisons-variables-natives.json','charset.json','prepares-non-inseres.json']},files=[dict(path=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size) for p in files]);save(R/'sources/lots/v0.50.json',spec);save(R/'publish-v050-files.json',[str(p.relative_to(R)) for p in files]+['sources/lots/v0.50.json','README.md','LISEZ-MOI.md','REPRISE-AUTOMATIQUE.md','etat-projet.json']);print(len(files),'authorized files')
