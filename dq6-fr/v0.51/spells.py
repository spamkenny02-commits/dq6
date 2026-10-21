"""Strict addition of 20 complete DS FR spell/action labels to the byte pool."""
from pathlib import Path
import json,re,struct
def apply_reviewed_spells(entries,groups,changed,root,encode):
 rows=json.loads((Path(__file__).resolve().parent/'revue-sorts-v038.json').read_text())
 assert len(rows)==20 and len({r['sid'] for r in rows})==20
 source=(root.parent/'upload/Dragon Quest VI - Maboroshi no Daichi (Japan).sfc').read_bytes()
 assert len(source)==0x400000
 glyphs=struct.unpack_from('<256H',source,0x11100)
 jtable={int(k,16):v for line in (root/'upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)<=4}
 ja=json.loads((root/'clean-base/ds-ja.json').read_text());fr=json.loads((root/'clean-base/ds-fr.json').read_text())
 for row in rows:
  sid=row['sid'];pos=groups[sid>>4]+(sid&15)
  assert pos==row['position'] and 1088<=pos<=1279 and row['status']=='RELU_POUR_INSERTION'
  assert pos not in changed and entries[pos].hex()==row['old_bytes']
  aliases=[n for n in range(2512) if groups[n>>4]+(n&15)==pos]
  assert aliases==row['runtime_sids']==[sid]
  assert re.fullmatch('[A-Za-z]+',row['french']) and len(row['french'])<=min(9,len(row['current']))
  assert '|' not in row['current']
  value=encode(row['french']);assert 255 not in value and value.hex()==row['new_bytes']
  a=0x3b8703+int.from_bytes(source[0x165e7+3*(sid>>4):0x165ea+3*(sid>>4)],'little')
  for _ in range(sid&15):a=source.index(0xac,a)+1
  jp=''.join(jtable.get(glyphs[b],f'<{glyphs[b]:04X}>') for b in source[a:source.index(0xac,a)])
  assert jp==row['sfc_jp']
  for ds in row['ds_sources']:
   jf=ds['file'].replace('/FR/','/JA/')
   j=next(x for x in ja if x['file']==jf and x['id']==ds['id']);f=next(x for x in fr if x['file']==ds['file'] and x['id']==ds['id'])
   # DS semicolon is an optional split inside a list label, not a SFC command.
   assert re.search(r'@(?:1|4)([^@]+)',j['text']).group(1).replace(';','')==jp
   assert re.search(r'@4([^@]+)',f['text']).group(1)==row['french']
  changed[pos]=value
