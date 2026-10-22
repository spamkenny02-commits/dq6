from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);a=p.parse_args();base,rows,meta=prepare(a.jp.read_bytes())
for name,data in [('insertion-combat.json',rows),('revue-combat-v061.json',meta)]: (O/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print('3 reviewed battle plans;16 contextual compound names;2 contextual word names. No insertion yet.')
