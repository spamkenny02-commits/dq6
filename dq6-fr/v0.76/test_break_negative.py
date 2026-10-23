"""Prove that the CPU grid diagnostic rejects an invalid break length.
The mutation affects only a private diagnostic fixture, never the release.
"""
from common import *
import argparse,subprocess
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--runner',type=Path,required=True);p.add_argument('--camp',type=Path,required=True);a=p.parse_args()
r=subprocess.run([sys.executable,str(O/'emulator_consumers.py'),'--jp',str(a.jp.resolve()),'--out',str(a.out.resolve()),'--runner',str(a.runner.resolve()),'--camp',str(a.camp.resolve()),'--mutate-break'],capture_output=True);error=r.stderr.decode();assert r.returncode!=0 and "('cursor', 'after', 805, 4, 5)" in error,error
q=dict(release='v0.76',ROM_sha256=sha((a.out/'result.sfc').read_bytes()),deliberate_mutation=dict(sid=805,correct_break_hex='94',mutated_break_hex='95',release_ROM_modified=False),expected_negative_observed=True,diagnostic='C3763A actual CPU grid/cursor after invalid metadata',observed_final_cursor=4,expected_final_cursor=5,consumer_process_returncode=r.returncode,error_excerpt="('cursor', 'after', 805, 4, 5)",natural_validation=False);(O/'qa-negative-break.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps(q))
