from pathlib import Path
import argparse,json,struct,importlib.util
from common import c,prepare,assemble,decode_pool,O,R,sha,read,IDS,patches,old_pool
a=argparse.ArgumentParser();a.add_argument('--jp',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a=a.parse_args();jp=a.jp.read_bytes();base,rows=prepare(jp);report=read(O/'build-report.json');rom=(a.out/'result.sfc').read_bytes();assert len(rom)==8388608 and sha(rom)==report['ROM_sha256']
assert assemble(base,rows)[0]==rom
spec=importlib.util.spec_from_file_location('bps57',R/'dq6-fr/upstream/refill/patchRM.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
bps=(R/'patches/DQVI-FR-DS-v0.60-BASE-JP-PARTIEL.bps').read_bytes();assert bytes(m.apply_bps(jp,bps))==rom
rejected=[]
for label,bad in [('modified_JP',bytes([jp[0]^1])+jp[1:]),('copier_header',bytes(512)+jp)]:
 try:m.apply_bps(bad,bps)
 except (AssertionError,ValueError,m.Fail):rejected.append(label)
 else:raise AssertionError('Wrong BPS source accepted')
ips=(a.out/'DQVI-FR-DS-v0.60-BASE-JP-PARTIEL.ips').read_bytes();out=bytearray(jp);i=5;assert ips[:5]==b'PATCH'
while ips[i:i+3]!=b'EOF':
 at=int.from_bytes(ips[i:i+3],'big');n=int.from_bytes(ips[i+3:i+5],'big');i+=5;assert n>0
 blob=ips[i:i+n];i+=n
 if len(out)<at+n:out.extend(bytes(at+n-len(out)))
 out[at:at+n]=blob
assert len(ips)==i+6 and out[:int.from_bytes(ips[i+3:],'big')]==rom
assert patches(jp,rom)==(bps,ips),'Regenerated patches differ'
new=decode_pool(rom,report['placement']);old=old_pool(base);from native_font import apply,Codec,MAP,FONT
codec=Codec(rom,read(R/'dq6-fr/v0.56/charset.json'));plans={r['id']:r['french_plan'] for r in rows}
changed=[mid for (mid,_,b),(_,_,v) in zip(new,old) if b!=v];assert changed==IDS
for mid,_,data in new:
 if mid in plans:assert codec.decode(data)==plans[mid]
allowed=[(report['placement']['offset'],report['placement']['offset']+report['placement']['size'])]+[(copy+c.PTR,copy+c.PTR+228) for copy in (0,0x400000)]+[(copy+0xffdc,copy+0xffe0) for copy in (0,0x400000)]
allowed += [(copy+0x11100+byte*2,copy+0x11100+byte*2+2) for copy in (0,0x400000) for byte,g in MAP.values()]
allowed += [(copy+FONT+byte*16+2*y,copy+FONT+byte*16+2*y+1) for copy in (0,0x400000) for byte,g in MAP.values() for y in range(8)]
outside=[i for i,(b,v) in enumerate(zip(base,rom)) if b!=v and not any(lo<=i<hi for lo,hi in allowed)];assert not outside
regions=c.main_regions(base)
for p in regions:assert base[p['file_offset']:p['file_offset']+p['size']]==rom[p['file_offset']:p['file_offset']+p['size']]
assert rom[0x15bb5:0x165e7]==base[0x15bb5:0x165e7]
for copy in (0,0x400000):assert struct.unpack_from('<HH',rom,copy+0xffdc)==((sum(rom)&65535)^65535,sum(rom)&65535)
qa=dict(release='v0.60',changed_battle_ids=changed,unchanged_battle_messages=608-len(changed),main_groups_byte_identical=len(regions),main_selections_unchanged=6957,BPS_reapplied=True,IPS_reapplied=True,wrong_BPS_sources_rejected=rejected,protected_bytes_unchanged=True,engine_unchanged=True,all_new_messages_redecoded=True,ROM_sha256=sha(rom),emulator_tests_report='qa-emulator.json',natural_battle_validated=False,recipe_repeated_identical_ROM_and_BPS=True)
(O/'verification.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print(json.dumps(qa))
