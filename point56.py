"""Preserve exact baseline corrections and reviewed final-script accounting."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;D=R/'dq6-fr';O=D/'v0.56';B=D/'v0.55';read=lambda p:json.loads(p.read_text());save=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2));old={x['id']:x for x in read(B/'insertion-candidates.json')};new={x['id']:x for x in read(O/'insertion-candidates.json')};review={x['id']:x for x in read(O/'revue-lot-v056.json')}
assert len(old)==6941 and len(new)==6957 and set(new)==set(range(6957));changed=[i for i in old if old[i]['tokens']!=new[i]['tokens']];assert sorted(changed)==[5698,5699,5700]
revs=[dict(id=i,old_tokens_sha256=hashlib.sha256(json.dumps(old[i]['tokens'],separators=(',',':')).encode()).hexdigest(),old_text=old[i]['text'],reason=review[i]['review'],new_selection=new[i]) for i in sorted(changed)]
save(O/'revisions-messages.json',revs)
assert len(read(O/'prepares-non-inseres.json'))==0
save(O/'qa-progression-script.json',dict(selected=6957,total_entries=6957,linguistic_entries=6948,structural_entries=9,new_linguistic_translations=16,remaining_main=0,prepared_main_non_inserted=0,deferred_main=0,isolated_existing_revisions=sorted(changed),other_old_tokens_unchanged=6938,structural_layout_revisions=[5699,5700],structural_entries_not_counted_as_translations=[1,2,3,2358,5699,5700,5775,6213,6214],complete_project=False,exhaustive_reread_completed=False,natural_scene_audits_open=[322,323,1836,4095,610,1135,2404,5341,5351,6956],separate_tables_and_final_resource_search_pending=True))
print('6957 entries selected;16 new texts;3 explicit revisions;0 main texts left')
