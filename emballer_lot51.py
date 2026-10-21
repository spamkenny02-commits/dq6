"""Explicit public source/report/BPS allowlist for v0.51; no ROM or game saves."""
from pathlib import Path
import json,hashlib,shutil,sys
R=Path(__file__).resolve().parent;D=R/'dq6-fr';O=D/'v0.51';B=D/'v0.50'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
r=read(O/'revue-lot-v051.json');new=read(O/'insertion-candidates.json');old=read(B/'insertion-candidates.json');by={x['id']:x for x in new}
assert len(r)==16 and len(old)==6864 and len(new)==6880 and all(by[x['id']]['tokens']==x['tokens'] for x in old)
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
save(O/'qa-noms-moteur-inchanges.json',dict(old_tokens_unchanged=6864,name_sids_unchanged=2512,native_engine_tree_vectors_loader_and_name_frame_unchanged=True,baseline='v0.50 public BPS',result_sha256=digest))
state=read(R/'etat-projet.json');state.update(release='v0.51',baseline='v0.50',main_script=dict(validated=6880,visible_total=6957,new_this_pass=16,remaining=77),notes='16 descriptions de vocations SFC relues avec lexique DS explicite. Techniques, prérequis et mécaniques SFC conservés ; ancien IPS secondaire corrigé sans servir de validation.',next='Continuer les77 entrées, dont26 préparées non insérées, les tables et audits. Après traduction, recherche exhaustive des oublis et relecture de tous les textes par lots suivis.');state['separate_tables']['inventory_version']='v0.51'
for p in [R/'etat-projet.json',O/'etat-projet.json']:save(p,state)
text=f'''# DQVI FR v0.51 partielle

6880/6957 messages intégrés :16 ajouts,77 restants, dont26 préparés non insérés (12 fragments,14 brouillons). Aucun nouveau préparé. ROM8 Mio. Projet non finalisé.

Descriptions6020–6035 de toutes les vocations ordinaires et avancées, relues contre le japonais SFC. Le français DS fournit les noms de vocations/techniques par références explicites, sans prétendre à un alignement complet de dialogues. Le recrutement de monstres SFC reste décrit. Le Ranger requiert Voleur, Maître monstres et Marchand, pas Soldat comme dans l’ancien IPS. Dernière danse SFC traduite descriptivement : aucune identité de nom/SID avec Antidanse DS imposée. Les quatre paragraphes comiques de la Sommité et les conditions vagues du Héros sont conservés ; pas de condition de maîtrise totale inventée.

6864 anciens tokens et2512 noms inchangés. Aucun changement moteur, polices, commandes, Journal/Options, crédits retirés ni cadre du nom. prepare.py/build.py/verify.py :6960 entrées redécodées, BPS/IPS réappliqués, sources erronées rejetées et zones protégées contrôlées. Recette pass51.py idempotente ; restauration neuve et reconstruction identiques.

Snes9x :{len(pages['rows'])} pages pour les16 descriptions, toutes relues, et{len(reg['rows'])} pages de régression héritée784/6939/752 (noms, objet, nombre et DF), également relues. Démarrage et Journal vérifiés. Bus880 plages/{bus['bytes_checked']} octets contrôlés. Bancs au camp via message100 : pas de parcours naturel des vocations, de recrutement réel, transaction ou écriture SRAM validés. Aucun test de nouvelle commande rare revendiqué.

Inventaire séparé reproduit :2512 SID,2048 entrées physiques,464 alias ;37 libellés FR confirmés et4 aides grammaticales,25 lieux préparés.1558 autres textes,346 identifiants,83 vides à qualifier,23 identités DS nécessitant contexte et1 crédit retiré.0 japonais détecté ne signifie pas tables traduites. Les fenêtres et l’alphabet accentué restent à auditer.

Restent les choix/indices couplés610/1135/2404/5341/5351, fragments/compositions, commandes rares,6956 et audits naturels322/323/1836/4095. Les7 entrées structurelles/non linguistiques ne sont pas comptées comme traductions nouvelles. Relecture exhaustive non encore commencée : aucun faux compte de relecture globale.

SHA256 résultat :{digest}. BPS pour JP sans en-tête SHA25690ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Sources, revues, état du projet, rapports et patch seulement ; aucune ROM, SRAM ou état d’émulateur.
'''
for p in [R/'LISEZ-MOI.md',O/'LISEZ-MOI.md']:p.write_text(text)
(R/'README.md').write_text('# Dragon Quest VI — traduction française Super Famicom\n\nv0.51 partielle : **6880/6957 messages intégrés**,77 restants dont26 préparés non insérés.16 descriptions de vocations relues et testées en diagnostic. Tables et audits ouverts.\n\nPatch dans patches/. Lire LISEZ-MOI.md et REPRISE-AUTOMATIQUE.md. Restaurer par python restore_sources.py. Aucune ROM ou sauvegarde publiée.\n')
p=R/'REPRISE-AUTOMATIQUE.md';head='# Reprise v0.51\n\n'+state['notes']+' '+state['next']+' Ne pas recycler la revue de ce lot.\n\n';s=p.read_text();p.write_text(s if s.startswith(head) else head+s)
patch=R/'patches/DQVI-FR-DS-v0.51-BASE-JP-PARTIEL.bps';shutil.copy2(O/patch.name,patch)
files=[R/'plans51.py',R/'creer51.py',D/'pass51.py',D/'audit_reliquat_v051.py',Path(__file__).resolve(),R/'reconstruire_propre51.py',patch]
allowed={'revue-lot-v051.json','prepares-non-inseres.json','revues-preparatoires-remplacees.json','nouveaux-messages.json','nouveaux-prepares-v051.json','validation.json','couverture-preparation.json','etat-projet.json','LISEZ-MOI.md','inventaire-tables.json','layout-engine-check.json'}
for p in sorted(O.iterdir()):
 if p.suffix=='.py' or p.name in allowed or p.name.startswith('qa-') and p.suffix=='.json':files.append(p)
assert all(p.suffix in {'.py','.json','.md','.bps'} for p in files)
spec=dict(kind='readable_translation_delta',version='v0.51',baseline='v0.50',baseline_count=6864,new_count=16,recipe='dq6-fr/pass51.py',merged_selection_sha256=sha(O/'insertion-candidates.json'),generated_inputs={n:sha(O/n) for n in ['correspondances-revues.json','adaptations-francaises.json','liaisons-variables-natives.json','charset.json','prepares-non-inseres.json']},files=[dict(path=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size) for p in files]);save(R/'sources/lots/v0.51.json',spec);save(R/'publish-v051-files.json',[str(p.relative_to(R)) for p in files]+['sources/lots/v0.51.json','README.md','LISEZ-MOI.md','REPRISE-AUTOMATIQUE.md','etat-projet.json']);print(len(files),'authorized files')
