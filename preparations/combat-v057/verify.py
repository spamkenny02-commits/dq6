"""Verify preparation provenance and guard failures; does not claim ROM QA."""
from pathlib import Path
import argparse,json,hashlib,importlib.util,re,sys
O=Path(__file__).resolve().parent;R=O.parents[1];D=R/'dq6-fr';sys.path.insert(0,str(O));import prepare
ap=argparse.ArgumentParser();ap.add_argument('--jp',type=Path,required=True);a=ap.parse_args();raw=a.jp.read_bytes();rows=prepare.generate(raw,D/'clean-base');data=json.dumps(rows,ensure_ascii=False,indent=2).encode();assert data==(O/'prepares-non-inseres.json').read_bytes()
source=prepare.source_rows(raw);rejections=[]
def rejects(label,fn):
 try:fn()
 except AssertionError:rejections.append(label)
 else:raise AssertionError('Mutation accepted: '+label)
rejects('wrong_JP_source',lambda:prepare.checked_source(bytes([raw[0]^1])+raw[1:]))
p=prepare.PLANS[397];tokens=source[397]['private_tokens']
rejects('missing_actor_variable',lambda:prepare.validate_plan(p.replace('{B7}','',1),tokens))
swap=p.replace('{B7}','__ACTOR__',1).replace('{B8}','{B7}',1).replace('__ACTOR__','{B8}',1)
rejects('actor_target_reordered',lambda:prepare.validate_plan(swap,tokens))
rejects('lost_B1_pause',lambda:prepare.validate_plan(p.replace('{B1}','',1),tokens))
rejects('unresolved_DS_markup',lambda:prepare.validate_plan(p+'%a000010',tokens))
rejects('dictionary_byte_as_control',lambda:prepare.validate_plan(p+'{C9}',tokens))
mod=importlib.util.spec_from_file_location('patch',D/'upstream/refill/patchRM.py');patch=importlib.util.module_from_spec(mod);mod.loader.exec_module(patch);bps=R/'patches/DQVI-FR-DS-v0.56-BASE-JP-PARTIEL.bps';result=bytes(patch.apply_bps(raw,bps.read_bytes()));digest=hashlib.sha256(result).hexdigest();assert digest=='e14ebc5611642b229edd3e7becae27813c823ef8182e2d06058953d593f2375d'
needs=[r['id'] for r in rows if any(len(re.sub(r'\{[^}]+\}','',line))>22 for line in r['french_plan'].split('{AD}')) or any(x in r['french_plan'] for x in ['{B7}','{B8}','{B2}','{B5}'])]
report=dict(checkpoint='combat-v057',status='PREPARE_NON_INSERE',prepared=107,semantic_reviewed_prepared=105,semantic_reserve_ids=[464,465],with_explicit_DS_references=sum(bool(r['ds_references']) for r in rows),direct_SFC_without_established_DS=sum(not r['ds_references'] for r in rows),all_source_native_order_and_counts_preserved_except_AD_layout=True,all_source_terminators_preserved=True,idempotent_output_verified=True,guard_rejections=rejections,needs_layout_review_ids=needs,codec_approved=False,new_inserted=0,rom_bytes_written=0,Snes9x_executed=False,baseline_BPS_reapplied_to_intact_JP=True,baseline_result_sha256=digest,main_script_selected_unchanged=6957,source_tables_unchanged=True,full_main_proofread_progress=0,limits=['These are preparations, not an insertable or rendered release.','Two shiritori/virelangue adaptations remain semantically reserved.','The other105 language reviews do not validate runtime bindings, byte encoding, widths, B1 pacing or battle scenes.','The497 inherited battle texts have not been globally reviewed in this checkpoint.','No raw ROM data or inherited decoded ROM text is exported in these preparation reports.'])
(O/'qa-preparation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='needs_layout_review_ids'},ensure_ascii=False))
