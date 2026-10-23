from pathlib import Path
import sys,importlib.util,json,hashlib,struct,re
O=Path(__file__).resolve().parent;R=O.parents[1]
def module(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
sys.path.insert(0,str(R/'dq6-fr/v0.65'));parent=module('parent66',R/'dq6-fr/v0.65/common.py');c=parent.c;sha=parent.sha;read=parent.read;patches=parent.patches;Codec=parent.Codec;names=parent.names;decode_pool=parent.decode_pool;expand=parent.expand
BASE=read(R/'dq6-fr/v0.65/build-report.json');POOL=parent.POOL;TAIL=parent.TAIL;END=parent.END;SIDS=[417,418,423,425,426,430,443,450]
REVIEWS={417:'トルッカ : même ville, français DS Puidebourg. Le nom propre remplace Torukka sans déterminant ajouté.',418:'ホルコッタ : même village, Pierrebrute DS. Onze glyphes, pas de saut ou abréviation.',423:'ペスカニ : même village de pêcheurs, Milmarin DS. Nom distinct de Militia/アークボルト, aucun rapprochement de sonorité.',425:'カルベローナ : Sorcéria DS, cohérent avec la cité des mages. Accent é complet conservé.',426:'カルカド : Aridéa DS, même ville. Ne pas conserver la translittération Calcado déjà remplacée dans le principal.',430:'ぜつぼうのまち : Mélankolia DS, la ville du désespoir. Distinct deよくぼうのまち/Kupidia. Accent é conservé.',443:'ゼニスのしろ : Zénithia DS, château de Zénith. Le libellé DS est un nom propre complet, sans ajouter Château de dans la table.',450:'ちていまじょう : Fort-Terreur DS, fort souterrain. Remplace Ile des Cavernes hérité, qui ne décrit pas ce nom JP. Tiret officiel conservé.'}
def packed(codec,pairs,text):
 raw=codec.encode(text+'{AC}');out=bytearray();i=0
 while i<len(raw):
  if raw[i:i+2] in pairs:out.append(pairs[raw[i:i+2]]);i+=2
  else:out.append(raw[i]);i+=1
 assert codec.decode(out)==text+'{AC}'
 return bytes(out)
def prepare(jp):
 assert sha(jp)=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e','Wrong JP source'
 bps=(R/'patches/DQVI-FR-DS-v0.65-BASE-JP-PARTIEL.bps').read_bytes();assert sha(bps)==BASE['BPS_sha256'];b=module('bps66',R/'dq6-fr/upstream/refill/patchRM.py');base=bytes(b.apply_bps(jp,bps));assert sha(base)==BASE['ROM_sha256'];codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'));ns=names(base);pairs={base[0x3fb50+2*i:0x3fb52+2*i]:0xc9+i for i in range(50)}
 ja={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-ja.json')};fr={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-fr.json')};glyphs=struct.unpack_from('<256H',jp,0x11100);jt={int(k,16):v for l in (R/'dq6-fr/upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in l for k,v in [l.split('=',1)] if len(k)<=4};rows=[];changes={}
 for row in read(R/'dq6-fr/v0.33/lieux-prepares-non-inseres.json'):
  sid=row['sid']
  if sid not in SIDS:continue
  at,old=ns[sid];assert sum(p==at for p,b in ns)==1;current=codec.decode(old)[:-4];assert current==row['current'];pos=POOL+int.from_bytes(jp[0x165e7+3*(sid>>4):0x165ea+3*(sid>>4)],'little')
  for _ in range(sid&15):pos=jp.index(0xac,pos)+1
  raw=jp[pos:jp.index(0xac,pos)];source=''.join(jt[glyphs[x]] for x in raw);assert source==row['sfc_jp'];refs=[]
  for ref in row['ds_sources']:
   j=ja[ref['file'].replace('/FR/','/JA/'),ref['id']];f=fr[ref['file'],ref['id']];assert j['text']=='@1'+source+'@' and f['text']=='@1'+row['french']+'@';refs.append(dict(JA_file=j['file'],FR_file=f['file'],id=f['id'],JA_text=j['text'],FR_text=f['text'],JA_sha256=sha(j['text'].encode()),FR_sha256=sha(f['text'].encode())))
  new=packed(codec,pairs,row['french']);assert max(len(current),len(row['french']))<=20 and not any(0xab<=v<=0xc8 for v in old[:-1]+new[:-1]);changes[at]=new;rows.append(dict(sid=sid,position=row['position'],sfc_jp=source,previous=current,french=row['french'],DS_references=refs,source_bytes_sha256=sha(raw),previous_encoded_hex=old.hex(),encoded_hex=new.hex(),previous_sha256=sha(old),encoded_sha256=sha(new),old_columns=len(current),new_columns=len(row['french']),storage_delta=len(new)-len(old),runtime_sids=[sid],review=REVIEWS[sid],status='RELU_POUR_INSERTION',limits='Native field/B2 diagnostics required; natural travel window not claimed.'))
 assert [x['sid'] for x in rows]==SIDS and sum(x['storage_delta'] for x in rows)==0
 payload=bytearray();moved={}
 for at,old in sorted(dict(ns).items()):moved[str(at)]=len(payload);payload+=changes.get(at,old)
 assert len(payload)==TAIL-POOL
 return base,dict(rows=rows,payload_hex=payload.hex(),moved=moved)
def assemble(base,meta):
 out=bytearray(base);ns=names(base);payload=bytes.fromhex(meta['payload_hex'])
 for copy in (0,0x400000):
  out[copy+POOL:copy+TAIL]=payload
  for g in range(157):out[copy+0x165e7+g*3:copy+0x165ea+g*3]=meta['moved'][str(ns[g*16][0])].to_bytes(3,'little')
 checksum=sum(out)&65535
 for copy in (0,0x400000):struct.pack_into('<HH',out,copy+0xffdc,checksum^65535,checksum)
 assert sum(out)&65535==checksum
 return bytes(out)
