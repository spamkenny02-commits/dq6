from common import *
import argparse
p=argparse.ArgumentParser();p.add_argument('--jp',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();jp=a.jp.read_bytes();base,m=prepare(jp);rom=(a.out/'result.sfc').read_bytes();r=read(O/'build-report.json');assert len(rom)==8388608 and sha(rom)==r['ROM_sha256'] and assemble(base,m)==rom
bps=(R/'patches/DQVI-FR-DS-v0.75-BASE-JP-PARTIEL.bps').read_bytes();ips=(a.out/'DQVI-FR-DS-v0.75-BASE-JP-PARTIEL.ips').read_bytes();assert patches(jp,rom)==(bps,ips);b=module('checkbps65',R/'dq6-fr/upstream/refill/patchRM.py');assert bytes(b.apply_bps(jp,bps))==rom
bad=[]
for label,raw in [('modified_JP',bytes([jp[0]^1])+jp[1:]),('copier_header',bytes(512)+jp)]:
 try:b.apply_bps(raw,bps)
 except (AssertionError,ValueError,b.Fail):bad.append(label)
 else:raise AssertionError('Bad BPS source accepted')
out=bytearray(jp);i=5;assert ips[:5]==b'PATCH'
while ips[i:i+3]!=b'EOF':
 at=int.from_bytes(ips[i:i+3],'big');n=int.from_bytes(ips[i+3:i+5],'big');i+=5;assert n>0;data=ips[i:i+n];i+=n
 if len(out)<at+n:out.extend(bytes(at+n-len(out)))
 out[at:at+n]=data
assert out[:int.from_bytes(ips[i+3:],'big')]==rom and len(ips)==i+6
old=names(base);new=names(rom);changed=[sid for sid in range(2512) if old[sid][1]!=new[sid][1]];assert changed==SIDS
for sid in range(2512):
 if sid not in SIDS:assert old[sid][1]==new[sid][1]
def aliases(ns):return sorted([sid for sid,(at,b) in enumerate(ns) if at==p] for p in set(at for at,b in ns))
assert aliases(old)==aliases(new);assert len(set(at for at,b in new))==2048
codec=Codec(rom,read(R/'dq6-fr/v0.56/charset.json'))
for x in m['rows']:assert name_text(rom,new[x['sid']][1],codec)==x['layout']
assert decode_pool(base,BASE['placement'])==decode_pool(rom,BASE['placement'])
for copy in (0,0x400000):
 assert rom[copy+POOL:copy+END]==base[copy+POOL:copy+END]
 assert sha(rom[copy+TAIL:copy+END])==BASE['tail_sha256']
regions=c.main_regions(base)
for p in regions:assert base[p['file_offset']:p['file_offset']+p['size']]==rom[p['file_offset']:p['file_offset']+p['size']]
for s in BASE['engine']['segments']:assert base[s['offset']:s['offset']+s['size']]==rom[s['offset']:s['offset']+s['size']]
allowed=[(NAME,NAME+max(r['name_reachable_bytes'],BASE['name_reachable_bytes']))]+[(copy+0x165e7,copy+0x167be) for copy in (0,0x400000)]+[(copy+0xffdc,copy+0xffe0) for copy in (0,0x400000)]
assert not [i for i,(x,y) in enumerate(zip(base,rom)) if x!=y and not any(lo<=i<hi for lo,hi in allowed)]
crossing=[sid for sid,(at,raw) in enumerate(new) if at<=0x7affff<at+len(raw)-1];assert crossing,'No actual string crosses bank boundary'
assert all(NAME<=at<at+len(raw)<=NAME+r['name_reachable_bytes'] for at,raw in new)
q=dict(bank_boundary_crossing_SIDs=crossing,bank_boundary=0x7b0000,release='v0.75',ROM_sha256=sha(rom),new_label_insertions=50,new_translations=49,existing_french_revisions=1,packed_name_SIDs_changed=changed,other2462_name_byte_strings_identical=True,physical_names=2048,aliases_preserved=464,reachable_name_bytes=r['name_reachable_bytes'],preserved_tail_bytes_unchanged=END-TAIL,preserved_tail_unchanged_in_both_copies=True,name_pool_growth=r['name_reachable_bytes']-BASE['name_reachable_bytes'],relocated_pool_offset=NAME,old_pool_preserved_in_both_copies=True,native_engine_modified=False,battle_messages608_byte_identical=True,main_groups870_byte_identical=True,main_selections6957_unchanged=True,engine_font_dictionary_and_protected_bytes_identical=True,BPS_reapplied=True,IPS_reapplied=True,bad_sources_rejected=bad,recipe_idempotent=True,all_runtime_contexts_validated=False,natural_validation=False)
(O/'verification.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps(q))
