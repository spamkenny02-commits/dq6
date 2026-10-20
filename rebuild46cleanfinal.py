from pathlib import Path
import sys,json,hashlib,shutil,subprocess
R=Path(__file__).resolve().parent;D=R.parent/'reprise-restore45';O=R/'dq6-fr/v0.46';T=D/'dq6-fr/v0.46';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Only this task's disposable v0.46 output directory is cleared. No user worktree is touched.
if T.exists():shutil.rmtree(T)
sys.path.insert(0,str(R));from restore_lots import restore_lots
restore_lots(R,D)
assert (T/'insertion-candidates.json').read_bytes()==(O/'insertion-candidates.json').read_bytes()
for script in ['prepare.py','build.py','verify.py']:subprocess.run([sys.executable,str(T/script)],check=True)
assert sha(T/'result.sfc')==sha(O/'result.sfc')
(O/'qa-restauration-propre.json').write_text(json.dumps(dict(restored_from_public_baseline_and_explicit_delta=True,baseline_v045_rom_sha256=sha(D/'dq6-fr/v0.45/result.sfc'),result_sha256=sha(O/'result.sfc'),restored_selection_byte_identical=True,independent_build_and_verify_passed=True,new_version_directory_fresh=True,original_sources_checked_by_prior_init=True,notes='The prior reuse attempt preserved older generated selections as designed; only this task-owned v0.46 output directory was cleared before a fresh delta restoration and rebuild.'),indent=2));print('FINAL CLEAN BUILD MATCH',sha(T/'result.sfc'),flush=True)
