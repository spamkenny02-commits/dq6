"""Differential CPU diagnostics: field tile writer and native B2 name buffer.
No natural-menu/path coverage claim; no consumer code changed.
"""
from common import *
import argparse,tempfile,subprocess
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--runner',type=Path,required=True);p.add_argument('--camp',type=Path,required=True);a=p.parse_args()
base=bytes(module('patch65cons',R/'dq6-fr/upstream/refill/patchRM.py').apply_bps(a.jp.read_bytes(),(R/'patches/DQVI-FR-DS-v0.64-BASE-JP-PARTIEL.bps').read_bytes()));candidate=(a.out/'result.sfc').read_bytes();assert sha(base)==BASE['ROM_sha256'];assert sha(candidate)==read(O/'build-report.json')['ROM_sha256']
code=bytearray.fromhex('78c230f47e7eabab')
def emit(h):code.extend(bytes.fromhex(h))
def word(v):return v.to_bytes(2,'little').hex()
for i,sid in enumerate(SIDS):
 # Clear complete tilemap area and name buffer before each diagnostic.
 emit('a2fe07a900009e6830caca10f9a23e009eb859caca10f9')
 for at,value in [(0x3886,0),(0x388a,0),(0x3898,0),(0x389a,0)]:emit('a9'+word(value)+'8d'+word(at))
 emit('a9'+word(sid)+'223a76c3')
 emit('a20000bd68309f'+(0x7f0000+i*0x1000).to_bytes(3,'little').hex()+'e8e8e00008d0f2')
 emit('ad8a388f'+(0x7f0800+i*0x1000).to_bytes(3,'little').hex())
 emit('a9'+word(sid)+'22f0fdc6')
 emit('a20000bdb8599f'+(0x7f0810+i*0x1000).to_bytes(3,'little').hex()+'e8e8e04000d0f2')
emit('a9efbe8f006f7e80fe')
regions=c.main_regions(candidate)+[dict(file_offset=BASE[k]['allocation']['offset'],size=BASE[k]['allocation']['size']) for k in ['engine']]+[dict(file_offset=BASE['placement']['offset'],size=BASE['placement']['size'])]
off=next(x for x in range(0x771800,0x7b8000,256) if all(not(p['file_offset']<x+len(code) and p['file_offset']+p['size']>x) for p in regions))
results=[]
for tag,rom in [('before',base),('after',candidate)]:
 fixture=bytearray(rom);fixture[off:off+len(code)]=code
 for copy in (0,0x400000):assert fixture[copy+0x2ae2:copy+0x2ae6]==bytes.fromhex('c230f47e');fixture[copy+0x2ae2:copy+0x2ae6]=b'\x5c'+off.to_bytes(3,'little')
 with tempfile.NamedTemporaryFile(dir=a.out,suffix='.sfc') as f:
  f.write(fixture);f.flush();proc=subprocess.run([sys.executable,str(a.runner.resolve()),'--rom',str(Path(f.name).resolve()),'--load-state',str(a.camp.resolve()),'--session','v065-consumers-'+tag,'--tag','v065-consumers-'+tag,'--sequence',json.dumps([dict(button='a',frames=4,press=1),dict(frames=330),dict(button='a',frames=1,press=1),dict(frames=300)])],capture_output=True,timeout=90);assert proc.returncode==0,proc.stderr.decode()
 w=(a.runner.resolve().parent/'wram.bin').read_bytes();assert w[0x6f00:0x6f02]==bytes.fromhex('efbe');results.append(w[0x10000:0x15000])
assert results[0]==results[1],'Actual consumer output changed'
rows=[];ns=names(candidate)
for i,sid in enumerate(SIDS):
 w=results[1][i*0x1000:(i+1)*0x1000];expanded=expand(candidate,ns[sid][1])[:-1];width=int.from_bytes(w[0x800:0x802],'little');assert width==len(expanded),(sid,width,len(expanded));buffer=b''.join(bytes([b,0]) for b in expanded)+bytes.fromhex('ab00');assert w[0x810:0x810+len(buffer)]==buffer
 tiles=[int.from_bytes(w[j*2:j*2+2],'little') for j in range(width)];assert tiles==[0x300+b for b in expanded],(sid,tiles,expanded.hex())
 rows.append(dict(sid=sid,native_field_glyphs_checked=width,native_B2_glyphs_checked=len(expanded),field_tilemap_sha256=sha(w[:0x800]),B2_buffer_sha256=sha(buffer),before_after_identical=True))
q=dict(release='v0.65',ROM_sha256=sha(candidate),field_consumer='C3763A, actual JSL including C0315E/C031DB and C376F2',B2_consumer='C6FDF0, actual JSL including C0315E/C031DB and existing DTE dictionary',rows=rows,all_five_changed_encodings_checked=True,natural_validation=False,limits='Private CPU redirection from camp. Dynamic SID branch09A7..09C9 and other natural menu paths not validated; no renderer code modified.')
(O/'qa-name-consumers.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps(q))
