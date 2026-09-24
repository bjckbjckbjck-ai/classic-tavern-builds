#!/usr/bin/env bash
set -euo pipefail
cat > /etc/systemd/system/classic-tavern-backup.service <<'EOF'
[Unit]
Description=Encrypted consistent Classic Tavern database backup
[Service]
User=tavern
Group=tavern
Environment=TAVERN_DATA=/var/lib/classic-tavern
ExecStart=/opt/classic-tavern/venv/bin/python /opt/classic-tavern/deploy/backup.py
UMask=0077
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/var/lib/classic-tavern
EOF
cat > /etc/systemd/system/classic-tavern-backup.timer <<'EOF'
[Unit]
Description=Daily 04:00 Asia/Shanghai database backup
[Timer]
OnCalendar=*-*-* 04:00:00 Asia/Shanghai
Persistent=true
RandomizedDelaySec=30
[Install]
WantedBy=timers.target
EOF
systemctl daemon-reload
systemctl enable --now classic-tavern-backup.timer
systemctl start classic-tavern-backup.service
systemctl list-timers classic-tavern-backup.timer --no-pager
