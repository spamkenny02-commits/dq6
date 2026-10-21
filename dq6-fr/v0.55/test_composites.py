"""Real AE callback composition in camp diagnostic; no natural spell event claim.
Prefix100 returns AE, camp yes101/103 continue the SAME window. A private AF
before final source terminator holds the capture. Release bytes are not changed.
"""
from pathlib import Path
import json,struct,subprocess,sys,hashlib,shutil,itertools
O=Path(__file__).resolve().parent;D=O.parent;E=D/'emulator-tests';R=D.parent;S=O/'screenshots';S.mkdir(exist_ok=True)
base=(O/'result.sfc').read_bytes();rows={x['id']:x for x in json.loads((O/'insertion-candidates.json').read_text())};root=struct.unpack_from('<H',base,0x2bfb)[0];n=root//2+1;trees=[struct.unpack_from('<'+str(n)+'H',base,a) for a in [0x167be,0x1700e]];codes={}
def visit(node,bits):
 for bit in [0,1]:
  v=trees[bit][node//2]
  if v&32768:visit(v&32767,bits+[bit])
  else:codes.setdefault(v&8191,bits+[bit])
visit(root,[])
cpu=int.from_bytes(base[0x15bb5+36:0x15bb8+36],'little');pos=cpu&0x3fffff if cpu>=0xc00000 else cpu;bit=7;original=[]
for _ in range(8):
 ts=[]
 while True:
  v=root|32768
  while v&32768:
   b=(base[pos]>>bit)&1;bit-=1
   if bit<0:pos+=1;bit=7
   v=trees[b][(v&32767)//2]
  ts.append(v&8191)
  if ts[-1] in [0xac,0xae]:break
 original.append(ts)
layout=json.loads((O/'placements.json').read_text());out=[]
def fixture(label,ids,value=12345):
 group=[t[:] for t in original];group[4]=rows[ids[0]]['tokens'][:]
 assert group[4][-1]==0xae
 if len(ids)==2:
  tail=rows[ids[1]]['tokens'][:];tail.insert(len(tail)-1,0xaf);group[5]=tail;group[6]=tail
 else:
  assert len(ids)==3;group[5]=rows[ids[1]]['tokens'][:];group[6]=group[5][:];group[7]=rows[ids[2]]['tokens'][:];group[7].insert(len(group[7])-1,0xaf)
 bits=[b for ts in group for t in ts for b in codes[t]];blob=bytearray((len(bits)+7)//8)
 for i,b in enumerate(bits):
  if b:blob[i//8]|=1<<(7-i%8)
 a=next(a for a in range(0x771800,0x7b8703-len(blob),256) if a>>16==(a+len(blob)-1)>>16 and all(not(x['file_offset']<a+len(blob) and x['file_offset']+x['size']>a) for x in layout));rom=bytearray(base);rom[a:a+len(blob)]=blob
 for copy in [0,0x400000]:rom[copy+0x15bb5+36:copy+0x15bb8+36]=a.to_bytes(3,'little')
 c=sum(rom)&65535
 for copy in [0,0x400000]:struct.pack_into('<HH',rom,copy+0xffdc,c^65535,c)
 path=E/('composite-v055-'+label+'.sfc');path.write_bytes(rom)
 seq=[{'button':'a','frames':4,'press':1},{'frames':330},{'button':'down','frames':8,'press':1},{'frames':250},{'button':'a','frames':1,'press':1},{'frames':240}]
 cmd=[sys.executable,str(E/'run_core.py'),'--rom',str(path),'--session','composite-v055-'+label,'--tag','v055-composite-'+label,'--load-state',str(R.parent/'work-v026/dq6-fr/emulator-tests/v026-camp.state'),'--set-wram',json.dumps({'0x5a2e':list(value.to_bytes(3,'little'))}),'--sequence',json.dumps(seq)]
 r=subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=45);observed=json.loads(r.stdout.splitlines()[0])['message_id'];assert observed==(101 if len(ids)==2 else 103),(label,observed)
 p=E/('v055-composite-'+label+'.png');shutil.copy2(p,S/p.name)
 out.append(dict(label=label,ids=ids,BB=value,message_id=observed,screenshot='screenshots/'+p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),output=r.stdout))
 (O/'render-composites-private.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
for a,b in itertools.product([5820,5821],[5822,5823]):
 for value in [12345,16777215]:fixture(f'{a}-{b}-{value}',[a,b],value)
for b in range(5833,5840):fixture(f'5832-{b}',[5832,b])
for a,b,c in itertools.product([1313,1314,1315],[1318,1319,1320],[1323,1324,1325]):fixture(f'{a}-{b}-{c}',[a,b,c])
(O/'qa-compositions.json').write_text(json.dumps(dict(result_sha256=hashlib.sha256(base).hexdigest(),rows=out,private_hold_AF_before_final_source_terminator=True,source_AE_returns_preserved=True,limits='Camp100/101/103 callbacks, yes branch forced by input. No actual coordinate calculation, itinerant service, riddle door trigger or reward verified.'),ensure_ascii=False,indent=2));print(len(out),'composite captures')
