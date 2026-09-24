"""Create a whitelisted bundle; never archive secrets or the whole workspace."""
import json,re,tarfile,sys,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
game=Path(sys.argv[1]).resolve()
binary=Path(sys.argv[2]).resolve()
out=root/'artifacts';out.mkdir(exist_ok=True)
files=set();todo=['scripts/service_server.gd']
while todo:
    rel=todo.pop()
    if rel in files:continue
    p=game/rel
    if not p.is_file():raise RuntimeError(rel)
    files.add(rel)
    if p.suffix=='.gd':
        todo += [x for x in re.findall(r'res://([^"\n]+)',p.read_text(encoding='utf-8')) if '%' not in x and (game/x).is_file()]
# Catalog loads JSON files through constructed paths as well.
files.update(str(p.relative_to(game)).replace('\\','/') for p in (game/'data').glob('*.json') if p.name!='remote.json')
project=out/'project.godot'
project.write_text('config_version=5\n[application]\nconfig/name="Classic Tavern Server"\n[rendering]\nrenderer/rendering_method="gl_compatibility"\n',encoding='utf-8')
with tarfile.open(out/'service.tar.gz','w:gz') as tar:
    for name in ['app.py','requirements.txt','requirements.lock']:
        tar.add(root/name,arcname=name)
    for p in (root/'deploy').glob('*'):
        if p.is_file():tar.add(p,arcname='deploy/'+p.name)
    for rel in sorted(files):tar.add(game/rel,arcname='game/'+rel)
    tar.add(project,arcname='game/project.godot')
    tar.add(binary,arcname='godot')
print(json.dumps({'files':len(files),'bytes':(out/'service.tar.gz').stat().st_size,'sha256':hashlib.sha256((out/'service.tar.gz').read_bytes()).hexdigest()}))
