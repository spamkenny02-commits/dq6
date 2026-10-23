"""Exact native-font foreground comparisons, supplementing source/visual review.
This is not semantic proofreading or proof of natural battle reachability.
"""
from common import *
from PIL import Image
import argparse
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();rom=(a.out/'result.sfc').read_bytes();q=read(O/'qa-native-B5-all-objects.json');assert q['ROM_sha256']==sha(rom);codec=Codec(rom,read(R/'dq6-fr/v0.56/charset.json'));by={x['sids'][0]:x for x in SELECTION if x['kind']=='item'};rows=[]
for case in q['results']:
 x=by[case['name_SID']];name=x['proposal'];capture=case['pages'][-1];impath=a.out/capture['capture'];assert sha(impath.read_bytes())==capture['sha256'];im=Image.open(impath).resize((256,224),Image.Resampling.NEAREST);assert len(name)<=24
 for col,ch in enumerate(name):
  b=codec.forward[ch];expected=rom[parent.font.FONT+b*16:parent.font.FONT+b*16+16:2];observed=bytes(sum((1<<(7-px)) for px in range(8) if min(im.getpixel((24+8*col+px,168+y)))>180) for y in range(8))
  assert expected==observed,(case['B5_value'],name,col,ch,expected.hex(),observed.hex())
 rows.append(dict(position=x['position'],name_SID=case['name_SID'],item_ID=case['B5_value'],French_name=name,glyphs_exactly_matched=len(name),name_starts_native_pixel=[24,168],screenshot_sha256=capture['sha256']))
assert len(rows)==80
report=dict(release='v0.78',ROM_sha256=sha(rom),cases=80,all_name_foreground_glyph_pixels_match=True,characters_checked=sum(x['glyphs_exactly_matched'] for x in rows),semantic_review_replaced_by_pixel_check=False,natural_battle=False,rows=rows);(O/'qa-B5-pixel-match.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('80 full variable names match exact foreground glyphs')
