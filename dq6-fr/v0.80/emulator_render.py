"""Private camp redirections, never natural target scenes or release ROM writes."""
from common import *
import argparse,subprocess,math
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--runner',type=Path,required=True);p.add_argument('--camp',type=Path,required=True);p.add_argument('--ids',default=','.join(map(str,IDS)));p.add_argument('--one-page',action='store_true');p.add_argument('--before',type=Path);p.add_argument('--audit1179',action='store_true');a=p.parse_args();rom=a.before.read_bytes() if a.before else (a.out/'result.sfc').read_bytes();assert sha(rom)==(BASE['ROM_sha256'] if a.before else read(O/'build-report.json')['ROM_sha256']);rows={x['id']:x for x in read(O/'selection.json')};
if a.audit1179:
 assert not a.before and a.ids=='1179';q=next(x for x in previous.current_main_selection() if x['id']==1179);rows[1179]=dict(q,old_tokens=q['tokens'],pause_count=q['tokens'].count(0xaf))
msgs,regs=decode_main(rom);blocked=[(r['file_offset'],r['file_offset']+r['size']) for r in regs]+[(parent.NAME,parent.NAME_LIMIT),(BASE['placement']['offset'],BASE['placement']['offset']+BASE['placement']['size']),(BASE['engine']['allocation']['offset'],BASE['engine']['allocation']['offset']+BASE['engine']['allocation']['size'])];codes=codes_for(rom);captures=[]
for mid in map(int,a.ids.split(',')):
 group=[x[:] for x in msgs[96:104]];group[4]=rows[mid]['old_tokens' if a.before else 'tokens'][:];blob=pack_group(group,codes);at=next(x for x in range(0x771800,0x7b8703-len(blob),256) if x>>16==(x+len(blob)-1)>>16 and all(not(lo<x+len(blob) and hi>x) for lo,hi in blocked));fixture=bytearray(rom);fixture[at:at+len(blob)]=blob
 for copy in (0,0x400000):fixture[copy+0x15bb5+12*3:copy+0x15bb8+12*3]=at.to_bytes(3,'little')
 checksum=sum(fixture)&65535
 for copy in (0,0x400000):struct.pack_into('<HH',fixture,copy+0xffdc,checksum^65535,checksum)
 fixturepath=(a.out/('fixture-v080-'+str(mid)+'.sfc')).resolve();fixturepath.write_bytes(fixture);count=rows[mid]['pause_count']+1
 for page in range(1,(1 if a.one_page else count)+1):
  tag=f'v080-'+('before-' if a.before else '')+f'{mid}-page{page}';cmd=[sys.executable,str(a.runner.resolve()),'--rom',str(fixturepath),'--session',f'v080-render-'+('before-' if a.before else '')+str(mid),'--tag',tag]
  seq=[dict(button='a',frames=4,press=1),dict(frames=330),dict(frames=240)] if page==1 else [dict(button='a',frames=4,press=1),dict(frames=240)]
  if page==1:cmd+=['--load-state',str(a.camp.resolve())]
  cmd+=['--sequence',json.dumps(seq)];proc=subprocess.run(cmd,capture_output=True,text=True,timeout=90);assert proc.returncode==0,proc.stderr;info=json.loads(proc.stdout.splitlines()[0]);assert info['message_id']==100,(mid,page,info)
  screenshot=a.runner.resolve().parent/(tag+'.png');captures.append(dict(id=mid,page=page,page_count=count,screenshot_name=screenshot.name,screenshot_sha256=sha(screenshot.read_bytes()),fixture_sha256=sha(fixture),fixture_group12_offset=at,sequence=seq,observed_message_id=info['message_id'],diagnostic=True,WRAM_injected=False,VRAM_injected=False,natural_scene=False))
  print(mid,page,'of',count,flush=True)
 save('qa-render-1179-partial.json' if a.audit1179 else ('qa-render-before-partial.json' if a.before else 'qa-render-partial.json'),captures)
save('qa-render-1179.json' if a.audit1179 else ('qa-render-before.json' if a.before else 'qa-render.json'),dict(ROM_sha256=sha(rom),all_changed_dialogues_completed=not a.one_page and sorted(set(x['id'] for x in captures))==IDS,captures=captures,natural_scenes_executed=False,private_camp_from_new_game=True,main_name_observed='AAAAAAAA',release_ROM_unchanged=True));print('captures',len(captures))
