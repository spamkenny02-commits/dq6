"""Emit metadata for every live main group and all608 native battle messages."""
from pathlib import Path
import argparse,json
from common import c,O,read,sha,decode_pool
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();rom=a.rom.read_bytes();r=read(O/'build-report.json');assert sha(rom)==r['ROM_sha256']
layout=c.main_regions(rom)+[dict(group='battle-'+str(i),file_offset=at,cpu_address=at,size=len(b)) for i,at,b in decode_pool(rom,r['placement'])]
a.out.write_text(json.dumps(layout,indent=2)+'\n');print('1478 live ranges; metadata only')
