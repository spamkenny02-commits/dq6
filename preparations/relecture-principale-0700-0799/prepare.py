"""Reproduce manual review700–799; audit item-name variables without inventing native tests."""
from pathlib import Path
import json,hashlib,re,collections
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,d):(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
notes=read(P/'notes.json');assert set(map(int,notes))==set(range(700,800));sel=read(R/'dq6-fr/v0.56/insertion-candidates.json');byid={x['id']:x for x in sel};assert len(sel)==6957
jp={x['id']:x for x in read(R/'dq6-fr/clean-base/sfc-jp.json')};ja={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-ja.json')};fr={(x['file'],x['id']):x for x in read(R/'dq6-fr/clean-base/ds-fr.json')}
norm=lambda t:t.replace('\\n','\n').replace('\\t','\t').replace('\\u3000','\u3000')
extras={752:[('data/MESS6/FR/0082.p',n) for n in range(49,57)],784:[('data/MESS6/FR/0084.p',n) for n in [521,522]]}
def refs_for(row):
 links={};ns=row.get('ds_id',[]);ns=[ns] if isinstance(ns,int) else ns
 for n in ns:links[(row['ds_file'],n)]=['REFERENCE_DE_LA_SELECTION_PUBLIEE']
 for ref in row.get('ds_references',[]):
  j=ja[(ref['file'],ref['id'])];f=fr[(ref['file'].replace('/JA/','/FR/'),ref['id'])];assert norm(ref['ja'])==j['text'] and norm(ref['fr'])==f['text'],(row['id'],ref['id'])
  links.setdefault((f['file'],ref['id']),[]).append(ref.get('scope','REFERENCE_EXPLICITE'))
 for key in extras.get(row['id'],[]):links.setdefault(key,[]).append('COMPARAISON_VARIANTE_OU_COMPOSITION_NON_INSEREE')
 out=[]
 for (file,n),scopes in links.items():
  f=fr[(file,n)];j=ja[(file.replace('/FR/','/JA/'),n)];out.append(dict(FR_file=file,JA_file=j['file'],id=n,FR_text=f['text'],JA_text=j['text'],scopes=scopes,FR_record_sha256=sha(json.dumps(f,ensure_ascii=False,sort_keys=True).encode()),JA_record_sha256=sha(json.dumps(j,ensure_ascii=False,sort_keys=True).encode())))
 return out
B2=chr(0xe0b2)
changes={701:[("D'après lui, il n'y a pas que l'argent dans la vie.","Il dit que je n'ai plus besoin de gagner de l'argent.")],702:[("ça prouve bien","Ça prouve bien")],703:[('ça fait des années','Ça fait des années')],735:[('ça ne paie pas de mine','Ça ne paie pas de mine')],751:[('le coeur de ces gens','le cœur de ces gens')],753:[('ça les aiderait','Ça les aiderait')],759:[('ça vous dit?','Ça vous dit?')],763:[('le coeur empli','le cœur empli')],765:[('ça vous pose un problème?','Ça vous pose un problème?')],783:[('ça va me prendre','Ça va me prendre')],784:[("Près du lit repose un splendide "+B2+" dont l'éclat éblouit le regard.","Près du lit repose le chef-d'oeuvre de Clume ("+B2+"). Son éclat éblouit le regard.")],799:[('ça y est!','Ça y est!')]}
reserves={719,720,752,755,756,764,768,769,780,784,785,797};ledger=[];proposals=[]
for row in sel:
 mid=row['id']
 if not 700<=mid<800:continue
 th=sha(json.dumps(row['tokens'],separators=(',',':')).encode());refs=refs_for(row);entry=dict(id=mid,status='PREPARE_NON_INSERE',review_outcome='PROPOSITION_REVISION' if mid in changes else ('RELU_AVEC_RESERVES' if mid in reserves else 'RELU_TEXTE_CONSERVE'),old_text=row['text'],old_tokens=row['tokens'],old_tokens_sha256=th,source_selection_file='dq6-fr/v0.56/insertion-candidates.json',source_japanese=row.get('source_japanese'),JP_record_sha256=sha(json.dumps(jp[mid],ensure_ascii=False,sort_keys=True).encode()),secondary_IPS_text=row.get('sfc_previous'),DS_references=refs,note=notes[str(mid)],native_tested=False,full_reread_final_accepted=False)
 if mid in changes:
  proposed=row['text']
  for before,after in changes[mid]:assert proposed.count(before)==1,(mid,before);proposed=proposed.replace(before,after)
  controls=lambda text:re.findall('[\ue000-\ue0ff]',text)
  assert proposed!=row['text'] and controls(proposed)==controls(row['text'])
  kind='SUJET_ENFANT_DANS_LA_REPLIQUE' if mid==701 else ('COMPOSITION_NOM_OBJET_SANS_ACCORD_IMPOSE' if mid==784 else 'TYPOGRAPHIE_SOUS_RESERVE_DE_GLYPHE')
  blockers=['ROM absente : pas de nouvel encodage,insertion,compilation,réapplication de patch ou rendu natif.']
  if mid==701:blockers.append('Adaptation isolée du français DS vers la précision japonaise ; rôle du père et de l\'enfant à confirmer dans la scène.')
  elif mid==784:blockers.append('Valeurs possibles de B2/B5,portée du sujet D3,parenthèses,ponctuation et pagination à tester pour chaque récompense réelle.')
  else:blockers.append('Ç ou œ requis absent du charset principal v056 ; ne pas supposer le glyphe disponible.')
  proposals.append(dict(id=mid,status='PREPARE_NON_INSERE',kind=kind,old_text=row['text'],proposed_text=proposed,old_tokens_sha256=th,native_baseline_tokens_preserved=row['tokens'],replacements=[dict(before=a,after=b) for a,b in changes[mid]],reason=notes[str(mid)],blockers=blockers,new_selection_generated=False,new_tokens_generated=False,integrated=False,native_tested=False));entry['proposal']=proposed
 ledger.append(entry)
assert [x['id'] for x in ledger]==list(range(700,800)) and len(proposals)==12
assert not {'Ç','œ'}&set(read(R/'dq6-fr/v0.56/charset.json').values())
assert byid[752]['tokens'].count(0xdf)==byid[752]['text'].count(chr(0xe0df))==1
# These are textual occurrences of variables, not proof of their live values or event bindings.
related=[]
for mid in [768,769,770,771,772,773,774,775,776,777,778,779,780,781,782,783,784,785,797]:
 row=byid[mid];related.append(dict(id=mid,text=row['text'],source_japanese=row.get('source_japanese'),old_tokens_sha256=sha(json.dumps(row['tokens'],separators=(',',':')).encode()),native_variables={f'{v:02X}':row['tokens'].count(v) for v in [0xb2,0xb5,0xd3] if v in row['tokens']},DS_references=refs_for(row)))
r=byid[784];p=next(x for x in proposals if x['id']==784)
for v,n in [(0xd3,2),(0xb2,1),(0xb5,1)]:assert r['tokens'].count(v)==r['text'].count(chr(0xe000+v))==p['proposed_text'].count(chr(0xe000+v))==n
assert ('data/MESS6/FR/0084.p',523) not in fr;unpaired=ja[('data/MESS6/JA/0084.p',523)]
audit=dict(scope='Comparaison textuelle dans le lot, pas simulation des récompenses.',status='OUVERT_PREPARE_NON_INSERE',description_revision_id=784,old_text=r['text'],proposed_text=p['proposed_text'],visible_variable_sequence_preserved=True,expected_source_counts={'D3':2,'B2':1,'B5':1},reward_list_or_B2_B5_mapping_verified=False,native_selection_or_item_IDs_inspected=False,natural_scene_executed=False,DS_JA_523_without_paired_FR_record_in_extraction=dict(file=unpaired['file'],id=523,text=unpaired['text'],record_sha256=sha(json.dumps(unpaired,ensure_ascii=False,sort_keys=True).encode()),FR_record_present_in_this_extraction=False,does_not_prove_missing_translation_in_DS_ROM=True),related_texts=related,required_tests=['Establish every actual native choice and its B2 and B5 values.','Test confirmation,cancellation,return,delivery and possession for every actual reward.','Render full names,player-name substitutions,parentheses and pagination naturally.','Keep diagnostic redirections distinct from the acquisition path; do not count a sample as all rewards.'])
save('registre-relecture.json',ledger);save('revisions-preparees-non-inserees.json',proposals);save('audit-composition-recompense-clume.json',audit)
q=dict(baseline_commit='3efe78b2a2beb418e47779ed7d8a26f2b4e44155',baseline_release='v0.78',reviewed_positions=list(range(700,800)),reviewed_positions_count=100,silence_composition_IDs=[755],new_prepared_existing_main_revisions=12,glyph_dependent_proposals=10,context_or_variable_composition_proposals=2,main_prepared_revisions_previous=41,main_prepared_revisions_current=53,names_prepared_unchanged=419,semantic_review_pending_runtime_cumulative=400,full_main_reread_final_accepted_added=0,rare_DF_in_752_preserved_not_native_validated=True,Clume_reward_choices_tested=False,new_encoded_selections=0,new_integrated=0,new_translations=0,ROM_sources_available=False,ROM_rebuilt=False,emulator_executed=False,source_selection_sha256=sha((R/'dq6-fr/v0.56/insertion-candidates.json').read_bytes()),DS_JA_sha256=sha((R/'dq6-fr/clean-base/ds-ja.json').read_bytes()),DS_FR_sha256=sha((R/'dq6-fr/clean-base/ds-fr.json').read_bytes()),notes_sha256=sha((P/'notes.json').read_bytes()),all_original_tokens_preserved_not_reencoded=True)
save('qa-preparation.json',q);print('100 positions;12 proposals;Clume variables2D3/1B2/1B5 preserved;0 integrated')
