"""Sequential native-page diagnostics. Private fixtures and legacy-state font refresh.
A fresh-boot font-load check is required independently; this is not a natural battle.
"""
from pathlib import Path
import argparse,json,subprocess,sys,tempfile,hashlib,shutil
from common import O,R,c,read,sha,IDS
from native_font import MAP,FONT
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--runner',type=Path,required=True);p.add_argument('--camp',type=Path,required=True);p.add_argument('--ids');p.add_argument('--profile',choices=['duplicate','distinct'],default='duplicate');p.add_argument('--b3',type=int,default=1);p.add_argument('--b5',type=int,default=1);a=p.parse_args();rom=(a.out/'result.sfc').read_bytes();report=read(O/'build-report.json');assert sha(rom)==report['ROM_sha256']
regions=c.main_regions(rom)+[dict(file_offset=report['placement']['offset'],size=report['placement']['size'])]
runner=a.runner.resolve();src=runner.read_text();pos=src.index('if args.set_wram:')
src=src[:pos]+"\n# Diagnostic legacy-state font refresh only; no WRAM edits here.\nvp=core.retro_get_memory_data(3)\nfor byte in "+repr([b for b,g in MAP.values()])+":\n data=b[0x56b5c+16*byte:0x56b5c+16*byte+16];C.memmove(vp+0x6000+32*byte,data,16)\n"+src[pos:]
old="for action in actions:\n args.button=action.get('button','');args.press=action.get('press',4)\n for current in range(action.get('frames',30)):core.retro_run()"
new="""page_meta=[];last_key=None;saved_key=None;stable=0;frame_no=0;finished=False
for action in actions:
 args.button=action.get('button','');args.press=action.get('press',4)
 for current in range(action.get('frames',30)):
  core.retro_run();frame_no+=1
  w=C.string_at(core.retro_get_memory_data(2)+0x6f00,8);started=w[2:4]==bytes.fromhex('cdab');done=w[0:2]==bytes.fromhex('efbe')
  if started and frame is not None:
   key=frame[144:216].tobytes()
   stable=stable+1 if key==last_key else 0;last_key=key
   if stable==2 and key!=saved_key:
    saved_key=key;name=args.tag+'-page'+str(len(page_meta))+'.png';Image.fromarray(frame).resize((frame.shape[1]*3,frame.shape[0]*3),Image.Resampling.NEAREST).save(P/name)
    page_meta.append(dict(capture=name,returned=done,frame=frame_no))
   if done and stable>=3:finished=True;break
 if finished:break
(P/(args.tag+'-pages.json')).write_text(json.dumps(page_meta))"""
assert old in src;src=src.replace(old,new);results=[]
with tempfile.NamedTemporaryFile(dir=runner.parent,suffix='.py',mode='w') as helper:
 helper.write(src);helper.flush()
 for mid in ([int(x) for x in a.ids.split(',')] if a.ids else IDS):
  assert mid in IDS
  code=bytearray.fromhex('c230f47e7eababa2de04a90000');loop=len(code);code+=bytes.fromhex('9d3420caca10');code.append((loop-len(code)-1)&255)
  code+=bytes.fromhex('a901008d5f208d93208d4f208d8320a904008d89209c5525a901008d5925a9f1028d285a')
  if a.profile=='distinct':
   code=code.replace(bytes.fromhex('8d8320a904008d8920'),bytes.fromhex('a906008d83209c8920'))
  encoded=next(bytes.fromhex(r['encoded_hex']) for r in read(O/'insertion-combat.json') if r['id']==mid)
  if 0xb3 in encoded:code+=b'\xa9'+a.b3.to_bytes(2,'little')+bytes.fromhex('8d245a')
  if 0xb5 in encoded:code+=b'\xa9'+a.b5.to_bytes(2,'little')+bytes.fromhex('8d2a5a')
  if 0xbb in encoded:code+=bytes.fromhex('a9e7038d2e5a9c305a')
  code+=bytes.fromhex('a2000022d5b8c2988f046f7ea2010022d5b8c2988f066f7ea9')+bytes.fromhex('cdab8f026f7ea9')+mid.to_bytes(2,'little')+bytes.fromhex('22292ac0a9efbe8f006f7e80fe')
  off=next(x for x in range(0x771800,0x7b8703-len(code),256) if all(not(p['file_offset']<x+len(code) and p['file_offset']+p['size']>x) for p in regions));out=bytearray(rom);out[off:off+len(code)]=code

  for copy in (0,0x400000):
   assert out[copy+0x2ae2:copy+0x2ae6]==bytes.fromhex('c230f47e');out[copy+0x2ae2:copy+0x2ae6]=b'\x5c'+off.to_bytes(3,'little')
  tag=f'v06068-{mid}-b3-{a.b3}-b5-{a.b5}'+('-distinct' if a.profile=='distinct' else '');actions=[dict(button='a',frames=4,press=1),dict(frames=330),dict(button='a',frames=1,press=1),dict(frames=255,capture=True)]
  for _ in range(16):actions.extend([dict(button='a',frames=1,press=1),dict(frames=120,capture=True)])
  with tempfile.NamedTemporaryFile(dir=a.out,suffix='.sfc') as f:
   f.write(out);f.flush();subprocess.run([sys.executable,helper.name,'--rom',str(Path(f.name).resolve()),'--load-state',str(a.camp.resolve()),'--session',tag,'--tag',tag,'--sequence',json.dumps(actions)],check=True,capture_output=True,timeout=60)
  w=(runner.parent/'wram.bin').read_bytes();assert w[0x6f00:0x6f02]==bytes.fromhex('efbe'),f'API did not return:{tag}'
  assert w[0x6f04:0x6f08]==bytes.fromhex('f102f102' if a.profile=='duplicate' else 'f1024f02')
  pages=read(runner.parent/(tag+'-pages.json'));assert pages
  for row in pages:
   path=runner.parent/row['capture'];row['sha256']=sha(path.read_bytes());shutil.copyfile(path,a.out/path.name)
  results.append(dict(id=mid,fixture_sha256=sha(out),B3_value=a.b3,B5_value=a.b5,BB_value=999,actor_and_target_SID='02F1',profile=a.profile,homonym_ordinals=['A','B'] if a.profile=='duplicate' else [],pages=pages,API_returned=True,manual_visual_review=False))
  print(mid,len(pages),flush=True)
(O/f'qa-pages-b3-{a.b3}-b5-{a.b5}-{a.profile}.json').write_text(json.dumps(dict(release='v0.60',ROM_sha256=sha(rom),diagnostic_main_redirect=True,legacy_state_VRAM_font_refreshed_from_ROM=True,diagnostic_native_mode2_override=False,natural_battle=False,production_engine_unchanged=True,results=results),ensure_ascii=False,indent=2)+'\n')
