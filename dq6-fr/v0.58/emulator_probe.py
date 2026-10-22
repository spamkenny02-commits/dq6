"""Private Snes9x diagnostics over the production patch; never publish fixtures/states."""
from pathlib import Path
import argparse,json,subprocess,sys,tempfile
from common import O,R,c,read,sha,decode_pool,IDS
a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--runner',type=Path,required=True);a.add_argument('--camp',type=Path,required=True);a.add_argument('--mode',choices=['reader','render'],required=True);a.add_argument('--mutate-pointer',action='store_true');a.add_argument('--compact',action='store_true');a.add_argument('--ids');a.add_argument('--profile',choices=['distinct','duplicate'],default='distinct');a=a.parse_args()
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
  f.write(out);f.flush();w,_=run(Path(f.name),'reader58-private',[dict(button='a',frames=4,press=1),dict(frames=330),dict(button='a',frames=4,press=1),dict(frames=330)],True)
 assert w[0x6f00:0x6f02]==bytes.fromhex('efbe');errors=[]
 for mid,at,data in rows:
  p=0x7000+mid*6;got=int.from_bytes(w[p:p+2],'little')|(w[p+2]<<16);first=int.from_bytes(w[p+4:p+6],'little')
  if got!=at+1 or first!=data[0]:errors.append(mid)
 assert errors==([8] if a.mutate_pointer else [])
 qa=dict(release='v0.58',production_ROM_sha256=sha(rom),IDs_checked=608,errors=errors,deliberate_pointer_mutation=a.mutate_pointer,expected_result_observed=True,full_messages_rendered=False,natural_battle=False)
 name='qa-native-pointer-negative.json' if a.mutate_pointer else 'qa-native-reader.json';(O/name).write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps(qa))
else:
 assert not a.mutate_pointer;results=[]
 for mid in ([int(x) for x in a.ids.split(',')] if a.ids else IDS):
  assert mid in IDS
  # C02A29 initializes the native printer; C02671 alone omits its state setup.
  api=0x2a4f if a.compact else 0x2a29
  assert rom[api:api+5]==bytes.fromhex('08c23048da')
  code=bytearray.fromhex('c230f47e7eababa2de04a90000');loop=len(code);code+=bytes.fromhex('9d3420caca10');code.append((loop-len(code)-1)&255)
  assert rom[0x24:0x2a]==bytes.fromhex('0c93c61593c6')
  code+=bytes.fromhex('a901008d5f208d93208d4f20a9')+(1 if a.profile=='duplicate' else 6).to_bytes(2,'little')+bytes.fromhex('8d8320')
  if a.profile=='duplicate':code+=bytes.fromhex('a904008d8920')
  code+=bytes.fromhex('9c5525a901008d5925a2000022d5b8c2988f046f7ea2010022d5b8c2988f066f7ea9')+mid.to_bytes(2,'little')+b'\x22'+api.to_bytes(2,'little')+bytes.fromhex('c0a9efbe8f006f7e80fe');out=fixture(code);pages=[]
  with tempfile.NamedTemporaryFile(dir=a.out,suffix='.sfc') as f:
   f.write(out);f.flush();tag=f'render58-{a.profile}-{mid}-private'
   actions=[dict(button='a',frames=4,press=1),dict(frames=330),dict(button='a',frames=1,press=1),dict(frames=255),dict(button='a',frames=1,press=1),dict(frames=120),dict(button='a',frames=1,press=1),dict(frames=120)]
   w,h=run(Path(f.name),tag,actions,True)
   import shutil
   shutil.copyfile(a.runner.resolve().parent/(tag+'.png'),a.out/(tag+'.png'))
   pages.append(dict(step='final_after_two_acknowledgements',screenshot_sha256=h,message_id=int.from_bytes(w[0x5998:0x599a],'little'),API_returned=w[0x6f00:0x6f02]==bytes.fromhex('efbe')))
  assert int.from_bytes(w[0x6f04:0x6f06],'little')==0x2f1 and int.from_bytes(w[0x6f06:0x6f08],'little')==(0x2f1 if a.profile=='duplicate' else 0x24f)
  results.append(dict(id=mid,fixture_sha256=sha(out),captures=pages,manual_visual_review=False))
 qa=dict(release='v0.58',production_ROM_sha256=sha(rom),native_API='C02A4F' if a.compact else 'C02A29',native_loader_unmodified=True,diagnostic_main_entry_redirect=True,natural_battle=False,entity_profile=a.profile,actor_name_SID='02F1',target_name_SID='02F1' if a.profile=='duplicate' else '024F',player_name_path_validated=False,results=results)
 (O/f'qa-emulator-{a.profile}-captures.json').write_text(json.dumps(qa,indent=2)+'\n');print(f'{len(results)} native fixtures captured ({a.profile}); manual visual review required')
