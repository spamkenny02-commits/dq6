"""Localized pair-name hook. Normal B2 and shared B3..B8 reader stay intact."""
import struct
class Asm:
 def __init__(self):self.b=bytearray();self.labels={};self.fix=[]
 def add(self,h):self.b+=bytes.fromhex(h);return self
 def long(self,op,at):self.b+=bytes([op])+at.to_bytes(3,'little');return self
 def label(self,n):self.labels[n]=len(self.b);return self
 def branch(self,op,n):self.b+=bytes([op,0]);self.fix.append((len(self.b)-1,n));return self
 def done(self):
  for p,n in self.fix:
   d=self.labels[n]-p-1;assert -128<=d<128;self.b[p]=d&255
  return bytes(self.b)
def apply(rom,off,names,codec):
 assert rom[0x69209:0x6920f]==bytes.fromhex('ad285a4cf0fd')
 assert rom[0x6fecf:0x70000]==bytes([255])*(0x70000-0x6fecf)
 assert rom[0x26759:0x2675d]==bytes.fromhex('22970ec0')
 from hashlib import sha256
 assert sha256(rom[0x26759:0x26796]).hexdigest()=='0de6d0ca4fc37db7bc2f451e9b786c0c9bdc6da0d9f8daced48f17c87ae6a773'
 table=off+0x180;strings=off+0x1b0;generation=off+0x100
 payload=bytearray();offsets=[]
 for text in names+['']:
  offsets.append(len(payload));payload+=codec.encode(text+'{AC}')
 assert len(payload)<0x250 and (off>>16)==((strings+len(payload))>>16)
 h=Asm().add('08ad285ac900ff').branch(0x90,'normal').add('c911ff').branch(0xb0,'normal')
 h.add('2829ff000aaa').long(0xbf,table).add('18').add('69'+(strings&65535).to_bytes(2,'little').hex()).add('85bae220a9'+bytes([strings>>16]).hex()+'85bcc2209cb459a00000a2ba00').long(0x5c,0xc6fe02)
 h.label('normal').add('28ad285a').long(0x5c,0xc6920c)
 handler=h.done();assert len(handler)<0x100
 g=Asm();rng=[]
 rng.append(generation+len(g.b));g.add('22970ec02903000aaada')
 g.add('a910ff8d285a22162ac0f101a301aa').long(0xbf,0xc26786).add('8d285a')
 rng.append(generation+len(g.b));g.add('22970ec0290300485aa3050a1863030900ff8d285aa3030aaaad285a22162ac0f2017a68fa0aaa').long(0xbf,0xc2678e).add('8d285a').long(0x5c,0xc26785)
 code=g.done();assert len(code)<0x80
 segments=[(off,handler),(generation,code),(table,b''.join(struct.pack('<H',n) for n in offsets)),(strings,bytes(payload))]
 # Production lower banks are mirrored; upper free data/code has no mirror.
 for at,old,new in [(0x69209,bytes.fromhex('ad285a'),bytes.fromhex('4cf0fe')),(0x6fef0,b'\xff'*4,b'\x5c'+off.to_bytes(3,'little')),(0x26759,bytes.fromhex('22970ec0'),b'\x5c'+generation.to_bytes(3,'little'))]:
  for copy in (0,0x400000):
   assert rom[copy+at:copy+at+len(old)]==old;segments.append((copy+at,new))
 out=bytearray(rom)
 for at,b in segments:out[at:at+len(b)]=b
 return out,dict(allocation=dict(offset=off,size=0x400),segments=[dict(offset=at,size=len(b),hex=b.hex()) for at,b in segments],RNG_call_offsets=rng,handler=off,generation=generation,table=table,strings=strings,virtual_SIDs=[f'{0xff00+i:04X}' for i in range(17)],names=names,normal_B2_entry_unchanged='C6920C',original_RTS_unchanged='C26785',new_WRAM_scratch=False)
