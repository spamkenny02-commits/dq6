"""Package only an explicitly reviewed, built and tested batch (no ROM/saves)."""
from pathlib import Path
import argparse,json,hashlib,shutil
ap=argparse.ArgumentParser();ap.add_argument('version');ap.add_argument('baseline');ap.add_argument('--notes',type=Path,required=True);a=ap.parse_args()
P=Path(__file__).resolve().parent;R=P.parent;O=P/a.version;tag=a.version.replace('.','');v=int(a.version.split('.')[1])
read=lambda p:json.loads(p.read_text())
save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
validation=read(O/'validation.json');review=read(O/f'revue-lot-{tag}.json');n=len(review);total=validation['ds_validated'];remaining=6957-total
assert n==validation['new_replacements'];assert validation['script_entries_verified']==6960
qa=read(O/'qa-patchs-regression.json');assert qa['new_rows_checked']==n
render=read(O/'qa-render-fixtures.json');assert render['result_sha256']==sha(O/'result.sfc');assert {r['id'] for r in render['rows']}=={r['id'] for r in review}
notes=read(a.notes);assert notes['visually_reviewed_pages']==len(render['rows']) and notes['journal_visually_reviewed']
state=read(R/'etat-projet.json');state.update(release=a.version,baseline=a.baseline,notes=notes['description'],next=f'Continuer les {remaining} textes et les tables. Audits hérités et scènes naturelles ouverts, pas finalisé.')
reliquat=read(O/'qa-reliquat.json');state['deferred_remaining_from_v034']=reliquat['historical_v034']['remaining_count'];state['resolved_from_v034_ids']=reliquat['historical_v034']['resolved_ids']
state['main_script'].update(validated=total,new_this_pass=n,remaining=remaining);state['separate_tables'].update(inventory_version=a.version,new_this_pass=0)
save(R/'etat-projet.json',state);save(O/'etat-projet.json',state);save(O/'prepares-non-inseres.json',[])
bus=read(P/'emulator-tests/bus-verification.json');assert bus['groups_checked']==874 and bus['all_rom_bus_reads_match'];save(O/'qa-script-and-name-bus.json',bus)
emulation=dict(result_sha256=sha(O/'result.sfc'),new_texts_rendered=n,pages_visually_reviewed=len(render['rows']),core_commit='1bcc369e89f08243e0a462882fb1f3e42e51de3a',journal_visually_reviewed=True,journal_sha256=sha(P/'emulator-tests'/f'{tag}-journal.png'),natural_scenes_played=False,real_transactions_tested=False,limits=notes['limits'])
if (O/'qa-stress-B5.json').exists():
 stress=read(O/'qa-stress-B5.json');assert stress['result_sha256']==sha(O/'result.sfc');assert notes['stress_visually_reviewed_pages']==len(stress['rows']);emulation.update(stress_texts=len({r['id'] for r in stress['rows']}),stress_pages_visually_reviewed=len(stress['rows']),stress_private_swap_positions=[1604,1638],stress_name='Iron Ball of Destruction',stress_cells=24)
save(O/f'qa-emulation-{tag}.json',emulation)
text=f'''# Dragon Quest VI FR — {a.version} partielle

{total}/6957 messages intégrés, {n} nouveaux ; {remaining} restants. Aucun préparé principal nouveau. Tables inchangées : 37 entrées françaises confirmées, 25 lieux préparés. Toujours 8 Mio.

{notes['description']}

Français DS fourni comme source principale, japonais SFC/DS et contexte relus, ancien IPS secondaire souvent décalé. Revue explicite revue-lot-{tag}.json. Les {total-n} anciennes sélections et les 2512 noms sont inchangés. Aucun handler modifié. Recette idempotente pass{v}.py, base {a.baseline}. Restaurer par restore_sources.py, puis init.py, prepare.py, build.py et verify.py sous dq6-fr/{a.version}. Périmètre limité aux nouveaux IDs relus. BPS/IPS réappliqués à la source intacte, mauvaises sources rejetées, 6960 entrées redécodées, zones protégées et occurrences natives contrôlées.

SHA256 résultat : {sha(O/'result.sfc')}.

Snes9x : {len(render['rows'])} pages de diagnostic relues pour les {n} textes ; bus de {bus['groups_checked']} plages et {bus['bytes_checked']} octets ; démarrage/Journal. {notes['test_details']}

Limites : {notes['limits']}

Appliquer patches/DQVI-FR-DS-{a.version}-BASE-JP-PARTIEL.bps directement sur la ROM JP intacte sans en-tête, SHA256 90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Aucun ancien patch préalable. Aucune ROM, SRAM, sauvegarde d’état ni archive de ROM publiée.

Scènes naturelles 322/323,1836,4095, indices différés, {state['deferred_remaining_from_v034']} cas encore différés sur les 26 cas historiques v0.34, alphabet accentué et fenêtres natives des tables restent ouverts. Ne pas annoncer finalisé.
'''
(O/'LISEZ-MOI.md').write_text(text);(R/'LISEZ-MOI.md').write_text(text)
(R/'README.md').write_text(f'# Dragon Quest VI — traduction française Super Famicom\n\nVersion {a.version} partielle : **{total}/6957 textes intégrés**, {remaining} restants. Dernier lot : {n} ajouts. Tables : 37 entrées françaises confirmées, 25 lieux préparés. Projet non finalisé.\n\nPatch BPS dans patches/, sur ROM japonaise intacte sans en-tête (CRC32 33304519). Sources : python restore_sources.py ; lire REPRISE-AUTOMATIQUE.md et LISEZ-MOI.md. Aucune ROM, SRAM ni sauvegarde d’état publiée.\n\nRestauration, reconstruction, patchs et régression vérifiés. Essais Snes9x décrits dans les rapports ; diagnostics au camp, pas parcours naturel ni transactions.\n')
reprise=R/'REPRISE-AUTOMATIQUE.md';reprise.write_text(f'# Reprise {a.version}\n\n'+state['notes']+' '+state['next']+'\n\n'+reprise.read_text())
patch=R/'patches'/f'DQVI-FR-DS-{a.version}-BASE-JP-PARTIEL.bps';shutil.copy2(O/patch.name,patch)
files=[P/f'pass{v}.py',Path(__file__),P/'audit_reliquat_v043.py',patch]
proof=R/f"verification-{a.baseline.replace('.','')}-depuis-git.json"
if proof.exists():files.append(proof)
for f in O.iterdir():
 if f.suffix=='.py' or f.name in [f'revue-lot-{tag}.json','revues-preparatoires-remplacees.json','nouveaux-messages.json','couverture-preparation.json','validation.json','layout-names-check.json','prepares-non-inseres.json','inventaire-tables.json','LISEZ-MOI.md','etat-projet.json'] or (f.name.startswith('qa-') and f.suffix=='.json'):files.append(f)
manifest=dict(kind='readable_translation_delta',version=a.version,baseline=a.baseline,baseline_count=total-n,new_count=n,recipe=f'dq6-fr/pass{v}.py',merged_selection_sha256=sha(O/'insertion-candidates.json'),generated_inputs={x:sha(O/x) for x in ['correspondances-revues.json','adaptations-francaises.json','liaisons-variables-natives.json','charset.json']},files=[dict(path=str(f.relative_to(R)),sha256=sha(f),bytes=f.stat().st_size) for f in files])
save(R/'sources/lots'/f'{a.version}.json',manifest);save(R/f'publish-{tag}-files.json',[str(f.relative_to(R)) for f in files]+[f'sources/lots/{a.version}.json','LISEZ-MOI.md','REPRISE-AUTOMATIQUE.md','etat-projet.json','README.md']);print(len(files),'authorized files')
