from pathlib import Path
import sys,importlib.util,json,hashlib,struct,re,unicodedata
O=Path(__file__).resolve().parent;R=O.parents[1]
def module(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
sys.path.insert(0,str(R/'dq6-fr/v0.60'));parent=module('base63',R/'dq6-fr/v0.60/common.py');c=parent.c;sha=parent.sha;read=parent.read;patches=parent.patches;decode_pool=parent.decode_pool
from native_font import Codec
plans=module('plans63',O/'plans.py');IDS=sorted(plans.BODIES)
BASE=read(R/'dq6-fr/v0.62/build-report.json');ENGINE=BASE['engine']['allocation']
def old_pool(rom):return decode_pool(rom,BASE['placement'])
def norm(t):
 t=unicodedata.normalize('NFKC',t);t=re.sub(r'\[(B[234578B])\]|%a\d+','X',t);t=re.sub(r'\[[A-F0-9]{2}\]|@[a-z][0-9]*|@','',t);return re.sub(r'\s+','',t).replace('。','.').replace('～','~')
def prepare(jp):
 assert sha(jp)=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e','Wrong JP source'
 patch=(R/'patches/DQVI-FR-DS-v0.62-BASE-JP-PARTIEL.bps').read_bytes();assert sha(patch)==BASE['BPS_sha256'];m=module('bps63',R/'dq6-fr/upstream/refill/patchRM.py');base=bytes(m.apply_bps(jp,patch));assert sha(base)==BASE['ROM_sha256']
 codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'));sys.path.insert(0,str(R/'preparations/combat-v057'));p57=module('source63',R/'preparations/combat-v057/prepare.py');guard=module('guard63',O/'source_guard.py');jp_rows=guard.checked_rows(jp,R)
 ja=read(R/'dq6-fr/clean-base/ds-ja.json');fr={(r['file'].replace('/FR/','/JA/'),r['id']):r['text'] for r in read(R/'dq6-fr/clean-base/ds-fr.json')};index={}
 for r in ja:
  if (('/MESS6/JA/080' in r['file']) or r['file']=='data/MESS6/JA/0099.p') and (r['file'],r['id']) in fr:index.setdefault(norm(r['text']),[]).append(r)
 old={i:b for i,a,b in old_pool(base)};previous=read(R/'dq6-fr/v0.62/inventaire-combat-v062.json');assert not set(IDS)&set(previous['integrated_ids']);rows=[]
 for mid in IDS:
  assert mid<=602,'Outside bounded JP pool';src=jp_rows[mid];tokens=src['private_tokens'];prefix=('{%02X}'%tokens[0]) if tokens[0] in (0xbc,0xbd) else ''
  tail=''.join('{%02X}'%x for x in (tokens[-2:] if tokens[-2] in (0xb1,0xc2,0xaf) else tokens[-1:]));plan=prefix+plans.BODIES[mid]+tail;
  try:p57.validate_plan(plan,tokens)
  except AssertionError as e:raise AssertionError((mid,plan,src)) from e
  data=codec.encode(plan);assert codec.decode(data)==plan
  refs=[]
  for r in index.get(norm(src['private_text']),[]):
   # Exact normalized full Japanese only. No score/substring acceptance.
   refs.append(dict(file=r['file'],id=r['id'],ja_text_sha256=sha(r['text'].encode()),fr_text_sha256=sha(fr[r['file'],r['id']].encode()),scope='JP_COMPLET_NORMALISE_IDENTIQUE_CONTROLES_ET_ROLES_SFC_CONSERVES'))
  for f,i in (plans.EXTRA_REFS.get(mid,[])):
   full=f if f.startswith('data/') else 'data/MESS6/JA/'+f;r=next(x for x in ja if x['file']==full and x['id']==i);refs.append(dict(file=full,id=i,ja_text_sha256=sha(r['text'].encode()),fr_text_sha256=sha(fr[full,i].encode()),scope='FRAGMENTS_JP_FR_RELUS_COMPOSITION_SFC_EXPLICITE_CONTROLES_CONSERVES'))
  oldtags=[f'{x:02X}' for x in old[mid] if 0xab<=x<=0xc8 and x!=0xad];newtags=[f'{x:02X}' for x in data if 0xab<=x<=0xc8 and x!=0xad]
  rows.append(dict(id=mid,status='RELU_PRET_POUR_INSERTION',semantic_review='RELU_JP_FR_CONTEXTE_DISPONIBLE',source_message_sha256=src['source_message_sha256'],source_text_sha256=src['source_text_sha256'],previous_message_sha256=sha(old[mid]),french_plan=plan,encoded_hex=data.hex(),ds_references=refs,source_context_ids=list(range(max(0,mid-2),min(603,mid+3))),review='Formulation DS adaptée lorsque la phrase japonaise complète normalisée concorde ; sinon adaptation directe SFC, aucun rapprochement flou validé. Noms et quantités restent des commandes natives ; accords évités pour les noms variables.',inherited_language='FRAGMENT_COMPOSITION_RELU' if mid in plans.FRAGMENT_IDS else ('FR_CORRIGE' if mid in plans.INHERITED_FRENCH_IDS else 'ANGLAIS_TRADUIT'),specific_review=plans.NOTES.get(mid,'Sens japonais et français DS disponibles relus ; contrôles et rôles SFC maintenus.'),legacy_command_audit=dict(previous=oldtags,source_and_new=newtags,changed=oldtags!=newtags,reason='Les commandes VF ajoutées ou perdues sont corrigées explicitement vers la séquence JP pour ce seul ID.' if oldtags!=newtags else 'Ordre et nombre conservés ; seuls AD de disposition remplacés par espaces.')))
 return base,rows

def assemble(base,rows):
 main=c.main_regions(base)+[dict(file_offset=ENGINE['offset'],size=ENGINE['size'])];changes={r['id']:bytes.fromhex(r['encoded_hex']) for r in rows};payload=bytearray();starts=[]
 for mid,at,b in old_pool(base):
  if mid%8==0:starts.append(len(payload))
  payload+=changes.get(mid,b)
 off=next(x for x in range(0x771800,0x7b8703-len(payload),256) if all(not(p['file_offset']<x+len(payload) and p['file_offset']+p['size']>x) for p in main));out=bytearray(base);out[off:off+len(payload)]=payload
 for copy in (0,0x400000):
  for g,s in enumerate(starts):out[copy+c.PTR+g*3:copy+c.PTR+g*3+3]=((off+s-0xf6debd)&0xffffff).to_bytes(3,'little')
 checksum=sum(out)&65535
 for copy in (0,0x400000):struct.pack_into('<HH',out,copy+0xffdc,checksum^65535,checksum)
 assert sum(out)&65535==checksum
 return bytes(out),dict(offset=off,size=len(payload),messages=608,groups=76)
