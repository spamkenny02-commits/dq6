"""Explicit public source/report/BPS allowlist for v0.54; no ROM or game saves."""
from pathlib import Path
import json,hashlib,shutil,sys
R=Path(__file__).resolve().parent;D=R/'dq6-fr';O=D/'v0.54';B=D/'v0.53'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
r=read(O/'revue-lot-v054.json');new=read(O/'insertion-candidates.json');old=read(B/'insertion-candidates.json');by={x['id']:x for x in new}
assert len(r)==8 and len(old)==6895 and len(new)==6903 and all(by[x['id']]['tokens']==x['tokens'] for x in old)
digest=sha(O/'result.sfc');pages=read(O/'qa-render-fixtures.json');visual=read(O/'qa-relecture-visuelle.json');bus=read(O/'qa-script-name-engine-bus.json');reg=read(O/'qa-runtime.json')
for x in [pages,visual,bus,reg,read(O/'qa-runtime.json')]:assert x['result_sha256']==digest
assert visual['all_final_captures_reviewed'] and visual['accepted_final_pages']==len(pages['rows']) and {x['id'] for x in r}=={x['id'] for x in pages['rows']}
assert bus['groups_checked']==890 and bus['all_rom_bus_reads_match']
proof=O/'qa-restauration-propre.json'
if '--provisional' in sys.argv and not proof.exists():save(proof,dict(pending=True,result_sha256=digest))
if '--provisional' not in sys.argv:assert read(proof)['fresh_destination'] and read(proof)['result_sha256']==digest
# Isolated name/frame/font/engine equality checks, in both ROM mappings.
a=(O/'result.sfc').read_bytes();b=(B/'result.sfc').read_bytes()
for c in [0,0x400000]:
 for lo,hi in [(0x58366,0x58374),(0x4b,0x4e),(0x2b7e,0x2bfd),(0x165e7,0x1785e),(0x3b8703,0x3bc712),(0x159d2,0x15ad1),(71270,71305)]:assert a[c+lo:c+hi]==b[c+lo:c+hi],hex(lo)
save(O/'qa-noms-moteur-inchanges.json',dict(old_tokens_unchanged=6895,name_sids_unchanged=2512,native_engine_tree_vectors_loader_and_name_frame_unchanged=True,baseline='v0.53 public BPS',result_sha256=digest))
state=read(R/'etat-projet.json');state.update(release='v0.54',baseline='v0.53',main_script=dict(validated=6903,visible_total=6957,new_this_pass=8,remaining=54),notes='8 textes à commandes natives C7/DC/E0/E1 relus. Autorisation minimale du compilateur, moteur et anciens tokens inchangés ; branches et noms testés en diagnostic.',next='Continuer les54 entrées dont25 préparées non insérées, fragments assemblés, tables, audits naturels et relecture exhaustive.');state['separate_tables']['inventory_version']='v0.54'
q=read(O/'qa-reliquat.json');state.update(deferred_remaining_from_v034=q['historical_v034']['remaining_count'],resolved_from_v034_ids=q['historical_v034']['resolved_ids']);state['prepared_not_inserted'].update(main=25,reviewed_fragments=12,draft_main=13)
for p in [R/'etat-projet.json',O/'etat-projet.json']:save(p,state)
text=f'''# DQVI FR v0.54 partielle

6903/6957 messages intégrés :8 ajouts,54 restants dont25 préparés non insérés (12 fragments,13 brouillons). Aucun nouveau préparé. ROM8 Mio. Projet non finalisé.

3727 garde E0, pronom natif vous/vous tous ; Svetlana confirmée DS0009:542.6548 garde E1, BB et D5, sans transaction inventée.6716/6718 : Calvin confirmé DS0074:109 ; B5 et C7 restent deux objets natifs séparés.6922–6925 : scène finale relue contre DS0098:29–32, CC et DC conservés ; Homme SFC gardé plutôt que Gardien DS, Seigneur Zénith confirmé, avenir qui a grandi sans ajout d’une nouvelle ère ; B0 de6925 conservé.

Extension minimale de native_plan.py pour C7/DC/E0/E1 uniquement dans cette version. C7 lit5A2C, B5 lit5A2A via le même résolveur ; E0 imprime les helpers011D/011E ; DC appelle la routine native de nettoyage puis met5A06 à zéro ; E1 transforme59A8=16 en33. Les handlers, helpers et arbre déjà présents sont conservés. Aucun moteur modifié. L’analyse de DC ne prétend pas valider le chemin de nettoyage conditionnel5A04 non nul.

6895 anciens tokens et2512 noms inchangés. prepare.py/build.py/verify.py :6960 entrées redécodées, BPS/IPS réappliqués, mauvaises sources rejetées et zones protégées contrôlées. Journal/Options, crédits retirés, polices et cadre du nom conservés. Recette idempotente, restauration neuve et reconstruction identiques.

Snes9x :{len(pages['rows'])} pages des8 nouveaux textes et{len(reg['probes'])} pages de stress, toutes relues. E0 compte forcé1/2, objets B5/C7 distincts et second objet de24 cellules, BB maximal, E1 injecté à0/16, DC avec5A04=0 et5A06 initial4660. Les observations RAM après rendu sont enregistrées, sans les confondre avec une preuve globale des effets de la machine d’état. Bus890 plages/{bus['bytes_checked']} octets, dont les handlers natifs dans les deux mappings ; démarrage et Journal vérifiés. Redirections message100 au camp : aucune scène finale naturelle, partie de concours, vente, achat ou écriture SRAM validée.

Tables inchangées et réinventoriées :2512 SID/2048 entrées physiques/464 alias ;37 libellés FR confirmés et4 aides grammaticales,25 lieux préparés.1558 autres textes,346 identifiants,83 vides à qualifier,23 identités DS à vérifier et1 crédit retiré.0 japonais détecté ne signifie pas tables traduites. Audits610/5351, fragments composés,6956, scènes322/323/1836/4095 et routes1135/2404/5341 restent ouverts, ainsi que l’exécution naturelle des nouvelles commandes. Relecture exhaustive non encore commencée.

SHA256 résultat :{digest}. BPS pour JP sans en-tête SHA25690ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Sources, revues, rapports et patch seulement ; aucune ROM, SRAM ou état d’émulateur.
'''
for p in [R/'LISEZ-MOI.md',O/'LISEZ-MOI.md']:p.write_text(text)
(R/'README.md').write_text('# Dragon Quest VI — traduction française Super Famicom\n\nv0.54 partielle : **6903/6957 messages intégrés**,54 restants dont25 préparés non insérés. Huit ajouts et commandes rares testés en diagnostic. Tables et audits naturels ouverts.\n\nPatch dans patches/. Lire LISEZ-MOI.md et REPRISE-AUTOMATIQUE.md. Restaurer par python restore_sources.py. Aucune ROM ou sauvegarde publiée.\n')
p=R/'REPRISE-AUTOMATIQUE.md';head='# Reprise v0.54\n\n'+state['notes']+' '+state['next']+' Ne pas recycler la revue de ce lot.\n\n';s=p.read_text();p.write_text(s if s.startswith(head) else head+s)
patch=R/'patches/DQVI-FR-DS-v0.54-BASE-JP-PARTIEL.bps';shutil.copy2(O/patch.name,patch)
files=[R/'plans54.py',R/'creer54.py',D/'pass54.py',D/'audit_reliquat_v054.py',Path(__file__).resolve(),R/'reconstruire_propre54.py',patch]
allowed={'revue-lot-v054.json','prepares-non-inseres.json','revues-preparatoires-remplacees.json','nouveaux-messages.json','nouveaux-prepares-v054.json','validation.json','couverture-preparation.json','etat-projet.json','LISEZ-MOI.md','inventaire-tables.json','layout-engine-check.json'}
for p in sorted(O.iterdir()):
 if p.suffix=='.py' or p.name in allowed or p.name.startswith('qa-') and p.suffix=='.json':files.append(p)
assert all(p.suffix in {'.py','.json','.md','.bps'} for p in files)
spec=dict(kind='readable_translation_delta',version='v0.54',baseline='v0.53',baseline_count=6895,new_count=8,recipe='dq6-fr/pass54.py',merged_selection_sha256=sha(O/'insertion-candidates.json'),generated_inputs={n:sha(O/n) for n in ['correspondances-revues.json','adaptations-francaises.json','liaisons-variables-natives.json','charset.json','prepares-non-inseres.json']},files=[dict(path=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size) for p in files]);save(R/'sources/lots/v0.54.json',spec);save(R/'publish-v054-files.json',[str(p.relative_to(R)) for p in files]+['sources/lots/v0.54.json','README.md','LISEZ-MOI.md','REPRISE-AUTOMATIQUE.md','etat-projet.json']);print(len(files),'authorized files')
