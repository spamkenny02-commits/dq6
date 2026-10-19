from pathlib import Path
import json,struct

def lz10(d):
 assert d[0]==16
 size=int.from_bytes(d[1:4],'little');out=bytearray();p=4
 while len(out)<size:
  f=d[p];p+=1
  for bit in range(7,-1,-1):
   if len(out)>=size:break
   if f&(1<<bit):
    a,b=d[p:p+2];p+=2;n=(a>>4)+3;dist=((a&15)<<8|b)+1
    for _ in range(n):out.append(out[-dist])
   else:out.append(d[p]);p+=1
 assert len(out)==size
 return bytes(out)
if __name__=='__main__':
 es=json.loads(Path('dq6-fr/nds-files.json').read_text());d=next(Path('upload').glob('*.nds')).read_bytes()
 for e in [x for x in es if '/MESS6/FR/' in x['path']][:1]:
  b=lz10(d[e['offset']:e['offset']+e['size']]);Path('dq6-fr/sample.mpt').write_bytes(b)
  print(b[:64].hex());print(struct.unpack_from('<8I',b));print(repr(b[0xe054:0xe054+800]));print(repr(b[-800:]))
