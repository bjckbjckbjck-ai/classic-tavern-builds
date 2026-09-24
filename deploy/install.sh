#!/usr/bin/env bash
set -euo pipefail
base=/opt/classic-tavern
if systemctl is-active --quiet classic-tavern; then
  active=$(python3 -c "import sqlite3; c=sqlite3.connect('/var/lib/classic-tavern/accounts.sqlite3'); print(c.execute(\"SELECT count(*) FROM rooms WHERE phase NOT IN ('finished','aborted')\").fetchone()[0])")
  if [ "$active" != 0 ]; then echo 'Active rooms remain; drain and wait before updating.'; exit 2; fi
fi
id tavern >/dev/null 2>&1 || useradd --system --home-dir /var/lib/classic-tavern --create-home --shell /usr/sbin/nologin tavern
install -d -o tavern -g tavern -m 700 /var/lib/classic-tavern
install -d -m 755 "$base" /var/www/classic-tavern/downloads
tar -xzf /home/ubuntu/service.tar.gz -C "$base"
chmod 755 "$base/godot"
python3 -m venv "$base/venv"
"$base/venv/bin/pip" install -q -r "$base/requirements.lock"
"$base/venv/bin/pip" freeze > "$base/requirements.lock"
if [ ! -f /etc/classic-tavern.env ]; then
  (umask 077; printf 'TAVERN_TICKET_KEY=%s\nTAVERN_DATA=/var/lib/classic-tavern\nGODOT_BIN=/opt/classic-tavern/godot\nGAME_PATH=/opt/classic-tavern/game\n' "$(openssl rand -hex 32)" > /etc/classic-tavern.env)
fi
cat > /etc/systemd/system/classic-tavern.service <<'EOF'
[Unit]
Description=Classic Tavern four-table service
After=network-online.target
[Service]
User=tavern
Group=tavern
WorkingDirectory=/opt/classic-tavern
EnvironmentFile=/etc/classic-tavern.env
ExecStart=/opt/classic-tavern/venv/bin/uvicorn app:app --host 127.0.0.1 --port 18080 --workers 1 --proxy-headers --forwarded-allow-ips=127.0.0.1
Restart=on-failure
RestartSec=3
KillMode=control-group
TimeoutStopSec=30
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/classic-tavern
MemoryMax=6G
TasksMax=128
[Install]
WantedBy=multi-user.target
EOF
if [ ! -f /etc/nginx/sites-available/classic-tavern ]; then
cat > /etc/nginx/sites-available/classic-tavern <<'EOF'
limit_req_zone $binary_remote_addr zone=tavern_api:10m rate=100r/s;
server {
 listen 80;
 server_name bjckwrn.xyz;
 client_max_body_size 16k;
 location /downloads/ { alias /var/www/classic-tavern/downloads/; autoindex off; }
 location / { limit_req zone=tavern_api burst=200 nodelay; proxy_pass http://127.0.0.1:18080; proxy_set_header Host $host; proxy_set_header X-Forwarded-For $remote_addr; }
EOF
for slot in 1 2 3 4; do
  port=$((15000+slot))
  printf ' location = /play/%s { proxy_pass http://127.0.0.1:%s; proxy_http_version 1.1; proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection "upgrade"; proxy_read_timeout 75s; proxy_send_timeout 75s; }\n' "$slot" "$port" >> /etc/nginx/sites-available/classic-tavern
done
printf '}\n' >> /etc/nginx/sites-available/classic-tavern
fi
ln -sfn /etc/nginx/sites-available/classic-tavern /etc/nginx/sites-enabled/classic-tavern
nginx -t
systemctl daemon-reload
systemctl enable classic-tavern
systemctl restart classic-tavern
systemctl reload nginx
for attempt in 1 2 3 4 5; do
  if curl --fail --silent http://127.0.0.1:18080/api/health; then exit 0; fi
  sleep 1
done
exit 1
