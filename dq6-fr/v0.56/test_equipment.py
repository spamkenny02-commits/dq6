"""Equipment fragment layout probes, including native AE callback continuity.
Counted list sequences follow the audited original loop; the complete inventory
operation itself is not invoked. Flattened probes remove intermediate AC/AE only
in diagnostic ROMs, preserving original pacing and revised explicit line breaks.
"""
from pathlib import Path
import json,struct,subprocess,sys,hashlib,shutil,math
import native_helpers,names,argparse
ap=argparse.ArgumentParser();ap.add_argument("--stress",action="store_true");args=ap.parse_args();stress=args.stress
O=Path(__file__).resolve().parent;D=O.parent;E=D/'emulator-tests';R=D.parent;S=O/'screenshots';S.mkdir(exist_ok=True)
base=(O/'result.sfc').read_bytes();rows={x['id']:x for x in json.loads((O/'insertion-candidates.json').read_text())};root=struct.unpack_from('<H',base,0x2bfb)[0];n=root//2+1;trees=[struct.unpack_from('<'+str(n)+'H',base,a) for a in [0x167be,0x1700e]];codes={}
def visit(node,bits):
 for bit in [0,1]:
  v=trees[bit][node//2]
  if v&32768:visit(v&32767,bits+[bit])
  else:codes.setdefault(v&8191,bits+[bit])
visit(root,[]);cpu=int.from_bytes(base[0x15bb5+36:0x15bb8+36],'little');pos=cpu&0x3fffff if cpu>=0xc00000 else cpu;bit=7;original=[]
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
def rom(label,group):
 bits=[b for ts in group for t in ts for b in codes[t]];blob=bytearray((len(bits)+7)//8)
 for i,b in enumerate(bits):
  if b:blob[i//8]|=1<<(7-i%8)
 a=next(a for a in range(0x771800,0x7b8703-len(blob),256) if a>>16==(a+len(blob)-1)>>16 and all(not(x['file_offset']<a+len(blob) and x['file_offset']+x['size']>a) for x in layout));r=bytearray(base);r[a:a+len(blob)]=blob
 for copy in [0,0x400000]:r[copy+0x15bb5+36:copy+0x15bb8+36]=a.to_bytes(3,'little')
 c=sum(r)&65535
 for copy in [0,0x400000]:struct.pack_into('<HH',r,copy+0xffdc,c^65535,c)
 
 if stress:
  entries,groups,n=names.parse(r);sid=2352;entries[groups[sid>>4]+(sid&15)]=native_helpers.encode(long_name);packed=bytearray();starts=[]
  for e in entries[:n]:starts.append(len(packed));packed+=e+b'\xac'
  assert names.START+len(packed)<=names.END
  for copy in [0,0x400000]:
   r[copy+names.START:copy+names.END]=packed+b'\xff'*(names.END-names.START-len(packed))
   for g,pos in enumerate(groups):r[copy+names.TABLE+3*g:copy+names.TABLE+3*g+3]=starts[pos].to_bytes(3,'little')
   assert r[copy+0x69354:copy+0x6935a]==bytes.fromhex('ad2f3b4cf793');r[copy+0x69354:copy+0x6935a]=bytes.fromhex('a930094c0c92')
  c=sum(r)&65535
  for copy in [0,0x400000]:struct.pack_into('<HH',r,copy+0xffdc,c^65535,c)
 path=E/('equip-v056-'+('stress-' if stress else '')+label+'.sfc');path.write_bytes(r);return path
ram={'0x3b2f':[2,0]};long_name='ABCDEFGHIJKLMN'
def capture(label,path,seq,first=False,expect=100,ids=None,kind='flattened_list'):
 cmd=[sys.executable,str(E/'run_core.py'),'--rom',str(path),'--session','equip-v056-'+('stress-' if stress else '')+label,'--tag','v056-equip-'+('stress-' if stress else '')+label+'-'+str(len(out)),'--sequence',json.dumps(seq)]
 if first:cmd+=['--load-state',str(R.parent/'work-v026/dq6-fr/emulator-tests/v026-camp.state'),'--set-wram',json.dumps(ram)]
 p=subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=45);m=json.loads(p.stdout.splitlines()[0])['message_id'];assert m==expect,(label,m,expect);tag=cmd[cmd.index('--tag')+1];f=E/(tag+'.png');shutil.copy2(f,S/f.name);out.append(dict(label=label,kind=kind,ids=ids or [],message_id=m,screenshot='screenshots/'+f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),output=p.stdout))
 (O/('render-equipment-stress-private.json' if stress else 'render-equipment-private.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2))
initial=[{'button':'a','frames':4,'press':1},{'frames':330},{'button':'down','frames':8,'press':1},{'frames':250}];advance=[{'button':'a','frames':1,'press':1},{'frames':240}]
for count in [0,1,2,3,5,6,8]:
 ids=[5704] if count==0 else [5698]
 if count:
  for y in range(count):
   ids.append(5700 if y==2 else 5699)
   if count>=6 and y==4:ids.append(5701)
  ids.append(5703 if count<6 else 5702)
 ts=[]
 for mid in ids:ts.extend(rows[mid]['tokens'][:-1])
 ts.append(0xac);g=[x[:] for x in original];g[4]=ts;path=rom('list'+str(count),g)
 for page in range(1,max(1,ts.count(0xaf))+1):capture('list'+str(count),path,initial if page==1 else advance,page==1,100,ids)
for name in [5699,5700]:
 for suffix in [5702,5703]:
  ids=[5698,name,suffix];g=[x[:] for x in original];g[4]=rows[5698]['tokens'][:];g[5]=rows[name]['tokens'][:];g[6]=g[5][:];g[7]=rows[suffix]['tokens'][:];label=f'callback-{name}-{suffix}';path=rom(label,g)
  capture(label,path,initial,True,100,ids,'native_AE_callbacks')
  capture(label,path,advance,False,101,ids,'native_AE_callbacks')
  capture(label,path,advance,False,103,ids,'native_AE_callbacks')
(O/('qa-equipement-stress.json' if stress else 'qa-equipement.json')).write_text(json.dumps(dict(result_sha256=hashlib.sha256(base).hexdigest(),rows=out,long_name=long_name if stress else None,long_name_length=14 if stress else None,diagnostic_forced_C1_to_SID2352=stress,actual_actor_resolver_unchanged=not stress,prior_WRAM14_attempt_rejected=True,prior_attempt_observed='Olivier remained unchanged; hero buffer display capped at8, so it was not a valid C1 max-name test' ,counts=[0,1,2,3,5,6,8],source_callbacks_preserved=True,limits='List sequence follows static caller count logic. Intermediate terminators removed only in flattened layout probes; four separate3-message tests exercise true AE returns. No complete natural inventory/shop/equip operation verified.'),ensure_ascii=False,indent=2));print(len(out),'equipment captures')
