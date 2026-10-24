"""Reproduce text-only menu preparations from published extractions, without ROM access."""
from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;R=P.parents[1]
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,d):(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
d=read(P/'decisions.json');ledger=read(R/'dq6-fr/v0.69/registre-positions-0000-0399.json');bypos={x['position']:x for x in ledger};pending=read(R/'dq6-fr/v0.78/blocages-restants.json')['entries'];pendingpos={x['position'] for x in pending}
jp=read(R/'dq6-fr/clean-base/ds-ja.json');fr=read(R/'dq6-fr/clean-base/ds-fr.json');ji={(x['file'],x['id']):x for x in jp};fi={(x['file'],x['id']):x for x in fr}
refs=[];prepared=[];review=[]
def reference(file,mid):
 j=ji[('data/MENULIST6/JA/'+file,mid)];f=fi[('data/MENULIST6/FR/'+file,mid)]
 contexts=[]
 for n in range(mid-2,mid+3):
  if (j['file'],n) in ji and (f['file'],n) in fi:contexts.append(dict(id=n,JA=ji[(j['file'],n)]['text'],FR=fi[(f['file'],n)]['text']))
 return dict(JA_file=j['file'],FR_file=f['file'],id=mid,JA_text=j['text'],FR_text=f['text'],JA_extracted_record_sha256=sha(json.dumps(j,ensure_ascii=False,sort_keys=True).encode()),FR_extracted_record_sha256=sha(json.dumps(f,ensure_ascii=False,sort_keys=True).encode()),context=contexts)
for key,decision in d['new'].items():
 pos=int(key);proposal,file,mid,note=decision;assert pos not in pendingpos
 row=bypos[pos];ref=reference(file,mid);japanese=re.fullmatch(r'@1([^@]*)@',ref['JA_text']).group(1)
 assert row['sfc_jp'].rstrip(':')==japanese,(pos,row['sfc_jp'],japanese)
 french=re.search(r'@4([^@]*)@',ref['FR_text'])
 if not french:french=re.search(r'@1([^@]*)@',ref['FR_text'])
 assert proposal.rstrip(':')==french.group(1),(pos,proposal,ref['FR_text'])
 item={k:row[k] for k in ['position','sids','current','sfc_jp','current_message_sha256','JP_message_sha256','secondary_IPS_text','secondary_IPS_message_sha256']}
 item.update(proposal=proposal,status='PREPARE_NON_INSERE',DS_references=[ref],semantic_review=note,adaptation='Deux-points natif SFC conservé sans article DS.' if pos in [215,216,218] else 'Libellé DS exact ; métadonnées de genre/nombre non injectées.',runtime_blockers=['Sources ROM absentes : encodage, redécodage, compilation et tests natifs non exécutés.','Largeur, espacement technique, pagination, aliases et tous consommateurs SFC à contrôler avant insertion.'],integrated=False,native_tested=False)
 prepared.append(item);review.append(dict(position=pos,SIDs=row['sids'],new_preparation=True,note=note,DS_reference=dict(file=file,id=mid)))
for key,decision in d['existing'].items():
 pos=int(key);file,mid,note=decision;assert pos in pendingpos;row=next(x for x in pending if x['position']==pos);ref=reference(file,mid)
 assert re.fullmatch(r'@1([^@]*)@',ref['JA_text']).group(1)==row['sfc_jp'].rstrip(':'),(pos,ref['JA_text'],row['sfc_jp'])
 refs.append(dict(position=pos,sids=row['sids'],proposal=row['proposal'],prior_status='PREPARE_NON_INSERE',status='PREPARE_NON_INSERE',DS_references=[ref],context_review=note,resolves_reference_gap=True,resolves_runtime_blocker=False))
 review.append(dict(position=pos,SIDs=row['sids'],new_preparation=False,note=note,DS_reference=dict(file=file,id=mid)))
for key,note in d['unresolved'].items():
 pos=int(key);assert pos in pendingpos;review.append(dict(position=pos,SIDs=bypos[pos]['sids'],new_preparation=False,status='DIFFERE_REFERENCE_EXACTE',note=note))
assert len(prepared)==14 and len(refs)==27 and len(review)==43 and len({x['position'] for x in review})==43
save('prepares-non-inseres.json',prepared);save('references-propositions-existantes.json',refs);save('registre-relecture.json',sorted(review,key=lambda x:x['position']))
inputs=['preparations/menus-apres-v078/decisions.json','dq6-fr/v0.69/registre-positions-0000-0399.json','dq6-fr/v0.78/blocages-restants.json','dq6-fr/clean-base/ds-ja.json','dq6-fr/clean-base/ds-fr.json']
q=dict(baseline_release='v0.78',baseline_commit='46f7046d4e20f943fcfe772978ec4108705c74d7',reviewed_positions=43,new_prepared_not_inserted=14,existing_preparations_reference_gaps_documented=27,remaining_exact_reference_reserves=2,main_new_integrated=0,names_new_integrated=0,names_prepared_previous=405,names_prepared_current=419,names_french_qualified_unchanged=367,physical_table_positions_previously_examined=2048,new_physical_positions_examined=0,full_main_reread_unchanged=0,source_ROMs_available=False,rebuild_executed=False,emulator_executed=False,published_extraction_checks_only=True,inputs_sha256={n:sha((R/n).read_bytes()) for n in inputs},limits=['Published extraction identity is verified; extraction was not repeated from absent ROMs.','Previously prepared entries are not counted as new translations or new preparations.','No codec, glyph, window, alias, assembly, patch or natural scene validation is claimed.','This menu review does not close the full French script reread or inherited audits.'])
save('qa-extractions.json',q);print(json.dumps({k:v for k,v in q.items() if k!='inputs_sha256'},ensure_ascii=False))
