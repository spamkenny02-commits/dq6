"""Three extra native 8x8 accents; isolated from released v060 font."""
from pathlib import Path
import importlib.util,struct
R=Path(__file__).resolve().parents[2]
s=importlib.util.spec_from_file_location('font60',R/'dq6-fr/v0.60/native_font.py');old=importlib.util.module_from_spec(s);s.loader.exec_module(old)
FONT=old.FONT
MAP={'ô':(0x3f,0x25a),'ç':(0x40,0x25f),'É':(0x41,0x260)}
SHAPES={'ô':[0x18,0x24,0x7c,0xc6,0xc6,0xc6,0xc6,0x7c],'ç':[0,0x7c,0xc6,0xc0,0xc0,0x7e,0x18,0x30],'É':[0x0c,0x18,0xfe,0xc0,0xfc,0xc0,0xc0,0xfe]}
def apply(base,battle,names):
 used=set(v for _,_,raw in battle for v in raw)
 used.update(v for _,raw in names for v in raw)
 used.update(base[0x3fb50:0x3fbb4])
 assert not set(b for b,g in MAP.values())&used,'Accent slot occupied in known pool'
 out=bytearray(base)
 for ch,(byte,glyph) in MAP.items():
  assert struct.unpack_from('<H',base,0x11100+byte*2)[0]==0x200,'Nonblank mapping'
  for copy in (0,0x400000):
   assert struct.unpack_from('<H',base,copy+0x11100+byte*2)[0]==0x200,'Nonblank mirror mapping'
   struct.pack_into('<H',out,copy+0x11100+byte*2,glyph)
   for y,b in enumerate(SHAPES[ch]):out[copy+FONT+byte*16+2*y]=b
 return bytes(out)
class Codec(old.Codec):
 def __init__(self,rom,charset):
  super().__init__(rom,charset)
  for ch,(b,g) in MAP.items():
   if self.glyphs[b]==g:self.forward[ch]=b;self.extra[b]=ch
