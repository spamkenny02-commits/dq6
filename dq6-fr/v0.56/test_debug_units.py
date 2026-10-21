"""Private E1 hook units execute the exact native set/clear and walk-flag readers.
This tests helper effects and masks, not the complete natural debug menu path.
The E1 fixture is inherited6548, unrelated to any source dialogue mutation.
"""
from pathlib import Path
import json,subprocess,sys,struct,hashlib,shutil
import native_helpers
O=Path(__file__).resolve().parent;D=O.parent;E=D/'emulator-tests';R=D.parent;S=O/'screenshots';base=(O/'result.sfc').read_bytes();rows={x['id']:x for x in json.loads((O/'insertion-candidates.json').read_text())}
subprocess.run([sys.executable,str(O/'render_fixtures.py'),'v0.56','6548'],check=True)
fixture=(E/'fixture-v056-6548.sfc').read_bytes();layout=json.loads((O/'placements.json').read_text());g=int.from_bytes(fixture[0x15bb5+36:0x15bb8+36],'little');a=next(a for a in range(0x771800,0x7b8600,256) if not(g<=a<g+0x2000) and all(not(p['file_offset']<a+32 and p['file_offset']+p['size']>a) for p in layout));out=[]
cases=[(2,True,0x10,0x20),(2,True,0x10,0),(2,False,0x12,0x20),(2,False,0x12,0),(4,True,0x10,0x20),(4,False,0x14,0x20)]
for i,(mask,enable,initial,inp) in enumerate(cases):
 rom=bytearray(fixture);helper=0xc92e50 if enable else 0xc92e93;code=bytes([0xa9,inp,0,0x8d,0x40,0x58,0x22])+helper.to_bytes(3,'little')+bytes.fromhex('003d7e')+mask.to_bytes(2,'little')+bytes.fromhex('00227d90c56b');rom[a:a+len(code)]=code
 for copy in [0,0x400000]:
  assert rom[copy+0x695b1:copy+0x695c0]==bytes.fromhex('ada859c91000d006a921008da8596b');rom[copy+0x695b1:copy+0x695b6]=bytes([0x22])+a.to_bytes(3,'little')+bytes([0x6b])
 c=sum(rom)&65535
 for copy in [0,0x400000]:struct.pack_into('<HH',rom,copy+0xffdc,c^65535,c)
 p=E/f'debug-unit-v056-{i}.sfc';p.write_bytes(rom);tag=f'v056-debug-unit-{i}';ram={'0x3d00':list(initial.to_bytes(2,'little')),'0x6e51':[52,18],'0x5a2e':[57,48,0]};seq=[{'button':'a','frames':4,'press':1},{'frames':330},{'button':'down','frames':8,'press':1},{'frames':250}]
 cmd=[sys.executable,str(E/'run_core.py'),'--rom',str(p),'--session',tag,'--tag',tag,'--load-state',str(R.parent/'work-v026/dq6-fr/emulator-tests/v026-camp.state'),'--set-wram',json.dumps(ram),'--sequence',json.dumps(seq)];r=subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=45);w=(E/'wram.bin').read_bytes();flags=int.from_bytes(w[0x3d00:0x3d02],'little');walk=int.from_bytes(w[0x6e51:0x6e53],'little');expected=(initial|mask) if enable else(initial&~mask)
 assert flags==expected,(i,'flags',flags,expected);assert walk==int(bool(expected&2 and inp&0x20)),(i,'walk',walk)
 f=E/(tag+'.png');shutil.copy2(f,S/f.name);out.append(dict(mask=mask,enable=enable,initial_flags=initial,input_mask_forced=inp,observed_flags=flags,walk_indicator=walk,other_bits_preserved=True,screenshot='screenshots/'+f.name,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),output=r.stdout))
(O/'qa-unites-debug.json').write_text(json.dumps(dict(result_sha256=hashlib.sha256(base).hexdigest(),units=out,source_helpers_executed=['C92E50','C92E93','C5907D'],private_E1_hook=True,private_input_write_immediately_before_native_reader=True,limits='Masks and reader tested. No actual cancel-button movement, complete native menu choice, start-floor transition, fusion, drop or turn event executed.'),ensure_ascii=False,indent=2));print('6 native debug units passed')
