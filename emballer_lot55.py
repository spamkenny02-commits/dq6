"""Explicit public sources/review/QA/BPS allowlist; never a ROM or game state."""
from pathlib import Path
import json,hashlib,shutil,sys
R=Path(__file__).resolve().parent;D=R/'dq6-fr';O=D/'v0.55';B=D/'v0.54';read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
r=read(O/'revue-lot-v055.json');new=read(O/'insertion-candidates.json');old=read(B/'insertion-candidates.json');by={x['id']:x for x in new}
assert len(r)==38 and len(old)==6903 and len(new)==6941 and all(by[x['id']]['tokens']==x['tokens'] for x in old)
digest=sha(O/'result.sfc');pages=read(O/'qa-render-fixtures.json');comp=read(O/'qa-compositions.json');visual=read(O/'qa-relecture-visuelle.json');bus=read(O/'qa-script-name-engine-bus.json');reg=read(O/'qa-runtime.json')
for x in [pages,comp,visual,bus,reg]:assert x['result_sha256']==digest
assert visual['all_final_captures_reviewed'] and visual['all_composite_captures_reviewed'] and visual['accepted_final_pages']==len(pages['rows'])==29 and len(comp['rows'])==42
assert {x['id'] for x in r if not x.get('structural_only')}==set(visual['reviewed_ids'])
assert bus['groups_checked']>=890 and bus['all_rom_bus_reads_match']
proof=O/'qa-restauration-propre.json'
if '--provisional' in sys.argv and not proof.exists():save(proof,dict(pending=True,result_sha256=digest))
if '--provisional' not in sys.argv:assert read(proof)['fresh_destination'] and read(proof)['result_sha256']==digest
# No inherited engine/name/font/frame changes in either copy.
a=(O/'result.sfc').read_bytes();b=(B/'result.sfc').read_bytes()
for c in [0,0x400000]:
 for lo,hi in [(0x58366,0x58374),(0x4b,0x4e),(0x2b7e,0x2bfd),(0x165e7,0x1785e),(0x3b8703,0x3bc712),(0x159d2,0x15ad1),(71270,71305)]:assert a[c+lo:c+hi]==b[c+lo:c+hi],hex(lo)
save(O/'qa-noms-moteur-inchanges.json',dict(old_tokens_unchanged=6903,name_sids_unchanged=2512,native_engine_tree_vectors_loader_and_name_frame_unchanged=True,baseline='v0.54 public BPS',result_sha256=digest))
state=read(R/'etat-projet.json');state.update(release='v0.55',baseline='v0.54',main_script=dict(validated=6941,visible_total=6957,new_this_pass=38,new_linguistic_translations=29,new_structural_restorations=9,linguistic_selected=6932,structural_selected=9,remaining=16,remaining_linguistic=16),notes='29 traductions et9 restaurations exactes de structure. Toutes les6903 anciennes sélections inchangées. Tests de composition AE, énigme et directions ; audits naturels ouverts.',next='16 textes restants :12 debug ambigus et6956 préparés non insérés,3 fragments équipement différés. Tables, recherche exhaustive des oublis, relecture intégrale et audits naturels à poursuivre.');state['prepared_not_inserted'].update(main=13,reviewed_fragments=0,draft_main=12,boundary_audit=1);state['separate_tables']['inventory_version']='v0.55'
for p in [R/'etat-projet.json',O/'etat-projet.json']:save(p,state)
text=f'''# DQVI FR v0.55 partielle

6941/6957 sélections intégrées :29 nouvelles traductions et9 restaurations exactes de structure sans texte. Total6932 entrées linguistiques sélectionnées et9 structurelles.16 textes restent :13 préparés non insérés (12 ambiguïtés debug et6956),3 fragments équipement différés. Ces13 font partie des16. Aucune finalisation annoncée. ROM8 Mio.

Énigme610 et12 entrées de choix/échos : français DS relu contre JP et contexte, formule Frizzam, indices vérité/lame et galets/glace. Ordre des options natif conservé (réponses1/3/2). Prévisualisation de la princesse abrégée avec suspension, écho complet. Correction du contresens IPS1319.4952 : Roi Louis et paroles indéchiffrables, caption éditoriale assumée au lieu de glyphes chiffrés JP incompatibles ; aucun sens inventé au sort.5351 : statue Goyle, sud, main gauche au mur, premier buisson ; route SFC, pas géographie DS importée.6157 : château de Mortamor après la chute.6019 : confirmation neutre DE.12 fragments de directions/services itinérants composés avec AE/AC et variables BB conservés.

Entrées1/2/3/2358/5699/5700/5775/6213/6214 restaurées aux tokens japonais exacts, sans les compter comme traductions françaises. Audit hérité isolé : contrairement à une hypothèse précédente,5700 et5775 récupéraient des textes VF décalés ;5699 et6213 différaient aussi dans les espaces/la disposition. Aucun des6903 anciens messages sélectionnés réécrit.

Le compilateur ajoute un mode de disposition fixe pour fragments/choix, sans retour automatique supposant colonne zéro. Les commandes non typographiques et les terminators source sont préservés. Aucune modification du moteur, de la table des noms, de l'alphabet, des polices, du cadre du nom, Journal/Options ni des crédits retirés.

prepare.py/build.py/verify.py exécutés :6960 entrées redécodées, BPS/IPS réappliqués à la source JP intacte, mauvaises sources rejetées, zones protégées vérifiées. Vérification des9 structures contre JP. Snes9x :29 pages autonomes des8 textes concernés,42 captures composées couvrant les21 fragments (8 directions avec valeurs12345/16777215,7 services,27 combinaisons de l'énigme). Toutes ces captures ont été lues. Bus{bus['groups_checked']} plages/{bus['bytes_checked']} octets, démarrage et Journal1–3 lus. Tous les29 nouveaux textes sont couverts par ces diagnostics ; ce n'est pas une validation des scènes naturelles.

Tests de composition : commandes AE et D5 source réellement exécutées sur callbacks100/101/103 du camp. Un AF privé ajouté avant le terminator final retient la capture ; absent du patch publié. Le contexte du camp imprime parfois une étoile de locuteur par ligne. Aucun calcul naturel des coordonnées, déclenchement de service, choix de porte, levée de sceau, récompense, scène de Roi Louis, route du bouclier ou écriture de sauvegarde validé.

6956 : audit reproductible montre que l'extraction finale poursuit son décodage dans la table des noms après0x3b8703. Préfixe utile jusqu'au premier AF connu, mais terminator natif à établir. Traduction proposée conservée PREPARE_NON_INSERE ; aucun remplacement aveugle du faux texte final.12 libellés debug restent préparés tant que leur appel/fonction n'est pas établi,3 fragments d'équipement restent différés avec leur composition et5698 à auditer.

Tables réinventoriées :2512 SID,2048 entrées physiques,464 alias ;37 libellés FR confirmés et4 aides grammaticales,25 lieux préparés.1558 autres textes à revoir,346 identifiants,83 vides à qualifier,23 identités DS à vérifier et1 crédit retiré. Zéro japonais détecté ne prouve pas une traduction française. Audits322/323/1836/4095, routes1135/2404/5341/5351, énigme610 naturelle, alphabet et fenêtres restent ouverts. Recherche exhaustive des ressources et grosse relecture complète non terminées.

SHA256 résultat :{digest}. Patch BPS pour JP sans en-tête SHA25690ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e. Restauration neuve vérifiée avant publication ; preuve depuis Git publiée séparément après récupération du commit. Sources/revues/rapports/patch uniquement ; aucune ROM, SRAM ni état d'émulation.
'''
for p in [R/'LISEZ-MOI.md',O/'LISEZ-MOI.md']:p.write_text(text)
(R/'README.md').write_text('# Dragon Quest VI — traduction française Super Famicom\n\nv0.55 partielle : **6941/6957 sélections**, dont9 entrées structurelles ; **16 textes restants**.29 nouvelles traductions,9 restaurations source. Tables, audits naturels et relecture exhaustive encore ouverts.\n\nPatch dans patches/. Lire LISEZ-MOI.md et REPRISE-AUTOMATIQUE.md. Restaurer par python restore_sources.py. Aucune ROM ou sauvegarde publiée.\n')
p=R/'REPRISE-AUTOMATIQUE.md';head='# Reprise v0.55\n\n'+state['notes']+' '+state['next']+' Ne pas recycler cette revue. Ne pas prendre les9 structures pour9 traductions.\n\n';s=p.read_text();p.write_text(s if s.startswith(head) else head+s)
patch=R/'patches/DQVI-FR-DS-v0.55-BASE-JP-PARTIEL.bps';shutil.copy2(O/patch.name,patch)
files=[R/n for n in ['plans55.py','creer55.py','point55.py','emballer_lot55.py','reconstruire_propre55.py']]+[D/'pass55.py',D/'audit_frontiere_v055.py',patch]
allowed={'revue-lot-v055.json','prepares-non-inseres.json','revues-preparatoires-remplacees.json','nouveaux-messages.json','nouveaux-prepares-v055.json','validation.json','couverture-preparation.json','etat-projet.json','LISEZ-MOI.md','inventaire-tables.json','layout-engine-check.json'}
for p in sorted(O.iterdir()):
 if p.suffix=='.py' or p.name in allowed or p.name.startswith('qa-') and p.suffix=='.json':files.append(p)
assert all(p.suffix in {'.py','.json','.md','.bps'} for p in files)
spec=dict(kind='readable_translation_delta',version='v0.55',baseline='v0.54',baseline_count=6903,new_count=38,new_linguistic_translations=29,new_structural_restorations=9,recipe='dq6-fr/pass55.py',merged_selection_sha256=sha(O/'insertion-candidates.json'),generated_inputs={n:sha(O/n) for n in ['correspondances-revues.json','adaptations-francaises.json','liaisons-variables-natives.json','charset.json','prepares-non-inseres.json']},files=[dict(path=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size) for p in files]);save(R/'sources/lots/v0.55.json',spec);save(R/'publish-v055-files.json',[str(p.relative_to(R)) for p in files]+['sources/lots/v0.55.json','README.md','LISEZ-MOI.md','REPRISE-AUTOMATIQUE.md','etat-projet.json']);print(len(files),'authorized files')
