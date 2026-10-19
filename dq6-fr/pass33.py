"""Idempotent v0.33: eight reviewed place entries; no main-script changes."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;B=P/'v0.32';O=P/'v0.33'
O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
 if (O/name).exists():continue
 s=(B/name).read_text().replace('v0.32','VERSION_NEW').replace('v0.31','VERSION_BASE').replace('VERSION_NEW','v0.33').replace('VERSION_BASE','v0.32').replace('v032','v033').replace('v31','v32')
 if name=='build.py':
  s=s.replace('len(rows)-5731','len(rows)-5732').replace('other_name_strings_unchanged_except_credit_and_menu_labels=True','other_name_strings_unchanged_except_reviewed_places_credit_and_menu_labels=True,place_entries_changed=8')
 if name=='prepare.py':s=s.replace('correspondance_revue_v32','correspondance_revue_v33')
 if name=='names.py':
  needle=' source_end=START+'
  start=s.index(needle)
  extra=""" # Eight complete official place labels, with unchanged or smaller display width.
 review=json.loads((Path(__file__).resolve().parent/'revue-lieux-v033.json').read_text())
 assert len(review)==8
 for row in review:
  pos=row['position'];assert pos==groups[row['sid']>>4]+(row['sid']&15)
  assert entries[pos].hex()==row['old_bytes']
  assert re.fullmatch('[A-Za-z ]+',row['french'])
  assert len(row['french'])<=len(row['current'])
  value=encode(row['french']);assert value.hex()==row['new_bytes'] and 255 not in value
  changed[pos]=value
  # Independently confirm the original Japanese byte-name and both DS list fields.
  source=(root.parent/'upload/Dragon Quest VI - Maboroshi no Daichi (Japan).sfc').read_bytes()
  jtable={int(k,16):v for line in (root/'upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)<=4}
  glyphs=struct.unpack_from('<256H',source,0x11100);a=START+int.from_bytes(source[TABLE+3*(row['sid']>>4):TABLE+3*(row['sid']>>4)+3],'little')
  for _ in range(row['sid']&15):a=source.index(0xac,a)+1
  jname=''.join(jtable.get(glyphs[b],f'<{glyphs[b]:04X}>') for b in source[a:source.index(0xac,a)])
  assert jname==row['sfc_jp']
  ja=json.loads((root/'clean-base/ds-ja.json').read_text())
  for ds in row['ds_sources']:
   jf=ds['file'].replace('/FR/','/JA/');jrow=next(x for x in ja if x['file']==jf and x['id']==ds['id']);frow=next(x for x in fr if x['file']==ds['file'] and x['id']==ds['id'])
   assert re.search(r'@(?:1|4)([^@]+)',jrow['text']).group(1).replace(';','').strip()==jname
   assert re.search(r'@(?:1|4)([^@]+)',frow['text']).group(1).replace(';','').strip()==row['french']
"""
  s=s[:start]+extra+s[start:]
 if name=='verify.py':
  s=s.replace("assert changed_name_ids==[0x9c,0xe7,0xe9,0x30d,0x905,0x906,0x907,0x908,0x909],changed_name_ids", "review=json.loads((O/'revue-lieux-v033.json').read_text());place_sids=sorted({sid for r in review for sid in r['runtime_sids']})\nassert changed_name_ids==sorted([0x9c,0xe7,0xe9,0x30d,0x905,0x906,0x907,0x908,0x909]+place_sids),changed_name_ids\nfor row in review:\n for sid in row['runtime_sids']:assert name_entry(expected,sid).hex()==row['new_bytes']\nassert all(name_entry(expected,sid)==name_entry((P/'v0.32/result.sfc').read_bytes(),sid) for sid in range(2512) if sid not in place_sids)")
 (O/name).write_text(s)
for p in B.glob('*.json'):
 if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','audit-noms','audit-tables','inventaire-','lieux-prepares','revue-lot','revue-lieux')):continue
 if not (O/p.name).exists():shutil.copy2(p,O/p.name)
print('v0.33 : eight place entries, zero main-script additions')
