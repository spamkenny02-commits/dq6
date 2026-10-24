from pathlib import Path
import json,struct,hashlib,importlib.util,sys
O=Path(__file__).resolve().parent;R=O.parents[1]
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
sys.path.insert(0,str(R/'dq6-fr/v0.78'));parent=module('parent79',R/'dq6-fr/v0.78/common.py');c=parent.c
read=lambda p:json.loads(p.read_text());sha=lambda b:hashlib.sha256(b).hexdigest()
BASE=read(R/'dq6-fr/v0.78/build-report.json');JP_SHA='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e';IDS=[493,556,1018,1151,1181]
PLAN=[(493,'costaud','costaude'),(556,'pourrais','pourrai'),(1018,'gêolier','geôlier'),(1151,'Dites lui','Dites-lui'),(1181,'telle quelle est',"telle qu'elle est")]
PATCH='DQVI-FR-DS-v0.79-BASE-JP-PARTIEL'
sha256_tokens=lambda ts:sha(json.dumps(ts,separators=(',',':')).encode())
def save(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def baseline(jp):
 assert sha(jp)==JP_SHA,'Intact JP source required'
 b=module('bps79',R/'dq6-fr/upstream/refill/patchRM.py');p=(R/'patches/DQVI-FR-DS-v0.78-BASE-JP-PARTIEL.bps').read_bytes();assert sha(p)==BASE['BPS_sha256'];rom=bytes(b.apply_bps(jp,p));assert sha(rom)==BASE['ROM_sha256'];return rom

def tree(rom):
 root=int.from_bytes(rom[0x2bfb:0x2bfd],'little');n=root//2+1
 return root,[struct.unpack_from('<%dH'%n,rom,a) for a in (0x167be,0x1700e)]
def decode_main(rom):
 root,trees=tree(rom);messages=[];regions=[]
 for g in range(870):
  cpu=int.from_bytes(rom[0x15bb5+3*g:0x15bb8+3*g],'little');start=cpu&0x3fffff if cpu>=0xc00000 else cpu;pos=start;bit=7
  assert 0x37175b<=pos<0x3b8703 or 0x77175b<=pos<0x7b8703
  for _ in range(8):
   ts=[]
   for _ in range(20000):
    v=root|32768
    while v&32768:
     b=(rom[pos]>>bit)&1;bit-=1
     if bit<0:pos+=1;bit=7
     v=trees[b][(v&32767)//2]
    t=v&8191;ts.append(t)
    if t in (0xac,0xae):break
   else:raise AssertionError('unterminated')
   messages.append(ts)
  regions.append(dict(group=g,file_offset=start,cpu_address=cpu,size=pos-start+(bit!=7)))
 return messages,regions

def codes_for(rom):
 root,trees=tree(rom);out={}
 def walk(node,bits):
  for bit in (0,1):
   v=trees[bit][node//2]
   if v&32768:walk(v&32767,bits+[bit])
   else:out.setdefault(v&8191,bits+[bit])
 walk(root,[]);return out

def pack_group(messages,codes):
 bits=[bit for ts in messages for t in ts for bit in codes[t]];b=bytearray((len(bits)+7)//8)
 for i,v in enumerate(bits):b[i//8]|=v<<(7-i%8)
 return bytes(b)

def selection(base):
 selected={x['id']:x for x in read(R/'dq6-fr/v0.56/insertion-candidates.json')};actual,_=decode_main(base);charset={int(k,16):v for k,v in read(R/'dq6-fr/v0.56/charset.json').items()};rev={v:k for k,v in charset.items()};rev[' ']=0x200;rows=[]
 proposals={x['id']:x for p in sorted((R/'preparations').glob('relecture-principale-*/revisions-preparees-non-inserees.json')) for x in read(p)}
 for mid,before,after in PLAN:
  old=selected[mid];assert actual[mid]==old['tokens']==proposals[mid].get('native_baseline_tokens_preserved',proposals[mid].get('native_commands_preserved_as_baseline_tokens'));needle=[rev[t] for t in before];repl=[rev[t] for t in after];hits=[i for i in range(len(actual[mid])) if actual[mid][i:i+len(needle)]==needle];assert len(hits)==1
  at=hits[0];tokens=actual[mid][:at]+repl+actual[mid][at+len(needle):]
  assert [x for x in tokens if x<0x200]==[x for x in actual[mid] if x<0x200]
  lines=old['lines'][:];hitlines=[i for i,s in enumerate(lines) if before in s];assert len(hitlines)==1;line=hitlines[0];assert lines[line].count(before)==1;lines[line]=lines[line].replace(before,after);assert len(lines[line])<=24
  assert old['text'].count(before)==1;text=old['text'].replace(before,after);assert text==proposals[mid]['proposed_text']
  rows.append(dict(id=mid,before=before,after=after,old_text=old['text'],text=text,old_tokens=actual[mid],tokens=tokens,old_tokens_sha256=sha256_tokens(actual[mid]),tokens_sha256=sha256_tokens(tokens),lines=lines,changed_line=line,old_line=old['lines'][line],new_line=lines[line],pause_count=tokens.count(0xaf),all_controls_variables_breaks_pauses_preserved=True,DS_references=next(x for p in sorted((R/'preparations').glob('relecture-principale-*/registre-relecture.json')) for x in read(p) if x['id']==mid)['DS_references'],source_japanese=old['source_japanese'],secondary_IPS_text=old.get('sfc_previous'),reason=proposals[mid]['reason'],status='REVISION_INTEGREE_V079',natural_validation=False))
 return rows

def assemble(base,rows):
 messages,regions=decode_main(base);expected=[ts[:] for ts in messages]
 for row in rows:assert messages[row['id']]==row['old_tokens'];expected[row['id']]=row['tokens']
 blocked=[(p['file_offset'],p['file_offset']+p['size']) for p in regions]
 blocked += [(parent.NAME,parent.NAME_LIMIT),(BASE['placement']['offset'],BASE['placement']['offset']+BASE['placement']['size']),(BASE['engine']['allocation']['offset'],BASE['engine']['allocation']['offset']+BASE['engine']['allocation']['size'])]
 rom=bytearray(base);writes=[];codes=codes_for(base)
 for g in sorted({x['id']//8 for x in rows}):
  old=regions[g];blob=pack_group(expected[g*8:g*8+8],codes);at=old['file_offset']
  if len(blob)>old['size']:
   at=next((a for lo,hi in [(0x37175b,0x3b8703),(0x77175b,0x7b8703)] for a in range((lo+255)&~255,hi-len(blob)+1,256) if a>>16==(a+len(blob)-1)>>16 and all(not(l<a+len(blob) and h>a) for l,h in blocked)),None);assert at is not None,'No unprotected main-script gap'
  blocked.append((at,at+len(blob)));rom[at:at+len(blob)]=blob;cpu=at|0xc00000 if at<0x400000 else at
  for copy in (0,0x400000):rom[copy+0x15bb5+3*g:copy+0x15bb8+3*g]=cpu.to_bytes(3,'little')
  writes.append(dict(group=g,old_file_offset=old['file_offset'],old_size=old['size'],file_offset=at,size=len(blob),cpu_address=cpu,relocated=at!=old['file_offset']))
 total=sum(rom)&65535
 for copy in (0,0x400000):struct.pack_into('<HH',rom,copy+0xffdc,total^65535,total)
 assert sum(rom)&65535==total
 actual,_=decode_main(rom);assert actual==expected
 return bytes(rom),writes

# Read-only native table helpers inherited without changing their allocations.
decode_pool=parent.decode_pool;names=parent.names;cpu_for_file=parent.cpu_for_file
POOL=parent.POOL;END=parent.END;NAME=parent.NAME;WINDOW=parent.WINDOW

def current_main_selection():
 rows=read(R/'dq6-fr/v0.56/insertion-candidates.json');byid={x['id']:x for x in rows}
 for update in read(O/'selection.json'):
  row=byid[update['id']];assert row['tokens']==update['old_tokens']
  row.update(tokens=update['tokens'],text=update['text'],lines=update['lines'],last_revision='v0.79')
 assert len(rows)==6957
 return rows
