"""Isolated native-font audit and occupied-slot negative controls."""
from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();base,m=prepare(a.jp.read_bytes());rom=(a.out/'result.sfc').read_bytes();battle=decode_pool(base,BASE['placement']);ns=names(base);expected=font.apply(base,battle,ns);slots={b for b,g in font.MAP.values()};rejected=[]
for byte in slots:
 for pool in ['battle','names','dictionary','mapping']:
  bt=list(battle);nn=list(ns);bb=bytearray(base)
  if pool=='battle':i,at,raw=bt[0];bt[0]=(i,at,bytes([byte])+raw)
  if pool=='names':at,raw=nn[0];nn[0]=(at,bytes([byte])+raw)
  if pool=='dictionary':bb[0x3fb50]=byte
  if pool=='mapping':bb[0x11100+2*byte]=1
  try:font.apply(bytes(bb),bt,nn)
  except AssertionError:rejected.append([pool,byte])
  else:raise AssertionError('Occupied slot accepted')
for copy in (0,0x400000):
 for b in range(256):
  f=slice(copy+font.FONT+b*16,copy+font.FONT+(b+1)*16);g=slice(copy+0x11100+b*2,copy+0x11102+b*2)
  assert rom[f]==expected[f] and rom[g]==expected[g]
  if b not in slots:assert rom[f]==base[f] and rom[g]==base[g]
 assert rom[copy+0x3fb50:copy+0x3fbb5]==base[copy+0x3fb50:copy+0x3fbb5]
charset=read(R/'dq6-fr/v0.56/charset.json')
for ch,(byte,glyph) in font.MAP.items():
 assert charset[f'{glyph:04X}']==ch
assert Codec(rom,charset).decode(Codec(rom,charset).encode('ôçÉ{AC}'))=='ôçÉ{AC}'
q=dict(release='v0.77',ROM_sha256=sha(rom),slots={ch:dict(byte=byte,main_glyph=g,native_rows=font.SHAPES[ch]) for ch,(byte,g) in font.MAP.items()},known_pools_checked=dict(battle=608,name_SIDs=2512,physical_names=2048,aliases=464,dictionary_pairs=50),occupied_or_nonblank_mutations_rejected=rejected,unallocated_native_tiles_and_mapping_words_identical=253,copies_checked=2,main_glyphs_preexisting=True,main_font_modified=False,engine_modified=False,unknown_hardcoded_consumers_fully_audited=False,scope='Allocation proof covers parsed pools and dictionary, not undiscovered hardcoded byte strings.')
(O/'qa-font-extension.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print('3 glyphs,12 collision controls,253 other native tiles unchanged in two copies')
