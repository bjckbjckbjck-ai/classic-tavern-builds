"""Decrypt into a separate verification file; never overwrite a live database."""
import argparse,base64,hashlib,json,sqlite3
from pathlib import Path
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
p=argparse.ArgumentParser();p.add_argument('archive');p.add_argument('private_key');p.add_argument('output');args=p.parse_args()
output=Path(args.output)
if output.exists():raise SystemExit('Refusing to overwrite an existing file')
blob=json.loads(Path(args.archive).read_text(encoding='utf-8'));b64=base64.b64decode
private=serialization.load_pem_private_key(Path(args.private_key).read_bytes(),password=None)
key=private.decrypt(b64(blob['key']),padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
meta=b64(blob['meta']);plain=AESGCM(key).decrypt(b64(blob['nonce']),b64(blob['ciphertext']),meta)
assert hashlib.sha256(plain).hexdigest()==json.loads(meta)['database_sha256']
output.write_bytes(plain)
with sqlite3.connect(output) as c:
    assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    print(json.dumps({'integrity':'ok','accounts':c.execute('SELECT count(*) FROM accounts').fetchone()[0],'results':c.execute('SELECT count(*) FROM results').fetchone()[0]}))
