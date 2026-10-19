"""Restore the verified v0.19 sources and IPS files from this checkout."""
from pathlib import Path
import argparse, hashlib, io, json, tarfile, lzma, gzip

def checked_parts(root, manifest):
    chunks=[]
    for row in manifest['parts']:
        b=(root/row['path']).read_bytes()
        assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'], row['path']
        chunks.append(b)
    data=b''.join(chunks)
    assert len(data)==manifest['archive_bytes']
    assert hashlib.sha256(data).hexdigest()==manifest['archive_sha256']
    return data

def write_missing(path, data):
    if path.exists():
        if path.read_bytes()!=data:
            print('Preserved existing modified file:', path)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    dest=(args.output or root).resolve()
    manifest=json.loads((root/'sources/manifest.json').read_text())
    data=checked_parts(root, manifest)
    count=0
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:xz') as archive:
        for member in archive.getmembers():
            p=Path(member.name)
            assert member.isfile() and not p.is_absolute() and '..' not in p.parts
            assert p.suffix in {'.py','.json','.cpp','.tbl','.md'}
            write_missing(dest/p, archive.extractfile(member).read())
            count+=1
    assert count==manifest['files']
    ips_manifest=json.loads((root/'patches/ips-manifest.json').read_text())
    ips=lzma.decompress(checked_parts(root, ips_manifest))
    assert hashlib.sha256(ips).hexdigest()==ips_manifest['ips_sha256']
    write_missing(dest/'patches/DQVI-FR-DS-v0.19-BASE-JP-PARTIEL.ips', ips)
    old=gzip.decompress((root/'patches/Dq6f.ips.gz').read_bytes())
    assert hashlib.sha256(old).hexdigest()=='b34155f476d0bce3d2247c577417b3ade3ee071e7c9b8af634f8a7cb613cdd37'
    write_missing(dest/'upload/Dq6f.ips', old)
    print(f'Verified and restored {count} source files and both IPS files. No ROM included.')

if __name__=='__main__':
    main()
