"""Audit allocated bytes against all known old consumers and reject collisions."""
from pathlib import Path
import argparse,json,struct
from common import prepare,old_pool,O,R,read,sha
from native_font import apply,MAP,FONT
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();base,_=prepare(a.jp.read_bytes());rom=(a.out/'result.sfc').read_bytes();expected,meta=apply(base,old_pool(base));slots={b for b,g in MAP.values()};rejected=[]
for slot in slots:
 rows=old_pool(base);i,at,s=rows[0];rows[0]=(i,at,bytes([slot])+s)
 try:apply(base,rows)
 except AssertionError:rejected.append(f'occupied-battle-{slot:02X}')
 else:raise AssertionError('Occupied slot accepted')
for slot in slots:
 assert rom[FONT+slot*16:FONT+slot*16+16]==expected[FONT+slot*16:FONT+slot*16+16]
for slot in range(256):
 if slot in slots:continue
 assert rom[FONT+slot*16:FONT+(slot+1)*16]==base[FONT+slot*16:FONT+(slot+1)*16]
 assert rom[0x11100+slot*2:0x11102+slot*2]==base[0x11100+slot*2:0x11102+slot*2]
assert rom[0x3fb50:0x3fb50+101]==base[0x3fb50:0x3fb50+101]
assert rom[0x165e7:0x167be]==base[0x165e7:0x167be] and rom[0x3b8703:0x3bc712]==base[0x3b8703:0x3bc712]
meta.update(release='v0.60',baseline='v0.59',ROM_sha256=sha(rom),unallocated_native_tiles_and_mapping_words_identical=249,all_old_name_pool_bytes_identical=True,all_dictionary_bytes_identical=True,seven_occupied_slot_mutations_rejected=rejected,native_font_visual_review_report='qa-emulator.json',unknown_hardcoded_consumers_fully_audited=False)
(O/'qa-font-extension.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');print('Seven accents;249 old tiles/mappings and all known name/dictionary bytes unchanged;7 collisions rejected')
