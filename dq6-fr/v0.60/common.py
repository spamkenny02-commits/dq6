"""Native battle-only delta over the verified v0.59 BPS. No engine edits."""
from pathlib import Path
import hashlib,importlib.util,json,re,struct,zlib
O=Path(__file__).resolve().parent;R=O.parents[1]
s=importlib.util.spec_from_file_location
spec=s('codec58',R/'tools/combat-v058/codec.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
IDS=[311, 367, 382, 389, 390, 395, 397, 398, 403, 404, 407, 408, 409, 412, 413, 414, 415, 432, 433, 434, 435, 436, 437, 452, 453, 461, 466, 467, 468, 469, 470, 471, 473, 493, 495, 499, 500, 501, 502, 503, 504, 505, 509, 510, 511, 514, 515, 518, 522, 524, 528, 530, 531, 533, 534, 535, 537, 544, 546, 549, 550, 553, 562, 563]
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def prepare(jp):
 assert sha(jp)=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e','Wrong JP source'
 spec=s('bps58parent',R/'dq6-fr/upstream/refill/patchRM.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 assert sha((R/'patches/DQVI-FR-DS-v0.59-BASE-JP-PARTIEL.bps').read_bytes())=='070792b62c89780c84741ee2e9643a51bc77a5e1b71e441f9dde45194b991b67'
 base=bytes(m.apply_bps(jp,(R/'patches/DQVI-FR-DS-v0.59-BASE-JP-PARTIEL.bps').read_bytes()));assert sha(base)=='1b974538502319d1ba9d5020dd43708361d98b7bf985f66aab7c242a58aecceb'
 from native_font import apply,Codec
 fontbase,font_report=apply(base,old_pool(base))
 codec=Codec(fontbase,read(R/'dq6-fr/v0.56/charset.json'))
 observed=read(R/'tools/combat-v060/qa-resident-font.json')['field_glyphs_visually_reviewed']
 assert all(observed.get(f'{b:02X}')==ch for ch,b in codec.forward.items() if ch.isascii() or ch=='…')
 import sys
 sys.path.insert(0,str(R/'preparations/combat-v057'))
 spec=s('prep57source',R/'preparations/combat-v057/prepare.py');p57=importlib.util.module_from_spec(spec);spec.loader.exec_module(p57);jp_rows=p57.source_rows(jp)
 dsja={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-ja.json')};dsfr={(x['file'].replace('/FR/','/JA/'),x['id']):x for x in read(R/'dq6-fr/clean-base/ds-fr.json')}
 for mid,at in [(51,0x2ad4a),(427,0x2b3ca),(429,0x2b477)]:
  expected=bytes.fromhex('22162ac0')+mid.to_bytes(2,'little')
  assert jp[at:at+6]==base[at:at+6]==expected
 original={i:b for i,_,b in old_pool(base)};allrows={r['id']:r for r in read(R/'preparations/combat-v057/prepares-non-inseres.json')};review=read(O/'revue-combat-v060.json');out=[]
 assert [r['id'] for r in review]==IDS
 for r in review:
  mid=r['id'];p=allrows[mid];assert p['semantic_review']=='RELU_JP_FR_CONTEXTE_DISPONIBLE'
  assert r['preparation_plan']==p['french_plan'] and r['source_message_sha256']==p['source_message_sha256']
  from revisions import OVERRIDES
  assert r['french_plan']==re.sub(' +',' ',OVERRIDES.get(mid,p['french_plan']).replace('{AD}',' '))
  assert r['ds_references']==p['ds_references']
  for ref in r['ds_references']:
   key=ref['file'],ref['id']
   assert sha(dsja[key]['text'].encode())==ref['ja_text_sha256'] and sha(dsfr[key]['text'].encode())==ref['fr_text_sha256']
  data=codec.encode(r['french_plan']);assert codec.decode(data)==r['french_plan']
  # Only reviewed native name substitutions are allowed in this lot.
  assert not any(0xb2<=x<=0xbb and x not in (0xb2,0xb3,0xb5,0xb7,0xb8,0xbb) for x in data)
  assert jp_rows[mid]['source_message_sha256']==r['source_message_sha256']
  oldtags=[x for x in jp_rows[mid]['private_tokens'] if 0xab<=x<=0xc8 and x!=0xad]
  assert [x for x in data if 0xab<=x<=0xc8 and x!=0xad]==oldtags
  out.append(dict(id=mid,french_plan=r['french_plan'],encoded_hex=data.hex(),previous_v059_sha256=sha(original[mid]),source_message_sha256=r['source_message_sha256']))
 return base,out
def assemble(base,rows):
 main=c.main_regions(base);changes={r['id']:bytes.fromhex(r['encoded_hex']) for r in rows};payload=bytearray();starts=[]
 for mid,_,data in old_pool(base):
  if mid%8==0:starts.append(len(payload))
  payload+=changes.get(mid,data)
 off=next(x for x in range(0x771800,0x7b8703-len(payload),256) if all(not(p['file_offset']<x+len(payload) and p['file_offset']+p['size']>x) for p in main))
 from native_font import apply
 rom=bytearray(apply(base,old_pool(base))[0]);rom[off:off+len(payload)]=payload
 for copy in (0,0x400000):
  for g,start in enumerate(starts):rom[copy+c.PTR+g*3:copy+c.PTR+g*3+3]=((off+start-0xf6debd)&0xffffff).to_bytes(3,'little')
 checksum=sum(rom)&65535
 for copy in (0,0x400000):struct.pack_into('<HH',rom,copy+0xffdc,checksum^65535,checksum)
 assert sum(rom)&65535==checksum
 return bytes(rom),dict(offset=off,size=len(payload),groups=76,messages=608)
def decode_pool(rom,placement):
 out=[];ranges=[]
 for g in range(76):
  ptr=int.from_bytes(rom[c.PTR+3*g:c.PTR+3*g+3],'little');cpu=(ptr+0xf6debd)&0xffffff
  assert placement['offset']<=cpu<placement['offset']+placement['size'];start=cpu
  for low in range(8):
   at=cpu
   while cpu<placement['offset']+placement['size'] and rom[cpu] not in (0xac,0xae):cpu+=1
   assert cpu<placement['offset']+placement['size'];cpu+=1;out.append((g*8+low,at,rom[at:cpu]))
  assert not any(start<hi and cpu>lo for lo,hi in ranges);ranges.append((start,cpu))
 assert sum(hi-lo for lo,hi in ranges)==placement['size']
 return out
def vint(v):
 out=bytearray()
 while True:
  b=v&127;v>>=7
  if not v:out.append(b|128);return out
  out.append(b);v-=1
def patches(jp,rom):
 def mode(i):return (0 if i<0x400000 else 2) if rom[i]==jp[i%0x400000] else 1
 bps=bytearray(b'BPS1')+vint(len(jp))+vint(len(rom))+vint(0);i=0;rel=0
 while i<len(rom):
  kind=mode(i);at=i;i+=1
  while i<len(rom) and i!=0x400000 and mode(i)==kind:i+=1
  bps+=vint(((i-at-1)<<2)|kind)
  if kind==1:bps+=rom[at:i]
  elif kind==2:
   origin=at%0x400000;delta=origin-rel;bps+=vint((abs(delta)<<1)|int(delta<0));rel=origin+i-at
 bps+=struct.pack('<II',zlib.crc32(jp),zlib.crc32(rom));bps+=struct.pack('<I',zlib.crc32(bps))
 ips=bytearray(b'PATCH');i=0
 while i<len(rom):
  if i<len(jp) and rom[i]==jp[i]:i+=1;continue
  at=i;i+=1
  while i<len(rom) and (i>=len(jp) or rom[i]!=jp[i]) and i-at<65535:i+=1
  ips+=at.to_bytes(3,'big')+(i-at).to_bytes(2,'big')+rom[at:i]
 ips+=b'EOF'+len(rom).to_bytes(3,'big')
 return bytes(bps),bytes(ips)

def old_pool(rom):
 return decode_pool(rom,read(R/'dq6-fr/v0.59/build-report.json')['placement'])
