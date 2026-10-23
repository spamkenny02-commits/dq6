from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);a=p.parse_args();base,rows=prepare(a.jp.read_bytes());(O/'insertion-combat.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print(len(rows),'reviewed;DS refs',sum(bool(r['ds_references']) for r in rows));print('Legacy command corrections',[(r['id'],r['legacy_command_audit']) for r in rows if r['legacy_command_audit']['changed']])
