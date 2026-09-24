"""Root-run helper: export encrypted archives only, never raw database or keys."""
import json,os,pwd,shutil
from pathlib import Path
source=Path('/var/lib/classic-tavern/backups');dest=Path('/home/ubuntu/tavern-backup-export')
dest.mkdir(exist_ok=True,mode=0o700);user=pwd.getpwnam('ubuntu');os.chown(dest,user.pw_uid,user.pw_gid)
names=[]
for p in source.glob('*.enc.json'):
    for item in [p,source/(p.name+'.sha256')]:
        target=dest/item.name;shutil.copyfile(item,target);os.chmod(target,0o600);os.chown(target,user.pw_uid,user.pw_gid)
    names.append(p.name)
print(json.dumps(sorted(names)))
