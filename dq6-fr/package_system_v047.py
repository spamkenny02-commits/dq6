"""Publish v0.47 reviewed sources, reports and BPS; ROM/save files stay private."""
from pathlib import Path
import json,hashlib,shutil
P=Path(__file__).resolve().parent;R=P.parent;O=P/'v0.47';B=P/'v0.46'
read=lambda p:json.loads(p.read_text());save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=read(O/'revue-lot-v047.json');qa=read(O/'qa-render-fixtures.json');assert len(review)==142 and len(qa['rows'])==146
assert {x['id'] for x in review}=={x['id'] for x in qa['rows']}
assert qa['result_sha256']==sha(O/'result.sfc')==read(O/'qa-restauration-propre.json')['result_sha256']
assert read(O/'qa-relecture-visuelle.json')['accepted_final_pages']==146
assert all(json.loads(x['output'].splitlines()[0])['message_id']==100 for x in qa['rows'])
bus=read(O/'qa-script-name-engine-bus.json');assert bus['groups_checked']==880 and bus['all_rom_bus_reads_match']
a=(O/'result.sfc').read_bytes();b=(B/'result.sfc').read_bytes()
for c in [0,0x400000]:
 for lo,hi in [(0x58366,0x5836a),(0x4b,0x4e),(0x2bfb,0x2bfd),(0x165e7,0x1785e),(0x3b8703,0x3bc712)]:assert a[c+lo:c+hi]==b[c+lo:c+hi]
save(O/'qa-noms-moteur-inchanges.json',dict(all_2512_name_sids_unchanged_from_v046=True,pool_pointers_root_tree_C4_vector_naming_window_byte_equal_both_copies=True,new_variable_name_controls=0,new_native_warning_pauses_preserved=[6057,6067,6165]))
state=read(R/'etat-projet.json');reliquat=read(O/'qa-reliquat.json');pre=read(O/'prepares-non-inseres.json');assert len(pre)==19
state.update(release='v0.47',baseline='v0.46',notes='142 libellés techniques, progression des quêtes et textes de démonstration SFC relus directement. Français DS utilisé comme lexique explicite pour 47 entrées ; aucun dialogue DS équivalent déclaré. Trois pauses d’avertissement natives conservées et testées. Huit brouillons ambigus restent non insérés, avec onze fragments hérités.',next='Continuer les 428 messages restants dont 19 préparés non insérés, les tables et les audits naturels. Projet non finalisé.')
state['main_script'].update(validated=6529,new_this_pass=142,remaining=428);state['prepared_not_inserted'].update(main=19,reviewed_fragments=11,draft_main=8);state['separate_tables'].update(inventory_version='v0.47',new_this_pass=0);state['deferred_remaining_from_v034']=reliquat['historical_v034']['remaining_count'];state['resolved_from_v034_ids']=reliquat['historical_v034']['resolved_ids'];save(R/'etat-projet.json',state);save(O/'etat-projet.json',state)
text=f'''# DQVI FR v0.47 partielle

6529/6957 messages intégrés, 142 ajouts, 428 restants dont 19 préparés non insérés (11 fragments hérités et 8 brouillons différés). Projet non finalisé. Tables : 37 libellés français confirmés, quatre aides grammaticales v0.44, 25 lieux préparés. ROM de travail 8 Mio.

{state['notes']}

Ce lot traduit des libellés de débogage/progression et des messages de démonstration ; il ne représente pas 142 dialogues naturels. Japonais SFC, voisinage et ancien IPS secondaire conservés dans la revue. Les références DS lexicales sont explicitement séparées des correspondances de dialogues. La grotte du Baptême du brouillon devient la grotte Sacrée attestée par le DS ; les codes M/C sont conservés. Les avertissements6057/6067/6165 gardent leur pauseAF et la seconde partie démarre à la page suivante. Le premier rendu, sans ces limites de paragraphes, est rejeté ; les142 textes sont recapturés sur le binaire final.

6387 anciennes sélections identiques, 6960 entrées redécodées, 2512 noms, police, cadre du nom, Huffman et vecteur C4 inchangés. Journal/Options, crédits retirés et variables natives conservés. Réapplication BPS/IPS à la source intacte, rejet des mauvaises sources et zones protégées contrôlés. Restauration propre dans un nouveau dossier puis init.py/prepare.py/build.py/verify.py : résultat identique. Recette idempotente pass47.py.

Snes9x : 146 pages finales relues pour les142 textes ; bus des870 placements courants plus noms/moteur,880 plages/{bus['bytes_checked']} octets ; démarrage/menu Nouveau jeu. Diagnostics par redirection du message100 au camp, pas des scènes naturelles. Aucune commande de débogage, transaction ou écriture de sauvegarde exécutée par ces contrôles d’affichage. Les142 ajouts ne contiennent aucun nom variable nouveau ; les anciens tokens et noms sont inchangés.

SHA256 résultat : {sha(O/'result.sfc')}. BPS sur JP sans en-tête SHA25690ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Aucune ROM, SRAM, sauvegarde d’état ou archive de ROM publiée.

Ouverts : huit brouillons (6040–6042,6046–6048,6157,6207), onze fragments à assembler, scènes naturelles322/323/1836/4095, indices610/1135/2404/5341/5351, {reliquat['historical_v034']['remaining_count']} différés historiquesv0.34, tables et alphabet accentué. Les références de résolution v0.45 du rapport de reliquat sont corrigées ici ; les anciennes sources historiques restent inchangées.
'''
for p in [O/'LISEZ-MOI.md',R/'LISEZ-MOI.md']:p.write_text(text)
(R/'README.md').write_text('# Dragon Quest VI — traduction française Super Famicom\n\nv0.47 partielle : **6529/6957 messages intégrés**, 428 restants dont19 préparés non insérés. Dernier lot :142 libellés techniques/progression et textes de démonstration. Tables et audits ouverts ; projet non finalisé.\n\nPatch BPS dans patches/. Lire LISEZ-MOI.md et REPRISE-AUTOMATIQUE.md. Restaurer par python restore_sources.py. Aucune ROM ou sauvegarde publiée.\n')
f=R/'REPRISE-AUTOMATIQUE.md';head='# Reprise v0.47\n\n'+state['notes']+' '+state['next']+'\n\n';old=f.read_text();f.write_text(old if old.startswith(head) else head+old)
patch=R/'patches/DQVI-FR-DS-v0.47-BASE-JP-PARTIEL.bps';shutil.copy2(O/patch.name,patch)
files=[P/'pass47.py',Path(__file__).resolve(),P/'audit_reliquat_v047.py',R/'revoir_lot47.py',R/'reconstruire_propre47.py',R/'verification-v046-depuis-git.json',patch]
for p in O.iterdir():
 if p.suffix=='.py' or p.name in ['revue-lot-v047.json','prepares-non-inseres.json','blocages-brouillons-v047.json','revues-preparatoires-remplacees.json','nouveaux-messages.json','validation.json','couverture-preparation.json','etat-projet.json','LISEZ-MOI.md','inventaire-tables.json','layout-engine-check.json'] or p.name.startswith('qa-') and p.suffix=='.json':files.append(p)
spec=dict(kind='readable_translation_delta',version='v0.47',baseline='v0.46',baseline_count=6387,new_count=142,recipe='dq6-fr/pass47.py',merged_selection_sha256=sha(O/'insertion-candidates.json'),generated_inputs={n:sha(O/n) for n in ['correspondances-revues.json','adaptations-francaises.json','liaisons-variables-natives.json','charset.json']},files=[dict(path=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size) for p in files]);save(R/'sources/lots/v0.47.json',spec);save(R/'publish-v047-files.json',[str(p.relative_to(R)) for p in files]+['sources/lots/v0.47.json','README.md','LISEZ-MOI.md','REPRISE-AUTOMATIQUE.md','etat-projet.json']);print(len(files),'authorized files')
