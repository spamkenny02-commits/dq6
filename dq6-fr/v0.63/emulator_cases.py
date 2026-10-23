"""Private, sequential camp redirects; forced RNG only in diagnostic fixtures."""
from common import *
import argparse,subprocess,tempfile,shutil
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--runner',type=Path,required=True);p.add_argument('--camp',type=Path,required=True);p.add_argument('--cases',default='pair0-0');p.add_argument('--duplicate',action='store_true');a=p.parse_args();rom=(a.out/'result.sfc').read_bytes();report=read(O/'build-report.json');assert sha(rom)==report['ROM_sha256']
runner=a.runner.resolve();src=runner.read_text();pos=src.index('if args.set_wram:');src=src[:pos]+"\nvp=core.retro_get_memory_data(3)\nfor byte in [44,45,48,51,52,53,58]:\n data=b[0x56b5c+16*byte:0x56b5c+16*byte+16];C.memmove(vp+0x6000+32*byte,data,16)\n"+src[pos:]
old="for action in actions:\n args.button=action.get('button','');args.press=action.get('press',4)\n for current in range(action.get('frames',30)):core.retro_run()"
new="""page_meta=[];last_key=None;saved_key=None;stable=0;frame_no=0;finished=False
for action in actions:
 args.button=action.get('button','');args.press=action.get('press',4)
 for current in range(action.get('frames',30)):
  core.retro_run();frame_no+=1
  w=C.string_at(core.retro_get_memory_data(2)+0x6f00,8);started=w[2:4]==bytes.fromhex('cdab');done=w[0:2]==bytes.fromhex('efbe')
  if started and frame is not None:
   key=frame[144:216].tobytes();stable=stable+1 if key==last_key else 0;last_key=key
   if stable==2 and key!=saved_key:
    saved_key=key;name=args.tag+'-page'+str(len(page_meta))+'.png';Image.fromarray(frame).resize((frame.shape[1]*3,frame.shape[0]*3),Image.Resampling.NEAREST).save(P/name);page_meta.append(dict(capture=name,returned=done,frame=frame_no))
   if done and stable>=3:finished=True;break
 if finished:break
(P/(args.tag+'-pages.json')).write_text(json.dumps(page_meta))"""
assert old in src;src=src.replace(old,new)
regions=c.main_regions(rom)+[dict(file_offset=report['placement']['offset'],size=report['placement']['size']),dict(file_offset=report['engine']['allocation']['offset'],size=0x400)]
free=next(x for x in range(0x771800,0x7b8000,256) if all(not(p['file_offset']<x+0x300 and p['file_offset']+p['size']>x) for p in regions));results=[]
with tempfile.NamedTemporaryFile(dir=runner.parent,suffix='.py',mode='w') as helper:
 helper.write(src);helper.flush()
 for case in a.cases.split(','):
  out=bytearray(rom);code=bytearray.fromhex('c230f47e7eababa2de04a90000');loop=len(code);code+=bytes.fromhex('9d3420caca10');code.append((loop-len(code)-1)&255)
  code+=bytes.fromhex('a901008d5f208d93208d4f20a906008d83209c89209c5525a901008d5925a9cdab8f026f7e')
  if a.duplicate:code=code.replace(bytes.fromhex('a906008d83209c8920'),bytes.fromhex('a901008d8320a904008d8920'))
  diag=[]
  if case.startswith('pair') or case=='random':
   i,j=map(int,case[4:].split('-')) if case!='random' else (0,0);code+=bytes.fromhex('a9f00122292ac0a03412225967c2')
   for copy in (0,0x400000):assert out[copy+0x26785]==0x60;out[copy+0x26785]=0x6b
   for n,value in enumerate((i,j) if case!='random' else ()):
    stub=free+0x200+n*8;out[stub:stub+4]=b'\xa9'+value.to_bytes(2,'little')+b'\x6b';rng=report['engine']['RNG_call_offsets'][n];out[rng:rng+4]=b'\x22'+stub.to_bytes(3,'little')
   diag=['Caller RTS becomes RTL for the private JSL harness']+(['Both RNG calls replaced by deterministic LDA/RTL stubs'] if case!='random' else ['Original RNG calls left intact'])
  elif case.startswith('word'):
   i=int(case[4:]);code+=bytes.fromhex('a9d00122292ac0229667c2')
   for copy in (0,0x400000):assert out[copy+0x267ac]==0x60;out[copy+0x267ac]=0x6b;out[copy+0x26796:copy+0x2679a]=b'\x22'+(free+0x200).to_bytes(3,'little')
   out[free+0x200:free+0x204]=b'\xa9'+i.to_bytes(2,'little')+b'\x6b';diag=['Caller RTS becomes RTL for private JSL harness','RNG forced to one of all four native word choices']
  elif case.startswith('normal'):
   sid=int(case[6:],16);code+=b'\xa9'+sid.to_bytes(2,'little')+bytes.fromhex('8d285aa9b00122292ac0') # reviewed432 with ordinary B2
  else:raise ValueError(case)
  code+=bytes.fromhex('8f086f7e8a8f0a6f7e988f0c6f7ead285a8f0e6f7ea9efbe8f006f7e80fe');assert len(code)<0x200
  out[free:free+len(code)]=code
  for copy in (0,0x400000):assert out[copy+0x2ae2:copy+0x2ae6]==bytes.fromhex('c230f47e');out[copy+0x2ae2:copy+0x2ae6]=b'\x5c'+free.to_bytes(3,'little')
  tag='v063-'+case+('-duplicate' if a.duplicate else '');actions=[dict(button='a',frames=4,press=1),dict(frames=330),dict(button='a',frames=1,press=1),dict(frames=255)]
  for _ in range(22):actions.extend([dict(button='a',frames=1,press=1),dict(frames=120)])
  with tempfile.NamedTemporaryFile(dir=a.out,suffix='.sfc') as f:
   f.write(out);f.flush();proc=subprocess.run([sys.executable,helper.name,'--rom',str(Path(f.name).resolve()),'--load-state',str(a.camp.resolve()),'--session',tag,'--tag',tag,'--sequence',json.dumps(actions)],capture_output=True,timeout=90)
   assert proc.returncode==0,proc.stderr.decode()
  w=(runner.parent/'wram.bin').read_bytes();returned=w[0x6f00:0x6f02]==bytes.fromhex('efbe');values=[int.from_bytes(w[x:x+2],'little') for x in (0x6f08,0x6f0a,0x6f0c,0x6f0e)]
  pages=read(runner.parent/(tag+'-pages.json'))
  for row in pages:
   path=runner.parent/row['capture'];row['sha256']=sha(path.read_bytes());shutil.copyfile(path,a.out/path.name)
  result=dict(case=case,duplicate=a.duplicate,API_returned=returned,returned_A_X_Y_B2=values,fixture_sha256=sha(out),private_changes=diag,pages=pages,manual_visual_review=False)
  results.append(result);(O/('qa-'+case+('-duplicate' if a.duplicate else '')+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(case,returned,values,len(pages),flush=True)
  if not returned:raise AssertionError('Diagnostic did not return')
