"""Restore two absent native Huffman commands and their French grammar helpers.
The bag SID 09C8 is a saved runtime name; its empty ROM slot is intentional.
"""
import struct
from names import parse,encode as encode_names,START,END,TABLE
def encode(text):
 return b''.join(bytes([2+int(c)]) if c.isascii() and c.isdigit() else encode_names(c) for c in text)
HELPERS={0x118:('s',' et Cie'),0x11c:('M11C',''),0x11d:('M11D','vous tous'),0x11e:('M11E','vous')}
def apply_names(rom):
 original=bytes(rom);entries,groups,n=parse(rom);old_end=START+sum(len(e)+1 for e in entries[:n]);tail=bytes(rom[old_end:END]);content=tail.rstrip(b'\xff');changes={}
 for sid,(old,new) in HELPERS.items():
  pos=groups[sid>>4]+(sid&15);assert entries[pos]==encode(old),(sid,entries[pos].hex());assert sum(groups[s>>4]+(s&15)==pos for s in range(2512))==1
  changes[pos]=encode(new)
 packed=bytearray();starts=[]
 for i,e in enumerate(entries[:n]):starts.append(len(packed));packed+=changes.get(i,e)+b'\xac'
 assert START+len(packed)+len(content)<=END
 rom[START:END]=packed+content+b'\xff'*(END-START-len(packed)-len(content))
 for g,pos in enumerate(groups):rom[TABLE+3*g:TABLE+3*g+3]=starts[pos].to_bytes(3,'little')
 check,cg,cn=parse(rom);assert cg==groups and cn==n
 for i in range(n):assert check[i]==changes.get(i,entries[i])
 assert bytes(rom[START+len(packed):START+len(packed)+len(content)])==content
 assert rom[0x167be:0x1785e]==original[0x167be:0x1785e]
 return len(changes)

def expanded(root,left,right):
 left=list(left);right=list(right);tables=[left,right];old_root=(left[root//2],right[root//2]);parents={}
 for target in [0xd6,0xe1]:
  found=[(s,i) for s,t in enumerate(tables) for i,v in enumerate(t) if not v&0x8000 and v&0x1fff==target]
  assert len(found)==1 and found[0][1]!=root//2;parents[target]=found[0]
 assert not any(v&0x8000 and v&0x7fff==root for t in tables for v in t)
 # Reuse the old root slot for E1/DF; append D6/C4 and a relocated root.
 d6_node=len(left)*2;new_root=d6_node+2
 for t,v in zip(tables,old_root):t.extend([0,v])
 left[d6_node//2]=0xd6;right[d6_node//2]=0xc4
 left[root//2]=0xe1;right[root//2]=0xdf
 for target,node in [(0xd6,d6_node),(0xe1,root)]:s,i=parents[target];tables[s][i]=0x8000|node
 return new_root,left,right

def restore_commands(rom,root,left,right):
 root,left,right=expanded(root,left,right)
 for base in [0,0x400000]:
  assert rom[base+0x4b:base+0x4e]==bytes.fromhex('36fbc2')
  assert rom[base+0x6927b:base+0x6928b]==bytes.fromhex('221c2bc401ff3af006a918014c0c926b')
  rom[base+0x4b:base+0x4e]=bytes.fromhex('7b92c6')
  struct.pack_into('<H',rom,base+0x2bfb,root)
  for off,t in [(0x167be,left),(0x1700e,right)]:
   assert len(t)*2<0x850;struct.pack_into('<'+'H'*len(t),rom,base+off,*t)
 return root,left,right

def verify_tree(rom,raw,base):
 root=struct.unpack_from('<H',raw,0x2bfb)[0];n=root//2+1
 l,r=[struct.unpack_from('<'+'H'*n,raw,a) for a in [0x167be,0x1700e]];nr,l,r=expanded(root,l,r)
 expected=bytearray(raw[0x167be:0x1785e])
 for off,t in [(0x167be,l),(0x1700e,r)]:struct.pack_into('<'+'H'*len(t),expected,off-0x167be,*t)
 assert rom[base+0x167be:base+0x1785e]==expected
 assert struct.unpack_from('<H',rom,base+0x2bfb)[0]==nr
