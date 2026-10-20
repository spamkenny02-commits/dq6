"""Independent restore/build of the current v0.48 delta, with verified local originals."""
from pathlib import Path
import json,hashlib,subprocess,sys,importlib.util
R=Path(__file__).resolve().parent;D=R.parent/'finish428-clean48';O=R/'dq6-fr/v0.48'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not D.exists(),'Use a new empty independent output directory'
subprocess.run([sys.executable,str(R/'restore_sources.py'),'--output',str(D)],check=True)
U=D/'upload'
for src,name in [('Dragon Quest VI - Maboroshi no Daichi (Japan)(2).sfc','Dragon Quest VI - Maboroshi no Daichi (Japan).sfc'),('Dragon Quest VI - Realms of Reverie (E)(2).nds','Dragon Quest VI - Realms of Reverie (E).nds')]:
 (U/name).symlink_to((R.parent/'upload'/src).resolve())
P=D/'dq6-fr';T=P/'v0.48'
assert (T/'insertion-candidates.json').read_bytes()==(O/'insertion-candidates.json').read_bytes()
s=importlib.util.spec_from_file_location('patchRM',P/'upstream/refill/patchRM.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
base=bytes(m.apply_bps((U/'Dragon Quest VI - Maboroshi no Daichi (Japan).sfc').read_bytes(),(R/'patches/DQVI-FR-DS-v0.47-BASE-JP-PARTIEL.bps').read_bytes()))
assert hashlib.sha256(base).hexdigest()=='58c881b4c21dfa8e2b70c82871f005c4b2196c9f83347590c6974aa5d6820d40'
(P/'v0.47/result.sfc').write_bytes(base)
for n in ['init.py','prepare.py','build.py','verify.py']:subprocess.run([sys.executable,str(T/n)],check=True)
assert sha(T/'result.sfc')==sha(O/'result.sfc')
(O/'qa-restauration-propre.json').write_text(json.dumps(dict(fresh_destination=True,restored_selection_byte_identical=True,init_prepare_build_verify_passed=True,baseline_v047_reconstructed_from_public_bps=True,result_sha256=sha(T/'result.sfc')),indent=2))
print('INDEPENDENT BUILD MATCH',sha(T/'result.sfc'),flush=True)
