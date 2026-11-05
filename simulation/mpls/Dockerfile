FROM alpine:3.22
RUN apk add --no-cache frr iproute2 iptables python3 curl tcpdump
COPY mpls_runtime.py /opt/mpls/mpls_runtime.py
CMD ["python3", "/opt/mpls/mpls_runtime.py", "node", "--name", "P-Core"]
