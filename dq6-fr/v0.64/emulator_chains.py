from common import *
import argparse,subprocess,tempfile,shutil
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--runner',type=Path,required=True);p.add_argument('--camp',type=Path,required=True);a=p.parse_args();rom=(a.out/'result.sfc').read_bytes();report=read(O/'build-report.json');assert sha(rom)==report['ROM_sha256']
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
regions=c.main_regions(rom)+[dict(file_offset=report['placement']['offset'],size=report['placement']['size']),dict(file_offset=report['engine']['allocation']['offset'],size=report['engine']['allocation']['size'])]
free=next(x for x in range(0x771800,0x7b8000,256) if all(not(p['file_offset']<x+0x300 and p['file_offset']+p['size']>x) for p in regions));cases=[]
for value in [0,1,2,999,65536,16777215]:
 for multi in [False,True]:cases.append(dict(name=f'xp-{value}-'+('multi' if multi else 'solo'),kind='xp',value=value,multi=multi))
for values in [[1,2,3,4,5],[9,10,11,12,13],[99,98,97,96,95],[255,254,253,252,251]]:
 for selector in [1,2]:cases.append(dict(name=f'stats-{values[0]}-b3-{selector}',kind='stats',values=values,selector=selector))
for selector in [1,2]:
 for class_sid,rank_sid in [(0x8f0,0x397),(0x8f6,0x3dc)]:cases.append(dict(name=f'rank-{class_sid:x}-{rank_sid:x}-b3-{selector}',kind='rank',class_sid=class_sid,rank_sid=rank_sid,selector=selector))
results=[]
with tempfile.NamedTemporaryFile(dir=runner.parent,suffix='.py',mode='w') as helper:
 helper.write(src);helper.flush()
 for case in cases:
  out=bytearray(rom);code=bytearray.fromhex('c230f47e7eababa9cdab8f026f7e')
  def set16(at,value):return b'\xa9'+value.to_bytes(2,'little')+b'\x8d'+at.to_bytes(2,'little')
  changed=[]
  if case['kind']=='xp':
   value=case['value'];code+=set16(0x254d,value&65535)+set16(0x254f,value>>16)+bytes.fromhex('a9010022292ac0228f26c022')+(0xc2af26 if case['multi'] else 0xc2af2c).to_bytes(3,'little');changed=[(0x2af3e,0x60,0x6b)]
  elif case['kind']=='stats':
   code+=set16(0x5a24,case['selector'])+bytes.fromhex('9c305a9c6548')
   for at,value in zip([0x485b,0x485f,0x4861,0x485d,0x4863],case['values']):code+=set16(at,value)
   code+=bytes.fromhex('a93b0022292ac02206b0c2');changed=[(0x2b057,0x60,0x6b)]
  else:
   code+=set16(0x5a24,case['selector'])+set16(0x5a28,case['class_sid'])+set16(0x4877,case['rank_sid'])+bytes.fromhex('a9010022292ac022dcB2c2');changed=[(0x2b2ee,0x20,0x6b)]
  for at,old,new in changed:
   for copy in [0,0x400000]:assert out[copy+at]==old;out[copy+at]=new
  code+=bytes.fromhex('ad2e5a8f106f7ead305a8f126f7ead285a8f146f7ea9efbe8f006f7e80fe');out[free:free+len(code)]=code
  for copy in [0,0x400000]:assert out[copy+0x2ae2:copy+0x2ae6]==bytes.fromhex('c230f47e');out[copy+0x2ae2:copy+0x2ae6]=b'\x5c'+free.to_bytes(3,'little')
  tag='v064-'+case['name'];actions=[dict(button='a',frames=4,press=1),dict(frames=330),dict(button='a',frames=1,press=1),dict(frames=255)]
  for _ in range(26):actions.extend([dict(button='a',frames=1,press=1),dict(frames=120)])
  with tempfile.NamedTemporaryFile(dir=a.out,suffix='.sfc') as f:
   f.write(out);f.flush();proc=subprocess.run([sys.executable,helper.name,'--rom',str(Path(f.name).resolve()),'--load-state',str(a.camp.resolve()),'--session',tag,'--tag',tag,'--sequence',json.dumps(actions)],capture_output=True,timeout=90);assert proc.returncode==0,proc.stderr.decode()
  w=(runner.parent/'wram.bin').read_bytes();assert w[0x6f00:0x6f02]==bytes.fromhex('efbe'),case
  bb=int.from_bytes(w[0x6f10:0x6f13],'little');b2=int.from_bytes(w[0x6f14:0x6f16],'little')
  if case['kind']=='xp':assert bb==case['value']
  if case['kind']=='stats':assert bb==case['values'][-1]
  if case['kind']=='rank':assert b2==case['rank_sid']
  pages=read(runner.parent/(tag+'-pages.json'));assert pages
  for row in pages:
   path=runner.parent/row['capture'];row['sha256']=sha(path.read_bytes());shutil.copyfile(path,a.out/path.name)
  results.append(dict(case=case,private_caller_RTS_or_next_instruction_to_RTL=changed,fixture_sha256=sha(out),API_returned=True,BB_after=bb,B2_after=b2,pages=pages,manual_visual_review=False));print(case['name'],len(pages),flush=True)
(O/'qa-chains.json').write_text(json.dumps(dict(release='v0.64',ROM_sha256=sha(rom),results=results,original_inline_native_calls_executed=True,diagnostic_redirect=True,legacy_state_font_refresh=True,natural_battle=False),ensure_ascii=False,indent=2)+'\n')
