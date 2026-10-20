from pathlib import Path
import json,hashlib,shutil,subprocess,sys
R=Path(__file__).resolve().parent;O=R/'dq6-fr/v0.46';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();fs=[R/'dq6-fr/pass46.py']+[p for p in O.iterdir() if p.suffix=='.py' or p.name in ['revue-lot-v046.json','nouveaux-messages.json']]
spec=dict(kind='readable_translation_delta',version='v0.46',baseline='v0.45',baseline_count=6276,new_count=111,recipe='dq6-fr/pass46.py',merged_selection_sha256=sha(O/'insertion-candidates.json'),generated_inputs={n:sha(O/n) for n in ['correspondances-revues.json','adaptations-francaises.json','liaisons-variables-natives.json','charset.json']},files=[dict(path=str(p.relative_to(R)),sha256=sha(p),bytes=p.stat().st_size) for p in fs]);(R/'sources/lots/v0.46.json').write_text(json.dumps(spec,indent=2))
D=R.parent/'reprise-restore45'
# Reuse the independently restored baseline directory, preserving its local ROM builds.
# Install the immutable public v0.45 sources/reports before restoring the next delta.
for p in json.loads((R/'publish-v045-files.json').read_text()):
 q=D/p;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/p,q)
for p in fs+[R/'sources/lots/v0.46.json']:
 q=D/p.relative_to(R);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
subprocess.run([sys.executable,str(D/'restore_sources.py')],check=True)
assert (D/'dq6-fr/v0.46/insertion-candidates.json').read_bytes()==(O/'insertion-candidates.json').read_bytes()
for script in ['init.py','prepare.py','build.py','verify.py']:subprocess.run([sys.executable,str(D/'dq6-fr/v0.46'/script)],check=True)
assert sha(O/'result.sfc')==sha(D/'dq6-fr/v0.46/result.sfc')
(O/'qa-restauration-propre.json').write_text(json.dumps(dict(restored_from_public_baseline_and_explicit_delta=True,baseline_v045_rom_sha256=sha(D/'dq6-fr/v0.45/result.sfc'),result_sha256=sha(O/'result.sfc'),restored_selection_byte_identical=True,independent_build_and_verify_passed=True),indent=2));print('CLEAN RESTORATION MATCH',sha(O/'result.sfc'))
