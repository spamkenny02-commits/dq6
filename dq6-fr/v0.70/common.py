from pathlib import Path
import sys,importlib.util,json,hashlib,struct,re
O=Path(__file__).resolve().parent;R=O.parents[1]
def module(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
sys.path.insert(0,str(R/'dq6-fr/v0.69'));parent=module('parent70',R/'dq6-fr/v0.69/common.py');c=parent.c;sha=parent.sha;read=parent.read;patches=parent.patches;Codec=parent.Codec;names=parent.names;decode_pool=parent.decode_pool;expand=parent.expand;LogicalTable=parent.LogicalTable;cpu_for_file=parent.cpu_for_file
class Codec(parent.Codec):
 def __init__(self,rom,charset):
  super().__init__(rom,charset);assert int.from_bytes(rom[0x11100+2*0x85:0x11102+2*0x85],'little')==0x240;self.forward[':']=0x85
 def decode(self,data):return ''.join(':' if b==0x85 else super(Codec,self).decode(bytes([b])) for b in data)
BASE=read(R/'dq6-fr/v0.69/build-report.json');POOL=parent.POOL;TAIL=parent.TAIL;END=parent.END;NAME=parent.NAME;NAME_LIMIT=parent.NAME_LIMIT;NAME_BASE_CPU=parent.NAME_BASE_CPU
plans=module('plans70',O/'plans.py');PLANS=plans.PLANS;UNCHANGED=plans.UNCHANGED;PREPARED=plans.PREPARED;NEW_SIDS=sorted(PLANS);SIDS=NEW_SIDS;TEST_SIDS=SIDS
field=lambda s:(re.search(r'@4([^@]+)',s) or re.search(r'@1([^@]+)',s))[1].replace(';','') if re.search(r'@(?:1|4)([^@]+)',s) else None

PREVIOUS_CONFIRMED=[164, 165, 167, 171, 172, 174, 182, 186, 191, 210, 215, 216, 217, 218, 220, 221, 227, 229, 231, 232, 233, 237, 240, 242, 244, 250, 251, 252, 276, 277, 335, 340, 349, 353, 358, 366, 369, 370, 371, 374, 417, 418, 419, 420, 422, 423, 424, 425, 426, 427, 428, 429, 430, 432, 434, 435, 436, 437, 441, 442, 443, 444, 450, 464, 466, 470, 473, 481, 490, 491, 517, 781, 873, 874, 1106, 1112, 1115, 1117, 1121, 1124, 1125, 1128, 1140, 1141, 1147, 1148, 1156, 1163, 1164, 1175, 1188, 1247, 1250, 1252, 1845, 1846, 1847, 1848, 1849, 1888]

def prepare(jp):
 assert sha(jp)=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e'
 patch=(R/'patches/DQVI-FR-DS-v0.69-BASE-JP-PARTIEL.bps').read_bytes();assert sha(patch)==BASE['BPS_sha256'];m=module('bps69',R/'dq6-fr/upstream/refill/patchRM.py');base=bytes(m.apply_bps(jp,patch));assert sha(base)==BASE['ROM_sha256'];codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'));ns=names(base);tab=LogicalTable(base);pairs={base[0x3fb50+2*i:0x3fb52+2*i]:0xc9+i for i in range(50)}
 ja={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-ja.json')};fr={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-fr.json')};glyphs=struct.unpack_from('<256H',jp,0x11100);jt={int(k,16):v for l in (R/'dq6-fr/upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in l for k,v in [l.split('=',1)] if len(k)<=4}
 def ref(f,i):
  jf='data/MENULIST6/JA/b100'+f+'.mpt';ff=jf.replace('/JA/','/FR/');j=ja[jf,i];f=fr[ff,i];return dict(JA_file=jf,FR_file=ff,id=i,JA_text=j['text'],FR_text=f['text'],JA_sha256=sha(j['text'].encode()),FR_sha256=sha(f['text'].encode()))
 rows=[];changes={};ledger=[];lookup=[]
 for (f,i),j in ja.items():
  if '/MENULIST6/JA/' in f and not f.endswith('b1090000.mpt') and (f.replace('/JA/','/FR/'),i) in fr:lookup.append((j,fr[f.replace('/JA/','/FR/'),i]))
 for pos in range(400,800):
  sids=[sid for sid in range(2512) if tab.position(sid)==pos];sid=sids[0];at,old=ns[sid]
  try:cur=codec.decode(old)[:-4]
  except Exception:cur=tab.text(sid)
  a=POOL+int.from_bytes(jp[0x165e7+(sid>>4)*3:0x165ea+(sid>>4)*3],'little')
  for _ in range(sid&15):a=jp.index(0xac,a)+1
  raw=jp[a:jp.index(0xac,a)];source=''.join(jt.get(glyphs[b],'<%04X>'%glyphs[b]) for b in raw);refs=[]
  if pos in PLANS:
   french,f,i,review=PLANS[pos];refs=[ref(f,i)] if f else [];new=parent.parent.parent.packed(codec,pairs,french)
   assert codec.decode(new)==french+'{AC}' and len(french)<=len(cur),(pos,french,cur)
   assert len(sids)==1 and sid==pos and not any(0xab<=v<=0xc8 for v in new[:-1]+old[:-1]);changes[at]=new
   rows.append(dict(sid=sid,position=pos,french=french,previous=cur,sfc_jp=source,review=review,DS_references=refs,old_encoded_hex=old.hex(),encoded_hex=new.hex(),old_sha256=sha(old),new_sha256=sha(new),old_columns=len(cur),new_columns=len(french),status='RELU_POUR_INSERTION'))
   status='TRADUCTION_SELECTIONNEE';reason=review
  elif pos in UNCHANGED:
   candidates=[(j,f) for j,f in lookup if field(j['text'])==source and field(f['text'])==cur];assert candidates,(pos,source,cur)
   j,f=candidates[0];refs=[dict(JA_file=j['file'],FR_file=f['file'],id=j['id'],JA_text=j['text'],FR_text=f['text'],JA_sha256=sha(j['text'].encode()),FR_sha256=sha(f['text'].encode()))];status='FR_EXISTANT_RELU_SOURCE';reason='Libellé simple ou nom propre identique à la source française DS,JA exact; pas de modification, pas de nouvelle traduction. Fenêtre naturelle non parcourue.'
  elif pos in PREVIOUS_CONFIRMED:status='FR_CONFIRME_ANTERIEUR';reason='Traduction déjà qualifiée avant ce lot ; conservée, pas de nouvelle traduction.'
  elif pos in PREPARED:
   proposal=PREPARED[pos];hits=[(j,f) for j,f in lookup if field(j['text'])==source and field(f['text'])==proposal];assert hits,(pos,source,proposal)
   j,f=hits[0];refs=[dict(JA_file=j['file'],FR_file=f['file'],id=j['id'],JA_text=j['text'],FR_text=f['text'],JA_sha256=sha(j['text'].encode()),FR_sha256=sha(f['text'].encode()))]
   problems=[]
   if len(proposal)>len(cur):problems.append('largeur '+str(len(proposal))+' contre '+str(len(cur)))
   if set(proposal)-set(codec.forward):problems.append('glyphes non approuvés '+repr(sorted(set(proposal)-set(codec.forward))))
   if any(0xab<=v<=0xc8 for v in old[:-1]):problems.append('commande native à préserver/composer')
   if '|' in cur:problems.append('saut de ligne natif')
   if pos in [574,793]:problems.append('nom de capacité aussi présent en table entités : rôle exact à tracer')
   if source in ['デスタムーア','ムドー','ダークドレアム','まおうのつかい']:problems.append('variantes physiques homonymes à traiter ensemble')
   if not problems:problems.append('proposition source repérée, relecture détaillée et test de composition reportés')
   status='PREPARE_NON_INSERE';reason='Proposition DS '+proposal+' : '+ '; '.join(problems)+'. Pas une traduction qualifiée ; accords et contexte naturel non validés.'
  elif pos<415:status='DIFFERE_MENU_TECHNIQUE';reason='Menu diagnostic ou identifiant de carte, accès naturel/consommateur à établir ; aucune entrée supposée inutilisée.'
  elif not cur:status='VIDE_A_QUALIFIER';reason='Emplacement vide : rôle structurel et accès à établir, pas une traduction inventée.'
  elif re.fullmatch(r'(?:M[0-9A-F]{3}|[A-Z]+[0-9]+[A-Z]?)',cur):status='DIFFERE_IDENTIFIANT';reason='Identifiant de carte/test conservé ; la présence éventuelle d’un nom JP ne suffit pas à prouver son usage visible.'
  elif pos<544:status='DIFFERE_LIEU';reason='Lieu examiné. Référence DS exacte, largeur/commande et contexte de destination à établir ; préparations antérieures438/479 conservées.'
  else:status='DIFFERE_MONSTRE_CONTEXTE';reason='Nom de monstre ou entité technique examiné : référence DS non unique/absente, commande ou variante à lever avant qualification.'
  ledger.append(dict(position=pos,sids=sids,current=cur,sfc_jp=source,current_message_sha256=sha(old),JP_message_sha256=sha(raw),status=status,reason=reason,DS_references=refs,proposal=PREPARED.get(pos),position_examined=True,natural_context_validated=False))
 assert [x['sid'] for x in rows]==SIDS and len(ledger)==400
 payload=bytearray();moved={}
 for at,old in sorted(dict(ns).items()):moved[str(at)]=len(payload);payload+=changes.get(at,old)
 assert NAME+len(payload)<=NAME_LIMIT
 regions=c.main_regions(base)+[dict(file_offset=BASE['placement']['offset'],size=BASE['placement']['size']),dict(file_offset=BASE['engine']['allocation']['offset'],size=BASE['engine']['allocation']['size'])]
 assert all(not(x['file_offset']<NAME+len(payload) and x['file_offset']+x['size']>NAME) for x in regions)
 return base,dict(rows=rows,ledger=ledger,payload_hex=payload.hex(),moved=moved)

def assemble(base,m):
 out=bytearray(base);ns=names(base);payload=bytes.fromhex(m['payload_hex']);out[NAME:NAME+len(payload)]=payload
 for copy in (0,0x400000):
  for g in range(157):out[copy+0x165e7+g*3:copy+0x165ea+g*3]=((NAME+m['moved'][str(ns[g*16][0])]-NAME_BASE_CPU)&0xffffff).to_bytes(3,'little')
 checksum=sum(out)&65535
 for copy in (0,0x400000):struct.pack_into('<HH',out,copy+0xffdc,checksum^65535,checksum)
 assert sum(out)&65535==checksum
 return bytes(out)
