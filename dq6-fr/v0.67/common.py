from pathlib import Path
import sys,importlib.util,json,hashlib,struct,re
O=Path(__file__).resolve().parent;R=O.parents[1]
def module(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
sys.path.insert(0,str(R/'dq6-fr/v0.66'));parent=module('parent67',R/'dq6-fr/v0.66/common.py');c=parent.c;sha=parent.sha;read=parent.read;patches=parent.patches;Codec=parent.Codec;names=parent.names;decode_pool=parent.decode_pool;expand=parent.expand
BASE=read(R/'dq6-fr/v0.66/build-report.json');POOL=parent.POOL;TAIL=parent.TAIL;END=parent.END;NEW_SIDS=[420,424,428,434,441,466,470,473,491,517]
STORAGE_PLACES=[419,422,427,432,442,444];STORAGE_SPELLS=[1570,1576,1579,1581,1585,1589,1592,1604,1605,1611,1620,1627,1628,1639,1714,1716];STORAGE_SIDS=STORAGE_PLACES+STORAGE_SPELLS;SIDS=sorted(NEW_SIDS+STORAGE_SIDS)
REVIEWS={420:'アモール : Desmodia DS, même ville sous ses deux états, deux entrées DS19/40 concordantes.',424:'クリアベール : Vallonclair DS, même ville dans les deux mondes, deux libellés DS7/25 concordants.',428:'マウントスノー : Montgivré DS, nom de la ville enneigée, accent é conservé.',434:'ムドーのしろ : Donjon de Meurtor DS. Le propriétaireムドー est Meurtor, sans maintenir Mudo de la translittération héritée.',441:'ガンディーノ : Brigandia DS, même ville. Aucun amalgame avec un nom de monstre.',466:'せきしょ : Poste-frontière DS, nom de lieu; tiret et è conservés. La traduction générique checkpoint ne remplace pas le libellé de carte officiel.',470:'マーズのやかた : Chez madame Luce DS, demeure du personnage. Conserve la minuscule de madame de la source française officielle.',473:'メダルおうのしろ : Manoir Médaillon DS, demeure du roi des médailles. Le nom complet est conservé, sans le tronquer à Médaillon.',491:'いどのそこ : Au fond du puits DS, libellé de lieu, pas une phrase du dialogue ni un nom propre de personnage.',517:'まじゅつしのとう : Tour des Maléfices DS, même tour. Le pluriel et le é de la liste officielle sont conservés.'}
def packed(codec,pairs,text):
 raw=codec.encode(text+'{AC}');out=bytearray();i=0
 while i<len(raw):
  if raw[i:i+2] in pairs:out.append(pairs[raw[i:i+2]]);i+=2
  else:out.append(raw[i]);i+=1
 assert codec.decode(out)==text+'{AC}'
 return bytes(out)
def prepare(jp):
 assert sha(jp)=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e','Wrong JP source'
 bps=(R/'patches/DQVI-FR-DS-v0.66-BASE-JP-PARTIEL.bps').read_bytes();assert sha(bps)==BASE['BPS_sha256'];b=module('bps67',R/'dq6-fr/upstream/refill/patchRM.py');base=bytes(b.apply_bps(jp,bps));assert sha(base)==BASE['ROM_sha256'];codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'));ns=names(base);pairs={base[0x3fb50+2*i:0x3fb52+2*i]:0xc9+i for i in range(50)}
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
 assert [x['sid'] for x in rows]==NEW_SIDS and sum(x['storage_delta'] for x in rows)==26
 storage=[];prior=[]
 for f in ['revue-lieux-v033.json','../v0.38/revue-sorts-v038.json']:
  prior+=read(R/'dq6-fr/v0.33'/f)
 for row in prior:
  sid=row['sid']
  if sid not in STORAGE_SIDS:continue
  at,old=ns[sid];text=codec.decode(old)[:-4];assert text==row['french'];new=packed(codec,pairs,text);assert len(new)<len(old) and sid<0x9a7 and sum(p==at for p,b in ns)==1
  assert not any(0xab<=v<=0xc8 for v in old[:-1]+new[:-1]);changes[at]=new
  storage.append(dict(sid=sid,french=text,previous_encoded_hex=old.hex(),encoded_hex=new.hex(),saved_bytes=len(old)-len(new),expanded_glyph_bytes_identical=expand(base,old)==expand(base,new),status='STOCKAGE_EQUIVALENT_SANS_NOUVELLE_TRADUCTION'))
 assert sorted(x['sid'] for x in storage)==sorted(STORAGE_SIDS) and sum(x['saved_bytes'] for x in storage)==26
 payload=bytearray();moved={}
 for at,old in sorted(dict(ns).items()):moved[str(at)]=len(payload);payload+=changes.get(at,old)
 assert len(payload)==TAIL-POOL
 return base,dict(rows=rows,storage=storage,payload_hex=payload.hex(),moved=moved)
def assemble(base,meta):
 out=bytearray(base);ns=names(base);payload=bytes.fromhex(meta['payload_hex'])
 for copy in (0,0x400000):
  out[copy+POOL:copy+TAIL]=payload
  for g in range(157):out[copy+0x165e7+g*3:copy+0x165ea+g*3]=meta['moved'][str(ns[g*16][0])].to_bytes(3,'little')
 checksum=sum(out)&65535
 for copy in (0,0x400000):struct.pack_into('<HH',out,copy+0xffdc,checksum^65535,checksum)
 assert sum(out)&65535==checksum
 return bytes(out)
