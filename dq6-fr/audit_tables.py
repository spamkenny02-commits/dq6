"""Audit the separate name pool by runtime SID, against the supplied DS JA/FR.
No translation is inserted and no ROM is edited by this script.
"""
from pathlib import Path
import json,struct,re,unicodedata,collections,argparse,importlib.util
P=Path(__file__).resolve().parent;ap=argparse.ArgumentParser();ap.add_argument('version');args=ap.parse_args();O=P/args.version
jp=(P.parent/'upload/Dragon Quest VI - Maboroshi no Daichi (Japan).sfc').read_bytes();rom=(O/'result.sfc').read_bytes() if (O/'result.sfc').exists() else (P/'v0.12/result.sfc').read_bytes()
table={int(k,16):v for l in (P/'upstream/dq6-sfc/dq6 jp.tbl').read_text().splitlines() if '=' in l for k,v in [l.split('=',1)] if len(k)<=4};glyphs=struct.unpack_from('<256H',jp,0x11100)
def entry(data,sid):
 a=0x3b8703+int.from_bytes(data[0x165e7+3*(sid>>4):0x165ea+3*(sid>>4)],'little')
 for _ in range(sid&15):a=data.index(0xac,a)+1
 end=data.index(0xac,a);return a,data[a:end]
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKC',s.replace(';','')) if unicodedata.category(c)[0] in 'LN')
def field(s):
 m=re.search(r'@(?:1|4)([^@]+)',s)
 return m.group(1).replace(';','').strip() if m else None
fr=json.loads((P/'clean-base/ds-fr.json').read_text());ja=json.loads((P/'clean-base/ds-ja.json').read_text());fi={(r['file'].replace('/FR/','/JA/'),r['id']):r for r in fr};lookup=collections.defaultdict(list)
for r in ja:
 if '/MENULIST6/JA/' not in r['file'] or r['file'].endswith('b1090000.mpt'):continue
 f=fi.get((r['file'],r['id']));j=field(r['text']);v=field(f['text']) if f else None
 if j and v:lookup[norm(j)].append(dict(file=f['file'],id=f['id'],jp=j,fr=v))
spec=importlib.util.spec_from_file_location('nt',P/'upstream/refill/tools/nametable.py');nt=importlib.util.module_from_spec(spec);spec.loader.exec_module(nt);current=nt.Table(O/'result.sfc' if (O/'result.sfc').exists() else P/'v0.12/result.sfc')
rows=[]
for sid in range(2512):
 a,raw=entry(jp,sid);text=''.join(table.get(glyphs[b],f'<{glyphs[b]:04X}>') for b in raw);matches=lookup.get(norm(text),[]) if norm(text) else []
 rows.append(dict(sid=sid,jp_offset=a,jp=text,current_position=current.position(sid),current_text=current.text(sid),ds_candidates=matches,unique_french=len({m['fr'] for m in matches})==1))
(O/'audit-noms-menus.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));positions={r['current_position'] for r in rows};matched={r['current_position'] for r in rows if r['unique_french']};summary=dict(sids=2512,reachable_positions=len(positions),positions_with_unique_exact_ds_french=len(matched),not_inserted=True,warning='Les homonymes, alias et limites de fenêtres doivent être examinés avant insertion ; les noms DS sont complets et non tronqués.')
(O/'audit-tables-bilan.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False))
