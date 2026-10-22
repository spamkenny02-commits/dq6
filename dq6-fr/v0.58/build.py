from pathlib import Path
import argparse,json
from common import prepare,assemble,patches,O,R,sha,read
a=argparse.ArgumentParser();a.add_argument('--jp',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a=a.parse_args()
jp=a.jp.read_bytes();base,rows=prepare(jp);assert rows==read(O/'insertion-combat.json');rom,placement=assemble(base,rows);bps,ips=patches(jp,rom)
a.out.mkdir(parents=True,exist_ok=True);(a.out/'result.sfc').write_bytes(rom);(a.out/'DQVI-FR-DS-v0.58-BASE-JP-PARTIEL.ips').write_bytes(ips)
patch=R/'patches/DQVI-FR-DS-v0.58-BASE-JP-PARTIEL.bps';patch.write_bytes(bps)
report=dict(release='v0.58',baseline='v0.57',ROM_bytes=len(rom),ROM_sha256=sha(rom),BPS_sha256=sha(bps),IPS_sha256=sha(ips),new_battle_ids=[r['id'] for r in rows],new_battle_integrated=len(rows),battle_integrated_total=8+len(rows),main_selections_unchanged=6957,engine_modified=False,placement=placement,natural_battle_validation=False)
(O/'build-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report))
