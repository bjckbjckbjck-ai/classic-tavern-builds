"""Read the unified game from an exact Git commit, never from dirty working files."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTERS = ('service_client.gd', 'service_server.gd', 'service_updater.gd')


class GameSource:
    def __init__(self, directory, ref):
        self.directory = Path(directory).resolve()
        self.commit = self.git('rev-parse', '--verify', ref + '^{commit}').decode().strip()

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.directory), *args])

    def read(self, path):
        return self.git('show', self.commit + ':' + path)

    def files(self):
        return self.git('ls-tree', '-r', '--name-only', self.commit).decode('utf-8').splitlines()

    def server_files(self):
        available = set(self.files())
        found = set()
        todo = ['scripts/service_server.gd']
        while todo:
            path = todo.pop()
            if path in found:
                continue
            found.add(path)
            if path.endswith('.gd'):
                todo.extend(p for p in re.findall(r'res://([^"\n]+)', self.read(path).decode('utf-8'))
                            if '%' not in p and p in available)
        found.update(p for p in available if p.startswith('data/') and p.endswith('.json')
                     and p.count('/') == 1 and p != 'data/remote.json')
        return sorted(found)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game-dir', required=True, type=Path)
    parser.add_argument('--ref', help='New reviewed source revision; requires --update')
    parser.add_argument('--update', action='store_true', help='Update source pin and generated adapter snapshots, not live release metadata')
    args = parser.parse_args()
    manifest = ROOT / 'config/game-source.json'
    previous = json.loads(manifest.read_text()) if manifest.exists() else {}
    if args.ref and not args.update:
        parser.error('--ref requires --update')
    ref = args.ref or previous.get('commit')
    if not ref:
        parser.error('No pinned commit; use --ref with --update')
    source = GameSource(args.game_dir, ref)
    snapshots = {name: source.read('scripts/' + name) for name in ADAPTERS}
    digest = hashlib.sha256()
    for name in source.server_files():
        digest.update(name.encode() + b'\0' + source.read(name) + b'\0')
    value = {'repository': 'https://github.com/bjckbjckbjck-ai/classic-tavern-game.git',
             'branch': 'main', 'commit': source.commit, 'server_content_sha256': digest.hexdigest(),
             'adapter_sha256': {name: hashlib.sha256(body).hexdigest() for name, body in snapshots.items()}}
    if args.update:
        for name, body in snapshots.items():
            (ROOT / 'game_adapter' / name).write_bytes(body)
        manifest.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
        print('Updated candidate source pin and generated snapshots:', source.commit)
    else:
        if value != previous:
            raise SystemExit('Source pin/hash mismatch')
        for name, body in snapshots.items():
            if (ROOT / 'game_adapter' / name).read_bytes() != body:
                raise SystemExit('Generated adapter drift: ' + name)
        print('Pinned source and adapter snapshots verified:', source.commit)


if __name__ == '__main__':
    main()
