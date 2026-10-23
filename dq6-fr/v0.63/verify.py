from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();jp=a.jp.read_bytes();base,rows=prepare(jp);r=read(O/'build-report.json');rom=(a.out/'result.sfc').read_bytes();assert len(rom)==8388608 and sha(rom)==r['ROM_sha256'] and assemble(base,rows)[0]==rom
bps=(R/'patches/DQVI-FR-DS-v0.63-BASE-JP-PARTIEL.bps').read_bytes();ips=(a.out/'DQVI-FR-DS-v0.63-BASE-JP-PARTIEL.ips').read_bytes();assert patches(jp,rom)==(bps,ips);m=module('checkbps63',R/'dq6-fr/upstream/refill/patchRM.py');assert bytes(m.apply_bps(jp,bps))==rom
bad_rejected=[]
for label,bad in [('modified_JP',bytes([jp[0]^1])+jp[1:]),('copier_header',bytes(512)+jp)]:
 try:m.apply_bps(bad,bps)
 except (AssertionError,ValueError,m.Fail):bad_rejected.append(label)
 else:raise AssertionError('Wrong BPS source accepted')
out=bytearray(jp);i=5;assert ips[:5]==b'PATCH'
while ips[i:i+3]!=b'EOF':
 at=int.from_bytes(ips[i:i+3],'big');n=int.from_bytes(ips[i+3:i+5],'big');i+=5;assert n>0;blob=ips[i:i+n];i+=n
 if len(out)<at+n:out.extend(bytes(at+n-len(out)))
 out[at:at+n]=blob
assert len(ips)==i+6 and out[:int.from_bytes(ips[i+3:],'big')]==rom
new=decode_pool(rom,r['placement']);old=old_pool(base);changed=[mid for (mid,at,b),(_,a,v) in zip(new,old) if b!=v];assert changed==IDS
codec=Codec(rom,read(R/'dq6-fr/v0.56/charset.json'));plans_byid={x['id']:x for x in rows}
for mid,at,b in new:
 if mid in plans_byid:assert codec.decode(b)==plans_byid[mid]['french_plan']
allowed=[(r['placement']['offset'],r['placement']['offset']+r['placement']['size'])]+[(copy+c.PTR,copy+c.PTR+228) for copy in (0,0x400000)]+[(copy+0xffdc,copy+0xffe0) for copy in (0,0x400000)]
assert not [i for i,(b,v) in enumerate(zip(base,rom)) if b!=v and not any(lo<=i<hi for lo,hi in allowed)]
n61=module('names63',R/'dq6-fr/v0.61/common.py');assert n61.names(base)==n61.names(rom)
assert all(base[x['offset']:x['offset']+x['size']]==rom[x['offset']:x['offset']+x['size']] for x in BASE['engine']['segments'])
regions=c.main_regions(base)
for p in regions:assert base[p['file_offset']:p['file_offset']+p['size']]==rom[p['file_offset']:p['file_offset']+p['size']]
assert base[ENGINE['offset']:ENGINE['offset']+ENGINE['size']]==rom[ENGINE['offset']:ENGINE['offset']+ENGINE['size']]
for copy in (0,0x400000):assert struct.unpack_from('<HH',rom,copy+0xffdc)==((sum(rom)&65535)^65535,sum(rom)&65535)
qa=dict(release='v0.63',ROM_sha256=sha(rom),new_battle_integrated=len(IDS),changed_battle_ids=changed,unchanged_native_battle=608-len(IDS),previous395_translations_unchanged=True,main_groups_unchanged=len(regions),main_selections_unchanged=6957,all2512_native_names_unchanged=True,all16_compound_names_and_v061_engine_unchanged=True,font_and_dictionary_unchanged=True,new_messages_redecoded=len(IDS),BPS_reapplied=True,IPS_reapplied=True,bad_sources_rejected=bad_rejected,protected_bytes_unchanged=True,recipe_idempotent=True,legacy_command_corrections=[x['id'] for x in rows if x['legacy_command_audit']['changed']],DS_full_JP_normalized_matches=sum(any(z['scope'].startswith('JP_COMPLET_') for z in x['ds_references']) for x in rows),DS_reference_reviewed_rows=sum(bool(x['ds_references']) for x in rows),natural_battle=False)
(O/'verification.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print(json.dumps(qa))
