from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--ds',type=Path,required=True);p.add_argument('--ips',type=Path,required=True);a=p.parse_args();jp=a.jp.read_bytes();ds=a.ds.read_bytes();ips=a.ips.read_bytes();assert sha(ds)=='5667303e3c7ab518a1b6bb2119abdfcc17422b3387dc5083f67b8e2b54734fb5';assert sha(ips)=='b34155f476d0bce3d2247c577417b3ade3ee071e7c9b8af634f8a7cb613cdd37';base=baseline(jp);rows=selection(base)
sys.path.insert(0,str(R/'dq6-fr'));from probe import lz10
files={x['path']:x for x in read(R/'dq6-fr/clean-base/nds-files.json')};checked=0
for row in rows:
 for ref in row['DS_references']:
  for lang in ['JA','FR']:
   f=files[ref[lang+'_file']];raw=ds[f['offset']:f['offset']+f['size']];raw=lz10(raw) if raw[0]==16 else raw;assert raw[:4]==b'MPT0';_,lo,hi,n,tab,ts,txt=struct.unpack_from('<7I',raw,4);hits=[]
   for i in range(n):
    mid,length,off=struct.unpack_from('<HHH',raw,tab+6*i)
    if mid==ref['id']:hits.append(raw[tab+ts+off*4:tab+ts+off*4+length].decode())
   assert hits==[ref[lang+'_text']];checked+=1
save('selection.json',rows);save('delta-lisible.json',[dict(id=x['id'],old_text=x['old_text'],text=x['text'],changes=x['changes'],pause_count=x['pause_count']) for x in rows]);save('qa-sources.json',dict(JP_sha256=sha(jp),DS_sha256=sha(ds),IPS_sha256=sha(ips),DS_fields_checked_from_ROM=checked,fuzzy_match_used=False,revisions=len(rows),new_translations=0));print('3 prepared;DS ROM fields',checked)
