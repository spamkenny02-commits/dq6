"""Sequential private Snes9x variable diagnostics. Never publish generated ROMs/states/images."""
from pathlib import Path
import argparse,json,subprocess,sys,tempfile,shutil
from common import O,R,c,read,sha
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--runner',type=Path,required=True);p.add_argument('--camp',type=Path,required=True);a=p.parse_args()
rom=(a.out/'result.sfc').read_bytes();report=read(O/'build-report.json');assert sha(rom)==report['ROM_sha256']
regions=c.main_regions(rom)+[dict(file_offset=report['placement']['offset'],size=report['placement']['size'])]
scenarios=[(337,'distinct',0x61f,0),(337,'duplicate',0x2f1,0),(428,'distinct',0x61f,0),(428,'distinct',0x61f,1),(454,'distinct',0x24f,0),(454,'duplicate',0x2f1,0),(455,'distinct',0x2f1,0),(455,'duplicate',0x2f1,0),(428,'distinct',0x61f,2),(428,'duplicate',0x61f,2)]
results=[]
for n,(mid,profile,sid,b4index) in enumerate(scenarios):
 code=bytearray.fromhex('c230f47e7eababa2de04a90000');loop=len(code);code+=bytes.fromhex('9d3420caca10');code.append((loop-len(code)-1)&255)
 code+=bytes.fromhex('a901008d5f208d93208d4f20a9')+(1 if profile=='duplicate' else 6).to_bytes(2,'little')+bytes.fromhex('8d8320')
 if profile=='duplicate':code+=bytes.fromhex('a904008d8920')
 code+=bytes.fromhex('9c5525a901008d5925a9')+sid.to_bytes(2,'little')+bytes.fromhex('8d285aa9')+b4index.to_bytes(2,'little')+bytes.fromhex('8d225aa2000022d5b8c2988f046f7ea2010022d5b8c2988f066f7ea9')+mid.to_bytes(2,'little')+bytes.fromhex('22292ac0a9efbe8f006f7e80fe')
 at=next(x for x in range(0x771800,0x7b8703-len(code),256) if all(not(p['file_offset']<x+len(code) and p['file_offset']+p['size']>x) for p in regions))
 out=bytearray(rom);out[at:at+len(code)]=code
 for copy in (0,0x400000):
  assert out[copy+0x2ae2:copy+0x2ae6]==bytes.fromhex('c230f47e');out[copy+0x2ae2:copy+0x2ae6]=b'\x5c'+at.to_bytes(3,'little')
 tag=f'v05967-{n}-{mid}-{profile}'
 actions=[dict(button='a',frames=4,press=1),dict(frames=330),dict(button='a',frames=1,press=1),dict(frames=255),dict(button='a',frames=1,press=1),dict(frames=120),dict(button='a',frames=1,press=1),dict(frames=120)]
 with tempfile.NamedTemporaryFile(dir=a.out,suffix='.sfc') as f:
  f.write(out);f.flush();subprocess.run([sys.executable,str(a.runner.resolve()),'--rom',str(Path(f.name).resolve()),'--load-state',str(a.camp.resolve()),'--session',tag,'--tag',tag,'--sequence',json.dumps(actions)],check=True,capture_output=True,timeout=60)
 ep=a.runner.resolve().parent;w=(ep/'wram.bin').read_bytes();image=ep/(tag+'.png');shutil.copyfile(image,a.out/image.name)
 assert w[0x6f00:0x6f02]==bytes.fromhex('efbe'),f'Printer did not return:{tag}'
 assert int.from_bytes(w[0x6f04:0x6f06],'little')==0x2f1
 assert int.from_bytes(w[0x6f06:0x6f08],'little')==(0x2f1 if profile=='duplicate' else 0x24f)
 results.append(dict(id=mid,profile=profile,B2_SID=f'{sid:04X}',B4_lookup_index=b4index,API_returned=True,screenshot_sha256=sha(image.read_bytes()),private_capture=image.name,fixture_sha256=sha(out),manual_visual_review=False,negative_uninitialized_B4=(mid==428 and b4index==0)))
 print(tag,flush=True)
qa=dict(release='v0.59',production_ROM_sha256=sha(rom),native_API='C02A29',diagnostic_entry_redirect=True,natural_battle=False,engine_modified=False,player_name_path_validated=False,results=results)
(O/'qa-variable-captures.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
