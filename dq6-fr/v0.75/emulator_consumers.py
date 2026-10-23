"""Differential CPU diagnostics: field tile writer and native B2 name buffer.
No natural-menu/path coverage claim; no consumer code changed.
"""
from common import *
import argparse,tempfile,subprocess
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--runner',type=Path,required=True);p.add_argument('--camp',type=Path,required=True);p.add_argument('--sids');p.add_argument('--report-suffix',default='');a=p.parse_args();SIDS=json.loads(a.sids) if a.sids else SIDS;assert len(SIDS)<=25
base=bytes(module('patch65cons',R/'dq6-fr/upstream/refill/patchRM.py').apply_bps(a.jp.read_bytes(),(R/'patches/DQVI-FR-DS-v0.74-BASE-JP-PARTIEL.bps').read_bytes()));candidate=(a.out/'result.sfc').read_bytes();assert sha(base)==BASE['ROM_sha256'];assert sha(candidate)==read(O/'build-report.json')['ROM_sha256']
code=bytearray.fromhex('78c230f47e7eabab')
def emit(h):code.extend(bytes.fromhex(h))
def word(v):return v.to_bytes(2,'little').hex()
for i,sid in enumerate(SIDS):
 # Clear complete tilemap area and name buffer before each diagnostic.
 emit('a2fe07a900009e6830caca10f9a23e009eb859caca10f9')
 for at,value in [(0x3886,0),(0x388a,0),(0x3898,0),(0x389a,0)]:emit('a9'+word(value)+'8d'+word(at))
 emit('a9'+word(sid)+'223a76c3')
 emit('a20000bd68309f'+(0x7f0000+i*0x800).to_bytes(3,'little').hex()+'e8e8e00004d0f2')
 emit('ad8a388f'+(0x7f0400+i*0x800).to_bytes(3,'little').hex())
 emit('a9'+word(sid)+'22f0fdc6')
 emit('a20000bdb8599f'+(0x7f0410+i*0x800).to_bytes(3,'little').hex()+'e8e8e04000d0f2')
emit('a9efbe8f006f7e80fe')
regions=c.main_regions(candidate)+[dict(file_offset=NAME,size=NAME_LIMIT-NAME)]+[dict(file_offset=BASE[k]['allocation']['offset'],size=BASE[k]['allocation']['size']) for k in ['engine']]+[dict(file_offset=BASE['placement']['offset'],size=BASE['placement']['size'])]
off=next(x for x in range(0x771800,0x7b8000,256) if all(not(p['file_offset']<x+len(code) and p['file_offset']+p['size']>x) for p in regions))
results=[]
for tag,rom in [('before',base),('after',candidate)]:
 fixture=bytearray(rom);fixture[off:off+len(code)]=code
 for copy in (0,0x400000):assert fixture[copy+0x2ae2:copy+0x2ae6]==bytes.fromhex('c230f47e');fixture[copy+0x2ae2:copy+0x2ae6]=b'\x5c'+off.to_bytes(3,'little')
 with tempfile.NamedTemporaryFile(dir=a.out,suffix='.sfc') as f:
  f.write(fixture);f.flush();proc=subprocess.run([sys.executable,str(a.runner.resolve()),'--rom',str(Path(f.name).resolve()),'--load-state',str(a.camp.resolve()),'--session','v075-consumers-'+tag,'--tag','v075-consumers-'+tag,'--sequence',json.dumps([dict(button='a',frames=4,press=1),dict(frames=330),dict(button='a',frames=1,press=1),dict(frames=300)])],capture_output=True,timeout=90);assert proc.returncode==0,proc.stderr.decode()
 w=(a.runner.resolve().parent/'wram.bin').read_bytes();assert w[0x6f00:0x6f02]==bytes.fromhex('efbe');results.append(w[0x10000:0x20000])
assert len(results)==2
rows=[]
for tag,result,rom in [('before',results[0],base),('after',results[1],candidate)]:
 ns=names(rom)
 for i,sid in enumerate(SIDS):
  w=result[i*0x800:(i+1)*0x800];expanded=expand(rom,ns[sid][1])[:-1];width=int.from_bytes(w[0x400:0x402],'little');breaks=[j for j,b in enumerate(expanded) if 0x91<=b<=0x9d];assert len(breaks)<=1
  expected_tiles=[0]*512
  if breaks:
   cut=breaks[0];assert expanded[cut]==0x90+cut;assert cut<=13 and len(expanded)-cut-1<=28;assert width==len(expanded)-cut
   for j,v in enumerate(expanded[:cut]):expected_tiles[j]=0x300+v
   for j,v in enumerate(expanded[cut+1:]):expected_tiles[33+j]=0x300+v
  else:
   assert width==len(expanded) and width<=28
   for j,v in enumerate(expanded):expected_tiles[j]=0x300+v
  buffer=b''.join(bytes([b,0]) for b in expanded)+bytes.fromhex('ab00');assert w[0x410:0x410+len(buffer)]==buffer
  tiles=[int.from_bytes(w[j*2:j*2+2],'little') for j in range(512)];assert tiles==expected_tiles,(tag,sid,width,breaks)
  rows.append(dict(stage=tag,sid=sid,native_field_glyphs_checked=len(expanded)-len(breaks),native_break_codes=[expanded[j] for j in breaks],native_field_final_cursor=width,native_field_second_line_column=1 if breaks else None,native_B2_glyphs_checked=len(expanded),field_tilemap_sha256=sha(w[:0x400]),B2_buffer_sha256=sha(buffer),matches_expected_glyphs=True))
q=dict(release='v0.75',ROM_sha256=sha(candidate),field_consumer='C3763A, actual JSL including C0315E/C031DB and C376F2',B2_consumer='C6FDF0, actual JSL including C0315E/C031DB and existing DTE dictionary',rows=rows,checked_SIDs=SIDS,natural_validation=False,limits='Private CPU redirection from camp. Dynamic SID branch09A7..09C9 and other natural menu paths not validated; no renderer code modified. Nine two-line inputs preserve their exact break bytes; original and new C3763A grid checked in full, with observed second-line column1 and final cursor last-line width+1. B2 buffer preserves the break byte; B2 dialogue semantics checked separately.')
(O/('qa-name-consumers'+a.report_suffix+'.json')).write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps(q))
