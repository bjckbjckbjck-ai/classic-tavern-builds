"""Pre-release cleanup of the exact generated QA name formats. Requires service stopped."""
import re,sqlite3,subprocess
if subprocess.run(['systemctl','is-active','--quiet','classic-tavern']).returncode==0:raise SystemExit('Stop service before QA cleanup')
c=sqlite3.connect('/var/lib/classic-tavern/accounts.sqlite3')
ids={r[0] for r in c.execute('SELECT id,name FROM accounts') if re.fullmatch(r'qa_[0-9a-f]{8}|load_[0-9a-f]{6}_[0-9]+',r[1])}
rooms={r[0] for r in c.execute('SELECT room,account FROM members') if r[1] in ids}
for room in rooms:
    if any(r[0] not in ids for r in c.execute('SELECT account FROM members WHERE room=?',(room,))):raise SystemExit('Mixed real/test room; refuse cleanup')
with c:
    for room in rooms:
        c.execute('DELETE FROM results WHERE room=?',(room,));c.execute('DELETE FROM members WHERE room=?',(room,));c.execute('DELETE FROM rooms WHERE id=?',(room,))
    for uid in ids:
        c.execute('DELETE FROM sessions WHERE account=?',(uid,));c.execute('DELETE FROM queue WHERE account=?',(uid,));c.execute('DELETE FROM accounts WHERE id=?',(uid,))
print('Cleaned QA accounts:',len(ids),'rooms:',len(rooms))
