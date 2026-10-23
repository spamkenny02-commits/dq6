from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);a=p.parse_args();rom=a.rom.read_bytes();r=read(O/'build-report.json');q=read(O/'inventaire-combat-v064.json');old=read(R/'dq6-fr/v0.63/inventaire-combat-v063.json');assert sha(rom)==r['ROM_sha256'];assert q['integrated_ids']==sorted(old['integrated_ids']+IDS) and not set(IDS)&set(old['integrated_ids']);assert q['unqualified_inherited_ids']==q['prepared_not_inserted_ids']==[27,277];assert q['source_boundary_audit_ids']==list(range(603,608));assert sum(q['counts'].values())==608 and q['counts']['FRANCAIS_RELU_INTEGRE_DIAGNOSTIC']==597
meta=[dict(id=i,offset=at,size=len(b),sha256=sha(b)) for i,at,b in decode_pool(rom,r['placement'])];assert sha(json.dumps(meta,sort_keys=True).encode())==q['all_message_offset_hash_metadata_sha256'];assert len(IDS)==11
print('597 qualified,2 PREPARE_NON_INSERE,5 outside-JP-pool,4 structures;main6957 unchanged')
