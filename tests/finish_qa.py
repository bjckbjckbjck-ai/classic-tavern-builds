"""Server-only QA cleanup: refuse to interrupt any non-QA active match or queue."""
import re,sqlite3,subprocess,sys
from pathlib import Path
run=lambda *args:subprocess.run(args,check=True)
root=Path('/var/lib/classic-tavern')
run('python3','/opt/classic-tavern/deploy/ops.py','drain')
try:
    with sqlite3.connect(root/'accounts.sqlite3') as c:
        names=[r[0] for r in c.execute("SELECT a.name FROM rooms r JOIN members m ON r.id=m.room JOIN accounts a ON a.id=m.account WHERE r.phase NOT IN ('finished','aborted') UNION SELECT a.name FROM queue q JOIN accounts a ON a.id=q.account")]
    if any(not re.fullmatch(r'qa_[0-9a-f]{8}|load_[0-9a-f]{6}_[0-9]+',name) for name in names):
        raise SystemExit('Real players active: cleanup refused; service stays running.')
    run('systemctl','stop','classic-tavern')
    try:
        run('python3','/home/ubuntu/cleanup_qa.py')
        if len(sys.argv)>1:
            if sys.argv[1]!='/home/ubuntu/service-app-issue33.py':raise SystemExit('Unexpected app update path')
            run('install','-m','644',sys.argv[1],'/opt/classic-tavern/app.py')
    finally:
        run('systemctl','start','classic-tavern')
finally:
    run('python3','/opt/classic-tavern/deploy/ops.py','resume')
