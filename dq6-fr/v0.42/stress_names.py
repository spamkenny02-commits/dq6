"""Private diagnostic fixture only: swap two existing item-name entries."""
from pathlib import Path
import struct
from names import parse,START,END,TABLE
def apply(path):
 rom=bytearray(path.read_bytes());entries,groups,reachable=parse(rom)
 old_end=START+sum(len(e)+1 for e in entries[:reachable]);tail=bytes(rom[old_end:END]);used=list(entries[:reachable])
 used[1604],used[1638]=used[1638],used[1604]
 packed=bytearray();starts=[]
 for e in used:starts.append(len(packed));packed+=e+b'\xac'
 assert START+len(packed)+len(tail)==END
 for base in [0,0x400000]:
  rom[base+START:base+END]=packed+tail
  for g,pos in enumerate(groups):rom[base+TABLE+3*g:base+TABLE+3*g+3]=starts[pos].to_bytes(3,'little')
 for base in [0,0x400000]:rom[base+0xffdc:base+0xffe0]=bytes.fromhex('ffff0000')
 checksum=sum(rom)&65535
 for base in [0,0x400000]:struct.pack_into('<HH',rom,base+0xffdc,checksum^65535,checksum)
 path.write_bytes(rom)
