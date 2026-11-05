#!/bin/sh
set -eu
# A separate Docker daemon keeps all lab networking inside this controller.
# Runtime PID/socket files survive container stop/start and their old PIDs can
# belong to unrelated processes after restart. Use a fresh exec root each boot;
# the image/container data remains in the persistent /var/lib/docker volume.
exec_root=$(mktemp -d /tmp/hospital-docker.XXXXXX)
dockerd --data-root=/var/lib/docker --exec-root="$exec_root" \
    --pidfile="$exec_root/dockerd.pid" --storage-driver=overlay2 >/tmp/dockerd.log 2>&1 &
daemon_pid=$!
for n in $(seq 1 60); do
    if docker info >/dev/null 2>&1; then break; fi
    if ! kill -0 "$daemon_pid" 2>/dev/null; then
        cat /tmp/dockerd.log >&2
        exit 1
    fi
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
