"""Reproducible source/constraint audit of560 pre-existing proposals.
400 explicit semantic review decisions below are not insertion approvals.
"""
from common import *
import argparse,collections
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--ds',type=Path,required=True);p.add_argument('--ips',type=Path,required=True);a=p.parse_args();jp=a.jp.read_bytes();ds=a.ds.read_bytes();ips=a.ips.read_bytes();assert sha(ds)=='5667303e3c7ab518a1b6bb2119abdfcc17422b3387dc5083f67b8e2b54734fb5';assert sha(ips)=='b34155f476d0bce3d2247c577417b3ade3ee071e7c9b8af634f8a7cb613cdd37';base,_=prepare(jp);ns=names(base);codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'));old_resolved={x['position'] for v in ['73','74'] for x in read(R/f'dq6-fr/v0.{v}/preparations-resolues.json')};selected={x['position'] for x in SELECTION}
allrows=[]
for v,span in [('69','0000-0399'),('70','0400-0799'),('71','0800-1199'),('72','1200-2047')]:
 for row in read(R/f'dq6-fr/v0.{v}/registre-positions-{span}.json'):
  if row['status']=='PREPARE_NON_INSERE' and row['position'] not in old_resolved:allrows.append(row)
assert len(allrows)==560;pending=[x for x in allrows if x['position'] not in selected];assert len(pending)==510;batch=pending[:400];assert len(batch)==400 and batch[-1]['position']==1703
sys.path.insert(0,str(R/'dq6-fr'));from probe import lz10
files={x['path']:x for x in read(R/'dq6-fr/clean-base/nds-files.json')};cache={};checked=set()
def verify_ref(ref):
 for lang in ['JA','FR']:
  path=ref[lang+'_file'];key=(path,ref['id']);x=files[path]
  if path not in cache:
   raw=ds[x['offset']:x['offset']+x['size']];raw=lz10(raw) if raw[0]==16 else raw;assert raw[:4]==b'MPT0';size,lo,hi,n,tab,ts,txt=struct.unpack_from('<7I',raw,4);cache[path]={}
   for i in range(n):
    mid,length,off=struct.unpack_from('<HHH',raw,tab+6*i);assert mid not in cache[path];cache[path][mid]=raw[tab+ts+off*4:tab+ts+off*4+length].decode()
  assert cache[path][ref['id']]==ref[lang+'_text'];assert sha(ref[lang+'_text'].encode())==ref[lang+'_sha256'];checked.add(key)
# Reapply only the authorised old VF IPS to pristine JP, in memory.
vf=bytearray(512)+bytearray(jp);i=5;assert ips[:5]==b'PATCH'
while ips[i:i+3]!=b'EOF':
 at=int.from_bytes(ips[i:i+3],'big');n=int.from_bytes(ips[i+3:i+5],'big');i+=5
 if n:data=ips[i:i+n];i+=n
 else:n=int.from_bytes(ips[i:i+2],'big');data=ips[i+2:i+3]*n;i+=3
 assert at+n<=len(vf);vf[at:at+n]=data
assert i+3==len(ips);vf=bytes(vf[512:]);old=names(vf);ot=LogicalTable(vf)
glyphs=struct.unpack_from('<256H',jp,0x11100);jt={int(k,16):v for l in (R/'dq6-fr/upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in l for k,v in [l.split('=',1)] if len(k)<=4}
scan=[];bypos={}
for x in allrows:
 pos=x['position'];sid=x['sids'][0];raw=ns[sid][1];assert sha(raw)==x['current_message_sha256'];unapproved=False
 try:cur=name_text(base,raw,codec)
 except Exception:cur=LogicalTable(base).text(sid);unapproved=True
 assert cur==x['current']
 start=POOL+int.from_bytes(jp[0x165e7+(sid>>4)*3:0x165ea+(sid>>4)*3],'little')
 for _ in range(sid&15):start=jp.index(0xac,start)+1
 src=jp[start:jp.index(0xac,start)];ja=''.join(jt.get(glyphs[v],'<%04X>'%glyphs[v]) for v in src);assert ja==x['sfc_jp'] and sha(src)==x['JP_message_sha256']
 for ref in x['DS_references']:verify_ref(ref);assert field(ref['JA_text'])==ja and field(ref['FR_text'])==x['proposal']
 try:secondary=name_text(base,old[sid][1],codec)
 except Exception:secondary=ot.text(sid)
 assert sha(old[sid][1])==x['secondary_IPS_message_sha256'] and secondary==x['secondary_IPS_text']
 flags=[];proposal=x['proposal'];native=expand(base,raw)[:-1]
 if unapproved:flags.append('LEGACY_GLYPH_DECODE_NOT_APPROVED')
 if set(proposal)-set(codec.forward):flags.append('GLYPH_OR_DS_FORMATTING_NOT_APPROVED')
 if len(proposal)>len(cur):flags.append('LONGER_THAN_OLD_LABEL_NOT_A_WINDOW_MEASUREMENT')
 if any(0x91<=v<=0x9d for v in native):flags.append('NATIVE_LINE_BREAK_REQUIRES_LAYOUT')
 if not x['DS_references']:flags.append('NO_ESTABLISHED_DIRECT_DS_REFERENCE')
 if ja in ['デスタムーア','ダークドレアム','ムドー','まおうのつかい']:flags.append('HOMONYMOUS_PHYSICAL_FORMS')
 rr=dict(position=pos,sids=x['sids'],current=cur,proposal=proposal,sfc_jp=ja,current_sha256=sha(raw),JP_sha256=sha(src),IPS_sha256=sha(old[sid][1]),DS_reference_count=len(x['DS_references']),DS_references_verified_directly=bool(x['DS_references']),technical_flags=flags,status='INTEGRE_v075' if pos in selected else 'PREPARE_NON_INSERE',scope='Audit de sources et contraintes ; aucune largeur de fenêtre naturelle inférée par le nombre de caractères.')
 scan.append(rr);bypos[pos]=rr
special={287:'Le japonais かえる peut désigner changer/échanger ; « Jeter » n’est pas établi. Tracer le menu de cartes et comparer le contexte DS avant choix.',289:'くばる signifie distribuer dans ce contexte probable de cartes ; « DONNER » ne doit pas être validé comme commande générale sans tracé du consommateur.',373:'まおうのこと ne désigne pas explicitement Meurtor. Vérifier le locuteur et le sujet ; « Sur Meurtor » reste une proposition non approuvée.',708:'Le français DS brut contient super$chimérator. Le signe $ doit être interprété selon le format DS ; ni le rendre littéralement ni le remplacer automatiquement.',731:'Le français DS brut contient monstro$lanterne. Résoudre ce marqueur DS avant encodage ; ne pas le présenter comme un nouveau glyphe français.',674:'FR DS féminin : cornacérée. Le genre et les accords du moteur SFC doivent être établis ; le nom plus court seul ne valide pas la composition.',695:'FR DS roi gluant / rois gluants : pluriel interne. Vérifier le moteur grammatical SFC, pas seulement ajouter un s final.',741:'FR DS chef troll / chefs trolls : pluriel des deux mots. Vérifier la composition SFC.',793:'ドラゴラム apparaît dans la table des entités mais est aussi une compétence. « Pouf » ne doit pas être inséré sans établir le rôle de ce SID.',870:'モンスター est un nom japonais alors que « monstrueux » est adjectival. Le champ de titre/fenêtre doit être confirmé avant validation.',847:'かけきん désigne une mise/somme pariée ; « Pariés » dépend d’une composition de compteur. Ne pas le valider comme verbe de commande.',179:'ようすをみる signifie examiner un état ; la restriction aux candidats dépend du menu de recrutement. Contexte nécessaire.'}
review=[]
for x in batch:
 pos=x['position'];r=bypos[pos];refs=x['DS_references'];note=special.get(pos)
 if note:decision='DIFFERE_SENS_FORMAT_OU_COMPOSITION'
 elif pos<400:decision='DIFFERE_REFERENCE_ET_FENETRE';note='Japonais et proposition française relus. Les commandes, noms propres et fragments de menu demandent un champ DS établi et le consommateur naturel ; la traduction anglaise héritée ne suffit pas.'
 elif pos<804:decision='DIFFERE_INSERTION_NOM_MONSTRE';note='Nom japonais SFC et localisation française DS relus comme nom d’espèce ou de personnage dans le bloc monstres. Référence exacte, pas une traduction littérale de l’anglais. Longueur, rupture, glyphes et accords indiqués restent à résoudre ; aucune validation de rencontre naturelle.'
 elif pos<870:decision='DIFFERE_COMPOSITION_ARENE_CASINO';note='Libellé de classement ou compteur relu en regard du japonais/DS. Les ruptures de ligne et la phrase native complète de l’arène/casino restent à tracer.'
 elif pos<919:decision='DIFFERE_TITRE_OU_ESPECE';note='Titre de personnage, commande ou nom d’espèce relu. La même chaîne peut remplir un autre rôle que le nom de monstre ; fenêtre et genre à confirmer.'
 elif pos<1103:decision='DIFFERE_RANG_VOCATION';note='Rang japonais et titre français DS relus. La localisation DS peut s’éloigner de la traduction littérale ; conserver sa graphie, mais vérifier variante de genre et fenêtre avant insertion.'
 elif pos<1326:decision='DIFFERE_LIBELLE_ACTION';note='Compétence japonaise et nom français DS relus ; distinguer l’action des armes et sorts homonymes. Longueur, format natif et contexte de commande restent à vérifier.'
 else:decision='DIFFERE_NOM_OBJET';note='Nom japonais d’équipement et nom français DS complet relus ; distinguer arme, accessoire et compétence homonymes. Ne pas tronquer le nom officiel pour satisfaire la longueur héritée ; mise en page/glyphes encore à résoudre.'
 if refs and '@0F@' in refs[0]['FR_text']:note+=' La source DS indique un nom féminin : vérifier articles et accords SFC.'
 review.append(dict(position=pos,sids=x['sids'],sfc_jp=x['sfc_jp'],current=x['current'],proposal=x['proposal'],DS_references=refs,decision=decision,review_note=note,technical_flags=r['technical_flags'],status='PREPARE_NON_INSERE',new_position_examined=False,proposal_semantically_reread=True,insertion_approved=False,natural_context_validated=False,source_audit='audit-560-propositions.json'))
for i in range(2):(O/f'revue-propositions-400-part{i+1}.json').write_text(json.dumps(review[i*200:(i+1)*200],ensure_ascii=False,indent=2)+'\n')
(O/'audit-560-propositions.json').write_text(json.dumps(scan,ensure_ascii=False,indent=2)+'\n')
q=dict(release='v0.75',source_SHA256=dict(JP=sha(jp),DS=sha(ds),IPS=sha(ips)),pending_before=560,inserted_from_preparations=50,pending_after=510,technical_source_checks=560,direct_JP_messages_verified=560,secondary_IPS_messages_verified=560,rows_with_direct_DS_references=sum(bool(x['DS_references']) for x in allrows),unique_DS_fields_verified=len(checked),semantic_proposals_reread_after_selection=400,semantic_review_ids=[x['position'] for x in review],semantic_review_IDs_sha256=sha(json.dumps([x['position'] for x in review]).encode()),not_in_semantic_batch=110,next_pending_position=pending[400]['position'],new_physical_positions_examined=0,semantic_insertion_approvals_from_batch400=0,new_translations_from_batch400=0,decisions=dict(collections.Counter(x['decision'] for x in review)),limits='Les propositions étaient déjà préparées. Ce lot approfondit leur relecture et isole les réserves, sans les recompter comme nouveaux textes, nouvelles préparations ou traductions intégrées. Le comptage des caractères est une comparaison historique, pas une mesure de fenêtre naturelle.')
(O/'qa-revue-propositions-400.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in q.items() if k!='semantic_review_ids'},ensure_ascii=False))
