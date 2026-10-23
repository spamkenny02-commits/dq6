"""Private main-dialogue B2 diagnostic; five before/after pixel comparisons."""
from common import *
import argparse,subprocess,tempfile
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--runner',type=Path,required=True);p.add_argument('--camp',type=Path,required=True);a=p.parse_args();candidate=(a.out/'result.sfc').read_bytes();assert sha(candidate)==read(O/'build-report.json')['ROM_sha256'];m=module('bps65render',R/'dq6-fr/upstream/refill/patchRM.py');base=bytes(m.apply_bps(a.jp.read_bytes(),(R/'patches/DQVI-FR-DS-v0.64-BASE-JP-PARTIEL.bps').read_bytes()));assert sha(base)==BASE['ROM_sha256']
root=struct.unpack_from('<H',base,0x2bfb)[0];n=root//2+1;trees=[struct.unpack_from('<'+str(n)+'H',base,p) for p in [0x167be,0x1700e]];codes={}
def visit(node,bits):
 for bit in [0,1]:
  v=trees[bit][node//2]
  if v&32768:visit(v&32767,bits+[bit])
  else:codes.setdefault(v&8191,bits+[bit])
visit(root,[]);cpu=int.from_bytes(base[0x15bb5+36:0x15bb5+39],'little');pos=cpu&0x3fffff if cpu>=0xc00000 else cpu;bit=7;group=[]
for _ in range(8):
 ts=[]
 while True:
  v=root|32768
  while v&32768:
   b=(base[pos]>>bit)&1;bit-=1
   if bit<0:pos+=1;bit=7
   v=trees[b][(v&32767)//2]
  t=v&8191;ts.append(t)
  if t in [0xac,0xae]:break
 group.append(ts)
group[4]=[0xb2,0xad,0xb2,0xad,0xb2,0xac];bits=[b for ts in group for t in ts for b in codes[t]];blob=bytearray((len(bits)+7)//8)
for i,b in enumerate(bits):
 if b:blob[i//8]|=1<<(7-i%8)
regions=c.main_regions(candidate)+[dict(file_offset=BASE['placement']['offset'],size=BASE['placement']['size']),dict(file_offset=BASE['engine']['allocation']['offset'],size=BASE['engine']['allocation']['size'])];off=next(x for x in range(0x771800,0x7b8000,256) if all(not(p['file_offset']<x+len(blob) and p['file_offset']+p['size']>x) for p in regions));rows=[];shots=a.out/'render-names';shots.mkdir(exist_ok=True)
for sid in SIDS:
 images=[]
 for tag,rom in [('before',base),('after',candidate)]:
  fxt=bytearray(rom);fxt[off:off+len(blob)]=blob
  for copy in (0,0x400000):fxt[copy+0x15bb5+36:copy+0x15bb5+39]=off.to_bytes(3,'little')
  seq=[dict(button='a',frames=4,press=4),dict(frames=330),dict(button='down',frames=8,press=8),dict(frames=10),dict(button='a',frames=1,press=1),dict(frames=240)];name=f'v065-name-{sid:04x}-{tag}'
  with tempfile.NamedTemporaryFile(dir=a.out,suffix='.sfc') as f:
   f.write(fxt);f.flush();proc=subprocess.run([sys.executable,str(a.runner.resolve()),'--rom',str(Path(f.name).resolve()),'--load-state',str(a.camp.resolve()),'--session',name,'--tag',name,'--set-wram',json.dumps({'0x5a28':[sid&255,sid>>8]}),'--sequence',json.dumps(seq)],capture_output=True,timeout=90);assert proc.returncode==0,proc.stderr.decode()
  img=(a.runner.resolve().parent/(name+'.png')).read_bytes();(shots/(name+'.png')).write_bytes(img);images.append(img)
 assert images[0]==images[1],sid
 rows.append(dict(sid=sid,screenshot_sha256=sha(images[1]),before_after_pixels_identical=True))
q=dict(release='v0.65',ROM_sha256=sha(candidate),diagnostic_dialogues=10,changed_name_encodings_checked=5,B2_lookups_per_dialogue=3,rows=rows,natural_validation=False,limits='Three repeated main-dialogue B2 lookups per name at camp. No party recruitment, natural battle or native compact menu coverage. Visual review is recorded separately.');(O/'qa-name-render.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps(q))
