"""Private native-reader probe; no ROM output may be published."""
from pathlib import Path
import argparse,json,sys,importlib.util,subprocess,tempfile,hashlib
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('codec58',R/'tools/combat-v058/codec.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
a=argparse.ArgumentParser();a.add_argument('--jp',type=Path,required=True);a.add_argument('--camp',type=Path,required=True);a.add_argument('--runner',type=Path,required=True);a.add_argument('--mutate-pointer',action='store_true');a=a.parse_args();jp=a.jp.read_bytes();rom=bytearray(c.baseline_from_jp(jp,R));base=bytes(rom);rows=c.pool(rom);regions=c.main_regions(rom)
payload=bytearray();starts=[];expected=[]
for mid,_,data in rows:
 if mid%8==0:starts.append(len(payload))
 expected.append(len(payload));payload+=data
size=len(payload);off=next(x for x in range(0x771800,0x7b8703-size-128,256) if all(not(p['file_offset']<x+size+128 and p['file_offset']+p['size']>x) for p in regions))
rom[off:off+size]=payload
for copy in [0,0x400000]:
 for g,start in enumerate(starts):rom[copy+c.PTR+3*g:copy+c.PTR+3*g+3]=((off+start-0xf6debd)&0xffffff).to_bytes(3,'little')
mutation_id=None
if a.mutate_pointer:
 g=next(g for g in range(1,76) if len(rows[g*8][2])>3);mutation_id=g*8
 for copy in [0,0x400000]:rom[copy+c.PTR+3*g:copy+c.PTR+3*g+3]=((off+starts[g]+1-0xf6debd)&0xffffff).to_bytes(3,'little')
code_at=off+size
stub=bytearray.fromhex('c230f47e7eababa900008510');loop=len(stub)
stub+=bytes.fromhex('a5108d98599cae599cb45922b027c022ff27c08512a5100a1865100aaa')
stub+=bytes.fromhex('a5a09f00707ea5a29f02707ea5129f04707ee610a510c96002d0');delta=loop-(len(stub)+1);assert -128<=delta<0;stub.append(delta&255);stub+=bytes.fromhex('a9efbe8f006f7e80fe')
rom[code_at:code_at+len(stub)]=stub
for copy in [0,0x400000]:
 assert rom[copy+0x2ae2:copy+0x2ae6]==bytes.fromhex('c230f47e');rom[copy+0x2ae2:copy+0x2ae6]=b'\x5c'+code_at.to_bytes(3,'little')
with tempfile.TemporaryDirectory(prefix='native59-',dir=R) as d:
 p=Path(d)/'private.sfc';p.write_bytes(rom);cmd=[sys.executable,str(a.runner.resolve()),'--rom',str(p),'--load-state',str(a.camp.resolve()),'--session','native59-private','--tag','native59-private','--sequence',json.dumps([dict(button='a',frames=4,press=1),dict(frames=330),dict(button='a',frames=4,press=1),dict(frames=330)])];run=subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=45)
 w=(a.runner.resolve().parent/'wram.bin').read_bytes();assert w[0x6f00:0x6f02]==bytes.fromhex('efbe'),'Probe loop did not complete'
 errors=[]
 for mid,_,data in rows:
  at=0x7000+mid*6;got=int.from_bytes(w[at:at+2],'little')|(w[at+2]<<16);first=int.from_bytes(w[at+4:at+6],'little');wanted=off+expected[mid]+1
  if got!=wanted or first!=data[0]:errors.append(dict(id=mid,pointer=got,expected=wanted,first_byte_matches=first==data[0]))
 report=dict(mutated_pointer_id=mutation_id,checkpoint='combat-v059',messages=608,all_native_CPU_pointers_and_first_bytes_match=not errors,error_count=len(errors),errors_metadata=errors[:10],probe_loop_completed=True,buffer_mode_cleared=True,execution_stops_after_probe=True,native_loader='C027B0',native_reader='C027FF',renderer_tested=False,private_fixture_sha256=hashlib.sha256(rom).hexdigest(),new_inserted=0)
 (R/'mutation59-private.json' if a.mutate_pointer else O/'qa-native-loader.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
 if a.mutate_pointer:assert [x['id'] for x in errors]==[mutation_id],'Pointer mutation not detected precisely'
 else:assert not errors,'Native pointers/read bytes mismatch'
