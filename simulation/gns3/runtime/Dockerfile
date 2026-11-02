FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    frr iproute2 iptables iputils-ping traceroute curl dnsmasq isc-dhcp-relay \
    isc-dhcp-client dnsutils tcpdump conntrack python3 suricata wireguard-tools \
    procps ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY node.py /usr/local/bin/hospital-node
COPY config /opt/hospital/config
CMD ["python3", "/usr/local/bin/hospital-node"]
