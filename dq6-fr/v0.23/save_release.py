"""Save the reviewed release and its readable, ROM-free incremental Git delta."""
from pathlib import Path
import hashlib,json,math,shutil,subprocess,sys
O=Path(__file__).resolve().parent;P=O.parent;R=P.parent
def read(p):return json.loads(p.read_text())
def save(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
v=read(O/'validation.json');qa=read(O/'qa-render-fixtures.json');ids=[383,397,407,458,459,489,526]
rows=read(O/'nouveaux-messages.json');byid={r['id']:r for r in rows}
pages=sum(math.ceil(len(byid[mid]['lines'])/3) for mid in ids)
assert v['ds_validated']==5128 and v['new_replacements']==30 and len(rows)==30
assert qa['result_sha256']==v['result_sha256'] and len(qa['rows'])==pages==27
bus=read(P/'emulator-tests/bus-verification.json');assert bus['groups_checked']==870 and bus['bytes_checked']==v['payload_bytes']
save(O/'qa-bus.json',bus)
for r in rows:
    for i,line in enumerate(r['lines']):assert len(line)<=(22 if i==0 else 24),(r['id'],i,line)
save(O/'qa-longueurs.json',dict(new_messages=30,first_line_columns_max=22,other_line_columns_max=24,all_new_lines_checked=True))
qa.update(visible_pages=pages,reviewed_ids=ids,visual_review='27 captures relues : accents, accueil pluriel, descriptions des pieces, noms Pretre et Lynx, tarifs 50000 et 2000, pagination dans le cadre.',limits='Redirections diagnostiques dans le camp ; le menu Oui/Non appartient au banc. Pas de parcours naturel complet. Audit semantique 322/323 ouvert et ancien blocage 1836 differe.')
save(O/'qa-render-fixtures.json',qa)
notes='30 dialogues supplémentaires relus à Colombourg et autour du defi de Lynx, soit 5128/6957 messages intégrés du script principal ; 1829 restants, plus les tables séparées. Les 5098 anciennes sélections restent identiques. Accueil pluriel, lieux SFC conservés avec appui IPS et conclusion du tapis conservée. BPS/IPS relus, 6960 entrées redécodées, 870 groupes contrôlés sur le bus et 27 pages sur sept messages relues. Audit ouvert : insertion 322 différée et ancien message 323 à revoir ensemble, sans modifier les anciens tokens ici. Le compte intégré ne vaut pas validation sémantique complète de toutes les anciennes sélections. Aucun parcours naturel complet déclaré.'
subprocess.run([sys.executable,str(P/'checkpoint.py'),'v0.23','--notes',notes],check=True)
shutil.copy2(O/'etat-projet.json',R/'etat-projet.json')
patch=O/'DQVI-FR-DS-v0.23-BASE-JP-PARTIEL.bps';assert patch.read_bytes().startswith(b'BPS1')
shutil.copy2(patch,R/'patches'/patch.name)
paths=['README.md','REPRISE-AUTOMATIQUE.md','etat-projet.json','dq6-fr/pass23.py','patches/'+patch.name,'sources/lots/v0.23.json']
names={'revue-lot-v023.json','audit-tapis-reordonne.json','etat-projet.json','LISEZ-MOI.md','validation.json','couverture-preparation.json','qa-bus.json','qa-render-fixtures.json','qa-longueurs.json','qa-patchs-regression.json','nouveaux-messages.json'}
paths += [str(p.relative_to(R)) for p in sorted(O.iterdir()) if p.is_file() and (p.suffix=='.py' or p.name in names)]
files=[p for p in paths if p.startswith('dq6-fr/v0.23/') or p in ['dq6-fr/pass23.py','patches/'+patch.name]]
spec=dict(kind='readable_translation_delta',version='v0.23',baseline='v0.22',baseline_count=5098,new_count=30,recipe='dq6-fr/pass23.py',merged_selection_sha256=digest(O/'insertion-candidates.json'),generated_inputs={name:digest(O/name) for name in ['correspondances-revues.json','adaptations-francaises.json','liaisons-variables-natives.json','charset.json']},files=[dict(path=p,sha256=digest(R/p),bytes=(R/p).stat().st_size) for p in files],no_rom_sram_or_state=True,open_semantic_audit=[322,323])
save(R/'sources/lots/v0.23.json',spec);save(R/'publication-v023.json',paths)
print('Readable publication:',len(paths),'files; no ROM, SRAM, emulator state or opaque archive.')
