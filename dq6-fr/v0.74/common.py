from pathlib import Path
import sys,importlib.util,json,hashlib,struct,re
O=Path(__file__).resolve().parent;R=O.parents[1]
def module(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
sys.path.insert(0,str(R/'dq6-fr/v0.73'));parent=module('parent74',R/'dq6-fr/v0.73/common.py');c=parent.c;sha=parent.sha;read=parent.read;patches=parent.patches;Codec=parent.Codec;names=parent.names;decode_pool=parent.decode_pool;expand=parent.expand;LogicalTable=parent.LogicalTable;cpu_for_file=parent.cpu_for_file
BASE=read(R/'dq6-fr/v0.73/build-report.json');POOL=parent.POOL;TAIL=parent.TAIL;END=parent.END;NAME=parent.NAME;NAME_LIMIT=parent.NAME_LIMIT;NAME_BASE_CPU=parent.NAME_BASE_CPU
SELECTION=read(O/'selection.json');SIDS=sorted(s for x in SELECTION for s in x['sids']);NEW_SIDS=SIDS;TEST_SIDS=SIDS
class Plans:CORRECTED_EXISTING_SIDS=[]
plans=Plans()
def prepare(jp):
 assert sha(jp)=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e'
 patch=(R/'patches/DQVI-FR-DS-v0.73-BASE-JP-PARTIEL.bps').read_bytes();assert sha(patch)==BASE['BPS_sha256'];b=module('bps74',R/'dq6-fr/upstream/refill/patchRM.py');base=bytes(b.apply_bps(jp,patch));assert sha(base)==BASE['ROM_sha256'];codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'));ns=names(base);tab=LogicalTable(base);pairs={base[0x3fb50+2*i:0x3fb52+2*i]:0xc9+i for i in range(50)}
 helper=parent
 while not hasattr(helper,'packed'):helper=helper.parent
 glyphs=struct.unpack_from('<256H',jp,0x11100);jt={int(k,16):v for l in (R/'dq6-fr/upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in l for k,v in [l.split('=',1)] if len(k)<=4};rows=[];changes={}
 for x in SELECTION:
  pos=x['position'];sid=x['sids'][0];assert len(x['sids'])==1 and tab.position(sid)==pos
  at,old=ns[sid];cur=codec.decode(old)[:-4];assert cur==x['current'] and sha(old)==x['current_message_sha256']
  start=POOL+int.from_bytes(jp[0x165e7+(sid>>4)*3:0x165ea+(sid>>4)*3],'little')
  for _ in range(sid&15):start=jp.index(0xac,start)+1
  raw=jp[start:jp.index(0xac,start)];source=''.join(jt.get(glyphs[v],'<%04X>'%glyphs[v]) for v in raw);assert source==x['sfc_jp'] and sha(raw)==x['JP_message_sha256']
  french=x['proposal'];assert set(french)<=set(codec.forward) and len(french)<=len(cur)
  assert len(x['DS_references'])==1;ref=x['DS_references'][0];assert parent.parent.field(ref['JA_text'])==source and parent.parent.field(ref['FR_text'])==french
  new=helper.packed(codec,pairs,french);assert codec.decode(new)==french+'{AC}' and not any(0xab<=v<=0xc8 for v in old[:-1]+new[:-1]) and '|' not in cur
  changes[at]=new;rows.append(dict(sid=sid,position=pos,french=french,previous=cur,sfc_jp=source,DS_references=x['DS_references'],review=x['review_note'],old_encoded_hex=old.hex(),encoded_hex=new.hex(),old_sha256=sha(old),new_sha256=sha(new),old_columns=len(cur),new_columns=len(french),status='RELU_POUR_INSERTION',natural_validation=False))
 payload=bytearray();moved={}
 for at,old in sorted(dict(ns).items()):moved[str(at)]=len(payload);payload+=changes.get(at,old)
 assert NAME+len(payload)<=NAME_LIMIT
 return base,dict(rows=rows,payload_hex=payload.hex(),moved=moved)
assemble=parent.assemble

PREVIOUS_CONFIRMED=set(parent.PREVIOUS_CONFIRMED)|set(parent.PLANS)|set(parent.UNCHANGED)
PLANS={x['position']:x['proposal'] for x in SELECTION}
UNCHANGED=[]
