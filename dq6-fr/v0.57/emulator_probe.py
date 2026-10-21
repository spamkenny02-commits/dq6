"""Private Snes9x diagnostics over the production patch; never publish fixtures/states."""
from pathlib import Path
import argparse,json,subprocess,sys,tempfile
from common import O,R,c,read,sha,decode_pool,IDS
a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--runner',type=Path,required=True);a.add_argument('--camp',type=Path,required=True);a.add_argument('--mode',choices=['reader','render'],required=True);a.add_argument('--mutate-pointer',action='store_true');a.add_argument('--compact',action='store_true');a.add_argument('--ids');a=a.parse_args()
rom=(a.out/'result.sfc').read_bytes();report=read(O/'build-report.json');assert sha(rom)==report['ROM_sha256'];rows=decode_pool(rom,report['placement']);regions=c.main_regions(rom)+[dict(file_offset=report['placement']['offset'],size=report['placement']['size'])]
def free(size):return next(x for x in range(0x771800,0x7b8703-size,256) if all(not(p['file_offset']<x+size and p['file_offset']+p['size']>x) for p in regions))
def fixture(code):
 out=bytearray(rom);at=free(len(code));out[at:at+len(code)]=code
 for copy in (0,0x400000):
  assert out[copy+0x2ae2:copy+0x2ae6]==bytes.fromhex('c230f47e');out[copy+0x2ae2:copy+0x2ae6]=b'\x5c'+at.to_bytes(3,'little')
 return out
def run(p,tag,actions,initial=False):
 cmd=[sys.executable,str(a.runner.resolve()),'--rom',str(p.resolve()),'--session',tag,'--tag',tag,'--sequence',json.dumps(actions)]
 if initial:cmd+=['--load-state',str(a.camp.resolve())]
 subprocess.run(cmd,check=True,capture_output=True,timeout=60)
 e=a.runner.resolve().parent
 return (e/'wram.bin').read_bytes(),sha((e/(tag+'.png')).read_bytes())
if a.mode=='reader':
 code=bytearray.fromhex('c230f47e7eababa900008510');loop=len(code)
 code+=bytes.fromhex('a5108d98599cae599cb45922b027c022ff27c08512a5100a1865100aaa')
 code+=bytes.fromhex('a5a09f00707ea5a29f02707ea5129f04707ee610a510c96002d0');code.append((loop-len(code)-1)&255);code+=bytes.fromhex('a9efbe8f006f7e80fe');out=fixture(code)
 if a.mutate_pointer:
  for copy in (0,0x400000):
   at=copy+c.PTR+3;v=int.from_bytes(out[at:at+3],'little');out[at:at+3]=((v+1)&0xffffff).to_bytes(3,'little')
 with tempfile.NamedTemporaryFile(dir=a.out,suffix='.sfc') as f:
  f.write(out);f.flush();w,_=run(Path(f.name),'reader57-private',[dict(button='a',frames=4,press=1),dict(frames=330),dict(button='a',frames=4,press=1),dict(frames=330)],True)
 assert w[0x6f00:0x6f02]==bytes.fromhex('efbe');errors=[]
 for mid,at,data in rows:
  p=0x7000+mid*6;got=int.from_bytes(w[p:p+2],'little')|(w[p+2]<<16);first=int.from_bytes(w[p+4:p+6],'little')
  if got!=at+1 or first!=data[0]:errors.append(mid)
 assert errors==([8] if a.mutate_pointer else [])
 qa=dict(release='v0.57',production_ROM_sha256=sha(rom),IDs_checked=608,errors=errors,deliberate_pointer_mutation=a.mutate_pointer,expected_result_observed=True,full_messages_rendered=False,natural_battle=False)
 name='qa-native-pointer-negative.json' if a.mutate_pointer else 'qa-native-reader.json';(O/name).write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps(qa))
else:
 assert not a.mutate_pointer;results=[]
 for mid in ([int(x) for x in a.ids.split(',')] if a.ids else IDS):
  assert mid in IDS
  # C02A29 initializes the native printer; C02671 alone omits its state setup.
  api=0x2a4f if a.compact else 0x2a29
  assert rom[api:api+5]==bytes.fromhex('08c23048da')
  code=bytes.fromhex('c230f47e7eababa9')+mid.to_bytes(2,'little')+b'\x22'+api.to_bytes(2,'little')+bytes.fromhex('c0a9efbe8f006f7e80fe');out=fixture(code);pages=[]
  with tempfile.NamedTemporaryFile(dir=a.out,suffix='.sfc') as f:
   f.write(out);f.flush();tag=f'render57{"compact" if a.compact else ""}-{mid}-private'
   for step,actions in enumerate([[dict(button='a',frames=4,press=1),dict(frames=330),dict(button='a',frames=1,press=1),dict(frames=1)]]+[[dict(frames=n)] for n in [2,4,8,16,32,64,128]]+[[dict(button='a',frames=1,press=1),dict(frames=120)],[dict(button='a',frames=1,press=1),dict(frames=120)]]):
    w,h=run(Path(f.name),tag,actions,step==0)
    import shutil
    image=a.runner.resolve().parent/(tag+'.png');shutil.copyfile(image,a.out/f'render{"compact" if a.compact else ""}-{mid}-{step}-private.png')
    pages.append(dict(step=step,screenshot_sha256=h,message_id=int.from_bytes(w[0x5998:0x599a],'little'),API_returned=w[0x6f00:0x6f02]==bytes.fromhex('efbe')))
  results.append(dict(id=mid,fixture_sha256=sha(out),captures=pages,manual_visual_review=False))
 qa=dict(release='v0.57',production_ROM_sha256=sha(rom),native_API='C02A4F' if a.compact else 'C02A29',native_loader_unmodified=True,diagnostic_main_entry_redirect=True,natural_battle=False,results=results)
 (O/('qa-emulator-compact-captures.json' if a.compact else 'qa-emulator-captures.json')).write_text(json.dumps(qa,indent=2)+'\n');print('Eight native printer fixtures captured; manual review still required')
