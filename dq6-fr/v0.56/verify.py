"""Release checks independent of the build's writer and text reader."""
from pathlib import Path
import json,struct,zlib,hashlib,importlib.util
P=Path(__file__).resolve().parents[1];O=P/'v0.56';U=P.parent/'upload'
source=(U/'Dragon Quest VI - Maboroshi no Daichi (Japan).sfc').read_bytes();expected=(O/'result.sfc').read_bytes()
spec=importlib.util.spec_from_file_location('patchRM',P/'upstream/refill/patchRM.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
bps=(O/'DQVI-FR-DS-v0.56-BASE-JP-PARTIEL.bps').read_bytes();assert bytes(module.apply_bps(source,bps))==expected
rejected=[]
for label,bad in [('en_tete_copieur',bytes(512)+source),('source_modifiee',bytes([source[0]^1])+source[1:])]:
 try:module.apply_bps(bad,bps)
 except (ValueError,AssertionError,module.Fail):rejected.append(label)
 else:raise AssertionError('Wrong source accepted')
patch=(O/'DQVI-FR-DS-v0.56-BASE-JP-PARTIEL.ips').read_bytes();out=bytearray(source);i=5;assert patch[:5]==b'PATCH'
while patch[i:i+3]!=b'EOF':
 a=int.from_bytes(patch[i:i+3],'big');n=int.from_bytes(patch[i+3:i+5],'big');i+=5
 if n:blob=patch[i:i+n];i+=n
 else:n=int.from_bytes(patch[i:i+2],'big');blob=patch[i+2:i+3]*n;i+=3
 if len(out)<a+n:out.extend(b'\0'*(a+n-len(out)))
 out[a:a+n]=blob
assert len(patch)==i+6;out=out[:int.from_bytes(patch[i+3:],'big')];assert out==expected
checksum=sum(expected)&65535
for copy in [0,0x400000]:assert struct.unpack_from('<HH',expected,copy+0xffdc)==(checksum^65535,checksum)
old={r['id']:r for r in json.loads((P/'v0.55/insertion-candidates.json').read_text())};new={r['id']:r for r in json.loads((O/'insertion-candidates.json').read_text())}
assert set(old)<=set(new)
assert all(old[i]['tokens']==new[i]['tokens'] for i in old if i not in [5698,5699,5700])
assert len(new)-len(old)==json.loads((O/'couverture-preparation.json').read_text())['new_prepared']
# French alphabet/style markers only; all DS layout/conditional commands resolved.
for i,r in new.items():
 assert not any(c in r['text'] for c in ['%','@','㈡','㈢','и','я','И','Я','\ue100'])
 assert r['tokens'][-1] in [0xac,0xae]
 if i not in old:assert ''.join(r['lines']).replace(' ','')==r['text'].replace(' ',''),(i,'glyph sequence changed while wrapping')
from bounded_source import bounded
jp={r['id']:bounded(r) for r in json.loads((P/'clean-base/sfc-jp.json').read_text())}
protected={0xda,0xd5,0xb0,0xd6,0xbb,0xc1,0xb3,0xb2,0xc5,0xb5}
for mid,r in new.items():
 if mid in old:continue
 assert [t for t in jp[mid]['tokens'] if t in protected]==[t for t in r['tokens'] if t in protected],mid
 if 0xc0 in r['tokens']:assert 0xc0 in jp[mid]['tokens']
# Resolve every string ID independently by following the runtime pointers.
name_source=(P/'clean-base/vf-base-headered.sfc').read_bytes()[512:]
def name_entry(data,sid):
 a=0x3b8703+int.from_bytes(data[0x165e7+3*(sid>>4):0x165ea+3*(sid>>4)],'little')
 assert 0x3b8703<=a<0x3bc712
 for _ in range(sid&15):a=data.index(0xac,a)+1
 end=data.index(0xac,a);assert end<0x3bc712
 return data[a:end]
changed_name_ids=[sid for sid in range(2512) if name_entry(name_source,sid)!=name_entry(expected,sid)]
review=json.loads((O/'revue-lieux-v033.json').read_text());place_sids=sorted({sid for r in review for sid in r['runtime_sids']})
extra_names=json.loads((O/'revue-noms-v035.json').read_text());extra_sids=sorted({sid for r in extra_names for sid in r['runtime_sids']})
assert extra_sids==[2352]
for row in extra_names:
 for sid in row['runtime_sids']:assert name_entry(expected,sid).hex()==row['new_bytes']
spell_reviews=json.loads((O/'revue-sorts-v038.json').read_text());spell_sids=sorted({sid for r in spell_reviews for sid in r['runtime_sids']})
assert len(spell_sids)==20
for row in spell_reviews:
 for sid in row['runtime_sids']:assert name_entry(expected,sid).hex()==row['new_bytes']
assert changed_name_ids==sorted([0x9c,0xe7,0xe9,0x30d,0x905,0x906,0x907,0x908,0x909]+place_sids+extra_sids+spell_sids+[0x118,0x11c,0x11d,0x11e]),changed_name_ids
for row in review:
 for sid in row['runtime_sids']:assert name_entry(expected,sid).hex()==row['new_bytes']
previous_names_rom=(P/'v0.55/result.sfc').read_bytes()
assert all(name_entry(expected,sid)==name_entry(previous_names_rom,sid) for sid in range(2512) if sid not in [0x118,0x11c,0x11d,0x11e])
assert name_entry(expected,0x9c)==b''
assert name_entry(expected,0xe7)==bytes.fromhex('195056534f424d')
assert name_entry(expected,0xe9)==bytes.fromhex('1e51554a504f54')
for sid in range(2512):assert name_entry(expected,sid)==name_entry(expected[0x400000:],sid)
report=dict(name_ids_resolved_independently=2512,changed_name_ids_from_ips=changed_name_ids,legacy_credit_entry_empty=True,save_slot_label_journal=True,settings_label_options=True,bps_matches=True,ips_matches=True,wrong_sources_rejected=rejected,header_checksums_match=True,v55_messages_retained=len(old),new_selections=len(new)-len(old),new_reviewed_translations=16,source_structural_entries=0,isolated_existing_revisions=[5698,5699,5700],v55_tokens_unchanged_except_explicit_equipment_revisions=True,unresolved_ds_commands_absent_from_insertions=True,protected_native_controls_preserved=True,result_sha256=hashlib.sha256(expected).hexdigest())
# Exact naming window change in both CPU mappings.
for base in [0,0x400000]:
 assert expected[base+0x58366:base+0x5836a]==bytes.fromhex('01051d0d')
report['hero_naming_window']={'descriptor':147,'x':1,'width':29,'right_edge_unchanged':True}
# With the previous local build available, check all non-script bytes.
baseline=P/'v0.55/result.sfc'
if baseline.exists():
 oldrom=baseline.read_bytes();assert len(oldrom)==len(expected)
 allowed=[]
 for copy in [0,0x400000]:
  allowed += [(copy+0x58366,copy+0x5836a),(copy+0x4b,copy+0x4e),(copy+0x2bfb,copy+0x2bfd),(copy+0x167be,copy+0x1785e)]
  allowed += [(copy+0x165e7,copy+0x167be),(copy+0x3b8703,copy+0x3bc712)]
  allowed += [(copy+0x15bb5,copy+0x15bb5+870*3),(copy+0x37175b,copy+0x3b8703),(copy+0xffdc,copy+0xffe0)]
 allowed.sort();merged=[]
 for a,b in allowed:
  if merged and a<=merged[-1][1]:merged[-1][1]=max(merged[-1][1],b)
  else:merged.append([a,b])
 allowed=merged;start=0
 for a,b in allowed:
  assert expected[start:a]==oldrom[start:a],hex(start)
  start=b
 assert expected[start:]==oldrom[start:]
 report['all_other_bytes_equal_v55_except_script_names_pointers_checksums_and_naming_window']=True
# Every newly scoped native name/number retains its source occurrence count.
bindings=json.loads((O/'liaisons-variables-natives.json').read_text())
checked=[]
for mid,r in new.items():
 if mid in old:continue
 for control in set(bindings.get(str(mid),{}).values()):
  assert r['tokens'].count(control)==jp[mid]['tokens'].count(control),(mid,hex(control))
 checked.append(mid)
# Body occurrences exclude only consolidated native speaker labels.
import re
for mid,r in new.items():
 if mid in old:continue
 if r.get('method') in ['native_plan_reviewed','native_fixed_layout_reviewed','native_source_structure_restored']:
  assert [t for t in r['tokens'] if t<0x200 and t not in [0xad,0xaf,0xac,0xae]]==[t for t in jp[mid]['tokens'] if t<0x200 and t not in [0xad,0xaf,0xac,0xae]],mid
  assert r['tokens'].count(0xaf)>=jp[mid]['tokens'].count(0xaf)
  continue
 body=re.sub(r'\[CODE D4\](?:\[CODE (?:D9|DA|DB|DE)\])*[^「]{0,80}「','',jp[mid]['text'])
 for code in set(range(0xc9,0xd4))|{0xc0,0xc1,0xbb,0xb3,0xb2,0xc5,0xb5,0xc3,0xd8}:
  assert body.count('[CODE '+f'{code:02X}'+']')==r['text'].count(chr(0xe000+code))-(1 if r.get('source_actor')==code else 0),(mid,hex(code),'body occurrence mismatch')
report['all_new_body_name_and_number_counts_preserved']=True
assert len(checked)==16
report['new_scoped_native_occurrences_preserved']=True
report['new_rows_checked']=len(checked)
(O/'qa-patchs-regression.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

import native_helpers
for base in [0,0x400000]:native_helpers.verify_tree(expected,name_source,base)
assert expected[0x4b:0x4e]==source[0x4b:0x4e]
for sid,(_,new_text) in native_helpers.HELPERS.items():assert name_entry(expected,sid)==native_helpers.encode(new_text)

# Explicit original pauses in debug warnings retain their paragraph boundary.
for mid in [6057,6067,6165]:
 assert new[mid]["tokens"].count(0xaf)==jp[mid]["tokens"].count(0xaf)==1
 assert new[mid]["lines"][3].startswith({6057:"Obtenez",6067:"Les testeurs",6165:"Amenez"}[mid])

for mid in [1,2,3,2358,5775,6213,6214]:assert new[mid]['tokens']==jp[mid]['tokens']

assert {i for i in old if old[i]["tokens"]!=new[i]["tokens"]}=={5698,5699,5700}
for mid in [5698,5699,5700]:
 assert [t for t in new[mid]["tokens"] if t<512 and t not in [0xad,0xaf,0xac,0xae]]==[t for t in jp[mid]["tokens"] if t<512 and t not in [0xad,0xaf,0xac,0xae]]
 assert new[mid]["tokens"].count(0xaf)>=jp[mid]["tokens"].count(0xaf)
assert new[6956]["tokens"][-2:]==[0xaf,0xac]
