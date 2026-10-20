"""Restore one reviewed separate name, with all v0.34 script selections retained."""
from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent;B=P/'v0.34';O=P/'v0.35';O.mkdir(exist_ok=True)
for name in ['init.py','prepare.py','build.py','verify.py','names.py']:
 if (O/name).exists():continue
 s=(B/name).read_text()
 if name!='names.py':s=s.replace('v0.34','VERSION_NEW').replace('v0.33','VERSION_BASE').replace('VERSION_NEW','v0.35').replace('VERSION_BASE','v0.34').replace('v33','v34')
 if name=='prepare.py':s=s.replace('v034','v035').replace('correspondance_revue_v34','correspondance_revue_v35')
 if name=='build.py':s=s.replace('len(rows)-5732','len(rows)-5853').replace('other_name_strings_unchanged_except_reviewed_places_credit_and_menu_labels=True','other_name_strings_unchanged_except_reviewed_names_places_credit_and_menu_labels=True,additional_character_names_changed=1')
 if name=='names.py':
  extra=""" # Official French default name of the recruited slime; no width increase.
 review_names=json.loads((Path(__file__).resolve().parent/'revue-noms-v035.json').read_text())
 assert len(review_names)==1
 for row in review_names:
  assert row['sid']==2352 and row['position']==1888
  pos=groups[row['sid']>>4]+(row['sid']&15);assert pos==row['position']
  assert entries[pos].hex()==row['old_bytes']
  assert re.fullmatch('[A-Za-z ]+',row['french']) and len(row['french'])<=len(row['current'])
  value=encode(row['french']);assert value.hex()==row['new_bytes'] and 255 not in value
  source=(root.parent/'upload/Dragon Quest VI - Maboroshi no Daichi (Japan).sfc').read_bytes()
  glyphs=struct.unpack_from('<256H',source,0x11100)
  jtable={int(k,16):v for line in (root/'upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)<=4}
  a=START+int.from_bytes(source[TABLE+3*(row['sid']>>4):TABLE+3*(row['sid']>>4)+3],'little')
  for _ in range(row['sid']&15):a=source.index(0xac,a)+1
  assert ''.join(jtable.get(glyphs[b],f'<{glyphs[b]:04X}>') for b in source[a:source.index(0xac,a)])==row['sfc_jp']
  ja=json.loads((root/'clean-base/ds-ja.json').read_text())
  for ds in row['ds_sources']:
   jf=ds['file'].replace('/FR/','/JA/');jrow=next(x for x in ja if x['file']==jf and x['id']==ds['id']);frow=next(x for x in fr if x['file']==ds['file'] and x['id']==ds['id'])
   assert re.search(r'@(?:1|4)([^@]+)',jrow['text']).group(1).replace(';','').strip()==row['sfc_jp']
   assert re.search(r'@(?:1|4)([^@]+)',frow['text']).group(1).replace(';','').strip()==row['french']
  changed[pos]=value
"""
  s=s.replace(' source_end=START+',extra+' source_end=START+',1)
 if name=='verify.py':
  s=s.replace("assert changed_name_ids==sorted([0x9c", "extra_names=json.loads((O/'revue-noms-v035.json').read_text());extra_sids=sorted({sid for r in extra_names for sid in r['runtime_sids']})\nassert extra_sids==[2352]\nfor row in extra_names:\n for sid in row['runtime_sids']:assert name_entry(expected,sid).hex()==row['new_bytes']\nassert changed_name_ids==sorted([0x9c")
  s=s.replace('+place_sids),changed_name_ids','+place_sids+extra_sids),changed_name_ids')
  s=s.replace('for sid in range(2512))','for sid in range(2512) if sid not in extra_sids)')
 (O/name).write_text(s)
for p in B.glob('*.json'):
 if p.name.startswith(('qa-','validation','verification','etat-projet','nouveaux-messages','couverture-','insertion-','placements','a-revoir','audit-noms','audit-tables','inventaire-','lieux-prepares')):continue
 if not (O/p.name).exists():shutil.copy2(p,O/p.name)
r=json.loads((O/'revue-lot-v035.json').read_text());assert r==[]
assert len(json.loads((B/'insertion-candidates.json').read_text()))==5853
print('v0.35 inputs ready: one separate name, zero main-script additions')
