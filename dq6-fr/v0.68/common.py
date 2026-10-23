from pathlib import Path
import sys,importlib.util,json,hashlib,struct,re
O=Path(__file__).resolve().parent;R=O.parents[1]
def module(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
sys.path.insert(0,str(R/'dq6-fr/v0.67'));parent=module('parent68',R/'dq6-fr/v0.67/common.py');c=parent.c;sha=parent.sha;read=parent.read;patches=parent.patches;Codec=parent.Codec;decode_pool=parent.decode_pool;expand=parent.expand
BASE=read(R/'dq6-fr/v0.67/build-report.json');POOL=parent.POOL;TAIL=parent.TAIL;END=parent.END;NEW_SIDS=[436,437,464,481,490];SIDS=NEW_SIDS;TEST_SIDS=sorted(NEW_SIDS+[231,233,873,1570,2309]);NAME=0x7af000;NAME_LIMIT=0x7b8703;NAME_BASE_CPU=0xfb8703
REVIEWS={436:'ダーマしんでん : Abbaye des Vocations DS, même sanctuaire dans deux états; références4/14 concordantes. Nom complet20glyphes,capitales officielles.',437:'フォーンじょう : Château de Joliroche DS, château du roi associé au miroir de Râ. Le nom complet20glyphes et le â sont conservés; aucune abréviation arbitraire.',464:'デスコッド : Pic des Terreurs DS, même village bonus. Nom complet officiel et pluriel conservés.',481:'ふなつきば : Cap de Somnia DS, même débarcadère. La spécificité Somnia est celle du libellé DS et non une inférence du seul nom commun JP.',490:'なげきのろうごく : Prison du Chagrin DS, prison du monde sombre. Nom complet et majuscule officielle de Chagrin conservés.'}
def cpu_for_file(at):
 assert 0<=at<0x7e0000
 return 0xc00000+at if at<0x400000 else at
def file_for_cpu(cpu):
 if 0xc00000<=cpu<=0xffffff:return cpu&0x3fffff
 if 0x400000<=cpu<0x7e0000:return cpu
 raise AssertionError('Not a supported ROM address')
def names(rom):
 out=[]
 for sid in range(2512):
  offset=int.from_bytes(rom[0x165e7+3*(sid>>4):0x165ea+3*(sid>>4)],'little');cpu=(NAME_BASE_CPU+offset)&0xffffff;at=file_for_cpu(cpu)
  for _ in range(sid&15):at=rom.index(0xac,at)+1
  end=rom.index(0xac,at)+1;assert end-at<256;out.append((at,rom[at:end]))
 assert len(set(a for a,b in out))==2048
 return out
class LogicalTable:
 def __init__(self,rom):
  self.rows=names(rom);self.positions={at:i for i,at in enumerate(sorted(set(a for a,b in self.rows)))}
  nt=module('legacy_nt68',R/'dq6-fr/upstream/refill/tools/nametable.py');self.dict=nt.read_dictionary(rom)[2];self.decoder=nt.Table.decode
 def position(self,sid):return self.positions[self.rows[sid][0]]
 def text(self,sid):return self.decoder(self,self.rows[sid][1][:-1])

def packed(codec,pairs,text):
 raw=codec.encode(text+'{AC}');out=bytearray();i=0
 while i<len(raw):
  if raw[i:i+2] in pairs:out.append(pairs[raw[i:i+2]]);i+=2
  else:out.append(raw[i]);i+=1
 assert codec.decode(out)==text+'{AC}'
 return bytes(out)
def prepare(jp):
 assert sha(jp)=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e','Wrong JP source'
 bps=(R/'patches/DQVI-FR-DS-v0.67-BASE-JP-PARTIEL.bps').read_bytes();assert sha(bps)==BASE['BPS_sha256'];b=module('bps68',R/'dq6-fr/upstream/refill/patchRM.py');base=bytes(b.apply_bps(jp,bps));assert sha(base)==BASE['ROM_sha256'];codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'));ns=names(base);pairs={base[0x3fb50+2*i:0x3fb52+2*i]:0xc9+i for i in range(50)}
 ja={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-ja.json')};fr={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-fr.json')};glyphs=struct.unpack_from('<256H',jp,0x11100);jt={int(k,16):v for l in (R/'dq6-fr/upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in l for k,v in [l.split('=',1)] if len(k)<=4};rows=[];changes={}
 for row in read(R/'dq6-fr/v0.33/lieux-prepares-non-inseres.json'):
  sid=row['sid']
  if sid not in NEW_SIDS:continue
  at,old=ns[sid];assert sum(p==at for p,b in ns)==1;current=codec.decode(old)[:-4];assert current==row['current'];pos=POOL+int.from_bytes(jp[0x165e7+3*(sid>>4):0x165ea+3*(sid>>4)],'little')
  for _ in range(sid&15):pos=jp.index(0xac,pos)+1
  raw=jp[pos:jp.index(0xac,pos)];source=''.join(jt[glyphs[x]] for x in raw);assert source==row['sfc_jp'];refs=[]
  for ref in row['ds_sources']:
   j=ja[ref['file'].replace('/FR/','/JA/'),ref['id']];f=fr[ref['file'],ref['id']];assert j['text']=='@1'+source+'@' and f['text']=='@1'+row['french']+'@';refs.append(dict(JA_file=j['file'],FR_file=f['file'],id=f['id'],JA_text=j['text'],FR_text=f['text'],JA_sha256=sha(j['text'].encode()),FR_sha256=sha(f['text'].encode())))
  new=packed(codec,pairs,row['french']);assert max(len(current),len(row['french']))<=20 and not any(0xab<=v<=0xc8 for v in old[:-1]+new[:-1]);changes[at]=new;rows.append(dict(sid=sid,position=row['position'],sfc_jp=source,previous=current,french=row['french'],DS_references=refs,source_bytes_sha256=sha(raw),previous_encoded_hex=old.hex(),encoded_hex=new.hex(),previous_sha256=sha(old),encoded_sha256=sha(new),old_columns=len(current),new_columns=len(row['french']),storage_delta=len(new)-len(old),runtime_sids=[sid],review=REVIEWS[sid],status='RELU_POUR_INSERTION',limits='Native field/B2 diagnostics required; natural travel window not claimed.'))
 assert [x['sid'] for x in rows]==NEW_SIDS and sum(x['storage_delta'] for x in rows)==34
 payload=bytearray();moved={}
 for at,old in sorted(dict(ns).items()):moved[str(at)]=len(payload);payload+=changes.get(at,old)
 assert len(payload)==TAIL-POOL+34 and NAME+len(payload)<=NAME_LIMIT
 regions=c.main_regions(base)+[dict(file_offset=BASE['placement']['offset'],size=BASE['placement']['size']),dict(file_offset=BASE['engine']['allocation']['offset'],size=BASE['engine']['allocation']['size'])]
 assert 0x77175b<=NAME<NAME+len(payload)<=0x7b8703
 assert all(not(x['file_offset']<NAME+len(payload) and x['file_offset']+x['size']>NAME) for x in regions),'Active reserved area overlap'
 assert all(not(copy+POOL<NAME+len(payload) and copy+END>NAME) for copy in (0,0x400000))
 return base,dict(rows=rows,payload_hex=payload.hex(),moved=moved)
def assemble(base,meta):
 out=bytearray(base);ns=names(base);payload=bytes.fromhex(meta['payload_hex']);out[NAME:NAME+len(payload)]=payload
 for copy in (0,0x400000):
  for g in range(157):
   cpu=NAME+meta['moved'][str(ns[g*16][0])];relative=(cpu-NAME_BASE_CPU)&0xffffff;assert (NAME_BASE_CPU+relative)&0xffffff==cpu
   out[copy+0x165e7+g*3:copy+0x165ea+g*3]=relative.to_bytes(3,'little')
 checksum=sum(out)&65535
 for copy in (0,0x400000):struct.pack_into('<HH',out,copy+0xffdc,checksum^65535,checksum)
 assert sum(out)&65535==checksum
 return bytes(out)
