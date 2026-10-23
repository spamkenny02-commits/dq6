from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);a=p.parse_args();base,m=prepare(a.jp.read_bytes());q=dict(release='v0.65',baseline='v0.64',new_translations=0,physical_name_storage_adaptations=5,saved_bytes=7,reviewed_names=m['rows'],tail_restore_source='v0.60 BPS on verified intact JP',tail_sha256=m['old_tail_sha256'],tail_size=m['tail_size'],tail_prefix_before_sha256=m['tail_prefix_before_sha256'],tail_prefix_restored_sha256=m['tail_prefix_restored_sha256'],engine_modified=False,font_modified=False)
(O/'revue-stockage-noms.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print('5 names,7 bytes recovered,0 new translations')
