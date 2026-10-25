#!/usr/bin/env python3
"""Create deterministic SHA256 release evidence manifest; signing performed by trusted CI identity."""
import hashlib,json,subprocess,sys
from pathlib import Path

def build(root):
    root=Path(root);entries=[]
    for f in sorted(root.rglob('*')):
        if not f.is_file() or '.git' in f.parts or '.build' in f.parts or '__pycache__' in f.parts or f.name in ('release-manifest.json','SHA256SUMS.txt'):continue
        entries.append({'path':f.relative_to(root).as_posix(),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'size':f.stat().st_size})
    return {'schema':'oc2.release-manifest.v1','files':entries,'file_count':len(entries)}
if __name__=='__main__':
    root=Path(sys.argv[1] if len(sys.argv)>1 else '.');(root/'release-manifest.json').write_text(json.dumps(build(root),sort_keys=True,indent=2)+'\n')
