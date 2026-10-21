"""Check the native message 465 word binding against intact JP and v0.56."""
from pathlib import Path
import argparse, hashlib, importlib.util, json
r=Path(__file__).resolve().parents[2]
s=importlib.util.spec_from_file_location('codec58',r/'tools/combat-v058/codec.py')
c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
a=argparse.ArgumentParser();a.add_argument('--jp',type=Path,required=True);a=a.parse_args()
jp=a.jp.read_bytes();baseline=c.baseline_from_jp(jp,r)
d=json.loads((Path(__file__).parent/'binding-465.json').read_text())
for label,rom in [('JP',jp),('v0.56',baseline)]:
 assert hashlib.sha256(rom[0x26796:0x267ad]).hexdigest()==d['caller_sha256'],label
 assert hashlib.sha256(rom[0x267ad:0x267b5]).hexdigest()==d['table_sha256'],label
 assert [int.from_bytes(rom[0x267ad+2*i:0x267af+2*i],'little') for i in range(4)]==[int(w['sid'],16) for w in d['words']],label
 assert rom[0x267a6:0x267ac]==bytes.fromhex('22162ac0d101'),label
print('Binding 465: caller and four SIDs unchanged in intact JP and v0.56; rendering untested')
