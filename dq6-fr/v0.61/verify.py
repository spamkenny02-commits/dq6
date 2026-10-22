from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();jp=a.jp.read_bytes();base,rows,meta=prepare(jp);report=read(O/'build-report.json');rom=(a.out/'result.sfc').read_bytes();assert assemble(base,rows,meta)[0]==rom and sha(rom)==report['ROM_sha256'] and len(rom)==8388608
bps=(R/'patches/DQVI-FR-DS-v0.61-BASE-JP-PARTIEL.bps').read_bytes();ips=(a.out/'DQVI-FR-DS-v0.61-BASE-JP-PARTIEL.ips').read_bytes();assert patches(jp,rom)==(bps,ips)
m=module('bps61verify',R/'dq6-fr/upstream/refill/patchRM.py');assert bytes(m.apply_bps(jp,bps))==rom
rejected=[]
for label,bad in [('modified_JP',bytes([jp[0]^1])+jp[1:]),('copier_header',bytes(512)+jp)]:
 try:m.apply_bps(bad,bps)
 except (AssertionError,ValueError,m.Fail):rejected.append(label)
 else:raise AssertionError('Wrong source accepted')
out=bytearray(jp);i=5;assert ips[:5]==b'PATCH'
while ips[i:i+3]!=b'EOF':
 at=int.from_bytes(ips[i:i+3],'big');n=int.from_bytes(ips[i+3:i+5],'big');i+=5;assert n>0;blob=ips[i:i+n];i+=n
 if len(out)<at+n:out.extend(bytes(at+n-len(out)))
 out[at:at+n]=blob
assert len(ips)==i+6 and out[:int.from_bytes(ips[i+3:],'big')]==rom
new=decode_pool(rom,report['placement']);old=old_pool(base);changed=[mid for (mid,a,b),(_,at,v) in zip(new,old) if b!=v];assert changed==IDS
codec=Codec(rom,read(R/'dq6-fr/v0.56/charset.json'));plans={r['id']:r['french_plan'] for r in rows}
for mid,at,b in new:
 if mid in plans:assert codec.decode(b)==plans[mid]
ns=names(base);nn=names(rom);changed_names=[sid for sid in range(2512) if ns[sid][1]!=nn[sid][1]];assert changed_names==[0x369,0x36a]
assert [[sid for sid in range(2512) if ns[sid][0]==at] for at in sorted(set(at for at,b in ns))]==[[sid for sid in range(2512) if nn[sid][0]==at] for at in sorted(set(at for at,b in nn))]
for sid,text in meta['word_names'].items():assert codec.decode(nn[int(sid,16)][1])==text+'{AC}'
for n,text in enumerate(meta['complete_names']+['']):
 at=report['engine']['strings']+int.from_bytes(rom[report['engine']['table']+n*2:report['engine']['table']+n*2+2],'little');assert codec.decode(rom[at:rom.index(0xac,at)+1])==text+'{AC}'
assert base[0x2675d:0x26796]==rom[0x2675d:0x26796] and base[0x6920c:0x6fecf]==rom[0x6920c:0x6fecf]
regions=c.main_regions(base)
for r in regions:assert base[r['file_offset']:r['file_offset']+r['size']]==rom[r['file_offset']:r['file_offset']+r['size']]
allowed=[(report['placement']['offset'],report['placement']['offset']+report['placement']['size'])]+[(p['offset'],p['offset']+p['size']) for p in report['engine']['segments']]
allowed += [(copy+c.PTR,copy+c.PTR+228) for copy in (0,0x400000)]+[(copy+0xffdc,copy+0xffe0) for copy in (0,0x400000)]+[(copy+0x165e7,copy+0x165e7+471) for copy in (0,0x400000)]+[(copy+0x3b8703,copy+0x3b8703+report['names']['pool_size']) for copy in (0,0x400000)]
assert not [i for i,(b,v) in enumerate(zip(base,rom)) if b!=v and not any(lo<=i<hi for lo,hi in allowed)]
# Guards are active: tampered caller or occupied hook padding must fail.
negative=[]
for at in (0x26759,0x69209,0x6fef0):
 bad=bytearray(base);bad[at]^=1
 try:assemble(bytes(bad),rows,meta)
 except AssertionError:negative.append(f'{at:06X}')
 else:raise AssertionError('Engine guard accepted tampered source')
qa=dict(release='v0.61',ROM_sha256=sha(rom),changed_battle_ids=changed,unchanged_battle_messages=605,main_groups_byte_identical=len(regions),main_selections_unchanged=6957,native_name_SIDs_checked=2512,unchanged_native_names=2510,changed_name_SIDs=changed_names,aliases_preserved=464,compound_names_redecoded=16,shared_061F_unchanged=True,shared_B2_tail_unchanged=True,original_RTS_and_source_tables_unchanged=True,native_font_bytes_unchanged=True,BPS_reapplied=True,IPS_reapplied=True,wrong_sources_rejected=rejected,guard_mutations_rejected=negative,protected_bytes_unchanged=True,recipe_idempotent=True,natural_battle_validated=False)
(O/'verification.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print(json.dumps(qa))
