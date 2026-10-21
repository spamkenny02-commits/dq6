"""Package the explicit v0.49 source/report/BPS allowlist; never ROM or state."""
from pathlib import Path
import json,hashlib,shutil,sys
R=Path(__file__).resolve().parent;D=R/'dq6-fr';O=D/'v0.49';B=D/'v0.48'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
review=read(O/'revue-lot-v049.json');qa=read(O/'qa-render-fixtures.json');runtime=read(O/'qa-runtime.json');bus=read(O/'qa-script-name-engine-bus.json');visual=read(O/'qa-relecture-visuelle.json')
digest=sha(O/'result.sfc');assert digest==qa['result_sha256']==runtime['result_sha256']==bus['result_sha256']==visual['result_sha256']
assert len(review)==57 and len(qa['rows'])==visual['accepted_final_pages']
assert visual['all_final_captures_reviewed'] and visual['stress_pages_reviewed']==len(runtime['probes'])
assert {x['id'] for x in review}=={x['id'] for x in qa['rows']}
assert bus['groups_checked']==880 and bus['all_rom_bus_reads_match']
proof=O/'qa-restauration-propre.json'
if '--provisional' in sys.argv and not proof.exists():save(proof,dict(pending=True,result_sha256=digest))
if '--provisional' not in sys.argv:assert read(proof)['fresh_destination'] and read(proof)['result_sha256']==digest
old=read(B/'insertion-candidates.json');now=read(O/'insertion-candidates.json');by={x['id']:x for x in now}
assert len(old)==6672 and len(now)==6729 and all(x['tokens']==by[x['id']]['tokens'] for x in old)
a=(O/'result.sfc').read_bytes();b=(B/'result.sfc').read_bytes()
for copy in [0,0x400000]:
 for lo,hi in [(0x58366,0x58374),(0x4b,0x4e),(0x2b7e,0x2bfd),(0x165e7,0x1785e),(0x3b8703,0x3bc712),(0x159d2,0x15ad1),(71270,71305)]:assert a[copy+lo:copy+hi]==b[copy+lo:copy+hi],hex(lo)
save(O/'qa-noms-moteur-inchanges.json',dict(old_tokens_unchanged=6672,name_sids_unchanged=2512,native_engine_tree_vectors_loader_and_name_frame_unchanged=True,source='v0.48/result.sfc reconstructed from public BPS',result_sha256=digest))
reliquat=read(O/'qa-reliquat.json');assert reliquat['remaining']==228
state=read(R/'etat-projet.json');state.update(release='v0.49',baseline='v0.48',main_script=dict(validated=6729,visible_total=6957,new_this_pass=57,remaining=228),notes='57 dialogues, narrations et répliques à commandes natives relus. Plans explicites : ordre de tous les contrôles hors mise en lignes conservé, pauses sources gardées, locuteurs et noms non consolidés. DS prioritaire pour les références explicites, écarts SFC conservés ; IPS secondaire non admis comme validation de ses décalages.',next='Continuer les 228 messages, dont19 préparés non insérés, les tables et les audits naturels. Les commandes rares C7/DC/E0/E1, les fragments assemblés et les choix couplés exigent encore une revue spécifique.',deferred_remaining_from_v034=reliquat['historical_v034']['remaining_count'],resolved_from_v034_ids=reliquat['historical_v034']['resolved_ids'])
state['separate_tables']['inventory_version']='v0.49';state['prepared_not_inserted']['main']=19
for p in [R/'etat-projet.json',O/'etat-projet.json']:save(p,state)
pages=len(qa['rows']);stress=len(runtime['probes']);refs=sum(bool(x['ds_references']) for x in review)
text=f'''# DQVI FR v0.49 partielle

6729/6957 messages intégrés, 57 ajouts, 228 restants. 19 préparés non insérés hérités : 11 fragments et 8 brouillons. Aucun nouveau texte principal en préparation dans ce lot. Projet non finalisé. ROM de travail 8 Mio.

Plans français/natifs explicites pour chaque nouveau texte : toutes les commandes hors AD/AF/terminator restent dans l'ordre japonais exact. Les AF sources sont explicites ; seules les pauses supplémentaires nécessaires à la pagination sont ajoutées. Les D4 et les noms de chaque tour restent présents. {refs} entrées ont des références DS explicites (fragments, formulation ou lexique) ; les autres sont adaptées directement du japonais SFC et de leur contexte. L'IPS secondaire est conservé dans la revue sans accepter ses lacunes. Le vin SFC de Magnus et le marchand d'objets de Tully ne deviennent pas le repas/distributeur de nourriture DS. Les accords devant C4 sont nominaux pour rester compatibles avec le groupe.

6672 anciens tokens et 2512 noms inchangés, ainsi que moteur, arbre Huffman, vecteur C4, polices, cadre du nom, Journal/Options et crédits retirés. prepare.py/build.py/verify.py, 6960 entrées redécodées, réapplication BPS/IPS, mauvaises sources refusées et zones protégées vérifiées. Recette pass49.py idempotente ; refus explicite de permutations/suppressions de commandes ou de pauses originales. Nouvelle restauration indépendante et reconstruction identique.

Snes9x : {pages} pages finales pour les 57 textes, toutes relues ; {stress} pages supplémentaires de stress, démarrage et Journal relus ; bus courant 880 plages/{bus['bytes_checked']} octets. C4 et Cie observé sur cinq textes par retour de compte forcé à 2 dans des ROM de diagnostic seulement. Objet de 24 cellules, BB=16777215 et B2 Maître des Combats testés. Ce sont des redirections du message100 au camp, pas des scènes naturelles ni des validations de calcul du groupe, d'acquisition, de Journal ou de SRAM. Le banc choisit maintenant une zone libre du script supérieur au lieu de supposer $7A0000 libre. Aucune modification du moteur de la version diffusée.

Tables séparées inchangées : 2512 SID, 2048 entrées physiques, 464 alias ; 37 libellés français confirmés, 4 aides grammaticales adaptées, 25 lieux préparés non insérés. Le zéro japonais détecté ne signifie pas traduction complète : 1558 textes autres à revoir, 346 identifiants, 83 vides à qualifier, 23 identités DS à vérifier en contexte, 1 crédit retiré et 37 confirmés. Pointeurs, tailles, commandes et fenêtres natives restent à contrôler avant insertion.

Ouverts : scènes322/323/1836/4095, indices610/1135/2404/5341/5351, fragments assemblés, commandes rares, alphabet accentué et tables. Le différé1356 est résolu par une revue directe du japonais et de ses DB, sans reprendre la VF lacunaire ; quatre différés historiques restent610/1135/2404/5341. Ne pas déclarer le jeu finalisé.

SHA256 résultat : {digest}. BPS sur JP sans en-tête SHA256 90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Aucune ROM, SRAM, état ou archive de ROM publiée.
'''
for p in [R/'LISEZ-MOI.md',O/'LISEZ-MOI.md']:p.write_text(text)
(R/'README.md').write_text('# Dragon Quest VI — traduction française Super Famicom\n\nv0.49 partielle : **6729/6957 messages intégrés**, 228 restants dont19 préparés non insérés. 57 ajouts relus et vérifiés. Tables et audits ouverts ; projet non finalisé.\n\nPatch BPS dans patches/. Lire LISEZ-MOI.md et REPRISE-AUTOMATIQUE.md. Restaurer par python restore_sources.py. Aucune ROM ou sauvegarde publiée.\n')
f=R/'REPRISE-AUTOMATIQUE.md';head='# Reprise v0.49\n\n'+state['notes']+' '+state['next']+' Lire native_plan.py et les plans du lot, ne pas recycler cette revue pour le prochain lot.\n\n';s=f.read_text();f.write_text(s if s.startswith(head) else head+s)
patch=R/'patches/DQVI-FR-DS-v0.49-BASE-JP-PARTIEL.bps';shutil.copy2(O/patch.name,patch)
files=[D/'pass49.py',D/'audit_reliquat_v049.py',Path(__file__).resolve(),R/'reconstruire_propre49.py',patch]
allowed={'revue-lot-v049.json','prepares-non-inseres.json','revues-preparatoires-remplacees.json','nouveaux-messages.json','validation.json','couverture-preparation.json','etat-projet.json','LISEZ-MOI.md','inventaire-tables.json','layout-engine-check.json'}
for p in sorted(O.iterdir()):
 if p.suffix=='.py' or p.name in allowed or p.name.startswith('qa-') and p.suffix=='.json':files.append(p)
assert all(p.suffix in {'.py','.json','.md','.bps'} for p in files)
spec=dict(kind='readable_translation_delta',version='v0.49',baseline='v0.48',baseline_count=6672,new_count=57,recipe='dq6-fr/pass49.py',merged_selection_sha256=sha(O/'insertion-candidates.json'),generated_inputs={n:sha(O/n) for n in ['correspondances-revues.json','adaptations-francaises.json','liaisons-variables-natives.json','charset.json']},files=[dict(path=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size) for p in files]);save(R/'sources/lots/v0.49.json',spec);save(R/'publish-v049-files.json',[str(p.relative_to(R)) for p in files]+['sources/lots/v0.49.json','README.md','LISEZ-MOI.md','REPRISE-AUTOMATIQUE.md','etat-projet.json']);print(len(files),'authorized files')
