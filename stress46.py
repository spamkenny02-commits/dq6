from pathlib import Path
import sys,json,struct,subprocess,hashlib
P=Path(__file__).resolve().parent/'dq6-fr';O=P/'v0.46';E=P/'emulator-tests';sys.path.insert(0,str(O));import names
r=bytearray((E/'fixture-v046-6228.sfc').read_bytes());entries,groups,n=names.parse(r);tail=bytes(r[names.START+sum(len(e)+1 for e in entries[:n]):names.END]);entries[1604],entries[1638]=entries[1638],entries[1604];packed=bytearray();offsets=[]
for e in entries[:n]:offsets.append(len(packed));packed+=e+b'\xac'
assert len(packed)+len(tail)==names.END-names.START
for c in [0,0x400000]:
 r[c+names.START:c+names.END]=packed+tail
 for g,i in enumerate(groups):r[c+names.TABLE+g*3:c+names.TABLE+g*3+3]=offsets[i].to_bytes(3,'little')
s=sum(r)&65535
for c in [0,0x400000]:struct.pack_into('<HH',r,c+0xffdc,s^65535,s)
f=E/'stress46-B5.sfc';f.write_bytes(r)
cmd=[sys.executable,str(E/'run_core.py'),'--rom',str(f),'--session','stress46','--tag','stress46-B5','--load-state',str(P.parents[1]/'work-v026/dq6-fr/emulator-tests/v026-camp.state'),'--set-wram',json.dumps({'0x5a24':[3,0],'0x5a2a':[1,0]}),'--sequence',json.dumps([{'button':'a','frames':4,'press':4},{'frames':330},{'button':'down','frames':8,'press':8},{'frames':10},{'button':'a','frames':1,'press':1},{'frames':240}])]
a=subprocess.run(cmd,check=True,capture_output=True,text=True);assert json.loads(a.stdout.splitlines()[0])['message_id']==100
(O/'qa-stress-B5.json').write_text(json.dumps(dict(result_sha256=hashlib.sha256((O/'result.sfc').read_bytes()).hexdigest(),private_name_pool_swap=[1604,1638],item='Iron Ball of Destruction',cells=24,target_pages=1,output=a.stdout,limits='Private display stress, released name pool unchanged.'),indent=2));print(a.stdout)
