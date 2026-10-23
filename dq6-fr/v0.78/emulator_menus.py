"""Actual field menu inputs plus explicit, private item-name binding fixtures.
No claim of obtaining every item or testing every shop/equipment context.
"""
from common import *
import argparse,subprocess,tempfile,shutil
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--runner',type=Path,required=True);p.add_argument('--field-state',type=Path,required=True);a=p.parse_args();rom=(a.out/'result.sfc').read_bytes();assert sha(rom)==read(O/'build-report.json')['ROM_sha256'];runner=a.runner.resolve();shots=a.out/'native-menus';shots.mkdir(exist_ok=True)
def run(data,tag,seq):
 with tempfile.NamedTemporaryFile(dir=a.out,suffix='.sfc') as f:
  f.write(data);f.flush();proc=subprocess.run([sys.executable,str(runner),'--rom',str(Path(f.name).resolve()),'--load-state',str(a.field_state.resolve()),'--session',tag,'--tag',tag,'--sequence',json.dumps(seq)],capture_output=True,timeout=90);assert proc.returncode==0,proc.stderr.decode()
 img=(runner.parent/(tag+'.png')).read_bytes();(shots/(tag+'.png')).write_bytes(img);return (runner.parent/'wram.bin').read_bytes(),sha(img)
def words(w,row,col,n):return [int.from_bytes(w[0x3068+2*(32*row+col+i):0x306a+2*(32*row+col+i)],'little')&0x3ff for i in range(n)]
mainseq=[dict(button='a',frames=1,press=1),dict(frames=120)];main=[]
for negative in [False,True]:
 data=bytearray(rom)
 if negative:
  for copy in (0,0x400000):data[copy+WINDOW+2]=16
 w,im=run(data,'v078-main-'+('negative' if negative else 'positive'),mainseq);violations=[];rows=[]
 for x in SELECTION:
  if x['kind']!='main_menu':continue
  sid=x['sids'][0];row=3+2*((sid-150)//2);col=4 if sid%2==0 else 13;bs=expand(rom,names(rom)[sid][1])[:-1];assert words(w,row,col,len(bs))==[0x300+b for b in bs]
  width=data[WINDOW+2]
  if col+len(bs)>2+width-1:violations.append(sid)
  rows.append(dict(sid=sid,row=row,column=col,expanded_glyphs=len(bs)))
 assert bool(violations)==negative
 main.append(dict(deliberate_old_width_mutation=negative,width_tiles=data[WINDOW+2],bounds_violations=violations,rows=rows,screenshot_sha256=im))
items=[x for x in SELECTION if x['kind']=='item'];results=[];ns=names(rom)
regions=c.main_regions(rom)+[dict(file_offset=NAME,size=NAME_LIMIT-NAME),dict(file_offset=BASE['placement']['offset'],size=BASE['placement']['size']),dict(file_offset=BASE['engine']['allocation']['offset'],size=BASE['engine']['allocation']['size'])]
# Execute the unchanged native menu printer with one diagnostic SID substitution.
original=rom[0x3763a:0x37642];assert original==bytes.fromhex('08c230f47e7eabab')
off=next(i for i in range(0x771800,0x7b8000,256) if all(not(z['file_offset']<i+64 and z['file_offset']+z['size']>i) for z in regions))
for x in items:
 sid=x['sids'][0];code=bytes.fromhex('08c230c91408d003a9')+sid.to_bytes(2,'little')+bytes.fromhex('28')+original+bytes.fromhex('5c4276c3');fixture=bytearray(rom);fixture[off:off+len(code)]=code
 for copy in (0,0x400000):fixture[copy+0x3763a:copy+0x3763e]=b'\x5c'+off.to_bytes(3,'little')
 expanded=expand(rom,ns[sid][1])[:-1];breaks=[i for i,v in enumerate(expanded) if 0x91<=v<=0x9d];assert len(breaks)<=1
 first=expanded[:breaks[0]] if breaks else expanded;second=expanded[breaks[0]+1:] if breaks else b'';assert len(first)<=12 and len(second)<=11
 for kind in ['inventory','equipment']:
  seq=list(mainseq)
  if kind=='inventory':seq +=[dict(button='down',frames=1,press=1),dict(frames=20),dict(button='a',frames=1,press=1),dict(frames=180)]
  else:
   for button in ['down','down','right','a','a']:seq +=[dict(button=button,frames=1,press=1),dict(frames=40)]
   seq +=[dict(frames=140)]
  w,im=run(fixture,f'v078-{kind}-{sid}',seq)
  row,col=(2,12) if kind=='inventory' else (2,3)
  assert words(w,row,col,len(first))==[0x300+b for b in first],(kind,sid,'first')
  if second:assert words(w,row+1,col+1,len(second))==[0x300+b for b in second],(kind,sid,'second')
  if kind=='equipment':
   assert words(w,4,18,len(first))==[0x300+b for b in first],(kind,sid,'selector first')
   if second:assert words(w,5,19,len(second))==[0x300+b for b in second],(kind,sid,'selector second')
  results.append(dict(sid=sid,position=x['position'],view=kind,first_line_glyphs=len(first),second_line_glyphs=len(second),full_text_tile_words_match=True,screenshot_sha256=im,private_fixture_SHA256=sha(fixture)))
q=dict(release='v0.78',ROM_sha256=sha(rom),initial_private_field_state_sha256=sha(a.field_state.read_bytes()),main_menu_natural_inputs=main,item_names_diagnostic_binding=True,item_name_SIDs=len(items),item_views=len(results),results=results,production_engine_modified=False,main_window8_width_change=dict(offset=WINDOW+2,before=16,after=20,copies=2),limits='Main menu opened through ordinary inputs from field state reached by prologue inputs. Each item name substituted for Cypress Stick in a private printer hook; actual inventory,equipment header and weapon selector rendered and tile words checked. Does not prove acquiring all items,other shops,item effects,all classes/genders or all natural paths.')
(O/'qa-native-menus.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(len(items),'items,',len(results),'views;positive main menu and old-width negative passed')
