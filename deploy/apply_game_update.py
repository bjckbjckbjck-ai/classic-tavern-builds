"""Switch a staged pinned game and API after drain; preserve DB and a rollback tree.

Run with sudo. Stage is an extracted deploy/bundle.py archive. Client manifests
are published separately only after this health-checked switch succeeds.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import time
import urllib.request


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', required=True, type=Path)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--protocol', required=True)
    parser.add_argument('--game-version', required=True)
    args = parser.parse_args()
    base = Path('/opt/classic-tavern')
    data = Path('/var/lib/classic-tavern')
    stage = args.stage.resolve()
    pin = json.loads((stage/'game-source.json').read_text())
    if pin['commit'] != args.commit:
        raise SystemExit('Staged game commit mismatch')
    digest = hashlib.sha256()
    files = sorted(p for p in (stage/'game').rglob('*') if p.is_file()
                   and '.godot' not in p.parts and p != stage/'game/project.godot')
    for path in files:
        relative = path.relative_to(stage/'game').as_posix()
        digest.update(relative.encode()+b'\0'+path.read_bytes()+b'\0')
    if digest.hexdigest() != pin['server_content_sha256']:
        raise SystemExit('Staged game content hash mismatch')

    def idle():
        if not (data/'maintenance').exists():raise RuntimeError('Drain first')
        with sqlite3.connect('file:'+str(data/'accounts.sqlite3')+'?mode=ro', uri=True) as conn:
            active = conn.execute("SELECT count(*) FROM rooms WHERE phase NOT IN ('finished','aborted')").fetchone()[0]
            queued = conn.execute('SELECT count(*) FROM queue').fetchone()[0]
        if active or queued:raise RuntimeError('Players active or queued; update deferred')

    def systemctl(action):
        subprocess.run(['systemctl', action, 'classic-tavern'], check=True)

    idle()
    subprocess.run(['systemctl', 'start', 'classic-tavern-backup.service'], check=True)
    rollback = base/('rollback-game-'+str(time.time_ns()))
    rollback.mkdir(mode=0o700)
    replacements = ['app.py', 'game-source.json', 'deploy/backup.py']
    existed = {}
    for relative in replacements:
        source = stage/relative
        if not source.is_file():raise RuntimeError('Missing staged file: '+relative)
        target = base/relative
        existed[relative] = target.exists()
        if target.exists():
            (rollback/relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, rollback/relative)
    next_game = rollback/'next-game'
    shutil.copytree(stage/'game', next_game, ignore=shutil.ignore_patterns('.godot'))
    (rollback/'rollback-info.json').write_text(json.dumps({'replacements': existed, 'new_commit': args.commit}))
    idle()
    systemctl('stop')
    moved_old = moved_new = False
    try:
        os.replace(base/'game', rollback/'game'); moved_old = True
        os.replace(next_game, base/'game'); moved_new = True
        for relative in replacements:
            shutil.copyfile(stage/relative, base/relative)
            (base/relative).chmod(0o644)
        systemctl('start')
        for _ in range(30):
            try:
                with urllib.request.urlopen('http://127.0.0.1:18080/api/health', timeout=2) as response:
                    health = json.load(response)
                if health.get('protocol') == args.protocol and health.get('game') == args.game_version:
                    break
            except OSError:pass
            time.sleep(.5)
        else:raise RuntimeError('Updated API did not pass health check')
    except Exception:
        systemctl('stop')
        if moved_new:os.replace(base/'game', rollback/'failed-game')
        if moved_old:os.replace(rollback/'game', base/'game')
        for relative in replacements:
            if existed[relative]:shutil.copy2(rollback/relative, base/relative)
            else:(base/relative).unlink(missing_ok=True)
        systemctl('start')
        print('ROLLED_BACK; maintenance remains enabled for operator review')
        raise
    print(json.dumps({'deployed': args.commit, 'health': health, 'server_files': len(files),
                      'rollback': str(rollback), 'maintenance': True}))


if __name__ == '__main__':
    main()
