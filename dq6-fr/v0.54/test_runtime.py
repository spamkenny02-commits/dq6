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
layout=json.loads((O/'placements.json').read_text())+[x for x in json.loads((P/'v0.53/layout-engine-check.json').read_text()) if not isinstance(x['group'],int)]
for copy in [0,0x400000]:
 for label,a,n in [('C7',0x692ee,16),('E0',0x6929b,22),('DC',0x69492,11),('DC_helper',0x6957e,20),('E1',0x695b1,15)]:layout.append(dict(group='native-'+label+'-'+str(copy),file_offset=copy+a,cpu_address=(0xc00000+a if copy==0 else copy+a),size=n))
(O/'layout-engine-check.json').write_text(json.dumps(layout,indent=2))
def run(args):
 r=subprocess.run([sys.executable,str(E/'run_core.py')]+args,capture_output=True,text=True,check=True,timeout=90)
 return r.stdout
boot=run(['--rom',str(O/'result.sfc'),'--session','v054-boot','--reset','--check-layout',str(O/'layout-engine-check.json'),'--tag','v054-boot','--sequence',json.dumps([{'frames':1260},{'button':'start','frames':4,'press':4},{'frames':120},{'button':'a','frames':4,'press':4},{'frames':120}])])
bus=json.loads((E/'bus-verification.json').read_text());bus.update(result_sha256=sha(rom),layout_sha256=sha((O/'layout-engine-check.json').read_bytes()));(O/'qa-script-name-engine-bus.json').write_text(json.dumps(bus,indent=2))
S=O/'screenshots';S.mkdir(exist_ok=True);shutil.copy2(E/'v054-boot.png',S/'v054-boot.png')
camp=P.parent.parent/'work-v026/dq6-fr/emulator-tests/v026-camp.state'
out=[]
def checksum(b):
 s=sum(b)&65535
 for copy in [0,0x400000]:struct.pack_into('<HH',b,copy+0xffdc,s^65535,s)
def probe(mid,kind,mutate=None,ram=None,max_pages=None):
 b=bytearray((E/f'fixture-v054-{mid}.sfc').read_bytes())
 if mutate:mutate(b)
 checksum(b);path=E/f'probe-v054-{kind}-{mid}.sfc';path.write_bytes(b)
 for page in range(1,min((len(rows[mid]['lines'])+2)//3,max_pages or 999)+1):
  tag=f'v054-{kind}-{mid}-page{page}'
  cmd=['--rom',str(path),'--session',f'v054-{kind}-{mid}','--tag',tag]
  if page==1:
   values={'0x5a2e':[255,255,255],'0x3b2d':[3,0],'0x5a24':[3,0],'0x5a2a':[1,0],'0x5a2c':[2,0],'0x5a28':[249,8]}
   values.update(ram or {})
   cmd+=['--load-state',str(camp),'--set-wram',json.dumps(values),'--sequence',json.dumps([{'button':'a','frames':4,'press':1},{'frames':330},{'button':'down','frames':8,'press':1},{'frames':10},{'frames':240}])]
  else:cmd+=['--sequence',json.dumps([{'button':'a','frames':1,'press':1},{'frames':240}])]
  stdout=run(cmd);assert json.loads(stdout.splitlines()[0])['message_id']==100,(mid,page)
  wram=(E/'wram.bin').read_bytes();observed={hex(a):int.from_bytes(wram[a:a+2],'little') for a in [0x59a8,0x5a04,0x5a06,0x5a2a,0x5a2c]}
  f=E/(tag+'.png');shutil.copy2(f,S/f.name);out.append(dict(id=mid,kind=kind,page=page,screenshot='screenshots/'+f.name,sha256=sha(f.read_bytes()),output=stdout,observed_wram=observed))
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
def e0_count(count):
 def mutate(b):
  for copy in [0,0x400000]:
   a=copy+0x6929b;assert b[a:a+6]==bytes.fromhex('221c2bc401ff');b[a:a+6]=bytes([0xa9,count,0,0xea,0xea,0xea])
 return mutate
for count in [1,2]:probe(3727,'E0-count'+str(count),e0_count(count))
for mid in [6716,6718]:probe(mid,'C7-max',plural_item,ram={'0x5a2a':[2,0],'0x5a2c':[1,0]})
for value in [0,16]:probe(6548,'E1-state'+str(value),ram={'0x59a8':list(value.to_bytes(2,'little'))})
for mid in [6922,6923,6924,6925]:probe(mid,'DC-reset',ram={'0x5a04':[0,0],'0x5a06':[52,18]})
report=dict(result_sha256=sha(rom),boot_output=boot,boot_screenshot='screenshots/v054-boot.png',boot_screenshot_sha256=sha((S/'v054-boot.png').read_bytes()),probes=out,diagnostic_forced_E0_return_counts=[1,2],diagnostic_item_name='Iron Ball of Destruction',C7_max_item_id=1,B5_other_item_id=2,BB_decimal=16777215,limits='Camp message100 redirections. E0 count forced in private diagnostic ROMs, not natural group calculation. E1/DC observations are after rendering in camp, not a complete audit of state-machine side effects or natural ending/shop execution. DC cleanup path with5A04 nonzero not exercised. No purchases, contest results, ending progression or SRAM effects validated.')
(O/'qa-runtime.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('Bus, boot and',len(out),'stress pages completed')
