"""Seven explicit native accents in slots unused by every known byte-string pool.
This extends resident8x8 font and byte-to-main glyph mapping; no engine code edits.
Unknown hardcoded consumers remain part of the final resource audit.
"""
from pathlib import Path
import struct,hashlib,importlib.util,json
R=Path(__file__).resolve().parents[2]
s=importlib.util.spec_from_file_location('legacy58',R/'tools/combat-v058/codec.py');legacy=importlib.util.module_from_spec(s);s.loader.exec_module(legacy)
FONT=0x56b5c
MAP={'à':(0x2c,0x251),'é':(0x2d,0x254),'è':(0x30,0x256),'ê':(0x33,0x255),'î':(0x34,0x259),'â':(0x35,0x252),'û':(0x3a,0x25c)}
def usage(base,battle):
 used=set();names=[]
 for _,_,b in battle:used.update(b)
 for sid in range(2512):
  a=0x3b8703+int.from_bytes(base[0x165e7+3*(sid>>4):0x165ea+3*(sid>>4)],'little')
  for _ in range(sid&15):a=base.index(0xac,a)+1
  b=base[a:base.index(0xac,a)];used.update(b);names.append((a,b))
 assert len(set(a for a,b in names))==2048
 at=0x3fb50;entries=0
 while base[at]!=255:used.update(base[at:at+2]);at+=2;entries+=1
 assert entries==50
 return used,names

def apply(base,battle):
 used,names=usage(base,battle);assert not set(b for b,g in MAP.values())&used,'Accent slot already used by an old byte string'
 row=lambda byte:list(base[FONT+byte*16:FONT+byte*16+16:2])
 aa=row(0x42)[1:7];ee=row(0x46)[1:7];uu=row(0x56)[1:7]
 shapes={'à':[0x30,0x18]+aa,'é':[0x0c,0x18]+ee,'è':[0x30,0x18]+ee,'ê':[0x18,0x24]+ee,'î':[0x18,0x24,0,0x38,0x18,0x18,0x18,0x3c],'â':[0x18,0x24]+aa,'û':[0x18,0x24]+uu}
 out=bytearray(base)
 for ch,(byte,glyph) in MAP.items():
  assert struct.unpack_from('<H',base,0x11100+byte*2)[0]==0x200
  for copy in (0,0x400000):
   struct.pack_into('<H',out,copy+0x11100+byte*2,glyph)
   for y,b in enumerate(shapes[ch]):out[copy+FONT+byte*16+2*y]=b
 return bytes(out),dict(slots={ch:dict(byte=f'{b:02X}',main_glyph=f'{g:04X}',native_rows=shapes[ch]) for ch,(b,g) in MAP.items()},known_consumers_checked=dict(battle_messages=608,runtime_name_SIDs=2512,physical_names=2048,aliases=464,dictionary_pairs=50),all_allocated_slots_previously_unused=True,all_other_native_tiles_unchanged=True,engine_modified=False,scope_limit='Every known string pool checked; unknown hardcoded consumers remain in the final resource audit.')

class Codec(legacy.BattleCodec):
 def __init__(self,rom,charset):
  super().__init__(rom,charset,False)
  for ch,(b,g) in MAP.items():
   assert self.glyphs[b]==g
   self.forward[ch]=b
  self.extra={b:ch for ch,(b,g) in MAP.items()}
 def decode(self,data):
  return ''.join(self.extra[b] if b in self.extra else super(Codec,self).decode(bytes([b])) for b in data)
