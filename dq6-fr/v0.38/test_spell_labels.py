"""Private B2 renderer fixture for every reviewed spell label.
Does not execute the spell, open its native menu, or alter the release ROM.
"""
from pathlib import Path
import argparse,json,struct,subprocess,sys,hashlib,shutil
ap=argparse.ArgumentParser();ap.add_argument('--camp-state',required=True,type=Path);a=ap.parse_args()
O=Path(__file__).resolve().parent;P=O.parent;E=P/'emulator-tests';base=(O/'result.sfc').read_bytes()
rows=json.loads((O/'revue-sorts-v038.json').read_text())
root=struct.unpack_from('<H',base,0x2bfb)[0];n=root//2+1;trees=[struct.unpack_from('<'+str(n)+'H',base,p) for p in [0x167be,0x1700e]];codes={}
def visit(node,bits):
 for bit in [0,1]:
  v=trees[bit][node//2]
  if v&32768:visit(v&32767,bits+[bit])
  else:codes.setdefault(v&8191,bits+[bit])
visit(root,[])
cpu=int.from_bytes(base[0x15bb5+36:0x15bb5+39],'little');pos=cpu&0x3fffff if cpu>=0xc00000 else cpu;bit=7;group=[]
for _ in range(8):
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
# Three native lookups on separate lines keep the diagnostic page observable
# even for short labels. This is NOT the layout of a native spell menu.
group[4]=[0xb2,0xad,0xb2,0xad,0xb2,0xac]
bits=[b for ts in group for t in ts for b in codes[t]];blob=bytearray((len(bits)+7)//8)
for i,b in enumerate(bits):
 if b:blob[i//8]|=1<<(7-i%8)
address=0x7a0000;placements=json.loads((O/'placements.json').read_text())
assert all(not(p['file_offset']<address+len(blob) and p['file_offset']+p['size']>address) for p in placements)
rom=bytearray(base);rom[address:address+len(blob)]=blob
for copy in [0,0x400000]:rom[copy+0x15bb5+36:copy+0x15bb5+39]=address.to_bytes(3,'little')
checksum=sum(rom)&65535
for copy in [0,0x400000]:struct.pack_into('<HH',rom,copy+0xffdc,checksum^65535,checksum)
fixture=E/'fixture-v038-spell-labels.sfc';fixture.write_bytes(rom)
S=O/'screenshots';S.mkdir(exist_ok=True);report=[]
seq=[{'button':'a','frames':4,'press':4},{'frames':330},{'button':'down','frames':8,'press':8},{'frames':10},{'button':'a','frames':1,'press':1},{'frames':240}]
for row in rows:
 sid=row['sid'];tag=f'v038-spell-{sid:04x}'
 cmd=[sys.executable,str(E/'run_core.py'),'--rom',str(fixture),'--session',f'v038-spell-{sid}','--load-state',str(a.camp_state),'--set-wram',json.dumps({'0x5a28':[sid&255,sid>>8]}),'--sequence',json.dumps(seq),'--tag',tag]
 r=subprocess.run(cmd,check=True,capture_output=True,text=True);s=E/(tag+'.png');shutil.copy2(s,S/s.name)
 report.append(dict(sid=sid,french=row['french'],screenshot='screenshots/'+s.name,sha256=hashlib.sha256(s.read_bytes()).hexdigest(),output=r.stdout.strip()))
assert (O/'result.sfc').read_bytes()==base
(O/'qa-spell-label-render.json').write_text(json.dumps(dict(result_sha256=hashlib.sha256(base).hexdigest(),rows=report,native_B2_lookups_per_label=3,release_rom_unchanged=True,limits='Diagnostic B2 lookup in camp, three repeated lines; no spell execution, no native spell/battle window or natural progression. Initial single-lookup fixture missed several short labels; exact cause not established.'),ensure_ascii=False,indent=2))
print(len(report),'spell/action labels rendered through B2')
