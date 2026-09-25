"""Publish immutable clients first, then atomically switch the update manifest.

No backend restart or account-data write. Run after exporting both clients.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--game-dir', type=Path, required=True)
    p.add_argument('--build', type=int, required=True)
    p.add_argument('--version', required=True)
    p.add_argument('--key', type=Path, required=True)
    p.add_argument('--host', default='ubuntu@bjckwrn.xyz')
    args = p.parse_args()
    source = (args.game_dir / 'scripts/service_updater.gd').read_text(encoding='utf-8')
    assert re.search(rf'^const BUILD={args.build}$', source, re.M), 'Build mismatch'
    assert f'const VERSION="{args.version}"' in source, 'Version mismatch'
    assert args.build > 0
    ssh = ['ssh', '-o', 'BatchMode=yes', '-i', str(args.key), args.host]
    def remote(command):
        return subprocess.check_output(ssh + [command], text=True).strip()
    manifest = {'channel': 'service', 'build': args.build, 'version': args.version, 'platforms': {}}
    publish = []
    for platform, extension in [('windows', 'exe'), ('android', 'apk')]:
        artifact = args.game_dir / 'build' / f'ClassicTavern-Service.{extension}'
        digest = hashlib.file_digest(artifact.open('rb'), 'sha256').hexdigest()
        filename = f'ClassicTavern-Service-{args.build}.{extension}'
        destination = f'/var/www/classic-tavern/downloads/{filename}'
        previous = remote(f'if test -f {destination}; then sha256sum {destination}; fi')
        if previous and previous.split()[0] != digest:
            raise RuntimeError('Build number already published with different content; increment it')
        stage = f'/home/ubuntu/{filename}.upload'
        if not previous:
            subprocess.run(['scp', '-q', '-i', str(args.key), str(artifact), args.host + ':' + stage], check=True)
            actual = remote('sha256sum ' + stage).split()[0]
            assert actual == digest, 'Upload checksum mismatch'
            remote(f'sudo install -m 644 {stage} {destination}.new && sudo mv {destination}.new {destination}')
        manifest['platforms'][platform] = {'file': filename, 'bytes': artifact.stat().st_size, 'sha256': digest}
        alias = f'/var/www/classic-tavern/downloads/ClassicTavern-Service.{extension}'
        publish.append(f'sudo cp {destination} {alias}.new && sudo mv {alias}.new {alias}')
    repo = Path(__file__).resolve().parents[1]
    output = repo / 'config/client-update.json'
    output.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    subprocess.run(['scp', '-q', '-i', str(args.key), str(output), args.host + ':/home/ubuntu/client-update.json.upload'], check=True)
    remote(' && '.join(publish + [
        'sudo install -m 644 /home/ubuntu/client-update.json.upload /var/www/classic-tavern/downloads/latest.json.new',
        'sudo mv /var/www/classic-tavern/downloads/latest.json.new /var/www/classic-tavern/downloads/latest.json'
    ]))
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
