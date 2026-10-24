from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();rom=a.rom.read_bytes();r=read(O/'build-report.json');assert sha(rom)==r['ROM_sha256']
layout=c.main_regions(rom)+[dict(group='battle-'+str(i),file_offset=at,cpu_address=at,size=len(b)) for i,at,b in decode_pool(rom,r['placement'])]
layout += [dict(group='engine-'+str(i),file_offset=s['offset'],cpu_address=cpu_for_file(s['offset']),size=s['size']) for i,s in enumerate(r['engine']['segments']) if s['offset']<0x400000 or s['offset']>=0x700000]
layout += [dict(group='name-'+str(sid),file_offset=at,cpu_address=cpu_for_file(at),size=len(raw)) for sid,(at,raw) in enumerate(names(rom))]
layout += [dict(group='legacy-name-pool-'+str(copy),file_offset=copy+POOL,cpu_address=cpu_for_file(copy+POOL),size=END-POOL) for copy in (0,0x400000)]
layout += [dict(group='name-pointers-'+str(copy),file_offset=copy+0x165e7,cpu_address=cpu_for_file(copy+0x165e7),size=157*3) for copy in (0,0x400000)]
layout += [dict(group='active-name-pool',file_offset=NAME,cpu_address=NAME,size=r['name_reachable_bytes'])]
layout += [dict(group=f'font-{copy}-{b}-{kind}',file_offset=copy+at,cpu_address=cpu_for_file(copy+at),size=size) for copy in (0,0x400000) for b,g in parent.parent.font.MAP.values() for kind,at,size in [('tile',parent.parent.font.FONT+b*16,16),('map',0x11100+b*2,2)]]
layout += [dict(group=f'window8-{copy}',file_offset=copy+WINDOW,cpu_address=cpu_for_file(copy+WINDOW),size=14) for copy in (0,0x400000)]
a.out.write_text(json.dumps(layout,indent=2)+'\n');print(len(layout),'ranges')
