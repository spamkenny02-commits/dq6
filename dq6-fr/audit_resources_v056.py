"""Post-script resource inventory. Counts are physical, never language guesses.
The separate battle pool is read through its own76 pointers, not the Huffman
script or the2512 name SIDs. Upstream documentation is verified against inputs.
"""
from pathlib import Path
import json,hashlib,struct,importlib.util,re,argparse,collections
D=Path(__file__).resolve().parent;R=D.parent;ap=argparse.ArgumentParser();ap.add_argument('--jp',type=Path,required=True);ap.add_argument('--result',type=Path,required=True);a=ap.parse_args();jp=a.jp.read_bytes();rom=a.result.read_bytes();assert hashlib.sha256(jp).hexdigest()=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e';assert hashlib.sha256(rom).hexdigest()=='e14ebc5611642b229edd3e7becae27813c823ef8182e2d06058953d593f2375d'
spec=importlib.util.spec_from_file_location('nt',D/'upstream/refill/tools/nametable.py');nt=importlib.util.module_from_spec(spec);spec.loader.exec_module(nt);first,base,dictionary=nt.read_dictionary(rom)
def pool(data):
 rows=[]
 for group in range(76):
  ptr=int.from_bytes(data[0x15ad1+group*3:0x15ad4+group*3],'little');p=0x36debd+ptr
  assert 0<=p<len(data)
  for low in range(8):
   start=p
   while data[p] not in [0xac,0xae]:
    p+=1;assert p-start<4096
   p+=1;rows.append(dict(id=group*8+low,offset=start,bytes=data[start:p]))
 return rows
old=pool(jp);new=pool(rom);assert len(old)==len(new)==608
# Independently inspect loader instructions for the third pointer table/base.
assert jp[0x27cd:0x27d1]==bytes.fromhex('bfd15ac1')
assert rom[0x27cd:0x27d1]==jp[0x27cd:0x27d1]
controls=set(range(0xab,0xce))
def text(blob):
 out=[]
 for b in blob:
  if b==0xad:out.append('[LINE]')
  elif b in [0xac,0xae]:out.append('[END '+f'{b:02X}'+']')
  elif b in dictionary:out.append(dictionary[b])
  elif b in controls:out.append('[CODE '+f'{b:02X}'+']')
  else:out.append(nt.base_char(b))
 return ''.join(out)
rows=[]
for j,r in zip(old,new):
 t=text(r['bytes']);plain=re.sub(r'\[[^]]*\]|<[^>]*>','',t).strip();match=re.fullmatch(r'[BM*]([0-9A-F]{2,4})',plain)
 status='IDENTIFIANT_CORRESPONDANT_A_ID' if match and int(match[1],16)==r['id'] else 'VIDE_OU_COMMANDES_SEULEMENT' if all(b in controls or b==1 for b in r['bytes']) else 'HERITE_NON_RELU_LANGUE_A_QUALIFIER'
 rows.append(dict(id=r['id'],jp_offset=j['offset'],current_offset=r['offset'],jp_message_sha256=hashlib.sha256(j['bytes']).hexdigest(),current_message_sha256=hashlib.sha256(r['bytes']).hexdigest(),status=status,french_validated_in_this_project=False,ending_kind='fragment' if r['bytes'][-1]==0xae else 'normal'))
counts=dict(collections.Counter(r['status'] for r in rows));names=json.loads((D/'v0.56/inventaire-tables.json').read_text());out=R/'audits';out.mkdir(exist_ok=True)
report=dict(version='v0.56',main_script=dict(selected=6957,linguistic=6948,structural=9,remaining=0,full_proofread=False),name_pool=names,battle_pool=dict(runtime_ids=608,unique_start_offsets=len({r['current_offset'] for r in rows}),aliases=608-len({r['current_offset'] for r in rows}),pointer_groups=76,pointer_table='0x015AD1',payload_base='0x36DEBD',loader_bytes_verified=True,classification_counts=counts,french_confirmed_by_project_review=0,all_entries_need_context_review=True,encoding='byte charset and dictionary, not Huffman',rows=rows),other_paths=dict(status='A_CARTOGRAPHIER_NON_VALIDE',scopes=['menus en fenêtres et libellés natifs','écran de nom et alphabet accentué','noms/objets/sorts/classes/actions/descriptions composées','fin et épilogue : script couvert, parcours naturels ouverts','messages système ou texte graphique hors tables identifiées']),no_translation_inserted=True,result_sha256=hashlib.sha256(rom).hexdigest(),limits=['Decoded text is used locally only for classification, never exported. This report contains metadata and hashes only, no raw ROM bytes or inherited decoded ROM text. Dictionary expansions come from the actual ROM.','608 entries are not assumed608 linguistic sentences; empty/control entries and aliases are counted separately.','This inventory does not establish all game resources have been found. It records the discovered third pool and remaining search scopes.','Existing37 confirmed name-pool entries and4 grammar helpers do not establish the entire separate tables are French.','Upstream BATTLE-POOL.md concerns another English patch; its107-placeholder claim is not reused as a count for this French ROM.'])
(out/'ressources-v056.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(dict(battle_entries=len(rows),battle_statuses=counts,battle_aliases=report['battle_pool']['aliases'],name_entries=2048,main_remaining=0),ensure_ascii=False))
