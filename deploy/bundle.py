"""Create a whitelisted bundle; never archive secrets or the whole workspace."""
import json,tarfile,sys,hashlib,io
from game_source import GameSource
from pathlib import Path
root=Path(__file__).resolve().parents[1]
game=Path(sys.argv[1]).resolve()
binary=Path(sys.argv[2]).resolve()
out=root/'artifacts';out.mkdir(exist_ok=True)
pin=json.loads((root/'config/game-source.json').read_text())
source=GameSource(game,pin['commit'])
files=source.server_files()
digest=hashlib.sha256()
for rel in files:digest.update(rel.encode()+b'\0'+source.read(rel)+b'\0')
if digest.hexdigest()!=pin['server_content_sha256']:raise RuntimeError('Pinned game source hash mismatch')
project=out/'project.godot'
project.write_text('config_version=5\n[application]\nconfig/name="Classic Tavern Server"\n[rendering]\nrenderer/rendering_method="gl_compatibility"\n',encoding='utf-8')
with tarfile.open(out/'service.tar.gz','w:gz') as tar:
    for name in ['app.py','requirements.txt','requirements.lock']:
        tar.add(root/name,arcname=name)
    for p in (root/'deploy').glob('*'):
        if p.is_file():tar.add(p,arcname='deploy/'+p.name)
    for rel in files:
        body=source.read(rel);entry=tarfile.TarInfo('game/'+rel);entry.size=len(body);entry.mode=0o644
        tar.addfile(entry,io.BytesIO(body))
    tar.add(root/'config/game-source.json',arcname='game-source.json')
    tar.add(project,arcname='game/project.godot')
    tar.add(binary,arcname='godot')
print(json.dumps({'files':len(files),'bytes':(out/'service.tar.gz').stat().st_size,'sha256':hashlib.sha256((out/'service.tar.gz').read_bytes()).hexdigest()}))
