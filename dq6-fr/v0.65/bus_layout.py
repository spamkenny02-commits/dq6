"""Emit metadata for every live main group and all608 native battle messages."""
from pathlib import Path
import argparse,json
from common import c,O,read,sha,decode_pool,names,TAIL,END
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();rom=a.rom.read_bytes();r=read(O/'build-report.json');assert sha(rom)==r['ROM_sha256']
layout=c.main_regions(rom)+[dict(group='battle-'+str(i),file_offset=at,cpu_address=at,size=len(b)) for i,at,b in decode_pool(rom,r['placement'])]
layout += [dict(group='pair-engine-'+str(i),file_offset=s['offset'],cpu_address=s['offset'] if s['offset']>=0x700000 else 0xc00000+s['offset'],size=s['size']) for i,s in enumerate(r['engine']['segments']) if s['offset']<0x400000 or s['offset']>=0x700000]
layout += [dict(group='name-'+str(sid)+'-mirror'+str(copy),file_offset=at+copy,cpu_address=(0xc00000+at if copy==0 else at+copy),size=len(b)) for sid,(at,b) in enumerate(names(rom)) for copy in (0,0x400000)]
layout += [dict(group='name-pointers-'+str(copy),file_offset=copy+0x165e7,cpu_address=(0xc165e7 if copy==0 else copy+0x165e7),size=157*3) for copy in (0,0x400000)]
layout += [dict(group='preserved-tail-'+str(copy),file_offset=copy+TAIL,cpu_address=(0xc00000+TAIL if copy==0 else copy+TAIL),size=END-TAIL) for copy in (0,0x400000)]
a.out.write_text(json.dumps(layout,indent=2)+'\n');print('Live main, battle and engine ranges; metadata only')
