from pathlib import Path
import sys,importlib.util,json,hashlib,struct
O=Path(__file__).resolve().parent;R=O.parents[1]
def module(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
sys.path.insert(0,str(R/'dq6-fr/v0.64'));p64=module('parent65',R/'dq6-fr/v0.64/common.py');c=p64.c;sha=p64.sha;read=p64.read;patches=p64.patches;decode_pool=p64.decode_pool;Codec=p64.Codec
names=module('names65',R/'dq6-fr/v0.61/common.py').names
BASE=read(R/'dq6-fr/v0.64/build-report.json');POOL=0x3b8703;TAIL=0x3bbf10;END=0x3bc712;SIDS=[0x369,0x36a,0x905,0x907,0x908]
def prepare(jp):
 assert sha(jp)=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e','Wrong JP source'
 m=module('bps65',R/'dq6-fr/upstream/refill/patchRM.py');bps=(R/'patches/DQVI-FR-DS-v0.64-BASE-JP-PARTIEL.bps').read_bytes();assert sha(bps)==BASE['BPS_sha256'];base=bytes(m.apply_bps(jp,bps));assert sha(base)==BASE['ROM_sha256']
 b60=bytes(m.apply_bps(jp,(R/'patches/DQVI-FR-DS-v0.60-BASE-JP-PARTIEL.bps').read_bytes()));assert sha(b60)==read(R/'dq6-fr/v0.60/build-report.json')['ROM_sha256']
 codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'));pairs={base[0x3fb50+2*i:0x3fb52+2*i]:0xc9+i for i in range(50)};assert len(pairs)==50 and base[0x3fbb4]==255;assert all(all(x<0xab for x in k) for k in pairs)
 ns=names(base);changes={};rows=[]
 for sid in SIDS:
  at,old=ns[sid];out=bytearray();i=0
  while i<len(old):
   pair=old[i:i+2]
   if len(pair)==2 and pair in pairs:out.append(pairs[pair]);i+=2
   else:out.append(old[i]);i+=1
  packed=bytes(out);assert codec.decode(packed)==codec.decode(old);assert all(x<0xab or x==0xac or x in pairs.values() for x in packed)
  changes[at]=packed;rows.append(dict(sid=sid,french=codec.decode(old)[:-4],old_message_sha256=sha(old),new_message_sha256=sha(packed),old_encoded_hex=old.hex(),new_encoded_hex=packed.hex(),saved_bytes=len(old)-len(packed),status='STOCKAGE_EQUIVALENT_SANS_NOUVELLE_TRADUCTION',review='Compression DTE existante, aucun changement de texte, glyphe, sélection, variable ou commande. Réserve tail héritée v061 traitée séparément et explicitement.'))
 assert sum(x['saved_bytes'] for x in rows)==7
 payload=bytearray();moved={}
 for at,old in sorted(dict(ns).items()):moved[at]=len(payload);payload+=changes.get(at,old)
 assert len(moved)==2048 and POOL+len(payload)==TAIL
 return base,dict(rows=rows,payload_hex=payload.hex(),moved={str(at):off for at,off in moved.items()},old_tail_sha256=sha(b60[TAIL:END]),tail_hex=b60[TAIL:END].hex(),tail_size=END-TAIL,tail_prefix_before_sha256=sha(base[TAIL:TAIL+7]),tail_prefix_restored_sha256=sha(b60[TAIL:TAIL+7]))
def assemble(base,meta):
 out=bytearray(base);payload=bytes.fromhex(meta['payload_hex']);tail=bytes.fromhex(meta['tail_hex']);ns=names(base)
 for copy in (0,0x400000):
  out[copy+POOL:copy+TAIL]=payload;out[copy+TAIL:copy+END]=tail
  for g in range(157):out[copy+0x165e7+g*3:copy+0x165ea+g*3]=meta['moved'][str(ns[g*16][0])].to_bytes(3,'little')
 checksum=sum(out)&65535
 for copy in (0,0x400000):struct.pack_into('<HH',out,copy+0xffdc,checksum^65535,checksum)
 assert sum(out)&65535==checksum
 return bytes(out)
def expand(rom,data):
 pairs={0xc9+i:rom[0x3fb50+2*i:0x3fb52+2*i] for i in range(50)}
 return b''.join(pairs.get(v,bytes([v])) for v in data)
