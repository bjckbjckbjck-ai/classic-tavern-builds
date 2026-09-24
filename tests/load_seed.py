"""Run on server as root during pre-release QA; creates named test accounts only."""
import hashlib,json,secrets,sqlite3,time,os,pwd
from pathlib import Path
c=sqlite3.connect('/var/lib/classic-tavern/accounts.sqlite3')
prefix='load_'+secrets.token_hex(3)+'_';users=[]
with c:
    for i in range(33):
        name=prefix+str(i);token=secrets.token_urlsafe(32)
        uid=c.execute('INSERT INTO accounts(name,password,recovery) VALUES(?,?,?)',(name,'!disabled-test-login','!disabled')).lastrowid
        c.execute('INSERT INTO sessions VALUES(?,?,?)',(hashlib.sha256(token.encode()).hexdigest(),uid,time.time()+3600))
        users.append({'id':uid,'name':name,'token':token})
p=Path('/home/ubuntu/load-users.json');p.write_text(json.dumps(users));os.chmod(p,0o600)
owner=pwd.getpwnam('ubuntu');os.chown(p,owner.pw_uid,owner.pw_gid)
print('Created 33 QA accounts')
