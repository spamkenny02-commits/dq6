from pathlib import Path
import ctypes as C,argparse,json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;root=P.parents[1]
a=argparse.ArgumentParser();a.add_argument('--frames',type=int,default=300);a.add_argument('--button',default='');a.add_argument('--press',type=int,default=1);a.add_argument('--reset',action='store_true');a.add_argument('--tag',default='screen');a.add_argument('--check-layout',type=Path);a.add_argument('--load-state',type=Path);a.add_argument('--snapshot',action='store_true');a.add_argument('--sram',type=Path);a.add_argument('--sequence');a.add_argument('--rom',type=Path);a.add_argument('--session',default='session');a.add_argument('--set-wram',help='Diagnostic fixtures only: JSON map of byte offsets to byte arrays');args=a.parse_args()
core=C.CDLL(str(root/'emulator-snes9x/libretro/snes9x_libretro.so'));pix=0;frame=None;variables={};strings={};pad={'b':0,'y':1,'select':2,'start':3,'up':4,'down':5,'left':6,'right':7,'a':8,'x':9,'l':10,'r':11};current=0
class Var(C.Structure):_fields_=[('key',C.c_char_p),('value',C.c_char_p)]
@C.CFUNCTYPE(C.c_bool,C.c_uint,C.c_void_p)
def env(cmd,data):
 global pix
 if cmd==10:pix=C.cast(data,C.POINTER(C.c_int))[0];return pix in [0,1,2]
 if cmd==3:C.cast(data,C.POINTER(C.c_bool))[0]=True;return True
 if cmd in [9,31]:
  strings['dir']=str(P).encode();C.cast(data,C.POINTER(C.c_char_p))[0]=strings['dir'];return True
 if cmd==52:C.cast(data,C.POINTER(C.c_uint))[0]=0;return True
 if cmd==16:
  p=C.cast(data,C.POINTER(Var));i=0
  while p[i].key:
   desc=p[i].value.decode();variables[p[i].key.decode()]=desc.split(';',1)[-1].strip().split('|')[0].encode();i+=1
  return True
 if cmd==15:
  v=C.cast(data,C.POINTER(Var));k=v[0].key.decode()
  if k in variables:v[0].value=variables[k];return True
  return False
 if cmd==17:C.cast(data,C.POINTER(C.c_bool))[0]=False;return True
 if cmd==39:C.cast(data,C.POINTER(C.c_uint))[0]=1;return True
 if cmd==47:C.cast(data,C.POINTER(C.c_int))[0]=3;return True
 if cmd in [8,11,18,35,42,36]:return True
 return False
@C.CFUNCTYPE(None,C.c_void_p,C.c_uint,C.c_uint,C.c_size_t)
def video(data,w,h,pitch):
 global frame
 if not data or int(data)==-1:return
 typ=np.uint32 if pix==1 else np.uint16
 buf=C.string_at(data,pitch*h);raw=np.frombuffer(buf,dtype=typ).reshape(h,pitch//np.dtype(typ).itemsize)[:,:w].astype(np.uint32)
 if pix==1:rgb=np.stack(((raw>>16)&255,(raw>>8)&255,raw&255),axis=-1)
 elif pix==2:rgb=np.stack((((raw>>11)&31)*255//31,((raw>>5)&63)*255//63,(raw&31)*255//31),axis=-1)
 else:rgb=np.stack((((raw>>10)&31)*255//31,((raw>>5)&31)*255//31,(raw&31)*255//31),axis=-1)
 frame=rgb.astype(np.uint8)
@C.CFUNCTYPE(None,C.c_int16,C.c_int16)
def audio(a,b):pass
@C.CFUNCTYPE(C.c_size_t,C.POINTER(C.c_int16),C.c_size_t)
def batch(data,n):return n
@C.CFUNCTYPE(None)
def poll():pass
@C.CFUNCTYPE(C.c_int16,C.c_uint,C.c_uint,C.c_uint,C.c_uint)
def inp(port,device,index,id):return int(port==0 and current<args.press and args.button in pad and id==pad[args.button])
for name,fn in [('environment',env),('video_refresh',video),('audio_sample',audio),('audio_sample_batch',batch),('input_poll',poll),('input_state',inp)]:
 getattr(core,'retro_set_'+name).argtypes=[type(fn)];getattr(core,'retro_set_'+name)(fn)
core.retro_init();core.retro_set_controller_port_device(0,1)
core.retro_get_memory_data.argtypes=[C.c_uint];core.retro_get_memory_data.restype=C.c_void_p;core.retro_get_memory_size.argtypes=[C.c_uint];core.retro_get_memory_size.restype=C.c_size_t
class Game(C.Structure):_fields_=[('path',C.c_char_p),('data',C.c_void_p),('size',C.c_size_t),('meta',C.c_char_p)]
rompath=args.rom.resolve() if args.rom else root/'dq6-fr/v0.3/result.sfc';b=rompath.read_bytes();buf=C.create_string_buffer(b);g=Game(str(rompath).encode(),C.cast(buf,C.c_void_p),len(b),None)
core.retro_load_game.argtypes=[C.POINTER(Game)];core.retro_load_game.restype=C.c_bool;assert core.retro_load_game(C.byref(g))
if args.sram and args.sram.exists():
 saved=args.sram.read_bytes();assert len(saved)==core.retro_get_memory_size(0);C.memmove(core.retro_get_memory_data(0),saved,len(saved))
if args.check_layout:
 peek=core.retro_test_read_rom_byte;peek.argtypes=[C.c_uint];peek.restype=C.c_uint
 placements=json.loads(args.check_layout.read_text());checked=0
 for entry in placements:
  off=entry['file_offset'];cpu=entry['cpu_address'];size=entry['size']
  for i in range(size):assert peek(cpu+i)==b[off+i],(entry['group'],hex(cpu+i))
  checked+=size
 report=dict(groups_checked=len(placements),bytes_checked=checked,upper_groups=sum(e['file_offset']>=0x400000 for e in placements),all_rom_bus_reads_match=True)
 (P/'bus-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
core.retro_serialize_size.restype=C.c_size_t;state=P/(args.session+'.state')
core.retro_serialize.argtypes=[C.c_void_p,C.c_size_t];core.retro_unserialize.argtypes=[C.c_void_p,C.c_size_t];core.retro_unserialize.restype=C.c_bool
load_state=args.load_state or state
if load_state.exists() and (args.load_state or not args.reset):
 s=load_state.read_bytes();sb=C.create_string_buffer(s);assert core.retro_unserialize(sb,len(s))
if args.set_wram:
 wram_size=core.retro_get_memory_size(2);wram_pointer=core.retro_get_memory_data(2)
 for offset,values in json.loads(args.set_wram).items():
  start=int(offset,0);data=bytes(values);assert 0<=start and start+len(data)<=wram_size
  C.memmove(wram_pointer+start,data,len(data))
actions=json.loads(args.sequence) if args.sequence else [dict(button=args.button,frames=args.frames,press=args.press)]
for action in actions:
 args.button=action.get('button','');args.press=action.get('press',4)
 for current in range(action.get('frames',30)):core.retro_run()
n=core.retro_serialize_size();s=C.create_string_buffer(n);assert core.retro_serialize(s,n);state.write_bytes(s.raw)
if args.snapshot:(P/(args.tag+'.state')).write_bytes(s.raw)
if args.sram:args.sram.write_bytes(C.string_at(core.retro_get_memory_data(0),core.retro_get_memory_size(0)))
if frame is not None:Image.fromarray(frame).resize((frame.shape[1]*3,frame.shape[0]*3),Image.Resampling.NEAREST).save(P/(args.tag+'.png'))
core.retro_get_memory_data.argtypes=[C.c_uint];core.retro_get_memory_data.restype=C.c_void_p;core.retro_get_memory_size.argtypes=[C.c_uint];core.retro_get_memory_size.restype=C.c_size_t
wram=C.string_at(core.retro_get_memory_data(2),core.retro_get_memory_size(2));(P/'wram.bin').write_bytes(wram);print(json.dumps(dict(pixel_format=pix,screenshot=args.tag,message_id=int.from_bytes(wram[0x5998:0x599a],'little'),frame_mean=float(frame.mean()) if frame is not None else None)))
core.retro_unload_game();core.retro_deinit()
