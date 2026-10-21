"""C9 conservative14-cell layout stress and repaired AF/AC return for6956.
Private C9 resolver forces a reviewed SID; no natural Tulipe event is claimed.
"""
from pathlib import Path
import json,subprocess,struct,sys,hashlib,shutil
import names,native_helpers
O=Path(__file__).resolve().parent;D=O.parent;E=D/'emulator-tests';R=D.parent;S=O/'screenshots';base=(O/'result.sfc').read_bytes();b=bytearray((E/'fixture-v056-6956.sfc').read_bytes());entries,groups,n=names.parse(b);oldend=names.START+sum(len(e)+1 for e in entries[:n]);tail=bytes(b[oldend:names.END]).rstrip(b'\xff');name='ABCDEFGHIJKLMN';sid=2352;entries[groups[sid>>4]+(sid&15)]=native_helpers.encode(name);packed=bytearray();starts=[]
for e in entries[:n]:starts.append(len(packed));packed+=e+b'\xac'
assert names.START+len(packed)+len(tail)<=names.END
for copy in [0,0x400000]:
 b[copy+names.START:copy+names.END]=packed+tail+b'\xff'*(names.END-names.START-len(packed)-len(tail))
 for g,pos in enumerate(groups):b[copy+names.TABLE+3*g:copy+names.TABLE+3*g+3]=starts[pos].to_bytes(3,'little')
 assert b[copy+0x693c1:copy+0x693c7]==bytes.fromhex('a901004cf793');b[copy+0x693c1:copy+0x693c7]=bytes.fromhex('a930094c0c92')
c=sum(b)&65535
for copy in [0,0x400000]:struct.pack_into('<HH',b,copy+0xffdc,c^65535,c)
p=E/'terminal-v056-6956.sfc';p.write_bytes(b);out=[]
for page in [1,2,3]:
 tag='v056-terminal-'+str(page);cmd=[sys.executable,str(E/'run_core.py'),'--rom',str(p),'--session','terminal-v056-6956','--tag',tag]
 if page==1:cmd+=['--load-state',str(R.parent/'work-v026/dq6-fr/emulator-tests/v026-camp.state'),'--sequence',json.dumps([{'button':'a','frames':4,'press':1},{'frames':330},{'button':'down','frames':8,'press':1},{'frames':250}])]
 else:cmd+=['--sequence',json.dumps([{'button':'a','frames':1,'press':1},{'frames':240}])]
 r=subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=45);m=json.loads(r.stdout.splitlines()[0])['message_id'];assert m==(101 if page==3 else 100),(page,m);f=E/(tag+'.png');shutil.copy2(f,S/f.name);out.append(dict(stage={1:'6956_AF_with_long_C9',2:'added_AC_returned_to_host_choice',3:'host_yes_continues101'}[page],message_id=m,screenshot='screenshots/'+f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),output=r.stdout))
(O/'qa-terminaison-6956.json').write_text(json.dumps(dict(result_sha256=hashlib.sha256(base).hexdigest(),rows=out,private_C9_forced_SID2352=True,name_length=14,added_AC_executed=True,limits='Repaired6956 redirected into camp100. Long-name resolver forced in private ROM. Return afterAF reaches host101. No natural Tulipe event, original source AC, or actual hero renaming validated.'),ensure_ascii=False,indent=2));print('6956 long C9 and explicit AC return passed')
