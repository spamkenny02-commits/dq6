"""Read every table-bound SID through C0315E/C031DB, with actual CPU bytes.
35 dynamic SIDs09A7..09C9 deliberately excluded from pointer equivalence.
"""
from common import *
import argparse,tempfile,subprocess
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--runner',type=Path,required=True);p.add_argument('--camp',type=Path,required=True);p.add_argument('--mutate-pointer',action='store_true');a=p.parse_args();rom=(a.out/'result.sfc').read_bytes();r=read(O/'build-report.json');assert sha(rom)==r['ROM_sha256']
regions=c.main_regions(rom)+[dict(file_offset=BASE['placement']['offset'],size=BASE['placement']['size']),dict(file_offset=BASE['engine']['allocation']['offset'],size=BASE['engine']['allocation']['size'])]
code=bytearray.fromhex('78c230f47e7eabab64106412');labels={};fix=[]
def emit(h):code.extend(bytes.fromhex(h))
def label(s):labels[s]=len(code)
def branch(op,target,n=1):
 emit(op);fix.append((len(code),target,n));code.extend(bytes(n))
label('sid');emit('a51285146416a510c9a709');branch('90','normal');emit('c9ca09');branch('b0','normal');emit('a5100a0a0aaaa9ffff9f00007f9f02007f');branch('80','record')
label('normal');emit('a510a28000225e31c0a5100a0a0aaaa5809f00007fa58229ff009f02007f')
label('read');emit('a2800022db31c0a612e2209f00607fc220e612e616c9ac00');branch('f0','record');emit('a516c90001');branch('b0','overflow');branch('80','read')
label('record');emit('a5100a0a0aaaa5169f04007fa5149f06007fe610a510c9d009');branch('b0','done');branch('82','sid',2)
label('overflow');emit('a9adde8f006f7e80fe')
label('done');emit('a9efbe8f006f7e80fe')
for at,target,n in fix:
 v=labels[target]-(at+n);assert -(1<<(n*8-1))<=v<(1<<(n*8-1));code[at:at+n]=(v&((1<<(n*8))-1)).to_bytes(n,'little')
off=next(x for x in range(0x771800,0x7b8000,256) if all(not(p['file_offset']<x+len(code) and p['file_offset']+p['size']>x) for p in regions));out=bytearray(rom);out[off:off+len(code)]=code
for copy in (0,0x400000):
 assert out[copy+0x2ae2:copy+0x2ae6]==bytes.fromhex('c230f47e');out[copy+0x2ae2:copy+0x2ae6]=b'\x5c'+off.to_bytes(3,'little')
 if a.mutate_pointer:
  at=copy+0x165e7+3;out[at:at+3]=(int.from_bytes(out[at:at+3],'little')+1).to_bytes(3,'little')
tag='v066-names-reader'+('-negative' if a.mutate_pointer else '')
with tempfile.NamedTemporaryFile(dir=a.out,suffix='.sfc') as f:
 f.write(out);f.flush();proc=subprocess.run([sys.executable,str(a.runner.resolve()),'--rom',str(Path(f.name).resolve()),'--load-state',str(a.camp.resolve()),'--session',tag,'--tag',tag,'--sequence',json.dumps([dict(button='a',frames=4,press=1),dict(frames=330),dict(button='a',frames=1,press=1),dict(frames=1200)])],capture_output=True,timeout=90);assert proc.returncode==0,proc.stderr.decode()
w=(a.runner.resolve().parent/'wram.bin').read_bytes();assert w[0x6f00:0x6f02]==bytes.fromhex('efbe'),w[0x6f00:0x6f02].hex();ns=names(rom);errors=[];metadata=[];stream=bytearray();excluded=[]
for sid,(at,b) in enumerate(ns):
 p=0x10000+sid*8;ptr=int.from_bytes(w[p:p+3],'little');size=int.from_bytes(w[p+4:p+6],'little');start=int.from_bytes(w[p+6:p+8],'little')
 if 0x9a7<=sid<0x9ca:assert w[p:p+4]==bytes.fromhex('ffffffff') and size==0;excluded.append(sid);continue
 assert size<256 and start+size<=0xa000;raw=w[0x16000+start:0x16000+start+size];stream+=raw
 if ptr!=0xc00000+at or raw!=b:errors.append(sid)
 metadata.append(dict(sid=sid,cpu_pointer=ptr,size=size,stream_start=start,sha256=sha(raw)))
assert errors==([16] if a.mutate_pointer else []);assert len(metadata)==2477 and len(excluded)==35
q=dict(release='v0.66',ROM_sha256=sha(rom),native_initializer='C0315E',native_raw_reader='C031DB',table_bound_SIDs_checked=2477,full_raw_bytes_checked=len(stream),actual_stream_sha256=sha(stream),actual_pointer_length_byte_metadata_sha256=sha(json.dumps(metadata,sort_keys=True).encode()),dynamic_SIDs_excluded=excluded,dynamic_initializer='C44FDF branch for09A7..09C9; no claim of table-pointer equivalence',fixture_sha256=sha(out),deliberate_pointer_mutation=a.mutate_pointer,errors=errors,expected_result_observed=True,natural_validation=False)
(O/('qa-names-native-negative.json' if a.mutate_pointer else 'qa-names-native-reader.json')).write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps(q))
