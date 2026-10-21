"""Prepare107 French battle translations; NEVER writes ROM bytes or insertion files.
Public output: newly authored French plans, IDs, controls, references and hashes.
Japanese decoded source and DS texts are read locally, not exported in reports.
"""
from pathlib import Path
import json,re,struct,hashlib,argparse,importlib.util,collections,sys
O=Path(__file__).resolve().parent;R=O.parents[1];D=R/'dq6-fr';sys.path.insert(0,str(O));from plans_fr import PLANS,SEMANTIC_RESERVES
sha=lambda b:hashlib.sha256(b).hexdigest();read=lambda p:json.loads(p.read_text())
def checked_source(raw):
 assert sha(raw)=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e','Wrong JP source'
def source_rows(jp):
 checked_source(jp);glyphs=struct.unpack_from('<256H',jp,0x11100);table={int(k,16):v for l in (D/'upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in l for k,v in [l.split('=',1)] if len(k)<=4};rows=[]
 # C9 begins voiced kana in JP, but begins the dictionary in this VF.
 # Thus C9..CD must NEVER be genericized into battle variables in JP.
 for group in range(76):
  p=0x36debd+int.from_bytes(jp[0x15ad1+group*3:0x15ad4+group*3],'little')
  for low in range(8):
   start=p;ts=[]
   while jp[p] not in [0xac,0xae]:ts.append(jp[p]);p+=1;assert p-start<4096
   ts.append(jp[p]);p+=1;text=''.join('['+f'{b:02X}'+']' if 0xab<=b<=0xc8 else table.get(glyphs[b],'<UNKNOWN>') for b in ts);rows.append(dict(id=group*8+low,private_text=text,private_tokens=ts,source_text_sha256=sha(text.encode()),source_message_sha256=sha(bytes(ts))))
 return rows
LAYOUT={0xad}
def native_tags(plan):return [int(x,16) for x in re.findall(r'\{([A-F0-9]{2})\}',plan)]
def validate_plan(plan,source):
 tags=native_tags(plan);assert not any(c in re.sub(r'\{[A-F0-9]{2}\}','',plan) for c in '{}%@'),'Unresolved markup'
 assert all(0xab<=t<=0xc8 for t in tags),'Unknown byte-system control'
 expected=[t for t in source if 0xab<=t<=0xc8 and t not in LAYOUT];assert [t for t in tags if t not in LAYOUT]==expected,'Native order/count changed'
 assert tags[-1]==source[-1] and source[-1] in [0xac,0xae]
NOTES={
390:'La DS fait voler le personnage puis tomber. Le japonais SFC dit poursuivre sa course et disparaître : garder le SFC, sans chute ajoutée.',
414:'DS FR dit tous les PM ; le SFC n’énonce pas la quantité. Préparation sans tous.',
415:'B8 est la cible et BB le nombre SFC, malgré les rôles/indices de variables DS différents. PM doit encore être confronté aux glyphes byte0D/0E avant encodage.',
454:'B7 puis B2, source de la voix. Ne pas permuter les variables comme le français DS ; type de chaîne B2 à établir dans cet appel, pas forcément un sort.',
455:'B8 puis B2 conservés ; même réserve sur la voix et le type de chaîne B2.',
464:'Le shiritori ne devient pas automatiquement le virelangue DS : réserve de cohérence avec465.',
465:'La DS supprime le mot variable B2 dans son virelangue. Préparation littérale seulement, adaptation française non approuvée ; conserver B2 et deux B7.',
467:'La DS remplace le gag coquin et le nez qui saigne par une blague. Le SFC conserve son gag allusif ; trois B7 et trois B1 conservés, pas d’acte explicite ajouté.',
469:'La DS parle de mixture ; le SFC donne de l’alcool et une réplique différente. Le SFC est conservé, sans transformer la réplique en simples glouglous.',
499:'Le SFC imite précisément la voix B3. La DS FR omet ce nom : B3 et toutes les occurrences B7 restent présentes, pas de simple prise de commandement.',
501:'ザオリーマ est rendu Dingue-dong dans DS0802:282/285. Choisir la réplique générique, sans importer les variantes vocales conditionnelles DS ; aucune nouvelle variable ajoutée.',
507:'Ordre cible B8 puis acteur B7 maintenu, même si DS FR inverse les deux.',
510:'La DS omet le nom de la personne admirée : B8 puis B7 restent tous deux dans la préparation SFC.',
512:'DS utilise une variable cible ; ce message SFC utilise B7 acteur. Ne pas remplacer B7 par B8 à cause de la concordance lexicale.',
519:'Pile selon DS0802:343, convention de localisation relue, pas une déduction omote/ura.',
520:'Face selon DS0802:346 ; cohérent avec519 et la convention officielle DS.',
521:'SFC B8 cible conservée malgré le rôle acteur de la variante DS.',
524:'デュラン est Dragore dans DS0802:355–360, pas une translittération supposée. Citation neutralisée gagner en force pour ne pas imposer un accord de genre ; trois B7 et quatre B1 conservés.',
527:'Le SFC dit faire sa toilette ; ne pas imposer le s’épousseter DS à un acteur possiblement animal.',
538:'Le japonais SFC décrit des secousses, pas nécessairement les fissures ajoutées dans le français DS.',
544:'Double BC natif conservé. L’histoire SFC commence dans un château ; ne pas importer la nuit d’orage de la localisation DS.',
563:'B8 SFC conservée, sans la convertir en acteur DS ni ajouter une quantité de PM.',
}
def generate(jp,dsdir):
 rows=source_rows(jp);inventory=read(R/'audits/ressources-v056.json')['battle_pool']['rows'];ids={r['id'] for r in inventory if r['status']=='IDENTIFIANT_CORRESPONDANT_A_ID'};assert ids==set(PLANS) and len(ids)==107
 refs=read(O/'references_ds.json');ja={(x['file'],x['id']):x for x in read(dsdir/'ds-ja.json')};fr={(x['file'].replace('/FR/','/JA/'),x['id']):x for x in read(dsdir/'ds-fr.json')};out=[]
 for mid in sorted(ids):
  s=rows[mid];assert '<UNKNOWN>' not in s['private_text'];plan=PLANS[mid];validate_plan(plan,s['private_tokens']);references=[]
  if str(mid) in refs:
   ref=refs[str(mid)]
   for i in ref['ids']:
    key=(ref['file'],i);assert key in ja and key in fr;references.append(dict(file=key[0],id=i,scope=ref['scope'],ja_text_sha256=sha(ja[key]['text'].encode()),fr_text_sha256=sha(fr[key]['text'].encode())))
  out.append(dict(system='BATTLE_BYTE_POOL',id=mid,status='PREPARE_NON_INSERE',semantic_review='RESERVE_ADAPTATION' if mid in SEMANTIC_RESERVES else 'RELU_JP_FR_CONTEXTE_DISPONIBLE',source_text_sha256=s['source_text_sha256'],source_message_sha256=s['source_message_sha256'],french_plan=plan,source_native_command_count=sum(0xab<=x<=0xc8 for x in s['private_tokens']),native_commands_preserved_except_AD_layout=True,ds_references=references,source_context_ids=list(range(max(0,mid-2),min(608,mid+3))),review=NOTES.get(mid,'Japonais SFC et français relus ; référence DS explicite lorsqu’établie. Variables et ordre SFC conservés, genre non imposé aux noms. Les formulations DS sont adaptées, pas copiées avec leurs macros.'),semantic_reserve=SEMANTIC_RESERVES.get(mid),insertion_blockers=['Encodeur byte et accents à établir sans emprunter celui du script Huffman.','Largeurs des variables/noms, pagination, B1/BC/BD/C2 et fenêtres de combat à tester.','Aucun rapprochement lexical seul ne vaut validation de l’appel natif.'],inserted=False,emulator_tested=False))
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--jp',required=True,type=Path);ap.add_argument('--ds-base',type=Path,default=D/'clean-base');a=ap.parse_args();rows=generate(a.jp.read_bytes(),a.ds_base);(O/'prepares-non-inseres.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print('107 prepared,105 semantic reviews,2 adaptation reserves;0 inserted')
