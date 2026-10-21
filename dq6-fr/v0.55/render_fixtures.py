"""Diagnostic ROMs only: redirect the first message to a selected new entry.
These ROMs are NOT release artifacts. Exercise the real renderer from the camp.
"""
from pathlib import Path
import json,struct
import argparse
ap=argparse.ArgumentParser();ap.add_argument('version');ap.add_argument('ids');args=ap.parse_args();version=args.version
P=Path(__file__).resolve().parents[1];O=P/'emulator-tests';base=(P/version/'result.sfc').read_bytes();rows={r['id']:r for r in json.loads((P/version/'insertion-candidates.json').read_text())}
root=struct.unpack_from('<H',base,0x2bfb)[0];n=root//2+1;trees=[struct.unpack_from('<'+str(n)+'H',base,a) for a in [0x167be,0x1700e]];codes={}
def visit(node,bits):
 for bit in [0,1]:
  v=trees[bit][node//2]
  if v&32768:visit(v&32767,bits+[bit])
  else:codes.setdefault(v&8191,bits+[bit])
visit(root,[])
cpu=int.from_bytes(base[0x15bb5+12*3:0x15bb5+12*3+3],'little');pos=cpu&0x3fffff if cpu>=0xc00000 else cpu;bit=7;group=[]
for i in range(8):
 ts=[]
 while True:
  v=root|32768
  while v&32768:
   b=(base[pos]>>bit)&1;bit-=1
   if bit<0:pos+=1;bit=7
   v=trees[b][(v&32767)//2]
  t=v&8191;ts.append(t)
  if t in [0xac,0xae]:break
 group.append(ts)
for label,mid in [(version.replace('.','')+'-'+i,int(i)) for i in args.ids.split(',')]:
 r=bytearray(base);gg=[t[:] for t in group];gg[4]=rows[mid]['tokens'][:];gg[4][-1]=0xac
 bits=[b for ts in gg for t in ts for b in codes[t]];blob=bytearray((len(bits)+7)//8)
 for i,b in enumerate(bits):
  if b:blob[i//8]|=1<<(7-i%8)
 placements=json.loads((P/version/'placements.json').read_text())
 a=next(a for a in range(0x771800,0x7b8703-len(blob),256) if (a>>16)==((a+len(blob)-1)>>16) and all(not(p['file_offset']<a+len(blob) and p['file_offset']+p['size']>a) for p in placements))
 assert 0x77175b<=a<a+len(blob)<=0x7b8703
 print('Diagnostic',mid,'free script address',hex(a),'bytes',len(blob))
 r[a:a+len(blob)]=blob
 for copy in [0,0x400000]:r[copy+0x15bb5+12*3:copy+0x15bb5+12*3+3]=a.to_bytes(3,'little')
 s=sum(r)&65535
 for copy in [0,0x400000]:struct.pack_into('<HH',r,copy+0xffdc,s^65535,s)
 (O/('fixture-'+label+'.sfc')).write_bytes(r)
print('Renderer fixtures use verified free gaps in upper script area; release ROM unchanged')
