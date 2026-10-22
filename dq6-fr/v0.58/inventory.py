"""Reproduce the active ledger from v0.57 and this exact review."""
from common import O,R,read,IDS,sha,decode_pool
import argparse,json
from pathlib import Path
a=argparse.ArgumentParser();a.add_argument('--rom',type=Path,required=True);a=a.parse_args()
p=read(R/'dq6-fr/v0.57/inventaire-combat-v057.json');q=read(O/'inventaire-combat-v058.json');review=read(O/'revue-combat-v058.json');prep={r['id']:r for r in read(R/'preparations/combat-v057/prepares-non-inseres.json')}
assert [r['id'] for r in review]==IDS and set(IDS)<=set(p['prepared_not_inserted_ids'])
pending=sorted(set(p['prepared_not_inserted_ids'])-set(IDS));integrated=sorted(p['integrated_ids']+IDS)
assert q['prepared_not_inserted_ids']==pending and q['integrated_ids']==integrated
refs=sum(bool(prep[i]['ds_references']) for i in pending);semantic=sum(prep[i]['semantic_review']=='RELU_JP_FR_CONTEXTE_DISPONIBLE' for i in pending)
assert (len(pending),refs,len(pending)-refs,semantic)==(71,54,17,69)
assert (q['prepared_semantic_reviewed'],q['prepared_with_DS_refs'],q['prepared_direct_SFC'])==(semantic,refs,len(pending)-refs)
assert sum(q['counts'].values())==608 and len(integrated)==q['counts']['FRANCAIS_RELU_INTEGRE_DIAGNOSTIC']==36
rom=a.rom.read_bytes();assert sha(rom)==read(O/'build-report.json')['ROM_sha256']
meta=[dict(id=i,offset=at,size=len(b),sha256=sha(b)) for i,at,b in decode_pool(rom,q['placement'])]
assert sha(json.dumps(meta,sort_keys=True).encode())==q['all_message_offset_hash_metadata_sha256']
print('Inventory verified:36 integrated,71 pending,497 inherited unreviewed,4 structural; main unchanged')
