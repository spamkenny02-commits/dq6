"""Prove specific native caller bindings; byte matches do not prove exhaustive reachability."""
from pathlib import Path
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--jp',required=True,type=Path);p.add_argument('--rom',required=True,type=Path);a=p.parse_args();jp=a.jp.read_bytes();rom=a.rom.read_bytes();folder=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(jp)=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e'
assert sha(rom)==json.loads((folder/'build-report.json').read_text())['ROM_sha256']
# Both native inline and accumulator forms converge on the same large-window setup.
api={0x2a16:'08c23048da5a8b78f47e7eabab20c52a4c622a',0x2a29:'08c23048da5a8b78f47e7eabab8d98594c622a',0x2a3c:'08c23048da5a8b78f47e7eabab20c52a4c922a',0x2a4f:'08c23048da5a8b78f47e7eabab8d98594c922a'}
checks=[]
def check(at,raw,role):
 raw=bytes.fromhex(raw) if isinstance(raw,str) else raw
 assert jp[at:at+len(raw)]==raw,(hex(at),'JP')
 for mirror in [0,0x400000]:assert rom[mirror+at:mirror+at+len(raw)]==raw,(hex(at),mirror)
 checks.append(dict(cpu_address=f'C{at:05X}',file_offset=at,bytes_hex=raw.hex(),role=role,JP_and_both_ROM_copies_identical=True))
for at,raw in api.items():check(at,raw,'Native API prologue: large setup2A62 or compact setup2A92')
inline={70:0x2b130,71:0x2b186,366:0x27262,433:0x5f481,434:0x5f489,435:0x5f452}
for mid,at in inline.items():check(at,bytes.fromhex('22162ac0')+mid.to_bytes(2,'little'),f'Inline message {mid} calls C02A16 (large)')
# Treasure-result path stores73, optionally replaces it with72, then calls the accumulator API.
check(0x2b18c,'a949008d9325ad2a5a221dedc38d285ab012c9c809f006a948008d9325ad932522292ac060','Messages73/72 selected into2593 and loaded immediately before C02A29')
q=dict(release='v0.78',ROM_sha256=sha(rom),source_JP_sha256=sha(jp),checks=checks,large_window_caller_found_ids=sorted(list(inline)+[72,73]),remaining_caller_binding_ids=[331,367],all_callers_exhaustively_identified=False,natural_scenes_played=False,compact_negative_diagnostic_retained=True,interpretation='Eight affected IDs have proven native large-window call sites. The forced compact diagnostic is not evidence of failure at those particular call sites. Other callers and dynamic paths are not exhaustively proven;331/367 remain unresolved. No ROM change, no new translation or completed reread.')
(folder/'audit-native-callers.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');print(json.dumps(q))
