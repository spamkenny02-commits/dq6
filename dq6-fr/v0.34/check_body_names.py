"""Compare native name occurrences in every new message, excluding speaker labels."""
from pathlib import Path
import json,re,collections
O=Path(__file__).resolve().parent;P=O.parent
source=json.loads((P/'clean-base/sfc-jp.json').read_text())
rows=json.loads((O/'nouveaux-messages.json').read_text())
codes=set(range(0xc9,0xd4))|{0xc0,0xc1,0xb2,0xc5,0xbb,0xb3};report=[]
for row in rows:
 jp=re.sub(r'\[CODE D4\][^「]*「','',source[row['id']]['text'])
 expected=[int(x,16) for x in re.findall(r'\[CODE ([0-9A-F]+)\]',jp) if int(x,16) in codes]
 text=row['text'];actor=row.get('source_actor')
 if actor is not None:
  prefix=chr(0xe000+actor)+'. ';assert text.startswith(prefix)
  text=text[len(prefix):]
 actual=[ord(ch)-0xe000 for ch in text if ord(ch)-0xe000 in codes]
 assert collections.Counter(expected)==collections.Counter(actual),(row['id'],expected,actual)
 report.append(dict(id=row['id'],source_body_names=expected,inserted_body_names=actual))
assert len(report)==121
(O/'qa-noms-dans-corps.json').write_text(json.dumps(dict(messages_checked=len(report),speaker_labels_excluded=True,all_occurrence_counts_preserved=True,rows=report),ensure_ascii=False,indent=2))
print('All 121 body-name occurrence checks passed')
