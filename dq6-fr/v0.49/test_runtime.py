"""Sequential Snes9x bus, boot and explicit diagnostic variable probes.
Run only after test_render.py completes. Private ROMs/states are never artifacts.
The forced C4 branch tests display/layout, not the real party-count computation.
"""
from pathlib import Path
import subprocess,sys,json,hashlib,struct,shutil
import names,native_helpers
O=Path(__file__).resolve().parent;P=O.parent;E=P/'emulator-tests'
sha=lambda b:hashlib.sha256(b).hexdigest()
rom=(O/'result.sfc').read_bytes();rows={x['id']:x for x in json.loads((O/'insertion-candidates.json').read_text())}
layout=json.loads((O/'placements.json').read_text())+[x for x in json.loads((P/'v0.48/layout-engine-check.json').read_text()) if not isinstance(x['group'],int)]
(O/'layout-engine-check.json').write_text(json.dumps(layout,indent=2))
def run(args):
 r=subprocess.run([sys.executable,str(E/'run_core.py')]+args,capture_output=True,text=True,check=True,timeout=90)
 return r.stdout
boot=run(['--rom',str(O/'result.sfc'),'--session','v049-boot','--reset','--check-layout',str(O/'layout-engine-check.json'),'--tag','v049-boot','--sequence',json.dumps([{'frames':1260},{'button':'start','frames':4,'press':4},{'frames':120},{'button':'a','frames':4,'press':4},{'frames':120}])])
bus=json.loads((E/'bus-verification.json').read_text());bus.update(result_sha256=sha(rom),layout_sha256=sha((O/'layout-engine-check.json').read_bytes()));(O/'qa-script-name-engine-bus.json').write_text(json.dumps(bus,indent=2))
S=O/'screenshots';S.mkdir(exist_ok=True);shutil.copy2(E/'v049-boot.png',S/'v049-boot.png')
camp=P.parent.parent/'work-v026/dq6-fr/emulator-tests/v026-camp.state'
out=[]
def checksum(b):
 s=sum(b)&65535
 for copy in [0,0x400000]:struct.pack_into('<HH',b,copy+0xffdc,s^65535,s)
def probe(mid,kind,mutate=None,ram=None):
 b=bytearray((E/f'fixture-v049-{mid}.sfc').read_bytes())
 if mutate:mutate(b)
 checksum(b);path=E/f'probe-v049-{kind}-{mid}.sfc';path.write_bytes(b)
 for page in range(1,(len(rows[mid]['lines'])+2)//3+1):
  tag=f'v049-{kind}-{mid}-page{page}'
  cmd=['--rom',str(path),'--session',f'v049-{kind}-{mid}','--tag',tag]
  if page==1:
   values={'0x5a2e':[255,255,255],'0x3b2d':[3,0],'0x5a24':[3,0],'0x5a2a':[1,0],'0x5a28':[249,8]}
   values.update(ram or {})
   cmd+=['--load-state',str(camp),'--set-wram',json.dumps(values),'--sequence',json.dumps([{'button':'a','frames':4,'press':1},{'frames':330},{'button':'down','frames':8,'press':1},{'frames':10},{'frames':240}])]
  else:cmd+=['--sequence',json.dumps([{'button':'a','frames':1,'press':1},{'frames':240}])]
  stdout=run(cmd);assert json.loads(stdout.splitlines()[0])['message_id']==100,(mid,page)
  f=E/(tag+'.png');shutil.copy2(f,S/f.name);out.append(dict(id=mid,kind=kind,page=page,screenshot='screenshots/'+f.name,sha256=sha(f.read_bytes()),output=stdout))
def plural_item(b):
 # Exact original JSL including its inline argument; force a returned count of 2.
 for copy in [0,0x400000]:
  a=copy+0x6927b;assert b[a:a+6]==bytes.fromhex('221c2bc401ff');b[a:a+6]=bytes.fromhex('a90200eaeaea')
 entries,groups,n=names.parse(b);packed=bytearray();starts=[]
 for i,e in enumerate(entries[:n]):
  starts.append(len(packed));packed+=(native_helpers.encode('Iron Ball of Destruction') if i in [1604,1638] else e)+b'\xac'
 oldend=names.START+sum(len(e)+1 for e in entries[:n]);tail=bytes(b[oldend:names.END]).rstrip(b'\xff')
 assert names.START+len(packed)+len(tail)<=names.END
 for copy in [0,0x400000]:
  b[copy+names.START:copy+names.END]=packed+tail+b'\xff'*(names.END-names.START-len(packed)-len(tail))
  for g,pos in enumerate(groups):b[copy+names.TABLE+3*g:copy+names.TABLE+3*g+3]=starts[pos].to_bytes(3,'little')
for mid in [29,83,84,866,1096]:probe(mid,'C4-plural-maxitem',plural_item)
probe(581,'BB-max')
probe(22,'B2-vocation')
report=dict(result_sha256=sha(rom),boot_output=boot,boot_screenshot='screenshots/v049-boot.png',boot_screenshot_sha256=sha((S/'v049-boot.png').read_bytes()),probes=out,diagnostic_forced_C4_return_count=2,diagnostic_item_name='Iron Ball of Destruction',diagnostic_item_physical_entries=[1604,1638],BB_decimal=16777215,B2_vocation_sid=0x8f9,limits='Camp message100 redirections. Forced C4 count is a display branch probe, not a natural party-count test. No natural transactions, naming writes, real item acquisition or SRAM effects validated.')
(O/'qa-runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('Bus, boot and',len(out),'stress pages completed')
