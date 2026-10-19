from pathlib import Path
import json,struct,collections
p=Path(__file__).parent;r=(p/'vf-base-headered.sfc').read_bytes()[512:];root=struct.unpack_from('<H',r,0x2bfb)[0];n=root//2+1
base={}
for line in (p.parent/'upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines():
 if '=' in line:
  k,v=line.split('=',1)
  if len(k)<=4:base[int(k,16)]=v
# Lecture visuelle des glyphes du patch, conservant les glyphes non identifies sous forme de tokens.
m={0x200:' '}
for first,s in [(0x201,'ABCDEFGHJKLNOPQRSUVXYabcdeghknopqrsuvxy?023456789Iftz-TZmw'),(0x23d,'ii l'),(0x240,'.!.,MW…*'),(0x24c,'j'),(0x250,"'àâäéêèëïîôöûüùçÉÔÈæ")]:
 for i,c in enumerate(s):m[first+i]=c
m[0x23b]='W';m[0x23f]='l'
# Resolve the shuffled Latin alphabet and distinguish lowercase i from digit 1.
for start,letters in [(2,'0123456789'),(0x10,'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),(0x42,'abcdefghijklmnopqrstuvwxyz')]:
 for i,ch in enumerate(letters):m[struct.unpack_from('<H',r,0x11100+2*(start+i))[0]]=ch
m.update({0x241:'!',0x242:'.',0x243:',',0x246:'…',0x247:'*',0x250:"'"})
trees=[struct.unpack_from('<'+str(n)+'H',r,a) for a in [0x167be,0x1700e]]
records=[]
for group in range(870):
 ptr=int.from_bytes(r[0x15bb5+group*3:0x15bb8+group*3],'little');pos=0x37175b+(ptr>>3);bit=ptr&7
 for j in range(8 if group<869 else 5):
  start=(pos,bit);tokens=[]
  for _ in range(20000):
   v=root|0x8000
   while v&32768:
    b=(r[pos]>>bit)&1;bit-=1
    if bit<0:pos+=1;bit=7
    v=trees[b][(v&32767)//2]
   t=v&8191;tokens.append(t)
   if t in [0xac,0xae]:break
  else:raise ValueError('Unterminated')
  records.append(dict(id=group*8+j,offset=start[0],bit=start[1],tokens=tokens,text=''.join(m.get(t,base.get(t,f'<{t:04X}>')) if t<0x201 else m.get(t,f'<{t:04X}>') for t in tokens)))
(p/'sfc-vf.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
(p/'table-vf-provisoire.json').write_text(json.dumps({f'{k:04X}':v for k,v in m.items()},ensure_ascii=False,indent=2))
print('root',hex(root),'nodes',n,'messages',len(records))
for i in [0,100,101,102,103,200,1000,4000,6950]:print(i,records[i]['text'][:600])
