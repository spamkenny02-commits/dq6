from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--rom',type=Path,required=True);a=p.parse_args();rom=a.rom.read_bytes();report=read(O/'build-report.json');assert sha(rom)==report['ROM_sha256'];old=read(R/'dq6-fr/v0.60/inventaire-combat-v060.json');q=read(O/'inventaire-combat-v061.json')
assert old['prepared_not_inserted_ids']==IDS and q['integrated_ids']==sorted(old['integrated_ids']+IDS) and q['prepared_not_inserted_ids']==[]
assert q['counts']==dict(FRANCAIS_RELU_INTEGRE_DIAGNOSTIC=107,IDENTIFIANT_EN_ATTENTE=0,HERITE_LANGUE_ET_CONTEXTE_NON_VALIDES=497,STRUCTURE_SANS_TEXTE=4)
assert sum(q['counts'].values())==608 and q['semantic_reserve_ids']==[] and q['names_confirmed_FR']==39 and q['prepared_character_names']==0
meta=[dict(id=i,offset=at,size=len(b),sha256=sha(b)) for i,at,b in decode_pool(rom,report['placement'])];assert sha(json.dumps(meta,sort_keys=True).encode())==q['all_message_offset_hash_metadata_sha256']
assert q['names']['confirmed_french_entries']==39 and q['names']['prepared_character_names']==0 and q['names']['compound_virtual_strings']==16
print('107 battle translations integrated,0 prepared,497 inherited unreviewed,4 structural;39 native names,16 separate compound strings.')
