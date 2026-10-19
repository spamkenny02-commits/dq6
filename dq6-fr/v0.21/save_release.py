"""Save the reviewed release metadata and a readable, ROM-free Git delta."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys

O=Path(__file__).resolve().parent;P=O.parent;R=P.parent
def read(p):return json.loads(p.read_text())
def save(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v=read(O/'validation.json');qa=read(O/'qa-render-fixtures.json')
assert v['ds_validated']==5078 and v['new_replacements']==20
assert qa['result_sha256']==v['result_sha256'] and len(qa['rows'])==31
bus=read(P/'emulator-tests/bus-verification.json')
assert bus['groups_checked']==870 and bus['bytes_checked']==v['payload_bytes']
save(O/'qa-bus.json',bus)
rows=read(O/'nouveaux-messages.json');assert len(rows)==20
for r in rows:
    for i,line in enumerate(r['lines']):assert len(line)<=(22 if i==0 else 24),(r['id'],i,line)
save(O/'qa-longueurs.json',dict(new_messages=20,first_line_columns_max=22,other_line_columns_max=24,all_new_lines_checked=True))
qa.update(visible_pages=31,reviewed_ids=[220,246,248,251,255,282],visual_review='31 captures relues : accents, noms des locuteurs, formulations neutres, apostrophe unique et pagination dans le cadre.',limits='Redirections diagnostiques depuis le camp ; le menu Oui/Non appartient au banc. Aucun parcours naturel complet des scenes declare.')
save(O/'qa-render-fixtures.json',qa)
notes='20 dialogues supplémentaires relus : fin de la quête de l’insigne du courage et Calcado/Aridéa avant et après l’île des Sourires. 5078/6957 messages du script principal ; 1879 restants, plus les tables séparées. Les 5058 sélections précédentes restent identiques. Deux variantes de genre DS neutralisées et une double apostrophe corrigée. BPS/IPS relus, 6960 entrées redécodées, 870 groupes contrôlés sur le bus. 31 pages de rendu ciblé sur six messages, sans parcours naturel complet.'
subprocess.run([sys.executable,str(P/'checkpoint.py'),'v0.21','--notes',notes],check=True)
shutil.copy2(O/'etat-projet.json',R/'etat-projet.json')
patch=O/'DQVI-FR-DS-v0.21-BASE-JP-PARTIEL.bps';assert patch.read_bytes().startswith(b'BPS1')
shutil.copy2(patch,R/'patches'/patch.name)
paths=['README.md','REPRISE-AUTOMATIQUE.md','etat-projet.json','dq6-fr/pass21.py','patches/'+patch.name,'sources/lots/v0.21.json']
names={'revue-lot-v021.json','etat-projet.json','LISEZ-MOI.md','validation.json','couverture-preparation.json','qa-bus.json','qa-render-fixtures.json','qa-longueurs.json','qa-patchs-regression.json','nouveaux-messages.json'}
paths += [str(p.relative_to(R)) for p in sorted(O.iterdir()) if p.is_file() and (p.suffix=='.py' or p.name in names)]
files=[p for p in paths if p.startswith('dq6-fr/v0.21/') or p in ['dq6-fr/pass21.py','patches/'+patch.name]]
spec=dict(kind='readable_translation_delta',version='v0.21',baseline='v0.20',baseline_count=5058,new_count=20,recipe='dq6-fr/pass21.py',merged_selection_sha256=digest(O/'insertion-candidates.json'),generated_inputs={name:digest(O/name) for name in ['correspondances-revues.json','adaptations-francaises.json','liaisons-variables-natives.json','charset.json']},files=[dict(path=p,sha256=digest(R/p),bytes=(R/p).stat().st_size) for p in files],no_rom_sram_or_state=True)
save(R/'sources/lots/v0.21.json',spec)
save(R/'publication-v021.json',paths)
print('Readable publication manifest:',len(paths),'files; no ROM, SRAM, state or opaque archive.')
