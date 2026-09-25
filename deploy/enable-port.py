"""Run with sudo: add the requested TLS listener without changing existing routes."""
import pathlib,subprocess
p=pathlib.Path('/etc/nginx/sites-available/classic-tavern')
before=p.read_text()
if 'listen 21111 ssl;' not in before:
    if 'listen 443 ssl;' not in before:raise SystemExit('Expected existing TLS server block')
    after=before.replace('listen 443 ssl;','listen 443 ssl;\n    listen 21111 ssl;',1)
    p.write_text(after)
    check=subprocess.run(['nginx','-t'])
    if check.returncode:
        p.write_text(before)
        raise SystemExit('Invalid nginx config; original restored')
    subprocess.run(['systemctl','reload','nginx'],check=True)
print('TLS listener 21111 configured; this does not waive provider ICP requirements.')
