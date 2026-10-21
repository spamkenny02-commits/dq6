"""Emit address/length metadata only for checking the unchanged v0.56 in Snes9x."""
from pathlib import Path
import argparse,json
from codec import baseline_from_jp,pool
R=Path(__file__).resolve().parents[2]
a=argparse.ArgumentParser();a.add_argument('--jp',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a=a.parse_args()
rom=baseline_from_jp(a.jp.read_bytes(),R)
a.out.write_text(json.dumps([dict(group=i,file_offset=off,cpu_address=off|0xc00000,size=len(data)) for i,off,data in pool(rom)],indent=2)+'\n')
print('608 message ranges,76 pointer groups; metadata only')
