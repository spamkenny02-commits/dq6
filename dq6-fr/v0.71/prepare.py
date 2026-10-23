from common import *
import argparse,collections
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--ds',type=Path,required=True);p.add_argument('--ips',type=Path,required=True);a=p.parse_args();jp=a.jp.read_bytes();ds=a.ds.read_bytes();ips=a.ips.read_bytes();assert sha(ds)=='5667303e3c7ab518a1b6bb2119abdfcc17422b3387dc5083f67b8e2b54734fb5';assert sha(ips)=='b34155f476d0bce3d2247c577417b3ade3ee071e7c9b8af634f8a7cb613cdd37';base,m=prepare(jp)
sys.path.insert(0,str(R/'dq6-fr'));from probe import lz10
files={x['path']:x for x in read(R/'dq6-fr/clean-base/nds-files.json')};checked=0
for row in m['ledger']:
 for ref in row['DS_references']:
  for lang in ['JA','FR']:
   x=files[ref[lang+'_file']];raw=ds[x['offset']:x['offset']+x['size']];raw=lz10(raw) if raw[0]==16 else raw;assert raw[:4]==b'MPT0';size,lo,hi,n,tab,ts,txt=struct.unpack_from('<7I',raw,4);hits=[]
   for i in range(n):
    mid,length,off=struct.unpack_from('<HHH',raw,tab+6*i)
    if mid==ref['id']:hits.append(raw[tab+ts+off*4:tab+ts+off*4+length].decode())
   assert hits==[ref[lang+'_text']];checked+=1
vf=bytearray(512)+bytearray(jp);i=5;assert ips[:5]==b'PATCH'
while ips[i:i+3]!=b'EOF':
 at=int.from_bytes(ips[i:i+3],'big');n=int.from_bytes(ips[i+3:i+5],'big');i+=5
 if n:data=ips[i:i+n];i+=n
 else:n=int.from_bytes(ips[i:i+2],'big');data=ips[i+2:i+3]*n;i+=3
 assert at+n<=len(vf);vf[at:at+n]=data
assert i+3==len(ips);vf=bytes(vf[512:]);old=names(vf);ot=LogicalTable(vf);codec=Codec(base,read(R/'dq6-fr/v0.56/charset.json'))
for row in m['ledger']:
 raw=old[row['sids'][0]][1]
 try:text=codec.decode(raw)[:-4]
 except Exception:text=ot.text(row['sids'][0])
 row['secondary_IPS_text']=text;row['secondary_IPS_message_sha256']=sha(raw)
for row in m['rows']:assert codec.decode(old[row['sid']][1])==row['previous']+'{AC}'
for name,data in [('revue-table-v071.json',m['rows']),('registre-positions-0800-1199.json',m['ledger'])]:(O/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
counts=dict(collections.Counter(x['status'] for x in m['ledger']));q=dict(release='v0.71',physical_positions_examined=400,positions=[800,1199],new_label_insertions=32,new_translations=17,existing_french_revisions=15,existing_french_source_reviewed=1,new_preparations=counts.get("PREPARE_NON_INSERE",0),status_counts=counts,next_position_to_examine=1200,source_SHA256=dict(JP=sha(jp),DS=sha(ds),IPS=sha(ips)),actual_DS_fields_checked=checked,secondary_IPS_positions_checked=400,all400_semantically_validated=False,natural_windows_validated=False)
(O/'qa-lot400.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps(q))
