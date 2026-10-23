from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--jp',required=True,type=Path);a=p.parse_args();jp=a.jp.read_bytes();base,rows=prepare(jp);g=module('sourceguard63',O/'source_guard.py');bounded=g.checked_rows(jp,R);old=list(old_pool(base));assert len(bounded)==603
# Reproduce the historical overrun explicitly, without qualifying those decodes.
p57=module('historical63',R/'preparations/combat-v057/prepare.py');unbounded=p57.source_rows(jp)
for i,b in enumerate(bounded):assert all(unbounded[i][k]==b[k] for k in ['source_text_sha256','source_message_sha256','private_tokens'])
p=0x37175b;over=[]
for mid in range(603,608):
 start=p
 while jp[p] not in (0xac,0xae):p+=1
 p+=1;v=old[mid][2];over.append(dict(id=mid,historical_JP_start=start,historical_JP_end=p,historical_bytes=p-start,JP_sha256=sha(jp[start:p]),opaque_VF_sha256=sha(v),status='SOURCE_JP_HORS_POOL_A_AUDITER',action='Octets VF conservés sans traduction ni classement structurel. Audit appelants et origine requis.'))
assert bounded[-1]['end']==g.LIMIT and over[0]['historical_JP_start']==g.LIMIT
q=dict(release='v0.63',source_sha256=sha(jp),bounded_JP_entries=603,bounded_text_entries=599,structural_entries=4,parsed_VF_slots=608,protected_main_region_start=g.LIMIT,first_main_relative_pointer=int.from_bytes(jp[0x15bb5:0x15bb8],'little'),last_valid_entries=[{k:b[k] for k in ['id','start','end','source_message_sha256']} for b in bounded[-3:]],source_guard_enforced_in_prepare=True,all603_valid_hashes_equal_historical=True,rejected_translation_ids=list(range(603,608)),overrun_entries=over,unused_or_unreachable_proven=False,negative_test='Any proposed ID603 is rejected by prepare before source indexing.')
assert q['first_main_relative_pointer']==7
import common
saved=common.IDS;common.IDS=[603]
try:
 try:common.prepare(jp)
 except AssertionError as e:assert 'Outside bounded JP pool' in str(e);q['negative_ID603_rejected']=True
 else:raise AssertionError('Invalid source accepted')
finally:common.IDS=saved
(O/'audit-frontiere-source.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print('603 bounded JP entries;5 historical decodes outside pool isolated')
