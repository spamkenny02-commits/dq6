"""Authorized v0.48 source/report/BPS checkpoint. Never include ROM or save data."""
from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parent;P=R/'dq6-fr';O=P/'v0.48';B=P/'v0.47'
read=lambda p:json.loads(p.read_text());save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=read(O/'revue-lot-v048.json');qa=read(O/'qa-render-fixtures.json');visual=read(O/'qa-relecture-visuelle.json');bus=read(O/'qa-script-name-engine-bus.json');proof=read(O/'qa-restauration-propre.json')
assert len(review)==143 and len(qa['rows'])==visual['accepted_final_pages']==272
assert {x['id'] for x in review}=={x['id'] for x in qa['rows']}
assert sha(O/'result.sfc')==qa['result_sha256']==proof['result_sha256']==bus['result_sha256']
assert bus['groups_checked']==880 and bus['all_rom_bus_reads_match']
assert all(json.loads(x['output'].splitlines()[0])['message_id']==100 for x in qa['rows'])
old=read(B/'insertion-candidates.json');now=read(O/'insertion-candidates.json');by={x['id']:x for x in now};assert len(old)==6529 and len(now)==6672
assert all(x['tokens']==by[x['id']]['tokens'] for x in old)
a=(O/'result.sfc').read_bytes();b=(B/'result.sfc').read_bytes()
for copy in [0,0x400000]:
 for lo,hi in [(0x58366,0x5836a),(0x4b,0x4e),(0x2bfb,0x2bfd),(0x165e7,0x1785e),(0x3b8703,0x3bc712)]:assert a[copy+lo:copy+hi]==b[copy+lo:copy+hi]
save(O/'qa-noms-moteur-inchanges.json',dict(previous_main_tokens_unchanged=6529,all_2512_name_sids_unchanged_from_v047=True,names_tree_C4_vector_naming_window_byte_equal_both_copies=True,new_variable_controls=0))
state=read(R/'etat-projet.json');reliquat=read(O/'qa-reliquat.json');assert reliquat['remaining']==285
state.update(release='v0.48',baseline='v0.47',notes='143 textes SFC relus : dialogues, panneaux, objets légendaires, commerces et quelques libellés techniques. 69 références DS de formulation, fragments ou lexique, avec écarts SFC documentés ; 74 adaptations directes sans équivalent DS validé. Pauses natives conservées. Ancien IPS secondaire relu mais ses nombreux décalages sont rejetés.',next='Terminer les 285 entrées restantes, dont19 préparées non insérées, en traitant les dialogues couplés et commandes avant toute annonce de finalisation. Continuer aussi les tables et audits naturels.')
state['main_script'].update(validated=6672,new_this_pass=143,remaining=285);state['separate_tables']['inventory_version']='v0.48';state['separate_tables']['new_this_pass']=0;state['deferred_remaining_from_v034']=reliquat['historical_v034']['remaining_count'];state['resolved_from_v034_ids']=reliquat['historical_v034']['resolved_ids'];save(R/'etat-projet.json',state);save(O/'etat-projet.json',state)
text=f'''# DQVI FR v0.48 partielle

6672/6957 messages intégrés,143 ajouts,285 restants.19 préparés non insérés :11 fragments hérités et8 brouillons différés. Tables séparées :37 libellés français confirmés, quatre aides grammaticales v0.44,25 lieux préparés. Projet non finalisé. ROM de travail8 Mio.

{state['notes']}

La revue garde le japonais, le contexte voisin, l’ancien IPS et les références DS effectivement relues. Rang A SFC, bouton R, maison de divination, consigne d’objets, quatre légendes et signes des équipements conservés ; ne pas importer les variantes DS incompatibles. Braséria, Pascal et les autres noms sont contrôlés contre les sources DS. Les messages de démonstration ou de débogage ne sont pas présentés comme des dialogues naturels.

6529 anciens tokens,2512 noms, police, Huffman, vecteur C4 et cadre du nom inchangés. Journal/Options et retrait des crédits conservés.6960 entrées redécodées ; réapplication BPS/IPS à la source intacte, rejet de mauvaises sources et zones protégées contrôlés. Recette pass48.py idempotente. Restauration dans un nouveau dossier puis init.py/prepare.py/build.py/verify.py : résultat identique.

Snes9x :272 pages finales pour143 textes, toutes relues ; bus des870 placements courants plus noms/moteur,880 plages/{bus['bytes_checked']} octets ; démarrage/menu Nouveau jeu. Le banc initial sautait le premier paragraphe très court5067 par maintien du bouton A. Protocole corrigé à un seul frame d’appui, testé sur quatre cas, puis recapture complète des143 textes. Aucune modification du moteur pour contourner ce problème de banc. Captures par redirection du message100 au camp : aucune scène naturelle, transaction, commande de débogage ou écriture SRAM validée. Aucun nouveau contrôle de nom variable dans ce lot.

SHA256 résultat :{sha(O/'result.sfc')}. BPS sur JP sans en-tête SHA25690ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Aucune ROM, SRAM, sauvegarde d’état ou archive de ROM publiée.

Ouverts : scènes322/323/1836/4095, indices610/1135/2404/5341/5351, fragments assemblés, commandes rares, tables et alphabet accentué. Les{reliquat['historical_v034']['remaining_count']} différés historiques non résolus sont conservés dans qa-reliquat.json. Aucune validation globale du jeu ou des tables n’est annoncée.
'''
for p in [R/'LISEZ-MOI.md',O/'LISEZ-MOI.md']:p.write_text(text)
(R/'README.md').write_text('# Dragon Quest VI — traduction française Super Famicom\n\nv0.48 partielle : **6672/6957 messages intégrés**,285 restants dont19 préparés non insérés.143 ajouts relus et vérifiés. Tables et audits ouverts ; projet non finalisé.\n\nPatch BPS dans patches/. Lire LISEZ-MOI.md et REPRISE-AUTOMATIQUE.md. Restaurer par python restore_sources.py. Aucune ROM ou sauvegarde publiée.\n')
f=R/'REPRISE-AUTOMATIQUE.md';head='# Reprise v0.48\n\n'+state['notes']+' '+state['next']+'\n\n';oldtext=f.read_text();f.write_text(oldtext if oldtext.startswith(head) else head+oldtext)
patch=R/'patches/DQVI-FR-DS-v0.48-BASE-JP-PARTIEL.bps';shutil.copy2(O/patch.name,patch)
files=[P/'pass48.py',P/'audit_reliquat_v048.py',Path(__file__).resolve(),R/'revoir_lot48.py',R/'traductions-v048.json',R/'reconstruire_propre48.py',R/'planches_relecture48.py',patch]
for p in O.iterdir():
 if p.suffix=='.py' or p.name in ['revue-lot-v048.json','prepares-non-inseres.json','revues-preparatoires-remplacees.json','nouveaux-messages.json','validation.json','couverture-preparation.json','etat-projet.json','LISEZ-MOI.md','inventaire-tables.json','layout-engine-check.json'] or p.name.startswith('qa-') and p.suffix=='.json':files.append(p)
spec=dict(kind='readable_translation_delta',version='v0.48',baseline='v0.47',baseline_count=6529,new_count=143,recipe='dq6-fr/pass48.py',merged_selection_sha256=sha(O/'insertion-candidates.json'),generated_inputs={n:sha(O/n) for n in ['correspondances-revues.json','adaptations-francaises.json','liaisons-variables-natives.json','charset.json']},files=[dict(path=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size) for p in files]);save(R/'sources/lots/v0.48.json',spec);save(R/'publish-v048-files.json',[str(p.relative_to(R)) for p in files]+['sources/lots/v0.48.json','README.md','LISEZ-MOI.md','REPRISE-AUTOMATIQUE.md','etat-projet.json']);print(len(files),'authorized source/report/patch files')
