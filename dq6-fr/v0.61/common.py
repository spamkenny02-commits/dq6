from pathlib import Path
import hashlib,importlib.util,json,struct,sys
O=Path(__file__).resolve().parent;R=O.parents[1]
sys.path.insert(0,str(R/'dq6-fr/v0.60'))
def module(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
p60=module('parent60',R/'dq6-fr/v0.60/common.py');c=p60.c
from native_font import Codec
sha=p60.sha;read=p60.read;patches=p60.patches;decode_pool=p60.decode_pool
IDS=[464,465,498]
PLANS={464:'{BC}{B7} se lance soudain dans un jeu de rimes !{B1}{AC}',465:'{BC}{B7}. Je commence ! {B2} ! Euh... je ne trouve pas de rime ! {B7} a perdu !{B1}{AC}',498:'{B2} !!{B1} Mais rien ne se passe !{B1}{AC}'}
PLACE=read(R/'dq6-fr/v0.60/build-report.json')['placement']
def old_pool(base):return decode_pool(base,PLACE)
def names(rom):
 out=[]
 for sid in range(2512):
  at=0x3b8703+int.from_bytes(rom[0x165e7+3*(sid>>4):0x165ea+3*(sid>>4)],'little')
  for _ in range(sid&15):at=rom.index(0xac,at)+1
  end=rom.index(0xac,at)+1;out.append((at,rom[at:end]))
 assert len(set(a for a,b in out))==2048
 return out
def prepare(jp):
 assert sha(jp)=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e','Wrong JP source'
 patch=(R/'patches/DQVI-FR-DS-v0.60-BASE-JP-PARTIEL.bps').read_bytes();assert sha(patch)=='edd1d03c6adc2d32dd62d35310251e628786ea717a4ae1080dc8c0764a412b5d'
 m=module('bps61parent',R/'dq6-fr/upstream/refill/patchRM.py');base=bytes(m.apply_bps(jp,patch));assert sha(base)=='4b8d7f5f484300402022e4563ed4d989c6ef30ac57a1b878cb1b58a6183f621c'
 codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'));sys.path.insert(0,str(R/'preparations/combat-v057'));p57=module('source57',R/'preparations/combat-v057/prepare.py');source=p57.source_rows(jp)
 ja={(x['file'],x['id']):x['text'] for x in read(R/'dq6-fr/clean-base/ds-ja.json')};fr={(x['file'].replace('/FR/','/JA/'),x['id']):x['text'] for x in read(R/'dq6-fr/clean-base/ds-fr.json')}
 def ref(f,i):return dict(JA_file=f,FR_file=f.replace('/JA/','/FR/'),id=i,JA_text_sha256=sha(ja[f,i].encode()),FR_text_sha256=sha(fr[f,i].encode()))
 prep=read(R/'preparations/combat-v066/noms-composes-prepares.json');complete=[]
 for row in prep['combinations']:
  r=row['DS_reference'];assert r==ref(r['JA_file'],r['id']);assert fr[r['JA_file'],r['id']]=='@1'+row['French_complete_name']+'@';complete.append(row['French_complete_name'])
 wordrefs=[ref('data/MENULIST6/JA/b1005000.mpt',i) for i in (349,351)]
 assert fr[wordrefs[0]['JA_file'],349]=='@1Braséria@' and fr[wordrefs[1]['JA_file'],351]=='@1Céleste@'
 old=dict((i,b) for i,a,b in old_pool(base));out=[]
 for mid in IDS:
  data=codec.encode(PLANS[mid]);assert codec.decode(data)==PLANS[mid]
  tags=lambda b:[x for x in b if 0xab<=x<=0xc8 and x!=0xad]
  assert tags(data)==tags(source[mid]['private_tokens'])
  out.append(dict(id=mid,french_plan=PLANS[mid],encoded_hex=data.hex(),source_message_sha256=source[mid]['source_message_sha256'],previous_sha256=sha(old[mid])))
 ns=names(base)
 for sid,ch in [(0x369,'Céleste'),(0x36a,'Braséria')]:
  assert sum(a==ns[sid][0] for a,b in ns)==1;assert codec.decode(ns[sid][1])==f'M{sid:03X}'+'{AC}'
 return base,out,dict(complete_names=complete,DS_compound_references=[r['DS_reference'] for r in prep['combinations']],word_references=wordrefs,battle_references=[ref('data/MESS6/JA/0802.p',i) for i in (181,182,183,276,279,280)],word_names={'0369':'Céleste','036A':'Braséria'},word_game_adaptation='Jeu de rimes : conserve les quatre mots B2, les deux B7 et la défaite SFC ; DS remplace le jeu par des virelangues sans mot variable. Adaptation explicite, pas une copie DS.',spelling_variant_resolution='Quatre バキ SFC / バギ DS : adaptation contextuelle explicite de la même ligne du produit cartésien, quatre suffixes identiques, douze autres paires exactes et même scène du sort inventé. Pas une identité japonaise ni une correction silencieuse.')
def assemble(base,rows,meta):
 codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'));regions=c.main_regions(base);changes={r['id']:bytes.fromhex(r['encoded_hex']) for r in rows};payload=bytearray();starts=[]
 for mid,a,data in old_pool(base):
  if mid%8==0:starts.append(len(payload))
  payload+=changes.get(mid,data)
 def free(size,extra=()):
  for off in range(0x771800,0x7b8703-size,256):
   if (off>>16)!=((off+size-1)>>16):continue
   if all(not(p['file_offset']<off+size and p['file_offset']+p['size']>off) for p in regions+list(extra)):return off
  raise ValueError('No free region')
 off=free(len(payload));rom=bytearray(base);rom[off:off+len(payload)]=payload
 for copy in (0,0x400000):
  for g,at in enumerate(starts):rom[copy+c.PTR+g*3:copy+c.PTR+g*3+3]=((off+at-0xf6debd)&0xffffff).to_bytes(3,'little')
 ns=names(base);physical=sorted(dict(ns).items());changed={ns[int(sid,16)][0]:codec.encode(text+'{AC}') for sid,text in meta['word_names'].items()};pool=bytearray();moved={}
 for at,data in physical:moved[at]=len(pool);pool+=changed.get(at,data)
 assert 0x3b8703+len(pool)<=0x3bc712
 for copy in (0,0x400000):
  rom[copy+0x3b8703:copy+0x3b8703+len(pool)]=pool
  for g in range(157):rom[copy+0x165e7+g*3:copy+0x165ea+g*3]=moved[ns[g*16][0]].to_bytes(3,'little')
 placement=dict(offset=off,size=len(payload),groups=76,messages=608)
 engineoff=free(0x400,[dict(file_offset=off,size=len(payload))]);engine=module('pair61',O/'pair_engine.py');rom,eng=engine.apply(rom,engineoff,meta['complete_names'],codec)
 checksum=sum(rom)&65535
 for copy in (0,0x400000):struct.pack_into('<HH',rom,copy+0xffdc,checksum^65535,checksum)
 assert sum(rom)&65535==checksum
 return bytes(rom),placement,eng,dict(pool_offset=0x3b8703,pool_size=len(pool),changed_SIDs=meta['word_names'],runtime_SIDs=2512,physical_names=2048,aliases=464)
