"""Server-only cleanup of the exact generated QA accounts in an explicit list.

Refuse mixed-player or active rooms. No process termination / service restart.
"""
import argparse,json,re,sqlite3,time
from pathlib import Path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--names',type=Path,default=Path('/home/ubuntu/room-qa-names.json'))
parser.add_argument('--dry-run',action='store_true')
args=parser.parse_args()
names=json.loads(args.names.read_text())
assert 1<=len(names)<=32 and len(set(names))==len(names) and all(re.fullmatch(r'qa_[0-9a-f]{8}',n) for n in names)
with sqlite3.connect('/var/lib/classic-tavern/accounts.sqlite3') as c:
    c.execute('PRAGMA foreign_keys=ON')
    ids={r[0] for r in c.execute('SELECT id FROM accounts WHERE name IN ('+','.join('?' for _ in names)+')',names)}
    if not ids:print('Already cleaned');raise SystemExit()
    slots=','.join('?' for _ in ids)
    rooms=c.execute(f'SELECT DISTINCT r.id,r.phase,r.updated FROM rooms r LEFT JOIN members m ON m.room=r.id WHERE r.owner IN ({slots}) OR m.account IN ({slots})',tuple(ids)*2).fetchall()
    for rid,phase,updated in rooms:
        if phase not in ('finished','aborted'):raise SystemExit('QA room still active; cleanup refused')
        if phase=='finished' and time.time()-updated<30:raise SystemExit('Wait for finished process cleanup before removing history')
        if any(a[0] not in ids for a in c.execute('SELECT account FROM members WHERE room=?',(rid,))):raise SystemExit('Non-QA member present; cleanup refused')
    if args.dry_run:
        print('Validated exact QA cleanup:',len(ids),'accounts,',len(rooms),'inactive rooms; no writes')
        raise SystemExit()
    for rid,phase,updated in rooms:
        for table in ['departures','results','members']:c.execute(f'DELETE FROM {table} WHERE room=?',(rid,))
        c.execute('DELETE FROM rooms WHERE id=?',(rid,))
    for table in ['departures','results','queue','sessions']:
        c.execute(f'DELETE FROM {table} WHERE account IN ({slots})',tuple(ids))
    c.execute(f'DELETE FROM accounts WHERE id IN ({slots})',tuple(ids))
    print('Removed exactly',len(ids),'QA accounts; retained accounts:',c.execute('SELECT count(*) FROM accounts').fetchone()[0])
