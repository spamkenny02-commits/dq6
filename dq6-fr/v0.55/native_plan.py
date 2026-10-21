"""Compile explicit French/native plans, rejecting reordered or missing commands.

Only display styles, known name/number variables and pacing commands are allowed.
Original AF boundaries are explicit. Layout adds AD and AF without consolidating
speaker labels. This is not a DS-to-SFC control conversion.
"""
import re
LAYOUT={0xad,0xaf,0xac,0xae}
ALLOWED={0xd4,0xd9,0xda,0xdb,0xde,0xb0,0xd5,0xd6,0xc0,0xc1,0xb2,0xb3,0xb5,0xbb,0xc3,0xc4,0xc5,0xd8,0xdf}|{0xc7,0xdc,0xe0,0xe1}|set(range(0xc9,0xd4))
WIDTH={t:14 for t in set(range(0xc9,0xd4))|{0xc0,0xc1,0xb3,0xc3,0xd8}}
WIDTH.update({0xb2:22,0xb5:24,0xbb:8,0xc5:8,0xc4:7,0xdf:0,0xc7:24,0xe0:9,0xdc:0,0xe1:0})
def compile_plan(d,source,rev,punct):
 assert d['status']=='RELU' and d['sfc_jp']==source['text']
 original=source['tokens'];plan=d['native_plan']
 if d.get('structural_only'):
  assert not any(t>=0x200 and t!=0x200 for t in original)
  return dict(id=source['id'],tokens=original[:],text='',lines=[],method='native_source_structure_restored',source_terminator=original[-1])
 if d.get('fixed_layout'):
  from fixed_plan import compile_fixed
  return compile_fixed(d,source,rev,punct,ALLOWED,WIDTH)
 first_limit=24 if original and original[0]==0xd4 else 22
 tags=[int(x,16) for x in re.findall(r'\{([A-F0-9]{2})\}',plan)]
 assert all(t in ALLOWED|{0xaf} for t in tags),'Unknown native command'
 assert [t for t in tags if t!=0xaf]==[t for t in original if t<0x200 and t not in LAYOUT],(source['id'],'native sequence changed')
 assert tags.count(0xaf)==original.count(0xaf),(source['id'],'original pause missing')
 plan=re.sub(r'\{([A-F0-9]{2})\}',lambda m:chr(0xe000+int(m[1],16)),plan)
 assert not any(c in plan for c in '{}%@'),'Unresolved markup'
 plan=plan.translate(punct);paragraphs=plan.split(chr(0xe0af));tokens=[];lines=[]
 def width(word):return sum(WIDTH.get(ord(c)-0xe000,0) if 0xe000<=ord(c)<0xe200 else 1 for c in word)
 def encode(line):
  out=[]
  for c in line:
   if 0xe000<=ord(c)<0xe200:out.append(ord(c)-0xe000)
   else:
    assert c in rev,(source['id'],'unknown glyph',c)
    out.append(rev[c])
  return out
 for n,para in enumerate(paragraphs):
  if not para.strip():
   assert n==len(paragraphs)-1 and n>0,'Empty internal paragraph'
   continue
  pl=[];line='';cols=0
  words=[]
  for word in para.split():
   if word in {'!','?','♥','♪',';'} and words and width(words[-1]+' '+word)<=24:
    words[-1]+=' '+word
   else:words.append(word)
  for word in words:
   w=width(word);assert w<=24,(source['id'],'word too wide',word)
   limit=first_limit if (len(lines)+len(pl))%3==0 else 24
   gap=1 if line else 0
   if line and cols+gap+w>limit:
    pl.append(line);line='';cols=0;gap=0
    limit=first_limit if (len(lines)+len(pl))%3==0 else 24
   if not line and w>limit:
    pl.append('')
   line+=(' ' if gap else '')+word;cols+=gap+w
  if line:pl.append(line)
  for k,line in enumerate(pl):
   if k:
    if k%3==0:tokens.append(0xaf)
    tokens.append(0xad)
   tokens.extend(encode(line))
  lines.extend(pl)
  if n<len(paragraphs)-1:
   # A source pause closes this page. Empty trailing paragraph is not a page.
   if paragraphs[n+1].strip():
    while len(lines)%3:
     lines.append('');tokens.append(0xad)
   tokens.append(0xaf)
   if paragraphs[n+1].strip():tokens.append(0xad)
 tokens.append(original[-1])
 assert all(width(line)<=(first_limit if i%3==0 else 24) for i,line in enumerate(lines)),(source['id'],'line overflow')
 assert original[-1] in {0xac,0xae}
 assert [t for t in tokens if t<0x200 and t not in LAYOUT]==[t for t in original if t<0x200 and t not in LAYOUT]
 return dict(id=source['id'],tokens=tokens,text=' '.join(' '.join(x.split()) for x in paragraphs if x.strip()),lines=lines,method='native_plan_reviewed',source_terminator=original[-1],original_af_count=original.count(0xaf))
