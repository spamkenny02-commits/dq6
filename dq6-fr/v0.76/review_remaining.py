"""Finish the110 pending proposal reviews, without replaying v075's400.
Direct ROM source verification accompanies the explicit semantic notes below.
"""
from common import *
import argparse,collections
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--ds',type=Path,required=True);p.add_argument('--ips',type=Path,required=True);a=p.parse_args();jp=a.jp.read_bytes();ds=a.ds.read_bytes();ips=a.ips.read_bytes();assert sha(ds)=='5667303e3c7ab518a1b6bb2119abdfcc17422b3387dc5083f67b8e2b54734fb5';assert sha(ips)=='b34155f476d0bce3d2247c577417b3ade3ee071e7c9b8af634f8a7cb613cdd37';base,_=prepare(jp);ns=names(base);codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'));tab=LogicalTable(base)
scan=read(R/'dq6-fr/v0.75/audit-560-propositions.json');prior=read(R/'dq6-fr/v0.75/qa-revue-propositions-400.json');done=set(prior['semantic_review_ids']);batch=[x for x in scan if x['status']=='PREPARE_NON_INSERE' and x['position'] not in done];assert len(batch)==110 and len(done|{x['position'] for x in batch})==510;assert not done&{x['position'] for x in batch}
refs={}
for v,span in [('69','0000-0399'),('70','0400-0799'),('71','0800-1199'),('72','1200-2047')]:
 for x in read(R/f'dq6-fr/v0.{v}/registre-positions-{span}.json'):refs[x['position']]=x['DS_references']
sys.path.insert(0,str(R/'dq6-fr'));from probe import lz10
files={x['path']:x for x in read(R/'dq6-fr/clean-base/nds-files.json')};cache={};checked=set()
def check(ref):
 for lang in ['JA','FR']:
  path=ref[lang+'_file'];x=files[path]
  if path not in cache:
   raw=ds[x['offset']:x['offset']+x['size']];raw=lz10(raw) if raw[0]==16 else raw;assert raw[:4]==b'MPT0';size,lo,hi,n,at,ts,txt=struct.unpack_from('<7I',raw,4);cache[path]={}
   for i in range(n):
    mid,length,off=struct.unpack_from('<HHH',raw,at+6*i);assert mid not in cache[path];cache[path][mid]=raw[at+ts+off*4:at+ts+off*4+length].decode()
  assert cache[path][ref['id']]==ref[lang+'_text'];assert sha(ref[lang+'_text'].encode())==ref[lang+'_sha256'];checked.add((path,ref['id']))
vf=bytearray(512)+bytearray(jp);i=5;assert ips[:5]==b'PATCH'
while ips[i:i+3]!=b'EOF':
 at=int.from_bytes(ips[i:i+3],'big');n=int.from_bytes(ips[i+3:i+5],'big');i+=5
 if n:data=ips[i:i+n];i+=n
 else:n=int.from_bytes(ips[i:i+2],'big');data=ips[i+2:i+3]*n;i+=3
 assert at+n<=len(vf);vf[at:at+n]=data
assert i+3==len(ips);old=names(bytes(vf[512:]));glyphs=struct.unpack_from('<256H',jp,0x11100);jt={int(k,16):v for l in (R/'dq6-fr/upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in l for k,v in [l.split('=',1)] if len(k)<=4};selected={x['position'] for x in SELECTION}
special={1762:'きん est or : le français DS brassard d’or corrige le Silver hérité. Ne pas confondre cet accessoire avec les autres bracelets ; disposition native à résoudre.',1770:'くじけぬこころ désigne un cœur qui ne fléchit pas ; Broken Heart inverse le sens. La localisation DS cœur impétueux est retenue comme proposition, avec œ non approuvé et composition à vérifier.',1782:'まほうのせいすい est l’eau magique ; Sage’s Stone hérité est faux. La proposition DS fiole d’eau magique est distincte de la pierre philosophale1784 ; largeur à traiter.',1784:'けんじゃのいし est la pierre philosophale DS, distincte de l’eau magique1782. Recovery Stone hérité ne doit pas servir de référence principale.',1797:'Le décodage ancien contient un glyphe non approuvé88. Le nom DS rosée onirique est relu mais l’encodage source et sa rupture doivent être audités avant remplacement.',1820:'Le japonais ドラゴンのさとり renvoie à l’accès à la vocation dragon ; le champ FR DS Vitesse de dragon est sémantiquement inhabituel. Tracer l’usage réel de cet objet DS et le code objet SFC avant validation, sans inventer un nom alternatif.',1821:'はぐれのさとり donne accès à une vocation ; vérifier le rôle du livre/enseignement et la correspondance objet DS avant insertion de esprit de mercure.',1929:'Tactique de conservation de la vie : le libellé DS Soins avant tout est relu, mais doit être contrôlé avec les fragments tactiques et la fenêtre native.',1930:'Tactique de commandes manuelles : Suivre les ordres est distinct de Me couvrir et Pas de magie. Disposition et fragments natifs à vérifier.'}
review=[]
for x in batch:
 pos=x['position'];sid=x['sids'][0];raw=ns[sid][1];assert sha(raw)==x['current_sha256']
 try:cur=name_text(base,raw,codec)
 except Exception:cur=tab.text(sid)
 assert cur==x['current'] and sha(old[sid][1])==x['IPS_sha256']
 start=POOL+int.from_bytes(jp[0x165e7+(sid>>4)*3:0x165ea+(sid>>4)*3],'little')
 for _ in range(sid&15):start=jp.index(0xac,start)+1
 source=jp[start:jp.index(0xac,start)];ja=''.join(jt.get(glyphs[b],'<%04X>'%glyphs[b]) for b in source);assert ja==x['sfc_jp'] and sha(source)==x['JP_sha256']
 for ref in refs[pos]:check(ref);assert field(ref['JA_text'])==ja and field(ref['FR_text'])==x['proposal']
 if pos in selected:decision='INTEGRE_v076';note='Nom complet DS relu et sélectionné ; disposition en deux lignes dans les longueurs anciennes. Métadonnée de rupture recalculée, isolée et testée dans les rapports natifs.'
 elif pos in special:decision='DIFFERE_SENS_COMPOSITION_OU_SOURCE';note=special[pos]
 elif pos>=1851:decision='DIFFERE_NOM_RECRUTABLE';note='Nom propre japonais et nom français DS relus. Établir l’association au personnage/monstre recruté SFC, sa largeur naturelle et le rôle des noms par défaut ; ne pas importer un nom homonyme sur la seule graphie.'
 else:decision='DIFFERE_NOM_OBJET';note='Japonais et nom français DS complet relus comme équipement, accessoire ou objet clé. La localisation DS peut différer du sens littéral ; conserver la proposition entière, sans troncature. Les réserves de glyphes, longueur et composition native indiquées restent ouvertes.'
 review.append(dict(position=pos,sids=x['sids'],sfc_jp=ja,current=cur,proposal=x['proposal'],DS_references=refs[pos],decision=decision,review_note=note,technical_flags=x['technical_flags'],status='INTEGRE_v076' if pos in selected else 'PREPARE_NON_INSERE',proposal_semantically_reread=True,natural_context_validated=False,JP_sha256=sha(source),IPS_sha256=sha(old[sid][1])))
(O/'revue-110-propositions.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
q=dict(release='v0.76',new_semantic_proposals_reread=110,reviewed_positions=[x['position'] for x in review],prior400_not_replayed=True,semantic_review_cycle_completed=510,initial560_minus_v075_resolved50=510,proposals_resolved_this_release=14,resolved_from_new110=sum(x['position'] in selected for x in batch),resolved_from_prior400=7,pending_names_after=496,new_preparations=0,direct_JP_messages_checked=110,secondary_IPS_messages_checked=110,unique_DS_fields_checked=len(checked),rows_with_direct_DS_refs=sum(bool(refs[x['position']]) for x in batch),source_SHA256=dict(JP=sha(jp),DS=sha(ds),IPS=sha(ips)),full_main_reread_recorded=0,natural_validation=False,decisions=dict(collections.Counter(x['decision'] for x in review)),limits='Relecture des propositions préparées, pas nouveau parcours des2048 ni validation des scènes naturelles. Les réserves de la v075 restent ouvertes sauf14résolutions explicites.')
(O/'qa-revue-110.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in q.items() if k!='reviewed_positions'},ensure_ascii=False))
