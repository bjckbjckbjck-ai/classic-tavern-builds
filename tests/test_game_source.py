import subprocess
from pathlib import Path

from deploy.game_source import GameSource


def test_bundle_source_ignores_uncommitted_rules_and_data(tmp_path):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(tmp_path), *args])
    git('init', '-q')
    (tmp_path / 'scripts').mkdir()
    (tmp_path / 'data').mkdir()
    (tmp_path / 'scripts/service_server.gd').write_text('preload("res://scripts/rules.gd")')
    (tmp_path / 'scripts/rules.gd').write_text('committed rules')
    (tmp_path / 'data/cards.json').write_text('{"version":1}')
    (tmp_path / 'data/remote.json').write_text('{"private":true}')
    git('add', '.')
    git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture')
    source = GameSource(tmp_path, 'HEAD')
    (tmp_path / 'scripts/rules.gd').write_text('unreviewed rules')
    (tmp_path / 'data/cards.json').write_text('{"version":2}')
    (tmp_path / 'data/untracked.json').write_text('{}')
    assert source.read('scripts/rules.gd') == b'committed rules'
    assert source.read('data/cards.json') == b'{"version":1}'
    assert source.server_files() == ['data/cards.json', 'scripts/rules.gd', 'scripts/service_server.gd']
