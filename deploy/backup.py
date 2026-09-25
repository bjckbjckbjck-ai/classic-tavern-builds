"""Consistent SQLite snapshot + AES-GCM / RSA-OAEP envelope. Public key only on cloud."""
import base64,hashlib,json,os,sqlite3,tempfile,time
from pathlib import Path
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
root=Path(os.environ.get('TAVERN_DATA','/var/lib/classic-tavern'))
output=root/'backups';output.mkdir(exist_ok=True,mode=0o700)
public=serialization.load_pem_public_key(Path('/etc/classic-tavern-backup-public.pem').read_bytes())
with tempfile.TemporaryDirectory(dir=root) as folder:
    snapshot=Path(folder)/'accounts.sqlite3'
    source=sqlite3.connect(root/'accounts.sqlite3');dest=sqlite3.connect(snapshot)
    source.backup(dest);source.close()
    if dest.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise RuntimeError('Database integrity check failed')
    dest.close();plain=snapshot.read_bytes()
key=AESGCM.generate_key(bit_length=256);nonce=os.urandom(12)
meta=json.dumps({'format':1,'created':time.time(),'database_sha256':hashlib.sha256(plain).hexdigest(),'game':'0.61.0','service':'0.2.0-preview','restore':'Stop service; restore DB; revoke sessions; abort active rooms; restart.'},sort_keys=True).encode()
b64=lambda b:base64.b64encode(b).decode()
package={'meta':b64(meta),'nonce':b64(nonce),'key':b64(public.encrypt(key,padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=None))),'ciphertext':b64(AESGCM(key).encrypt(nonce,plain,meta))}
name=time.strftime('tavern-%Y%m%d-%H%M%S',time.gmtime())+'.enc.json'
temp=output/(name+'.tmp');temp.write_text(json.dumps(package),encoding='utf-8');os.chmod(temp,0o600);temp.replace(output/name)
digest=hashlib.sha256((output/name).read_bytes()).hexdigest()
(output/(name+'.sha256')).write_text(digest+'  '+name+'\n',encoding='ascii')
print('BACKUP_CREATED',name,digest)
# Delete only old archives explicitly acknowledged by the receiver.
for p in output.glob('*.enc.json'):
    if time.time()-p.stat().st_mtime>7*86400 and p.with_suffix(p.suffix+'.received').exists():
        for item in [p,p.with_suffix(p.suffix+'.sha256'),p.with_suffix(p.suffix+'.received')]:item.unlink(missing_ok=True)
