"""Run with sudo on the server: status | drain | resume | backup."""
import json,sqlite3,subprocess,sys
from pathlib import Path
root=Path('/var/lib/classic-tavern');command=sys.argv[1]
if command=='drain':(root/'maintenance').touch();print('New room allocation paused. Existing games continue.')
elif command=='resume':(root/'maintenance').unlink(missing_ok=True);print('New room allocation resumed.')
elif command=='backup':subprocess.run(['systemctl','start','classic-tavern-backup.service'],check=True)
elif command=='status':
    with sqlite3.connect(root/'accounts.sqlite3') as c:
        print(json.dumps({'maintenance':(root/'maintenance').exists(),'accounts':c.execute('SELECT count(*) FROM accounts').fetchone()[0],'rooms':c.execute("SELECT slot,mode,phase FROM rooms WHERE phase NOT IN ('finished','aborted')").fetchall(),'queued':c.execute('SELECT count(*) FROM queue').fetchone()[0]}))
else:raise SystemExit('Unknown command')
