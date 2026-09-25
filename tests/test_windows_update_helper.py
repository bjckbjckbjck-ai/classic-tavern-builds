"""Exercise the actual embedded Windows installer using a disposable executable."""
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

import pytest


@pytest.mark.skipif(os.name != 'nt', reason='Windows executable replacement test')
def test_replace_preserves_previous_and_restarts(tmp_path):
    csc = Path(os.environ['WINDIR']) / 'Microsoft.NET/Framework64/v4.0.30319/csc.exe'
    if not csc.exists():
        pytest.skip('.NET Framework C# compiler unavailable')
    source = (Path(__file__).resolve().parents[1] / 'game_adapter/service_updater.gd').read_text(encoding='utf-8')
    helper = source.split('const INSTALL_SCRIPT="""', 1)[1].split('"""', 1)[0]
    # Spaces exercise argument passing used by user data / installation directories.
    directory = tmp_path / 'client update test'
    directory.mkdir()
    (directory / 'helper.ps1').write_text(helper, encoding='utf-8')
    (directory / 'new.cs').write_text(
        'using System; using System.IO; public class Program { public static void Main() {'
        ' File.WriteAllText(Path.Combine(AppDomain.CurrentDomain.BaseDirectory,"started.txt"),"new"); }}',
        encoding='utf-8',
    )
    subprocess.run([str(csc), '/nologo', '/target:winexe', '/out:new.exe', 'new.cs'], cwd=directory, check=True)
    target = directory / 'old.exe'
    target.write_bytes(b'previous-client')
    new = directory / 'new.exe'
    digest = hashlib.sha256(new.read_bytes()).hexdigest()
    (directory / 'job.json').write_text(json.dumps({
        'target': str(target), 'source': str(new), 'sha256': digest, 'pid': 99999999,
    }), encoding='utf-8')
    powershell = Path(os.environ['WINDIR']) / 'System32/WindowsPowerShell/v1.0/powershell.exe'
    subprocess.run([str(powershell), '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass',
                    '-File', str(directory / 'helper.ps1'), '-Config', str(directory / 'job.json')],
                   check=True, timeout=20)
    assert Path(str(target) + '.previous').read_bytes() == b'previous-client'
    assert hashlib.sha256(target.read_bytes()).hexdigest() == digest
    deadline = time.monotonic() + 5
    while not (directory / 'started.txt').exists() and time.monotonic() < deadline:
        time.sleep(.05)
    assert (directory / 'started.txt').read_text() == 'new'
