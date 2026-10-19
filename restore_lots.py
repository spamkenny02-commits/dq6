"""Restore readable translation deltas, preserving modified local files."""
from pathlib import Path
import hashlib,json,runpy

def merge_reviewed_revisions(old, revisions):
    """Apply explicitly reviewed corrections only to the exact recorded baseline."""
    byid={r['id']:r for r in old}
    assert len(byid)==len(old),'Duplicate baseline ID'
    seen=set()
    for revision in revisions:
        mid=revision['id']
        assert mid in byid and mid not in seen,'Unknown or duplicate revision ID'
        previous=byid[mid]
        digest=hashlib.sha256(json.dumps(previous['tokens'],separators=(',',':')).encode()).hexdigest()
        assert digest==revision['old_tokens_sha256'],'Revision baseline tokens differ'
        assert previous['text']==revision['old_text'],'Revision baseline text differs'
        replacement=revision['new_selection']
        assert replacement['id']==mid,'Replacement ID differs'
        assert revision['reason'].strip(),'Missing review reason'
        byid[mid]=replacement;seen.add(mid)
    return [byid[r['id']] for r in old]

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
        revision_path=spec.get('replacements_file')
        if revision_path:
            rp=Path(revision_path)
            assert not rp.is_absolute() and '..' not in rp.parts
            assert revision_path in {r['path'] for r in spec['files']},'Unmanifested revisions'
            old=merge_reviewed_revisions(old,json.loads((dest/rp).read_text()))
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
