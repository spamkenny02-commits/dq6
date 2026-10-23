from common import *
import argparse,collections
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--ds',type=Path,required=True);p.add_argument('--ips',type=Path,required=True);a=p.parse_args();jp=a.jp.read_bytes();ds=a.ds.read_bytes();ips=a.ips.read_bytes();assert sha(ds)=='5667303e3c7ab518a1b6bb2119abdfcc17422b3387dc5083f67b8e2b54734fb5';assert sha(ips)=='b34155f476d0bce3d2247c577417b3ade3ee071e7c9b8af634f8a7cb613cdd37';base,m=prepare(jp);m['ledger']=[dict(x,DS_references=x['DS_references']) for x in SELECTION]
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
for row in m['rows']:assert name_text(base,old[row['sid']][1],codec)==row['previous']
(O/'revue-table-v077.json').write_text(json.dumps(m['rows'],ensure_ascii=False,indent=2)+'\n')
for x in m['ledger']:x['status']='INTEGRE_v077';x['natural_context_validated']=False
(O/'preparations-resolues.json').write_text(json.dumps(m['ledger'],ensure_ascii=False,indent=2)+'\n')
(O/'qa-sources.json').write_text(json.dumps(dict(source_SHA256=dict(JP=sha(jp),DS=sha(ds),IPS=sha(ips)),DS_fields_checked=checked,IPS_positions_checked=len(SELECTION),JP_exact_matches=len(SELECTION),fuzzy_matches_used=0,new_label_insertions=len(SELECTION),new_translations=5,existing_french_revisions=0,natural_validation=False),ensure_ascii=False,indent=2)+'\n')
