from pathlib import Path
import sys,importlib.util,json,hashlib,struct,re
O=Path(__file__).resolve().parent;R=O.parents[1]
def module(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
sys.path.insert(0,str(R/'dq6-fr/v0.71'));parent=module('parent72',R/'dq6-fr/v0.71/common.py');c=parent.c;sha=parent.sha;read=parent.read;patches=parent.patches;Codec=parent.Codec;names=parent.names;decode_pool=parent.decode_pool;expand=parent.expand;LogicalTable=parent.LogicalTable;cpu_for_file=parent.cpu_for_file
class Codec(parent.Codec):
 def __init__(self,rom,charset):
  super().__init__(rom,charset);assert int.from_bytes(rom[0x11100+2*0x85:0x11102+2*0x85],'little')==0x240;self.forward[':']=0x85
 def decode(self,data):return ''.join(':' if b==0x85 else super(Codec,self).decode(bytes([b])) for b in data)
BASE=read(R/'dq6-fr/v0.71/build-report.json');POOL=parent.POOL;TAIL=parent.TAIL;END=parent.END;NAME=parent.NAME;NAME_LIMIT=parent.NAME_LIMIT;NAME_BASE_CPU=parent.NAME_BASE_CPU
plans=module('plans72',O/'plans.py');PLANS=plans.PLANS;UNCHANGED=plans.UNCHANGED;PREPARED=plans.PREPARED;NEW_SIDS=sorted(sid for pos in PLANS for sid in plans.POSITION_SIDS[pos]);SIDS=NEW_SIDS;TEST_SIDS=SIDS
field=lambda s:(re.search(r'@4([^@]+)',s) or re.search(r'@1([^@]+)',s))[1].replace(';','') if re.search(r'@(?:1|4)([^@]+)',s) else None

PREVIOUS_CONFIRMED=[164, 165, 167, 171, 172, 174, 182, 186, 191, 210, 215, 216, 217, 218, 220, 221, 227, 229, 231, 232, 233, 237, 240, 242, 244, 250, 251, 252, 276, 277, 335, 340, 349, 353, 358, 366, 369, 370, 371, 374, 417, 418, 419, 420, 422, 423, 424, 425, 426, 427, 428, 429, 430, 432, 434, 435, 436, 437, 441, 442, 443, 444, 450, 464, 466, 470, 473, 481, 490, 491, 517, 544, 545, 546, 548, 550, 555, 559, 572, 578, 584, 585, 586, 587, 589, 590, 592, 595, 596, 598, 600, 601, 604, 610, 611, 612, 614, 619, 620, 781, 866, 873, 874, 901, 903, 904, 905, 907, 908, 912, 913, 914, 922, 927, 928, 929, 931, 946, 947, 957, 962, 965, 974, 991, 993, 995, 1006, 1018, 1019, 1022, 1028, 1029, 1030, 1047, 1106, 1109, 1112, 1115, 1117, 1121, 1124, 1125, 1128, 1140, 1141, 1147, 1148, 1156, 1163, 1164, 1175, 1188, 1247, 1250, 1252, 1845, 1846, 1847, 1848, 1849, 1888]

def prepare(jp):
 assert sha(jp)=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e'
 patch=(R/'patches/DQVI-FR-DS-v0.71-BASE-JP-PARTIEL.bps').read_bytes();assert sha(patch)==BASE['BPS_sha256'];m=module('bps69',R/'dq6-fr/upstream/refill/patchRM.py');base=bytes(m.apply_bps(jp,patch));assert sha(base)==BASE['ROM_sha256'];codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'));ns=names(base);tab=LogicalTable(base);pairs={base[0x3fb50+2*i:0x3fb52+2*i]:0xc9+i for i in range(50)}
 ja={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-ja.json')};fr={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-fr.json')};glyphs=struct.unpack_from('<256H',jp,0x11100);jt={int(k,16):v for l in (R/'dq6-fr/upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in l for k,v in [l.split('=',1)] if len(k)<=4}
 def ref(f,i):
  jf='data/MENULIST6/JA/b100'+f+'.mpt';ff=jf.replace('/JA/','/FR/');j=ja[jf,i];f=fr[ff,i];return dict(JA_file=jf,FR_file=ff,id=i,JA_text=j['text'],FR_text=f['text'],JA_sha256=sha(j['text'].encode()),FR_sha256=sha(f['text'].encode()))
 rows=[];changes={};ledger=[];lookup=[]
 for (f,i),j in ja.items():
  if '/MENULIST6/JA/' in f and not f.endswith('b1090000.mpt') and (f.replace('/JA/','/FR/'),i) in fr:lookup.append((j,fr[f.replace('/JA/','/FR/'),i]))
 for pos in range(1200,2048):
  sids=[sid for sid in range(2512) if tab.position(sid)==pos];sid=sids[0];at,old=ns[sid]
  try:cur=codec.decode(old)[:-4]
  except Exception:cur=tab.text(sid)
  a=POOL+int.from_bytes(jp[0x165e7+(sid>>4)*3:0x165ea+(sid>>4)*3],'little')
  for _ in range(sid&15):a=jp.index(0xac,a)+1
  source_at=a;raw=jp[a:jp.index(0xac,a)];source=''.join(jt.get(glyphs[b],'<%04X>'%glyphs[b]) for b in raw);refs=[]
  if pos>=2042:source='[SOURCE_JP_OPAQUE_APRES_SID_09C9]'
  if pos in PLANS:
   french,f,i,review=PLANS[pos];refs=[ref(f,i)] if f else []
   helper=parent
   while not hasattr(helper,'packed'):helper=helper.parent
   new=helper.packed(codec,pairs,french)
   assert codec.decode(new)==french+'{AC}' and len(french)<=len(cur),(pos,french,cur)
   assert len(sids)==1 and sid in plans.POSITION_SIDS[pos] and not any(0xab<=v<=0xc8 for v in new[:-1]+old[:-1]);changes[at]=new
   rows.append(dict(sid=sid,position=pos,french=french,previous=cur,sfc_jp=source,review=review,DS_references=refs,old_encoded_hex=old.hex(),encoded_hex=new.hex(),old_sha256=sha(old),new_sha256=sha(new),old_columns=len(cur),new_columns=len(french),status='RELU_POUR_INSERTION'))
   status='REVISION_FR_EXISTANT' if pos in plans.CORRECTED_EXISTING else 'TRADUCTION_SELECTIONNEE';reason=review
  elif pos in UNCHANGED:
   candidates=[(j,f) for j,f in lookup if field(j['text'])==source and field(f['text'])==cur];assert candidates,(pos,source,cur)
   j,f=candidates[0];refs=[dict(JA_file=j['file'],FR_file=f['file'],id=j['id'],JA_text=j['text'],FR_text=f['text'],JA_sha256=sha(j['text'].encode()),FR_sha256=sha(f['text'].encode()))];status='FR_EXISTANT_RELU_SOURCE';reason='Vocation Sage/Ranger oupersonnage Amos : JP etFRDS exacts, rôle relu ; pas de nouvelle traduction ni scène naturelle revendiquée.'
  elif pos in PREVIOUS_CONFIRMED:status='FR_CONFIRME_ANTERIEUR';reason='Traduction déjà qualifiée avant ce lot ; conservée, pas de nouvelle traduction.'
  elif pos in PREPARED:
   proposal=PREPARED[pos];hits=[(j,f) for j,f in lookup if field(j['text'])==source and field(f['text'])==proposal];assert hits,(pos,source,proposal)
   j,f=hits[0];refs=[dict(JA_file=j['file'],FR_file=f['file'],id=j['id'],JA_text=j['text'],FR_text=f['text'],JA_sha256=sha(j['text'].encode()),FR_sha256=sha(f['text'].encode()))]
   problems=[]
   if len(proposal)>len(cur):problems.append('largeur '+str(len(proposal))+' contre '+str(len(cur)))
   if set(proposal)-set(codec.forward):problems.append('glyphes non approuvés '+repr(sorted(set(proposal)-set(codec.forward))))
   if any(0xab<=v<=0xc8 for v in old[:-1]):problems.append('commande native à préserver/composer')
   if '|' in cur:problems.append('saut de ligne natif')
   if source in ['デスタムーア','ムドー','ダークドレアム','まおうのつかい']:problems.append('variantes physiques homonymes à traiter ensemble')
   if not problems:problems.append('proposition source repérée, relecture détaillée et test de composition reportés')
   status='PREPARE_NON_INSERE';reason='Proposition DS '+proposal+' : '+ '; '.join(problems)+'. Pas une traduction qualifiée ; accords et contexte naturel non validés.'
  elif pos>=2042:status='DIFFERE_SOURCE_JP_OPAQUE';reason='VFvide ; JP séquentiel aprèsSID09C9 entre dans des octets non qualifiés comme texte dès3BC76D. Limite source inférée,consommateurs àauditer ; ne pas traduire le décodage de code/données.'
  elif 2007<=pos<=2041:status='STRUCTURE_DYNAMIQUE_WRAM';reason='SID09A7..09C9 redirigé parC44FDF versWRAM ; slotvide conservé,pas un dialogue àtraduire ni une preuve de rendu français dynamique.'
  elif pos==2006:status='RESERVE_VIDE_A_TRACER';reason='SID09A6 statique vide avant les35SIDs dynamiques ; accès àtracer,aucune traduction inventée.'
  elif pos>=1931:status='DIFFERE_LISTE_NOMS_A_TRACER';reason='Séquence de termes de saisie etnoms propres,potentiellement fonctionnelle ; ne pas traduire sans tracer le consommateur ni supposer du texte visible.'
  elif 1326<=pos<=1602:status='DIFFERE_COMPOSITION_NATIVE';reason='Fragment de description assemblée : voisinageJP/FR relu,anglais parfois faux. Adapter une phrase complète après traçage natif, pas un fragment d’après un nomDS homonyme.'
  elif 1254<=pos<=1325:status='DIFFERE_ACTION_SPECIFIQUE';reason='Commande mémoire ouaction technique/dejeu ; plusieursDS sont des échosjaponais,pas du français. Usage/chaîne àétablir.'
  elif not cur:status='VIDE_A_QUALIFIER';reason='Slotvide,rôle àconfirmer ; aucune traduction inventée.'
  elif re.fullmatch(r'[M*][0-9A-F]{3}',cur):status='DIFFERE_IDENTIFIANT';reason='Identifiant hérité,usage ettraduction àqualifier.'
  elif 1824<=pos<=1844:status='DIFFERE_VOCATION_GENRE';reason='Vocation ouoptionDS genrée/multiple : résoudre sans choix arbitraire.'
  elif 1851<=pos<=1924:status='DIFFERE_NOM_RECRUTABLE';reason='NompropreSFC sanscorrespondanceDS univoque ; pas une francisation phonétique seule.'
  else:status='DIFFERE_TEXTE_CONTEXTE';reason='Texte examiné,référenceDS/largeur/glyphes/commandes àétablir avant intégration.'
  ledger.append(dict(position=pos,sids=sids,current=cur,sfc_jp=source,current_message_sha256=sha(old),JP_message_sha256=sha(raw),JP_source_offset=source_at,JP_source_length=len(raw),status=status,reason=reason,DS_references=refs,proposal=PREPARED.get(pos),position_examined=True,natural_context_validated=False))
 assert [x['sid'] for x in rows]==SIDS and len(ledger)==848
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
