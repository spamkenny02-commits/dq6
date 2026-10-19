"""Restore readable translation deltas, preserving modified local files."""
from pathlib import Path
import hashlib,json,runpy

def restore_lots(root,dest):
    def write_missing(path,data):
        if path.exists():
            if path.read_bytes()!=data:print('Preserved existing modified file:',path)
        else:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    for path in sorted((root/'sources/lots').glob('v*.json')):
        spec=json.loads(path.read_text());assert spec['kind']=='readable_translation_delta'
        for row in spec['files']:
            p=Path(row['path']);assert not p.is_absolute() and '..' not in p.parts
            assert p.suffix in {'.py','.json','.md','.bps','.png'}
            b=(root/p).read_bytes();assert hashlib.sha256(b).hexdigest()==row['sha256']
            write_missing(dest/p,b)
        # The explicit review delta copies inherited JSON and adds only reviewed rows.
        recipe=dest/spec['recipe'];assert recipe.suffix=='.py'
        runpy.run_path(str(recipe),run_name='__main__')
        O=dest/'dq6-fr'/spec['version'];B=dest/'dq6-fr'/spec['baseline']
        old=json.loads((B/'insertion-candidates.json').read_text());new=json.loads((O/'nouveaux-messages.json').read_text())
        assert len(old)==spec['baseline_count'] and len(new)==spec['new_count']
        oldids={r['id'] for r in old};assert not oldids&{r['id'] for r in new}
        rows=sorted(old+new,key=lambda r:r['id'])
        data=json.dumps(rows,ensure_ascii=False,indent=2).encode()
        assert hashlib.sha256(data).hexdigest()==spec['merged_selection_sha256']
        for name in ['insertion-candidates.json','insertion-candidates-all.json']:write_missing(O/name,data)
        for name,digest in spec['generated_inputs'].items():
            assert hashlib.sha256((O/name).read_bytes()).hexdigest()==digest,'Input differs: '+name
        print('Verified readable delta',spec['version'],':',len(new),'new messages,',len(rows),'integrated selections. No ROM included.')

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path);a=parser.parse_args()
    root=Path(__file__).resolve().parent;restore_lots(root,(a.output or root).resolve())
