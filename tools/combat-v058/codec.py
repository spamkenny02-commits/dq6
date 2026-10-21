"""Strict candidate codec for the v0.56 battle byte pool; no ROM writer.
Read glyphs and dictionary from the supplied ROM. Reject unsupported accents,
shadow controls and unknown textual markup instead of silently dropping them.
This codec does not approve layouts, control semantics or an insertion.
"""
from pathlib import Path
import hashlib,struct,re,json,collections
BASELINE_SHA='e14ebc5611642b229edd3e7becae27813c823ef8182e2d06058953d593f2375d'
PTR=0x15ad1;BASE=0x36debd;LIMIT=0x37175b
# Deliberately no 00,0C..0F,82..9D,unknown glyphs, or dictionary codes.
SAFE=(1,*range(2,12),*range(0x10,0x2a),*range(0x42,0x5c),0x77,0x78,0x79,0x7a,0x7f,0x81,0x89,0x8b)
class CodecError(ValueError):pass
class BattleCodec:
 def __init__(self,rom,charset,check_hash=True):
  if check_hash and hashlib.sha256(rom).hexdigest()!=BASELINE_SHA:raise CodecError('Wrong baseline')
  self.rom=rom;self.glyphs=struct.unpack_from('<256H',rom,0x11100)
  self.chars={int(k,16):v for k,v in charset.items()};self.forward={}
  for b in SAFE:
   t=self.chars.get(self.glyphs[b]);
   if t is None or len(t)!=1:raise CodecError('Unknown safe glyph')
   if t in self.forward:raise CodecError('Ambiguous canonical glyph')
   self.forward[t]=b
  expected=" !,.?'-…*"+'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
  if set(self.forward)!=set(expected):raise CodecError('Unexpected baseline alphabet')
  first=int.from_bytes(rom[0x3fb25:0x3fb27],'little');at=int.from_bytes(rom[0x3fb30:0x3fb33],'little')&0x3fffff
  if first!=0xc9 or at!=0x3fb50:raise CodecError('Unexpected dictionary expander')
  self.dictionary={};i=0
  while rom[at+2*i]!=0xff:
   if first+i>255:raise CodecError('Dictionary overflow')
   pair=rom[at+2*i:at+2*i+2]
   if any(x>=0xab for x in pair):raise CodecError('Recursive/control dictionary entry')
   try:self.dictionary[first+i]=''.join(self.chars[self.glyphs[b]] for b in pair)
   except KeyError:raise CodecError('Unknown dictionary glyph')
   i+=1
 def encode(self,plan):
  out=bytearray();i=0
  while i<len(plan):
   if plan[i]=='{':
    m=re.match(r'\{([A-F0-9]{2})\}',plan[i:])
    if not m:raise CodecError('Malformed native tag')
    b=int(m[1],16)
    if not 0xab<=b<=0xc8:raise CodecError('Not a native control')
    out.append(b);i+=4
   else:
    if plan[i] not in self.forward:raise CodecError('Unsupported character U+%04X'%ord(plan[i]))
    out.append(self.forward[plan[i]]);i+=1
  if not out or out[-1] not in (0xac,0xae) or any(b in (0xac,0xae) for b in out[:-1]):raise CodecError('Invalid terminator boundary')
  return bytes(out)
 def decode(self,data):
  result=[]
  for b in data:
   if 0xab<=b<=0xc8:result.append('{%02X}'%b)
   elif b in self.dictionary:result.append(self.dictionary[b])
   elif b in SAFE:result.append(self.chars[self.glyphs[b]])
   else:raise CodecError('Unapproved byte %02X'%b)
  return ''.join(result)
def pool(rom):
 rows=[];ranges=[]
 for g in range(76):
  a=BASE+int.from_bytes(rom[PTR+3*g:PTR+3*g+3],'little');start=a
  if not BASE<=a<LIMIT:raise CodecError('Group outside protected battle region')
  for low in range(8):
   begin=a
   while a<LIMIT and rom[a] not in (0xac,0xae):a+=1
   if a>=LIMIT:raise CodecError('Unterminated battle group')
   a+=1;rows.append((g*8+low,begin,bytes(rom[begin:a])))
  if any(start<hi and a>lo for lo,hi in ranges):raise CodecError('Overlapping battle groups')
  ranges.append((start,a))
 return rows
def main_regions(rom):
 """Independently measure all870 live Huffman groups, including tail IDs."""
 root=int.from_bytes(rom[0x2bfb:0x2bfd],'little');n=root//2+1
 trees=[struct.unpack_from('<%dH'%n,rom,a) for a in (0x167be,0x1700e)];regions=[]
 for g in range(870):
  cpu=int.from_bytes(rom[0x15bb5+3*g:0x15bb8+3*g],'little');start=cpu&0x3fffff if cpu>=0xc00000 else cpu;pos=start;bit=7
  if not(0x37175b<=pos<0x3b8703 or 0x77175b<=pos<0x7b8703):raise CodecError('Main pointer outside reserved script regions')
  for low in range(8):
   for _ in range(20000):
    v=root|32768
    while v&32768:
     b=(rom[pos]>>bit)&1;bit-=1
     if bit<0:pos+=1;bit=7
     v=trees[b][(v&32767)//2]
    if (v&8191) in (0xac,0xae):break
   else:raise CodecError('Main Huffman message not terminated')
  regions.append(dict(group=g,file_offset=start,cpu_address=cpu,size=pos-start+(bit!=7)))
 return regions
def baseline_from_jp(jp,root):
 import importlib.util
 if hashlib.sha256(jp).hexdigest()!='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e':raise CodecError('Wrong intact JP source')
 spec=importlib.util.spec_from_file_location('bps58',root/'dq6-fr/upstream/refill/patchRM.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 rom=bytes(m.apply_bps(jp,(root/'patches/DQVI-FR-DS-v0.56-BASE-JP-PARTIEL.bps').read_bytes()))
 if hashlib.sha256(rom).hexdigest()!=BASELINE_SHA:raise CodecError('Wrong BPS output')
 return rom
