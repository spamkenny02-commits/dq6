"""Rebuild verified source extractions and the provided VF base, without editing uploads."""
from pathlib import Path
import hashlib,runpy,subprocess,sys
P=Path(__file__).resolve().parents[1];U=P.parent/'upload'
jp=U/'Dragon Quest VI - Maboroshi no Daichi (Japan).sfc';ds=U/'Dragon Quest VI - Realms of Reverie (E).nds'
assert hashlib.sha256(jp.read_bytes()).hexdigest()=='90ba1868f0e75734a19f873401fab515cb945c62cd0ad173f89cf352ab86f29e','Wrong Japanese source'
assert hashlib.sha256(ds.read_bytes()).hexdigest()=='5667303e3c7ab518a1b6bb2119abdfcc17422b3387dc5083f67b8e2b54734fb5','Different DS source'
subprocess.run([sys.executable,str(P/'extract.py'),'--ds',str(ds),'--sfc',str(jp),'--out',str(P/'clean-base')],check=True)
patch=(U/'Dq6f.ips').read_bytes();assert hashlib.sha256(patch).hexdigest()=='b34155f476d0bce3d2247c577417b3ade3ee071e7c9b8af634f8a7cb613cdd37','Different VF IPS'
rom=bytearray(512)+bytearray(jp.read_bytes());i=5;assert patch[:5]==b'PATCH'
while patch[i:i+3]!=b'EOF':
 off=int.from_bytes(patch[i:i+3],'big');n=int.from_bytes(patch[i+3:i+5],'big');i+=5
 if n:data=patch[i:i+n];i+=n
 else:n=int.from_bytes(patch[i:i+2],'big');data=patch[i+2:i+3]*n;i+=3
 assert len(data)==n and off+n<=len(rom);rom[off:off+n]=data
assert i+3==len(patch)
(P/'clean-base/vf-base-headered.sfc').write_bytes(rom)
runpy.run_path(str(P/'clean-base/decode_vf.py'),run_name='__main__')
