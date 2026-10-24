"""Reproduce a manually reviewed main-dialogue batch; never generate an inserted selection."""
from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(n,d):(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
notes=read(P/'notes.json');assert set(map(int,notes))==set(range(400,500))
selected=read(R/'dq6-fr/v0.56/insertion-candidates.json');assert len(selected)==6957
jp={x['id']:x for x in read(R/'dq6-fr/clean-base/sfc-jp.json')};fr={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-fr.json')};ja={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-ja.json')}
extra={425:[658],426:[659],445:[733,734,735,736],452:[759],478:[910],498:[970,971]};file='data/MESS6/FR/0075.p'
changes={410:[('ça vous tente?','Ça vous tente?')],416:[('ça... ça va pas!','Ça... Ça va pas!')],424:[('Dame Séductra. à quoi','Dame Séductra. À quoi')],429:[('ça fait presque','Ça fait presque')],433:[('ça sert à rien','Ça sert à rien')],440:[('ça vous tente,','Ça vous tente,')],458:[("ça coûte cher",'Ça coûte cher')],460:[('Lynx. ça marche!','Lynx. Ça marche!'),('à bientôt!','À bientôt!')],471:[('ça fait des années','Ça fait des années')],493:[('elle est plutôt costaud et','elle est plutôt costaude et')],499:[('ça fait deux!','Ça fait deux!')]}
reserves={425,426,430,441,445,473,498};ledger=[];proposals=[]
for row in selected:
 mid=row['id']
 if not 400<=mid<500:continue
 ids=row.get('ds_id',[]);ids=[ids] if isinstance(ids,int) else ids;refs=[]
 for did in dict.fromkeys(list(ids)+extra.get(mid,[])):
  f=fr[(row.get('ds_file') or file,did)];j=ja[(f['file'].replace('/FR/','/JA/'),did)]
  refs.append(dict(FR_file=f['file'],JA_file=j['file'],id=did,FR_text=f['text'],JA_text=j['text'],FR_record_sha256=sha(json.dumps(f,ensure_ascii=False,sort_keys=True).encode()),JA_record_sha256=sha(json.dumps(j,ensure_ascii=False,sort_keys=True).encode()),role='COMPARAISON_VARIANTE_OU_COMPLEMENT_NON_INSERE' if did in extra.get(mid,[]) else 'REFERENCE_DE_LA_SELECTION_PUBLIEE'))
 oldhash=sha(json.dumps(row['tokens'],separators=(',',':')).encode());item=dict(id=mid,status='PREPARE_NON_INSERE',review_outcome='PROPOSITION_REVISION' if mid in changes else ('RELU_AVEC_RESERVES' if mid in reserves else 'RELU_TEXTE_CONSERVE'),source_selection_file='dq6-fr/v0.56/insertion-candidates.json',old_text=row['text'],old_tokens_sha256=oldhash,old_tokens=row['tokens'],source_japanese=row.get('source_japanese'),JP_extracted_record_sha256=sha(json.dumps(jp[mid],ensure_ascii=False,sort_keys=True).encode()),secondary_IPS_text=row.get('sfc_previous'),DS_references=refs,note=notes[str(mid)],native_tested=False,full_reread_final_accepted=False)
 if mid in changes:
  proposed=row['text']
  for before,after in changes[mid]:assert proposed.count(before)==1,(mid,before);proposed=proposed.replace(before,after)
  assert proposed!=row['text'];controls=lambda t:re.findall('[\ue000-\ue0ff]',t);assert controls(proposed)==controls(row['text'])
  blockers=['Sources ROM absentes : aucune nouvelle sélection encodée, insertion, compilation ou validation de fenêtre/pagination.']
  if mid!=493:blockers.append('Capitales Ç/À absentes du charset principal v0.56 ; vérifier le moteur et les glyphes ou préparer une reformulation compatible avant insertion.')
  else:assert set(proposed)<=set(row['text']), 'No new characters expected for feminine agreement'
  proposal=dict(id=mid,status='PREPARE_NON_INSERE',kind='ACCORD_FEMININ' if mid==493 else 'CAPITALE_ACCENTUEE_SOUS_RESERVE_DE_GLYPHE',old_text=row['text'],proposed_text=proposed,old_tokens_sha256=oldhash,native_commands_preserved_as_baseline_tokens=row['tokens'],replacements=[dict(before=x,after=y) for x,y in changes[mid]],reason=notes[str(mid)],blockers=blockers,new_selection_generated=False,new_tokens_generated=False,integrated=False,native_tested=False)
  proposals.append(proposal);item['proposal']=proposed
 ledger.append(item)
assert [x['id'] for x in ledger]==list(range(400,500)) and len(proposals)==11
# Unsupported capital letters are a documented alphabet gap, not an automatically approved insertion.
charset=read(R/'dq6-fr/v0.56/charset.json');assert not {'Ç','À'}&set(charset.values())
dump('registre-relecture.json',ledger);dump('revisions-preparees-non-inserees.json',proposals)
q=dict(baseline_release='v0.78',baseline_commit='604800f9c31470b1801eaa99359715315617e660',reviewed_main_IDs=list(range(400,500)),reviewed_main_texts=100,empty_entries_counted_as_translations=0,new_prepared_existing_main_revisions=11,agreement_revisions=1,capitalization_proposals_under_glyph_reserve=10,source_composition_or_exact_DS_reserve_IDs=sorted(reserves),new_translations=0,new_integrated=0,new_encoded_selections=0,ROM_rebuilt=False,emulator_executed=False,ROM_sources_available=False,full_main_reread_final_accepted_added=0,semantic_review_pending_runtime_added=100,all100_native_tested=False,all6957_complete_reread=False,main_selection_sha256=sha((R/'dq6-fr/v0.56/insertion-candidates.json').read_bytes()),main_charset_sha256=sha((R/'dq6-fr/v0.56/charset.json').read_bytes()),DS_FR_extraction_sha256=sha((R/'dq6-fr/clean-base/ds-fr.json').read_bytes()),DS_JA_extraction_sha256=sha((R/'dq6-fr/clean-base/ds-ja.json').read_bytes()),notes_sha256=sha((P/'notes.json').read_bytes()),all_original_control_tokens_only_preserved_not_reencoded=True)
dump('qa-preparation.json',q);print('100 main texts reviewed;11 revision proposals;0 integrated;0 native tests')
