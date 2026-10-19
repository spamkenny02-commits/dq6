"""DQVI: extraction reproductible DS FR/JA et SFC JP. Aucune ROM modifiee."""
from pathlib import Path
import argparse,struct,json,hashlib,zlib
from probe import lz10

def save(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')

def ds_extract(path,out):
 d=path.read_bytes();fnt,_,fat,_=struct.unpack_from('<4I',d,0x40);files=[]
 def walk(di,base=''):
  off,idx,_=struct.unpack_from('<IHH',d,fnt+(di&4095)*8);pos=fnt+off
  while d[pos]:
   n=d[pos];pos+=1;name=d[pos:pos+(n&127)].decode('ascii');pos+=n&127
   if n&128:
    child=struct.unpack_from('<H',d,pos)[0];pos+=2;walk(child,base+name+'/')
   else:
    a,b=struct.unpack_from('<II',d,fat+idx*8);files.append(dict(id=idx,path=base+name,offset=a,size=b-a));idx+=1
 walk(0xf000);save(out/'nds-files.json',files);counts={}
 for lang in ['FR','JA']:
  records=[]
  for e in files:
   if '/'+lang+'/' not in e['path'] or not any('/'+x+'/' in e['path'] for x in ['MESS6','MENULIST6']):continue
   b=d[e['offset']:e['offset']+e['size']];b=lz10(b) if b[0]==16 else b
   assert b[:4]==b'MPT0',e
   size,lo,hi,n,tab,tablesize,textsize=struct.unpack_from('<7I',b,4)
   assert size==len(b) and tablesize==(6*n+3)//4*4 and tab+tablesize+textsize==len(b),e
   for i in range(n):
    mid,length,off=struct.unpack_from('<HHH',b,tab+6*i);start=tab+tablesize+off*4
    raw=b[start:start+length];assert len(raw)==length
    text=raw.decode('utf-8')
    assert text.encode('utf-8')==raw
    records.append(dict(file=e['path'],index=i,id=mid,range_start=lo,range_end=hi,byte_offset=start,byte_length=length,text=text))
  save(out/f'ds-{lang.lower()}.json',records);counts[lang]=len(records)
 return counts

def sfc_extract(path,out):
 raw=path.read_bytes();header=512 if len(raw)%32768==512 else 0;d=raw[header:]
 table={}
 for line in (Path(__file__).parent/'upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines():
  if '=' not in line:continue
  k,v=line.split('=',1)
  if len(k)<=4:table[int(k,16)]=v
 trees=[struct.unpack_from('<1064H',d,a) for a in [0x167be,0x1700e]]
 codes={}
 def traverse(v,bits):
  if v&0x8000:
   for bit in [0,1]:traverse(trees[bit][(v&32767)//2],bits+[bit])
  else:codes.setdefault(v&8191,[]).append(bits)
 traverse(0x884e,[])
 records=[];verified=0
 for group in range(870):
  ptr=int.from_bytes(d[0x15bb5+group*3:0x15bb8+group*3],'little');pos=0x37175b+(ptr>>3);bit=ptr&7
  for j in range(8 if group<869 else 5):
   start=(pos,bit);tokens=[]
   for _ in range(100000):
    v=0x884e;bits=[]
    while v&32768:
     b=(d[pos]>>bit)&1;bits.append(b);bit-=1
     if bit<0:pos+=1;bit=7
     v=trees[b][(v&32767)//2]
    token=v&8191;assert bits in codes[token];verified+=len(bits);tokens.append(token)
    if token in [0xac,0xae]:break
   else:raise ValueError('Unterminated string')
   records.append(dict(id=group*8+j,offset=start[0],bit=start[1],tokens=tokens,text=''.join(table.get(t,f'<{t:04X}>') for t in tokens)))
 save(out/'sfc-jp.json',records)
 return dict(header_bytes=header,sha256_unheadered=hashlib.sha256(d).hexdigest(),crc32_unheadered=f'{zlib.crc32(d):08x}',messages=len(records),huffman_bits_verified=verified,unknown_tokens=sorted({t for r in records for t in r['tokens'] if t not in table}))

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--ds',type=Path,required=True);a.add_argument('--sfc',type=Path,required=True);a.add_argument('--out',type=Path,default=Path('output'));args=a.parse_args()
 result={'ds':ds_extract(args.ds,args.out),'sfc':sfc_extract(args.sfc,args.out)};save(args.out/'validation.json',result);print(json.dumps(result,indent=2))
