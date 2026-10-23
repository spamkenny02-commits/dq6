"""Bound the Japanese native battle pool before the compressed main-script boundary.
Historical v057's unbounded reader is retained unchanged for provenance only.
"""
import struct,hashlib,json
LIMIT=0x37175b
sha=lambda b:hashlib.sha256(b).hexdigest()
def source_rows(jp,table):
 glyphs=struct.unpack_from('<256H',jp,0x11100);rows=[]
 for group in range(76):
  p=0x36debd+int.from_bytes(jp[0x15ad1+group*3:0x15ad4+group*3],'little')
  for low in range(8):
   if p==LIMIT:return rows
   assert p<LIMIT
   start=p;ts=[]
   while True:
    assert p<LIMIT,'Native read would enter protected main script'
    b=jp[p];p+=1;ts.append(b)
    if b in (0xac,0xae):break
   text=''.join('['+f'{b:02X}'+']' if 0xab<=b<=0xc8 else table.get(glyphs[b],'<UNKNOWN>') for b in ts)
   rows.append(dict(id=group*8+low,private_text=text,private_tokens=ts,source_text_sha256=sha(text.encode()),source_message_sha256=sha(bytes(ts)),start=start,end=p))
 raise AssertionError('Expected source boundary not reached')
def checked_rows(jp,repo):
 table={int(k,16):v for l in (repo/'dq6-fr/upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in l for k,v in [l.split('=',1)] if len(k)<=4};rows=source_rows(jp,table);assert len(rows)==603 and rows[-1]['end']==LIMIT
 return rows
