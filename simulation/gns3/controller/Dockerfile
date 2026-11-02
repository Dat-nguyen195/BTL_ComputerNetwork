FROM debian:bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    docker.io python3 python3-venv ca-certificates iproute2 curl \
    gcc make libpcap-dev busybox-static \
    && curl -fsSL https://github.com/GNS3/ubridge/archive/refs/tags/v0.9.19.tar.gz | tar xz -C /tmp \
    && make -C /tmp/ubridge-0.9.19 \
    && install /tmp/ubridge-0.9.19/ubridge /usr/local/bin/ubridge \
    && python3 -m venv /opt/gns3 \
    && /opt/gns3/bin/pip install --no-cache-dir gns3-server==2.2.55 \
    && rm -rf /var/lib/apt/lists/*
COPY patch_web_ui.py /usr/local/bin/patch-gns3-web-ui.py
RUN /opt/gns3/bin/python /usr/local/bin/patch-gns3-web-ui.py
COPY start.sh /usr/local/bin/start-lab-controller
ENTRYPOINT ["/bin/sh", "/usr/local/bin/start-lab-controller"]
