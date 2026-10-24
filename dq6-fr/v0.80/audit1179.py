"""Metadata repair only; native tokens remain exactly unchanged."""
from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--ds',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();base=baseline(a.jp.read_bytes());rom=(a.out/'result.sfc').read_bytes();assert sha(rom)==read(O/'build-report.json')['ROM_sha256'];before,_=decode_main(base);after,_=decode_main(rom);assert before[1179]==after[1179] and after[1179].count(0xc9)==1
row=next(x for x in current_main_selection() if x['id']==1179);meta=read(O/'metadata-1179.json');assert sha256_tokens(after[1179])==meta['tokens_sha256'];assert row['tokens']==after[1179] and row['text'].count(chr(0xe0c9))==1 and row['lines'][1].startswith(chr(0xe0c9))
reg=next(x for x in read(R/'preparations/relecture-principale-0900-1299/registre-relecture.json') if x['id']==1179);ds=a.ds.read_bytes();assert sha(ds)=='5667303e3c7ab518a1b6bb2119abdfcc17422b3387dc5083f67b8e2b54734fb5';sys.path.insert(0,str(R/'dq6-fr'));from probe import lz10
files={x['path']:x for x in read(R/'dq6-fr/clean-base/nds-files.json')};checked=[]
for ref in reg['DS_references']:
 for lang in ['JA','FR']:
  f=files[ref[lang+'_file']];raw=ds[f['offset']:f['offset']+f['size']];raw=lz10(raw) if raw[0]==16 else raw;assert raw[:4]==b'MPT0';_,lo,hi,n,tab,ts,txt=struct.unpack_from('<7I',raw,4);texts=[]
  for i in range(n):
   mid,length,off=struct.unpack_from('<HHH',raw,tab+6*i)
   if mid==ref['id']:texts.append(raw[tab+ts+off*4:tab+ts+off*4+length].decode())
  assert texts==[ref[lang+'_text']];checked.append(dict(file=ref[lang+'_file'],id=ref['id'],text=texts[0]))
save('audit-variable1179.json',dict(id=1179,compiled_tokens_unchanged=True,C9_occurrences=1,token_sha256=sha256_tokens(after[1179]),metadata_U_E000_replaced_by_U_E0C9=True,DS_fields_checked_from_ROM=checked,native_diagnostic_report='qa-render-1179.json',observed_hero_name='AAAAAAAA',all_two_pages_visually_read=True,no_overflow_observed=True,natural_Judith_scene_tested=False,scope='Réserve de représentation résolue ; contexte naturel reste nonvalidé.'))
