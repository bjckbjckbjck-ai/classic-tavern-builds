"""Run on the designated receiver. SSH port/key/path are explicit parameters."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--key',required=True);p.add_argument('--destination',required=True);p.add_argument('--host',default='ubuntu@bjckwrn.xyz');p.add_argument('--port',default='22');args=p.parse_args()
dest=Path(args.destination).resolve();dest.mkdir(parents=True,exist_ok=True)
ssh=['ssh','-o','BatchMode=yes','-o','ConnectTimeout=15','-p',args.port,'-i',args.key,args.host]
r=subprocess.run(ssh+['sudo /opt/classic-tavern/venv/bin/python /opt/classic-tavern/deploy/export_backups.py'],capture_output=True,text=True,check=True)
names=json.loads(r.stdout)
for name in names:
    if not name.startswith('tavern-') or '/' in name or '\\' in name:raise RuntimeError('Invalid remote backup name')
    existing=dest/name;checksum=dest/(name+'.sha256')
    if existing.exists() and checksum.exists() and hashlib.sha256(existing.read_bytes()).hexdigest()==checksum.read_text().split()[0]:continue
    for suffix in ['', '.sha256']:
        temporary=dest/(name+suffix+'.partial')
        subprocess.run(['scp','-q','-o','BatchMode=yes','-o','ConnectTimeout=15','-P',args.port,'-i',args.key,args.host+':/home/ubuntu/tavern-backup-export/'+name+suffix,str(temporary)],check=True)
    expected=(dest/(name+'.sha256.partial')).read_text().split()[0]
    actual=hashlib.sha256((dest/(name+'.partial')).read_bytes()).hexdigest()
    if expected!=actual:raise RuntimeError('Backup checksum mismatch')
    (dest/(name+'.partial')).replace(dest/name);(dest/(name+'.sha256.partial')).replace(dest/(name+'.sha256'))
    # name is constrained to the generated timestamp filename character set.
    if not all(ch.isalnum() or ch in '-.' for ch in name):raise RuntimeError('Unsafe filename')
    subprocess.run(ssh+['sudo touch /var/lib/classic-tavern/backups/'+name+'.received'],check=True)
print(json.dumps({'verified_archives':len(names),'destination':str(dest)},ensure_ascii=False))
