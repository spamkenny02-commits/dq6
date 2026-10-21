"""Explicit6956 boundary repair; not a silent source-extractor alteration."""
from pathlib import Path
import json
def bounded(s):
 if s['id']!=6956:return s
 proof=json.loads((Path(__file__).resolve().parent.parent/'v0.55/qa-frontiere-6956.json').read_text())
 assert s['text']==proof['source_text'] and proof['script_end_exclusive']==0x3b8703
 assert len(s['tokens'])>44 and s['tokens'][43]==0xaf
 assert [x['token'] for x in proof['trace']]==s['tokens']
 assert proof['trace'][43]['end']==[0x3b8702,7]
 return dict(s,tokens=s['tokens'][:44]+[0xac])
