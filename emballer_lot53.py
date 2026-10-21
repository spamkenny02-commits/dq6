"""Explicit public source/report/BPS allowlist for v0.53; no ROM or game saves."""
from pathlib import Path
import json,hashlib,shutil,sys
R=Path(__file__).resolve().parent;D=R/'dq6-fr';O=D/'v0.53';B=D/'v0.52'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
r=read(O/'revue-lot-v053.json');new=read(O/'insertion-candidates.json');old=read(B/'insertion-candidates.json');by={x['id']:x for x in new}
assert len(r)==12 and len(old)==6883 and len(new)==6895 and all(by[x['id']]['tokens']==x['tokens'] for x in old)
digest=sha(O/'result.sfc');pages=read(O/'qa-render-fixtures.json');visual=read(O/'qa-relecture-visuelle.json');bus=read(O/'qa-script-name-engine-bus.json');reg=read(O/'qa-runtime.json')
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
save(O/'qa-noms-moteur-inchanges.json',dict(old_tokens_unchanged=6883,name_sids_unchanged=2512,native_engine_tree_vectors_loader_and_name_frame_unchanged=True,baseline='v0.52 public BPS',result_sha256=digest))
state=read(R/'etat-projet.json');state.update(release='v0.53',baseline='v0.52',main_script=dict(validated=6895,visible_total=6957,new_this_pass=12,remaining=62),notes='12 textes : six C4, casino, variante technique à X littéraux, refrain et libellés. Commandes et noms natifs gardés, deux branches C4 testées en diagnostic.',next='Continuer les62 entrées dont25 préparées non insérées, les tables et audits naturels. Recherche des oublis et relecture exhaustive encore à faire.');state['separate_tables']['inventory_version']='v0.53'
q=read(O/'qa-reliquat.json');state.update(deferred_remaining_from_v034=q['historical_v034']['remaining_count'],resolved_from_v034_ids=q['historical_v034']['resolved_ids']);state['prepared_not_inserted'].update(main=25,reviewed_fragments=12,draft_main=13)
for p in [R/'etat-projet.json',O/'etat-projet.json']:save(p,state)
text=f'''# DQVI FR v0.53 partielle

6895/6957 messages intégrés :12 ajouts,62 restants dont25 préparés non insérés (12 fragments,13 brouillons). Aucun nouveau préparé ;6207 auparavant préparé est intégré en conservant explicitement le titre poker High-Low sans inventer ses règles. ROM8 Mio. Projet non finalisé.

Six répliques2664/2683/2684/3728/4854/5195 gardent le suffixe natif C4 conditionnel après vous : accord compatible avec personne vouvoyée ou groupe.4854 garde C9 pour le prince et C4 pour son escorte, sans rattacher et Cie au prince. D4, C9 et pauses sources gardés. IPS secondaire lacunaire ou décalé rejeté comme validation. Aucun équivalent DS complet déclaré pour ces six textes ; japonais et voisins relus directement.

74 garde deux BB et le coût en jetons confirmé DS0824:0, sans conversion numérique.1716 conserve deux X littéraux SFC, D3 puis B5 ; aucun BB ajouté depuis la variante IPS. Aucun compteur réel validé.6169 garde cinquante ans/cinquante yens et AF, avec notes de musique déjà disponibles.6171 est transcrit Danchoné sans sens inventé.0 est le libellé technique non vide Aucun message, pas une entrée vide comptée comme traduction.

6883 anciens tokens et2512 noms inchangés. Aucun changement moteur, commandes, polices, Journal/Options, crédits retirés ou cadre du nom. prepare.py/build.py/verify.py :6960 entrées redécodées, BPS/IPS réappliqués, mauvaises sources rejetées et zones protégées contrôlées. Recette pass53.py idempotente, restauration neuve et reconstruction identiques.

Snes9x :{len(pages['rows'])} pages pour12 textes, toutes relues ;{len(reg['probes'])} pages de stress également relues, C4 forcé aux comptes1/2 sur les six répliques, BB=16777215 et objet de24 cellules. Démarrage et Journal vérifiés. Bus880 plages/{bus['bytes_checked']} octets. ROMs de diagnostic privées par redirection message100 au camp : les branches forcées ne valident pas le calcul naturel du groupe ; aucune partie réelle de casino/poker, médaille, transaction, acquisition ou écriture SRAM validée.

Tables séparées réinventoriées et inchangées :2512 SID/2048 entrées physiques/464 alias ;37 libellés FR confirmés et4 aides grammaticales,25 lieux préparés.1558 autres textes,346 identifiants,83 vides à qualifier,23 identités DS à vérifier et1 crédit retiré.0 japonais détecté ne signifie pas tables traduites. Audits610/5351, fragments assemblés, commandes rares,6956, scènes322/323/1836/4095 et routes1135/2404/5341 restent ouverts. Relecture exhaustive non encore commencée.

SHA256 résultat :{digest}. BPS pour JP sans en-tête SHA25690ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Sources, revues, rapports et patch seulement ; aucune ROM, SRAM ou état d’émulateur.
'''
for p in [R/'LISEZ-MOI.md',O/'LISEZ-MOI.md']:p.write_text(text)
(R/'README.md').write_text('# Dragon Quest VI — traduction française Super Famicom\n\nv0.53 partielle : **6895/6957 messages intégrés**,62 restants dont25 préparés non insérés.12 ajouts relus et testés en diagnostic, tables et audits ouverts.\n\nPatch dans patches/. Lire LISEZ-MOI.md et REPRISE-AUTOMATIQUE.md. Restaurer par python restore_sources.py. Aucune ROM ou sauvegarde publiée.\n')
p=R/'REPRISE-AUTOMATIQUE.md';head='# Reprise v0.53\n\n'+state['notes']+' '+state['next']+' Ne pas recycler la revue de ce lot.\n\n';s=p.read_text();p.write_text(s if s.startswith(head) else head+s)
patch=R/'patches/DQVI-FR-DS-v0.53-BASE-JP-PARTIEL.bps';shutil.copy2(O/patch.name,patch)
files=[R/'plans53.py',R/'creer53.py',D/'pass53.py',D/'audit_reliquat_v053.py',Path(__file__).resolve(),R/'reconstruire_propre53.py',patch]
allowed={'revue-lot-v053.json','prepares-non-inseres.json','revues-preparatoires-remplacees.json','nouveaux-messages.json','nouveaux-prepares-v053.json','validation.json','couverture-preparation.json','etat-projet.json','LISEZ-MOI.md','inventaire-tables.json','layout-engine-check.json'}
for p in sorted(O.iterdir()):
 if p.suffix=='.py' or p.name in allowed or p.name.startswith('qa-') and p.suffix=='.json':files.append(p)
assert all(p.suffix in {'.py','.json','.md','.bps'} for p in files)
spec=dict(kind='readable_translation_delta',version='v0.53',baseline='v0.52',baseline_count=6883,new_count=12,recipe='dq6-fr/pass53.py',merged_selection_sha256=sha(O/'insertion-candidates.json'),generated_inputs={n:sha(O/n) for n in ['correspondances-revues.json','adaptations-francaises.json','liaisons-variables-natives.json','charset.json','prepares-non-inseres.json']},files=[dict(path=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size) for p in files]);save(R/'sources/lots/v0.53.json',spec);save(R/'publish-v053-files.json',[str(p.relative_to(R)) for p in files]+['sources/lots/v0.53.json','README.md','LISEZ-MOI.md','REPRISE-AUTOMATIQUE.md','etat-projet.json']);print(len(files),'authorized files')
