"""Server-side guarded update of API + table adapter; no active game interruption."""
import json,shutil,sqlite3,subprocess,time,urllib.request
from pathlib import Path

root=Path('/var/lib/classic-tavern');base=Path('/opt/classic-tavern')
stage=Path('/home/ubuntu/room-update')
if not (root/'maintenance').exists():raise SystemExit('Drain first; refusing unguarded update')
with sqlite3.connect(root/'accounts.sqlite3') as c:
    active=c.execute("SELECT count(*) FROM rooms WHERE phase NOT IN ('finished','aborted')").fetchone()[0]
    queued=c.execute('SELECT count(*) FROM queue').fetchone()[0]
if active or queued:raise SystemExit('Players still active or queued; update deferred')
subprocess.run(['systemctl','start','classic-tavern-backup.service'],check=True)
backup=base/('rollback-rooms-'+str(int(time.time())))
backup.mkdir(mode=0o700)
files={'app.py':base/'app.py','service_server.gd':base/'game/scripts/service_server.gd'}
for name,target in files.items():
    if not (stage/name).is_file():raise SystemExit('Missing staged file: '+name)
    shutil.copy2(target,backup/name)
subprocess.run(['systemctl','stop','classic-tavern'],check=True)
try:
    for name,target in files.items():
        shutil.copyfile(stage/name,target);target.chmod(0o644)
    subprocess.run(['systemctl','start','classic-tavern'],check=True)
    ready=False
    for _ in range(20):
        try:
            with urllib.request.urlopen('http://127.0.0.1:18080/api/health',timeout=2) as r:
                ready=json.load(r).get('service')=='0.3.0-preview'
            if ready:break
        except OSError:pass
        time.sleep(.5)
    if not ready:raise RuntimeError('New API health check failed')
except Exception:
    subprocess.run(['systemctl','stop','classic-tavern'],check=True)
    for name,target in files.items():shutil.copy2(backup/name,target)
    subprocess.run(['systemctl','start','classic-tavern'],check=True)
    (root/'maintenance').unlink(missing_ok=True)
    raise
(root/'maintenance').unlink(missing_ok=True)
print('API 0.3.0-preview and room adapter deployed; previous files: '+str(backup))
