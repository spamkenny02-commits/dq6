from pathlib import Path
import argparse,json
from common import prepare,O
a=argparse.ArgumentParser();a.add_argument('--jp',type=Path,required=True);a=a.parse_args()
_,rows=prepare(a.jp.read_bytes());(O/'insertion-combat.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print(f'{len(rows)} prepared for native battle insertion; no ROM written')
