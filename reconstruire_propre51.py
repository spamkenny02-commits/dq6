"""Fresh source restoration plus init/prepare/build/verify, no emulator concurrency."""
from pathlib import Path
import subprocess,sys,json,hashlib,importlib.util
R=Path(__file__).resolve().parent;T=R.parent/'reprise-v051-propre'
assert not T.exists(),'Use a genuinely fresh destination'
subprocess.run([sys.executable,str(R/'restore_sources.py'),'--output',str(T)],check=True)
for name in ['Dragon Quest VI - Maboroshi no Daichi (Japan).sfc','Dragon Quest VI - Realms of Reverie (E).nds']:(T/'upload'/name).symlink_to((R/'upload'/name).resolve())
D=T/'dq6-fr';O=D/'v0.51'
assert (O/'insertion-candidates.json').read_bytes()==(R/'dq6-fr/v0.51/insertion-candidates.json').read_bytes()
spec=importlib.util.spec_from_file_location('patch',D/'upstream/refill/patchRM.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
(D/'v0.50/result.sfc').write_bytes(bytes(m.apply_bps((T/'upload/Dragon Quest VI - Maboroshi no Daichi (Japan).sfc').read_bytes(),(R/'patches/DQVI-FR-DS-v0.50-BASE-JP-PARTIEL.bps').read_bytes())))
for name in ['init.py','prepare.py','build.py','verify.py']:subprocess.run([sys.executable,str(O/name)],check=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(O/'result.sfc')==sha(R/'dq6-fr/v0.51/result.sfc')
assert (O/'insertion-candidates.json').read_bytes()==(R/'dq6-fr/v0.51/insertion-candidates.json').read_bytes()
report=dict(fresh_destination=True,restored_selection_byte_identical=True,init_prepare_build_verify_passed=True,baseline_v050_reconstructed_from_public_bps=True,result_sha256=sha(O/'result.sfc'))
(R/'dq6-fr/v0.51/qa-restauration-propre.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
