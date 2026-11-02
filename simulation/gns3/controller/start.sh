#!/bin/sh
set -eu
# A separate Docker daemon keeps all lab networking inside this controller.
dockerd --data-root=/var/lib/docker --storage-driver=overlay2 >/tmp/dockerd.log 2>&1 &
for n in $(seq 1 60); do
    if docker info >/dev/null 2>&1; then break; fi
    sleep 1
done
docker info >/dev/null
mkdir -p /root/.config/GNS3/2.2
cat > /root/.config/GNS3/2.2/gns3_server.conf <<'EOF'
[Server]
host = 0.0.0.0
port = 3080
auth = False
projects_path = /lab/projects
images_path = /lab/images
report_errors = False
EOF
exec /opt/gns3/bin/gns3server --host 0.0.0.0 --port 3080
