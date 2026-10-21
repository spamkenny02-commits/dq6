"""Read-only proof that the final JP extraction crosses into the name pool.
No text truncation, insertion or terminator repair is authorized by this audit.
"""
from pathlib import Path
import json,struct,hashlib
D=Path(__file__).resolve().parent;R=D.parent;O=D/'v0.55';raw=(R/'upload/Dragon Quest VI - Maboroshi no Daichi (Japan).sfc').read_bytes();jp=json.loads((D/'clean-base/sfc-jp.json').read_text());source=jp[6956];pos=source['offset'];bit=source['bit'];trees=[struct.unpack_from('<1064H',raw,a) for a in [0x167be,0x1700e]]
# extract.py uses 0x884e (root node 0x084e), not the VF tree.
trace=[]
for i,t in enumerate(source['tokens']):
 start=[pos,bit];v=0x884e
 while v&32768:
  b=(raw[pos]>>bit)&1;bit-=1
  if bit<0:pos+=1;bit=7
  v=trees[b][(v&32767)//2]
 assert v&8191==t
 trace.append(dict(index=i,token=t,start=start,end=[pos,bit],crosses_name_pool=pos>=0x3b8703))
assert trace[43]['token']==0xaf and trace[43]['end']==[0x3b8702,7]
assert any(x['crosses_name_pool'] for x in trace[44:])
report=dict(id=6956,source_sha256=hashlib.sha256(raw).hexdigest(),script_end_exclusive=0x3b8703,name_pool_start=0x3b8703,source_text=source['text'],valid_prefix_through_AF_token_index=43,subsequent_tokens_not_a_reliable_dialogue=True,trace=trace,status='PREPARE_NON_INSERE',blocker='Need native last-message termination proof before replacing the truncated tail. No AC present within the bounded meaningful prefix.',ds_reference=dict(file='data/MESS6/JA/0816.p',id=12),proposed_french='Tulipe. {C9} a encore quelque chose à accomplir, non ?{AF}',limits='Does not establish a valid native terminator, natural inn scene, or repair the ROM.')
(O/'qa-frontiere-6956.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('6956 boundary audit retained without insertion')
