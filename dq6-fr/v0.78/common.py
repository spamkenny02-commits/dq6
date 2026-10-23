from pathlib import Path
import sys,importlib.util,json,hashlib,struct,re
O=Path(__file__).resolve().parent;R=O.parents[1]
def module(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
sys.path.insert(0,str(R/'dq6-fr/v0.77'));parent=module('parent78',R/'dq6-fr/v0.77/common.py');c=parent.c;sha=parent.sha;read=parent.read;patches=parent.patches;Codec=parent.Codec;names=parent.names;decode_pool=parent.decode_pool;expand=parent.expand;LogicalTable=parent.LogicalTable;cpu_for_file=parent.cpu_for_file
BASE=read(R/'dq6-fr/v0.77/build-report.json');POOL=parent.POOL;TAIL=parent.TAIL;END=parent.END;NAME=parent.NAME;NAME_LIMIT=parent.NAME_LIMIT;NAME_BASE_CPU=parent.NAME_BASE_CPU
SELECTION=read(O/'selection.json');SIDS=sorted(s for x in SELECTION for s in x['sids']);NEW_SIDS=SIDS;TEST_SIDS=SIDS
class Plans:CORRECTED_EXISTING_SIDS=[150,151,152,153,154,169]
plans=Plans()
def prepare(jp):
 assert sha(jp)=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e'
 patch=(R/'patches/DQVI-FR-DS-v0.77-BASE-JP-PARTIEL.bps').read_bytes();assert sha(patch)==BASE['BPS_sha256'];b=module('bps78',R/'dq6-fr/upstream/refill/patchRM.py');base=bytes(b.apply_bps(jp,patch));assert sha(base)==BASE['ROM_sha256'];codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'));ns=names(base);tab=LogicalTable(base);pairs={base[0x3fb50+2*i:0x3fb52+2*i]:0xc9+i for i in range(50)}
 helper=parent
 while not hasattr(helper,'packed'):helper=helper.parent
 glyphs=struct.unpack_from('<256H',jp,0x11100);jt={int(k,16):v for l in (R/'dq6-fr/upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in l for k,v in [l.split('=',1)] if len(k)<=4};rows=[];changes={}
 for x in SELECTION:
  pos=x['position'];sid=x['sids'][0];assert len(x['sids'])==1 and tab.position(sid)==pos
  at,old=ns[sid];cur=name_text(base,old,codec);assert cur==x['current'] and sha(old)==x['current_message_sha256']
  start=POOL+int.from_bytes(jp[0x165e7+(sid>>4)*3:0x165ea+(sid>>4)*3],'little')
  for _ in range(sid&15):start=jp.index(0xac,start)+1
  raw=jp[start:jp.index(0xac,start)];source=''.join(jt.get(glyphs[v],'<%04X>'%glyphs[v]) for v in raw);assert source==x['sfc_jp'] and sha(raw)==x['JP_message_sha256']
  french=x['proposal'];assert set(french)<=set(codec.forward)
  assert len(x['DS_references'])==1;ref=x['DS_references'][0];assert field(ref['JA_text'])==source and field(ref['FR_text'])==french
  layout=x['layout'];oldlines=cur.split('|');newlines=layout.split('|');assert len(oldlines)==len(newlines);assert layout.replace('|',' ').rstrip()==french
  if x['kind']=='item':assert len(newlines[0])<=12 and (len(newlines)==1 or len(newlines[1])<=11)
  else:assert (pos in range(150,156) or pos==169) and len(newlines)==1 and len(layout)<=8
  if len(newlines)==2:
   breaks=[v for v in expand(base,old) if 0x91<=v<=0x9d];assert len(breaks)==1 and breaks[0]==0x90+len(oldlines[0]);assert 1<=len(newlines[0])<=13;new=helper.packed(codec,pairs,newlines[0])[:-1]+bytes([0x90+len(newlines[0])])+helper.packed(codec,pairs,newlines[1])
  else:new=helper.packed(codec,pairs,layout)
  assert name_text(base,new,codec)==layout and not any(0xab<=v<=0xc8 for v in old[:-1]+new[:-1])
  assert len([v for v in expand(base,old) if 0x91<=v<=0x9d])==len([v for v in expand(base,new) if 0x91<=v<=0x9d])==len(newlines)-1
  changes[at]=new;rows.append(dict(sid=sid,position=pos,french=french,layout=layout,previous=cur,sfc_jp=source,DS_references=x['DS_references'],review=x['review_note'],old_encoded_hex=old.hex(),encoded_hex=new.hex(),old_sha256=sha(old),new_sha256=sha(new),old_columns=len(cur),new_columns=len(french),status='RELU_POUR_INSERTION',natural_validation=False))
 for audit in BATTLE_LAYOUT:
  before=bytes.fromhex(audit['old_encoded_hex']);after=bytes.fromhex(audit['encoded_hex']);assert codec.decode(before)==audit['before'] and codec.decode(after)==audit['after']
  assert sha(before)==audit['old_sha256'] and sha(after)==audit['new_sha256']
  tags=lambda b:[v for v in b if 0xab<=v<=0xc8 and v!=0xad]
  assert tags(before)==tags(after)
  normalized=lambda t:' '.join(t.replace('{AD}',' ').split())
  assert normalized(audit['before'])==normalized(audit['after']) and after.count(0xad)>before.count(0xad)
 assert [x['id'] for x in BATTLE_LAYOUT]==[70,71,72,73,331,366,367,433,434,435]
 payload=bytearray();moved={}
 for at,old in sorted(dict(ns).items()):moved[str(at)]=len(payload);payload+=changes.get(at,old)
 assert NAME+len(payload)<=NAME_LIMIT
 return base,dict(rows=rows,payload_hex=payload.hex(),moved=moved)
BATTLE_LAYOUT=read(O/'battle-layout.json')
BATTLE=BASE['placement']['offset']
WINDOW=0x57bcc
def assemble(base,m):
 out=bytearray(base)
 for copy in (0,0x400000):
  assert out[copy+WINDOW:copy+WINDOW+14]==bytes.fromhex('02021007060009000000029d29c3')
  out[copy+WINDOW+2]=20
 out=bytearray(parent.parent.assemble(bytes(out),m));changes={x['id']:bytes.fromhex(x['encoded_hex']) for x in BATTLE_LAYOUT};payload=bytearray();starts=[]
 for mid,at,data in decode_pool(base,BASE['placement']):
  if mid%8==0:starts.append(len(payload))
  if mid in changes:
   x=next(x for x in BATTLE_LAYOUT if x['id']==mid);assert data.hex()==x['old_encoded_hex']
  payload+=changes.get(mid,data)
 assert BATTLE+len(payload)<=NAME and len(starts)==76
 for region in c.main_regions(base):assert not(region['file_offset']<BATTLE+len(payload) and region['file_offset']+region['size']>BATTLE)
 out[BATTLE:BATTLE+len(payload)]=payload
 for copy in (0,0x400000):
  for g,start in enumerate(starts):out[copy+c.PTR+3*g:copy+c.PTR+3*g+3]=((BATTLE+start-0xf6debd)&0xffffff).to_bytes(3,'little')
 checksum=sum(out)&65535
 for copy in (0,0x400000):struct.pack_into('<HH',out,copy+0xffdc,checksum^65535,checksum)
 assert sum(out)&65535==checksum
 return bytes(out)

PREVIOUS_CONFIRMED=set(parent.PREVIOUS_CONFIRMED)|set(parent.PLANS)|set(parent.UNCHANGED)
PLANS={x['position']:x['proposal'] for x in SELECTION}
UNCHANGED=[]

field=parent.field
def name_text(rom,raw,codec):
 return ''.join('|' if 0x91<=v<=0x9d else codec.decode(bytes([v])) for v in expand(rom,raw)[:-1])

def battle_placement(rom):
 start=(int.from_bytes(rom[c.PTR:c.PTR+3],'little')+0xf6debd)&0xffffff
 at=(int.from_bytes(rom[c.PTR+3*75:c.PTR+3*75+3],'little')+0xf6debd)&0xffffff
 for _ in range(8):
  while rom[at] not in (0xac,0xae):at+=1
  at+=1
 assert start==BATTLE and at<=NAME
 return dict(offset=start,size=at-start,groups=76,messages=608)
