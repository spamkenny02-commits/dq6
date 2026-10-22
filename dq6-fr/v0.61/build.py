from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();jp=a.jp.read_bytes();base,rows,meta=prepare(jp);assert rows==read(O/'insertion-combat.json') and meta==read(O/'revue-combat-v061.json');rom,placement,engine,names_report=assemble(base,rows,meta);bps,ips=patches(jp,rom)
a.out.mkdir(exist_ok=True,parents=True);(a.out/'result.sfc').write_bytes(rom);(a.out/'DQVI-FR-DS-v0.61-BASE-JP-PARTIEL.ips').write_bytes(ips);(R/'patches/DQVI-FR-DS-v0.61-BASE-JP-PARTIEL.bps').write_bytes(bps)
report=dict(release='v0.61',baseline='v0.60',ROM_bytes=len(rom),ROM_sha256=sha(rom),BPS_sha256=sha(bps),IPS_sha256=sha(ips),new_battle_ids=IDS,new_battle_integrated=3,battle_integrated_total=107,main_selections_unchanged=6957,engine_modified=True,native_font_unchanged=True,placement=placement,engine=engine,names=names_report,natural_battle_validation=False)
(O/'build-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(report['ROM_sha256'])
