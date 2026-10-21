"""PRIVATE diagnostic only: route camp host to native battle byte renderer.
REJECTED rendering experiment: no readable native dialogue capture obtained.
Never a release ROM or natural battle test. Output ROM/state must stay local.
"""
from pathlib import Path
import argparse,json,sys,struct,hashlib
from codec import BattleCodec,BASELINE_SHA,main_regions,baseline_from_jp
R=Path(__file__).resolve().parents[2]
ap=argparse.ArgumentParser();ap.add_argument('--jp',type=Path,required=True);ap.add_argument('--id',type=int,default=51);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
rom=bytearray(baseline_from_jp(a.jp.read_bytes(),R));c=BattleCodec(rom,json.loads((R/'dq6-fr/v0.56/charset.json').read_text()));rows={x['id']:x for x in json.loads((R/'preparations/combat-v057/prepares-non-inseres.json').read_text())};blob=c.encode(rows[a.id]['french_plan']);placements=main_regions(rom)
off=next(off for off in range(0x771800,0x7b8703-len(blob),256) if off>>16==(off+len(blob)-1)>>16 and all(not(p['file_offset']<off+len(blob) and p['file_offset']+p['size']>off) for p in placements));rom[off:off+len(blob)]=blob
# Main renderer entry is redirected to an independent native byte renderer.
# Stack/DB setup mirrors the entry being replaced; native renderer opens its own
# three-row window and processes AB..C8 itself. No Huffman glyph substitution.
main=bytes.fromhex('c230f47e7eabab')+b'\xa9'+a.id.to_bytes(2,'little')+bytes.fromhex('8d9859227126c06b')
loader=bytes.fromhex('08c230a9')+(off&65535).to_bytes(2,'little')+bytes.fromhex('85a0a9')+(off>>16).to_bytes(2,'little')+bytes.fromhex('85a264a4286b')
assert len(blob)<=256
code_at=off+256
assert code_at+len(main)+len(loader)<=0x7b8703
assert code_at>>16==(code_at+len(main)+len(loader)-1)>>16
assert all(not(p['file_offset']<code_at+len(main)+len(loader) and p['file_offset']+p['size']>code_at) for p in placements)
rom[code_at:code_at+len(main)+len(loader)]=main+loader
for copy in [0,0x400000]:
 assert rom[copy+0x2ae2:copy+0x2ae6]==bytes.fromhex('c230f47e')
 assert rom[copy+0x27b0:copy+0x27b5]==bytes.fromhex('08c230f47e')
 rom[copy+0x2ae2:copy+0x2ae6]=b'\x5c'+code_at.to_bytes(3,'little')
 rom[copy+0x27b0:copy+0x27b4]=b'\x5c'+(code_at+len(main)).to_bytes(3,'little')
checksum=sum(rom)&65535
for copy in [0,0x400000]:struct.pack_into('<HH',rom,copy+0xffdc,checksum^65535,checksum)
a.out.write_bytes(rom)
print(json.dumps(dict(id=a.id,diagnostic_only=True,native_reader='C027FF',native_renderer='C02831',native_loop='C02671',payload_cpu_address=off,payload_size=len(blob),fixture_sha256=hashlib.sha256(rom).hexdigest(),natural_battle=False)))
