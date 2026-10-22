from common import *
import argparse,subprocess,tempfile
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--runner',type=Path,required=True);p.add_argument('--camp',type=Path,required=True);a=p.parse_args();rom=(a.out/'result.sfc').read_bytes();rep=read(O/'build-report.json');assert sha(rom)==rep['ROM_sha256'];regions=c.main_regions(rom)+[dict(file_offset=rep['placement']['offset'],size=rep['placement']['size']),dict(file_offset=rep['engine']['allocation']['offset'],size=0x400)]
code=bytearray.fromhex('c230f47e7eababa900008510');loop=len(code);code+=bytes.fromhex('a510a2ba00225e31c0a5100a0aaaa5ba9f00707ea5bc9f02707ee610a510c9d009d0');code.append((loop-len(code)-1)&255);code+=bytes.fromhex('a9efbe8f006f7e80fe')
off=next(x for x in range(0x771800,0x7b8000,256) if all(not(p['file_offset']<x+len(code) and p['file_offset']+p['size']>x) for p in regions));out=bytearray(rom);out[off:off+len(code)]=code
for copy in (0,0x400000):out[copy+0x2ae2:copy+0x2ae6]=b'\x5c'+off.to_bytes(3,'little')
with tempfile.NamedTemporaryFile(dir=a.out,suffix='.sfc') as f:
 f.write(out);f.flush();subprocess.run([sys.executable,str(a.runner.resolve()),'--rom',str(Path(f.name).resolve()),'--load-state',str(a.camp.resolve()),'--session','v061-names','--tag','v061-names','--sequence',json.dumps([dict(button='a',frames=4,press=1),dict(frames=330),dict(button='a',frames=1,press=1),dict(frames=300)])],check=True,capture_output=True,timeout=90)
w=(a.runner.resolve().parent/'wram.bin').read_bytes();assert w[0x6f00:0x6f02]==bytes.fromhex('efbe');errors=[];static=[];dynamic=list(range(0x9a7,0x9ca));ns=names(rom)
for sid,(at,b) in enumerate(ns):
 if sid in dynamic:continue
 got=int.from_bytes(w[0x7000+4*sid:0x7003+4*sid],'little');expected=0xc00000+at
 if got!=expected:errors.append(dict(sid=sid,got=hex(got),expected=hex(expected)))
 static.append(sid)
assert not errors,errors[:10]
qa=dict(release='v0.61',ROM_sha256=sha(rom),native_static_name_SIDs_checked=len(static),dynamic_SIDs_excluded=dynamic,errors=errors,new_name_SIDs_included=[0x369,0x36a],all_2512_file_name_entries_checked_in='verification.json',natural_battle=False)
(O/'qa-native-names.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps(qa))
