"""Read resident font tiles in a private field-state diagnostic, not a battle proof."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,subprocess,sys,tempfile
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parents[2]
s=importlib.util.spec_from_file_location('codec58',r/'tools/combat-v058/codec.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
a=argparse.ArgumentParser();a.add_argument('--jp',type=Path,required=True);a.add_argument('--camp',type=Path,required=True);a.add_argument('--runner',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--advance-intro',action='store_true');a=a.parse_args()
a.out.mkdir(parents=True,exist_ok=True);rom=c.baseline_from_jp(a.jp.read_bytes(),r)
runner=a.runner.resolve();src=runner.read_text();assert src.count("wram=C.string_at")==1
src=src.replace("wram=C.string_at","vram=C.string_at(core.retro_get_memory_data(3),core.retro_get_memory_size(3));(P/'resident60-private-vram.bin').write_bytes(vram)\nwram=C.string_at")
with tempfile.NamedTemporaryFile(dir=runner.parent,suffix='.py',mode='w') as helper,tempfile.NamedTemporaryFile(dir=a.out,suffix='.sfc') as f:
 helper.write(src);helper.flush();f.write(rom);f.flush()
 subprocess.run([sys.executable,helper.name,'--rom',str(Path(f.name).resolve()),'--load-state',str(a.camp.resolve()),'--sequence',json.dumps(([{'button':'a','frames':240,'press':1}]*60) if a.advance_intro else [{'button':'a','frames':4,'press':1},{'frames':330},{'button':'a','frames':4,'press':1},{'frames':330}]),'--tag','resident60-private','--session','resident60-private'],check=True,capture_output=True)
vram=(runner.parent/'resident60-private-vram.bin').read_bytes();assert len(vram)==65536
font=vram[0x6000:0x8000];canvas=Image.new('RGB',(16*48,16*48),(45,45,45));draw=ImageDraw.Draw(canvas)
for b in range(256):
 tile=font[b*32:(b+1)*32];x=(b%16)*48;y=(b//16)*48;draw.text((x,y),f'{b:02X}',fill='yellow')
 for row in range(8):
  for col in range(8):
   v=sum(((tile[row*2+(plane%2)+(plane//2)*16]>>(7-col))&1)<<plane for plane in range(4))
   if v&1:draw.rectangle((x+col*4,y+12+row*4,x+col*4+3,y+15+row*4),fill='white')
canvas.save(a.out/'resident60-private-atlas.png')
report={'ROM_release':'v0.56','context':('camp then 60 A presses spaced240 frames' if a.advance_intro else 'supplied field state, A + wait330 + A + wait330'),'vram_size':len(vram),'tile_byte_base':'6000','tile_count':256,'planes':4,'visual_mask':'plane0 only; planes1..3 are filled palette background in this field state','resident_font_sha256':hashlib.sha256(font).hexdigest(),'initial_state_sha256':hashlib.sha256(a.camp.read_bytes()).hexdigest(),'nonempty_plane0_tile_indices':[b for b in range(256) if any(font[b*32:b*32+16:2])],'battle_font_loaded':False,'native_render_approved':False,'new_inserted':0}
(a.out/'resident60-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
