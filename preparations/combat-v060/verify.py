"""Validate the reviewed Celeste preparation against restored DS and native source."""
from pathlib import Path
import argparse,json,hashlib,importlib.util,tempfile
r=Path(__file__).resolve().parents[2];o=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('c',r/'tools/combat-v058/codec.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
a=argparse.ArgumentParser();a.add_argument('--jp',type=Path,required=True);a=a.parse_args()
d=json.loads((o/'nom-celeste.json').read_text());assert d['status']=='PREPARE_NON_INSERE' and not d['inserted'] and d['french']=='Céleste'
ja={(x['file'],x['id']):x for x in json.loads((r/'dq6-fr/clean-base/ds-ja.json').read_text())};fr={(x['file'],x['id']):x for x in json.loads((r/'dq6-fr/clean-base/ds-fr.json').read_text())}
for ref in d['ds_references']:
 for lang,lookup in [('ja',ja),('fr',fr)]:
  text=lookup[(ref[lang+'_file'],ref['id'])]['text'];assert hashlib.sha256(text.encode()).hexdigest()==ref[lang+'_text_sha256'];assert text==ref[lang+'_excerpt']
rom=c.baseline_from_jp(a.jp.read_bytes(),r)
s=importlib.util.spec_from_file_location('n',r/'dq6-fr/upstream/refill/tools/nametable.py');n=importlib.util.module_from_spec(s);s.loader.exec_module(n)
with tempfile.NamedTemporaryFile(dir=r,suffix='.sfc') as f:
 f.write(rom);f.flush();t=n.Table(f.name);sid=int(d['sid'],16);pos=t.position(sid)
 assert pos==d['physical_entry_v056'] and t.text(sid)=='M369'
 assert [f'{i:04X}' for i in range(2512) if t.position(i)==pos]==d['runtime_alias_sids_v056']
print('DS source hashes and Celeste SID/physical-alias checks passed; no insertion or render approval')
