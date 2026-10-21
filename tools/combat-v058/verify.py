"""Reproduce byte-codec measurements; no insertion and no ROM output."""
from pathlib import Path
import argparse,json,re,hashlib,collections
from codec import *
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--jp',type=Path,required=True);a=ap.parse_args()
rom=baseline_from_jp(a.jp.read_bytes(),R);charset=json.loads((R/'dq6-fr/v0.56/charset.json').read_text());c=BattleCodec(rom,charset);rows=pool(rom);regions=main_regions(rom)
plans=json.loads((R/'preparations/combat-v057/prepares-non-inseres.json').read_text());good=[];bad=[];coverage=collections.Counter()
for p in plans:
 text=re.sub(r'\{[A-F0-9]{2}\}','',p['french_plan']);missing=sorted(set(text)-set(c.forward));coverage.update(missing)
 if missing:bad.append({'id':p['id'],'unsupported_characters':missing})
 else:
  encoded=c.encode(p['french_plan']);assert c.decode(encoded)==p['french_plan'];good.append(p['id'])
assert len(good)==43 and len(bad)==64
# Independent anchors from established ASCII byte alphabet, then real font IDs.
assert c.encode('HMPG !,.?\'{AC}')==bytes([0x17,0x1c,0x1f,0x16,1,0x7a,0x8b,0x7f,0x79,0x77,0xac])
assert c.glyphs[0x7a]==0x241 and c.glyphs[0x81]==0x246
rejections=[]
def rejected(label,f):
 try:f()
 except (CodecError,AssertionError):rejections.append(label)
 else:raise AssertionError('Mutation accepted: '+label)
rejected('wrong_intact_JP',lambda:baseline_from_jp(b'wrong',R))
rejected('wrong_baseline',lambda:BattleCodec(rom[:-1]+bytes([rom[-1]^1]),charset))
rejected('unsupported_accent_without_lossy_fallback',lambda:c.encode('été{AC}'))
rejected('shadow_PM_byte_not_ordinary_glyph',lambda:c.decode(bytes([0x0d,0xac])))
rejected('dictionary_code_not_a_native_variable',lambda:c.encode('{C9}{AC}'))
rejected('unresolved_DS_macro',lambda:c.encode('%a000090{AC}'))
rejected('embedded_terminator',lambda:c.encode('A{AC}B{AC}'))
rejected('missing_terminator',lambda:c.encode('A'))
mut=bytearray(rom);mut[PTR:PTR+3]=b'\xff'*3
rejected('pointer_outside_battle_region',lambda:pool(mut))
mut=bytearray(rom);mut[PTR+3:PTR+6]=mut[PTR:PTR+3]
rejected('aliased_overlapping_group',lambda:pool(mut))
mut=bytearray(rom);_,start,data=rows[0];mut[start+len(data)-1]=1
rejected('lost_terminator_crosses_group',lambda:pool(mut))
# Keep all original text private; only coverage categories and hashes leave RAM.
unknown=collections.Counter(b for _,_,data in rows for b in data if b not in SAFE and not 0xab<=b<=0xc8 and b not in c.dictionary)
controls=collections.Counter(b for _,_,data in rows for b in data if 0xab<=b<=0xc8)
report={'checkpoint':'combat-v058-codec','release_unchanged':'v0.56','baseline_sha256':BASELINE_SHA,'source_intact_JP_checked':True,'BPS_reapplied':True,'ROM_bytes':len(rom),'pool_entries':len(rows),'pool_bytes':sum(len(data) for _,_,data in rows),'physical_aliases':0,'pool_pointer_bounds_and_nonoverlap_checked':True,'main_live_groups_measured':len(regions),'main_visible_selections_unchanged':6957,'prepared_total_unchanged':107,'new_translations':0,'new_inserted':0,'canonical_roundtrip_preparation_ids':good,'unsupported_preparations':bad,'unsupported_characters_entry_counts':dict(coverage),'dictionary_entries_read_locally':len(c.dictionary),'native_command_occurrences':{f'{k:02X}':v for k,v in sorted(controls.items())},'unapproved_original_byte_occurrences':{f'{k:02X}':v for k,v in sorted(unknown.items())},'rejected_mutations':rejections,'native_encoding_candidate_only':True,'renderer_approved':False,'full_main_reread_progress':0,'limits':['43 strict byte encodings are candidate encodings, not inserted or runtime validated messages.','64 preparations require accents not present in the safe byte alphabet; no lossy fallback used.','The old English documentation maps ! to81, but current VF font maps7A to! and81 toellipsis.','0C..0F shadow glyphs and all unapproved source bytes are excluded from ordinary textual encoding.','No extension of the global byte charset, dictionary, engine or native commands has been made.','497 inherited battle texts and semantic reserves464/465 remain open.']}
(O/'qa-codec.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['unsupported_preparations','native_command_occurrences','canonical_roundtrip_preparation_ids']},ensure_ascii=False))
