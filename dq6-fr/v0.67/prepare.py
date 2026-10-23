from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--ds',type=Path,required=True);p.add_argument('--ips',type=Path,required=True);a=p.parse_args();jp=a.jp.read_bytes();ds=a.ds.read_bytes();ips=a.ips.read_bytes();assert sha(ds)=='5667303e3c7ab518a1b6bb2119abdfcc17422b3387dc5083f67b8e2b54734fb5';assert sha(ips)=='b34155f476d0bce3d2247c577417b3ade3ee071e7c9b8af634f8a7cb613cdd37';base,m=prepare(jp)
# Check actual DS MPT records directly at the indexed source-file offsets.
sys.path.insert(0,str(R/'dq6-fr'));from probe import lz10
files={x['path']:x for x in read(R/'dq6-fr/clean-base/nds-files.json')}
for row in m['rows']:
 for ref in row['DS_references']:
  for lang in ['JA','FR']:
   entry=files[ref[lang+'_file']];raw=ds[entry['offset']:entry['offset']+entry['size']];raw=lz10(raw) if raw[0]==16 else raw;assert raw[:4]==b'MPT0';size,lo,hi,n,tab,ts,txt=struct.unpack_from('<7I',raw,4);hits=[]
   for i in range(n):
    mid,length,off=struct.unpack_from('<HHH',raw,tab+6*i)
    if mid==ref['id']:hits.append(raw[tab+ts+off*4:tab+ts+off*4+length].decode())
   assert hits==[ref[lang+'_text']]
# Apply the old headered IPS privately; record exact secondary source labels.
vf=bytearray(512)+bytearray(jp);i=5;assert ips[:5]==b'PATCH'
while ips[i:i+3]!=b'EOF':
 off=int.from_bytes(ips[i:i+3],'big');n=int.from_bytes(ips[i+3:i+5],'big');i+=5
 if n:data=ips[i:i+n];i+=n
 else:n=int.from_bytes(ips[i:i+2],'big');data=ips[i+2:i+3]*n;i+=3
 assert off+n<=len(vf);vf[off:off+n]=data
assert i+3==len(ips);vf=bytes(vf[512:]);codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'));old=names(vf)
for row in m['rows']:assert codec.decode(old[row['sid']][1])==row['previous']+'{AC}'
(O/'revue-lieux-v067.json').write_text(json.dumps(m['rows'],ensure_ascii=False,indent=2)+'\n');q=dict(release='v0.67',source_SHA256=dict(JP=sha(jp),DS=sha(ds),IPS=sha(ips)),actual_DS_MPT_records_checked=2*sum(len(x['DS_references']) for x in m['rows']),old_IPS_name_rows_checked=10,selected_SIDs=NEW_SIDS,previous_prepared=17,now_resolved_for_insertion=10,prepared_remaining=7,net_name_pool_growth=0,preserved_tail_untouched=True)
(O/'revue-stockage.json').write_text(json.dumps(m['storage'],ensure_ascii=False,indent=2)+'\n');(O/'qa-sources.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print('10 place names: JP,actualDS and IPS verified')
