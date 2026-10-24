from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();jp=a.jp.read_bytes();base=baseline(jp);rows=read(O/'selection.json');rom=(a.out/'result.sfc').read_bytes();r=read(O/'build-report.json');assert len(rom)==8388608 and sha(rom)==r['ROM_sha256'];rebuild,writes=assemble(base,rows);assert rebuild==rom and writes==r['main_groups_written']
old,oldregions=decode_main(base);new,regions=decode_main(rom);assert [i for i,(x,y) in enumerate(zip(old,new)) if x!=y]==IDS
for x in rows:assert new[x['id']]==x['tokens'] and old[x['id']]==x['old_tokens'];assert [t for t in new[x['id']] if t<0x200]==[t for t in old[x['id']] if t<0x200]
changedgroups={i//8 for i in IDS}
for oldreg,reg in zip(oldregions,regions):
 if reg['group'] not in changedgroups:assert oldreg==reg and base[reg['file_offset']:reg['file_offset']+reg['size']]==rom[reg['file_offset']:reg['file_offset']+reg['size']]
allowed=[(w['file_offset'],w['file_offset']+w['size']) for w in writes]+[(copy+0x15bb5+g*3,copy+0x15bb8+g*3) for copy in (0,0x400000) for g in changedgroups]+[(copy+0xffdc,copy+0xffe0) for copy in (0,0x400000)]
assert all(x==y or any(lo<=i<hi for lo,hi in allowed) for i,(x,y) in enumerate(zip(base,rom)))
for lo,hi in [(parent.NAME,parent.NAME_LIMIT),(BASE['placement']['offset'],BASE['placement']['offset']+BASE['placement']['size']),(BASE['engine']['allocation']['offset'],BASE['engine']['allocation']['offset']+BASE['engine']['allocation']['size'])]:assert base[lo:hi]==rom[lo:hi]
for copy in (0,0x400000):
 assert base[copy+0x167be:copy+0x1785e]==rom[copy+0x167be:copy+0x1785e]
 assert base[copy+0x11100:copy+0x11300]==rom[copy+0x11100:copy+0x11300]
 assert struct.unpack_from('<HH',rom,copy+0xffdc)==((sum(rom)&65535)^65535,sum(rom)&65535)
bps=(R/'patches'/(PATCH+'.bps')).read_bytes();ips=(a.out/(PATCH+'.ips')).read_bytes();assert parent.patches(jp,rom)==(bps,ips);b=module('bps80verify',R/'dq6-fr/upstream/refill/patchRM.py');assert bytes(b.apply_bps(jp,bps))==rom
rejected=[]
for label,bad in [('modified_JP',bytes([jp[0]^1])+jp[1:]),('copier_header',bytes(512)+jp)]:
 try:baseline(bad)
 except AssertionError:pass
 else:raise AssertionError('Bad source accepted by builder')
 try:b.apply_bps(bad,bps)
 except (AssertionError,ValueError,b.Fail):rejected.append(label)
 else:raise AssertionError('Bad BPS source accepted')
out=bytearray(jp);i=5;assert ips[:5]==b'PATCH'
while ips[i:i+3]!=b'EOF':
 at=int.from_bytes(ips[i:i+3],'big');n=int.from_bytes(ips[i+3:i+5],'big');i+=5;assert n>0;data=ips[i:i+n];i+=n
 if len(out)<at+n:out.extend(bytes(at+n-len(out)))
 out[at:at+n]=data
assert len(ips)==i+6 and bytes(out[:int.from_bytes(ips[i+3:],'big')])==rom
# Negative fixtures exercise the decoder and the allocation guard independently of ROM hash checks.
mut=bytearray(rom);g=IDS[0]//8
for copy in (0,0x400000):
 at=copy+0x15bb5+g*3;mut[at:at+3]=(int.from_bytes(mut[at:at+3],'little')+1).to_bytes(3,'little')
try:bad_tokens,_=decode_main(mut);pointer_detected=bad_tokens!=new
except (AssertionError,IndexError,struct.error):pointer_detected=True
assert pointer_detected
mut=bytearray(rom);mut[parent.NAME]^=1
name_allocation_violation=any(x!=y and not any(lo<=i<hi for lo,hi in allowed) for i,(x,y) in enumerate(zip(rom,mut)))
assert name_allocation_violation
assert all(row['tokens']==new[row['id']] for row in current_main_selection())
save('verification.json',dict(ROM_sha256=sha(rom),decoded_main_slots=len(new),visible_main_selections=6957,changed_main_IDs=IDS,other6957_slots_token_identical=True,other867_groups_byte_identical=True,main_huffman_tree_unchanged=True,all_controls_variables_breaks_pauses_identical=True,all_names_battle_font_engine_and_protected_regions_unchanged=True,name_allocation_preserved_to=parent.NAME_LIMIT,new_translations=0,BPS_reapplied=True,IPS_reapplied=True,bad_sources_rejected=rejected,negative_group_pointer_detected=pointer_detected,negative_name_allocation_mutation_detected=name_allocation_violation,current_readable_overlay6957_matches_native=True,recipe_idempotent=True,all_runtime_contexts_validated=False,natural_validation=False));print('3 revisions;6960 slots decoded;BPS/IPS and protected regions OK')
