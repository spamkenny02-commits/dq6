"""Update companion default names from the supplied DS French name list.
Preserve every other byte string and rebuild the existing groups-of-16 pointers.
"""
import struct,re,json
from pathlib import Path
START=0x3b8703;END=0x3bc712;TABLE=0x165e7;GROUPS=157

def encode(s):
 # Naming on the SFC uses its byte alphabet, which lacks a capital É.
 s=s.replace('É','E')
 return bytes(0x10+ord(c)-65 if 'A'<=c<='Z' else 0x42+ord(c)-97 if 'a'<=c<='z' else 1 if c==' ' else 255 for c in s)

def parse(rom):
 entries=[];starts=[];start=START
 for pos in range(START,END):
  if rom[pos]==0xac:entries.append(bytes(rom[start:pos]));starts.append(start);start=pos+1
 byoffset={a:i for i,a in enumerate(starts)};groups=[]
 for g in range(GROUPS):
  e=int.from_bytes(rom[TABLE+3*g:TABLE+3*g+3],'little');address=START+e
  assert address in byoffset;groups.append(byoffset[address])
 return entries,groups,max(groups)+16

def apply(rom,root):
 original=bytes(rom);entries,groups,reachable=parse(original)
 fr=json.loads((root/'clean-base/ds-fr.json').read_text());names={r['id']:re.search(r'@1([^@]+)',r['text']).group(1) for r in fr if r['file']=='data/MENULIST6/FR/b1001000.mpt' and r['id'] in [1,2,3,4,5,6]}
 expected={0x905:('Hassan',1),0x906:('Muriel',2),0x907:('Chamoro',3),0x908:('Barbara',4),0x909:('Terry',5),0x30d:('Terry',5)}
 changed={};metadata=[]
 for sid,(old,dsid) in expected.items():
  pos=groups[sid>>4]+(sid&15)
  # The NPC Terry entry uses the existing 'er' digraph; other defaults are literal.
  wanted=bytes.fromhex('23da535a') if sid==0x30d else encode(old)
  assert entries[pos]==wanted,(sid,entries[pos].hex())
  new=encode(names[dsid]);assert 255 not in new and len(names[dsid])<=8
  changed[pos]=new;metadata.append(dict(sfc_id=sid,position=pos,old=old,ds_id=dsid,ds_name=names[dsid],sfc_name=names[dsid].replace('É','E')))
 # Remove only the legacy translation credit string at SID 009C.
 # All its aliases are checked by the independent release verification.
 assert groups[0x9c>>4]+(0x9c&15)==156
 assert entries[156]==bytes.fromhex('25da544aea0147ef4f4442e0d685011f545949cd4cda0188011057464401e201f456554a464fcad68501010101010101010101010123da4edffa0123ef455644554aea')
 changed[156]=b''
 # The engine appends the slot number to SID 00E7.
 assert groups[0xe7>>4]+(0xe7&15)==231
 assert entries[231]==bytes.fromhex('224256574648d045d64b4656')
 changed[231]=encode('Journal')
 assert groups[0xe9>>4]+(0xe9&15)==233
 assert entries[233]==bytes.fromhex('1249cf48da011fd0ce4655f054')
 changed[233]=encode('Options')
 source_end=START+sum(len(e)+1 for e in entries[:reachable]);tail=original[source_end:END];packed=bytearray();starts=[]
 for pos,e in enumerate(entries[:reachable]):
  starts.append(START+len(packed));packed+=changed.get(pos,e)+b'\xac'
 assert START+len(packed)+len(tail)<=END
 rom[START:START+len(packed)]=packed;rom[START+len(packed):START+len(packed)+len(tail)]=tail
 if START+len(packed)+len(tail)<END:rom[START+len(packed)+len(tail):END]=b'\xff'*(END-START-len(packed)-len(tail))
 for g,position in enumerate(groups):rom[TABLE+g*3:TABLE+g*3+3]=(starts[position]-START).to_bytes(3,'little')
 check,newgroups,newreachable=parse(rom);assert newgroups==groups and newreachable==reachable
 for i in range(reachable):assert check[i]==changed.get(i,entries[i])
 # No dictionary, glyph table or Huffman byte was changed by repacking names.
 assert rom[0x167be:0x1785e]==original[0x167be:0x1785e]
 return metadata,reachable
