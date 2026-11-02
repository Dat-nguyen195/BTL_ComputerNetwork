# Khả năng nền tảng và phạm vi đã kiểm

**Nền tảng thực tế: GNS3 2.2.55 + FRR/Linux; metadata/version trong [evidence](../test_results/runtime/README.md).**

| Tính năng | GNS3 Linux | Cisco IOS/Packet Tracer |
| --- | --- | --- |
| VLAN802.1Q, access/trunk, ACL ingress | PASS, bridge VLAN và gói tin thật | Cấu hình tham chiếu; chưa chạy |
| OSPF passive/P2P/route/default | PASS,4 router Full; default rút khi hai ISP mất | Chưa kiểm parser/timer |
| NAT/PBR/track | PASS hai nhóm nguồn và fault upstream từng ISP/cả hai | Linux health loop tương đương mục tiêu, không phải IOS IP SLA |
| Stateful LAN/OUTSIDE/DMZ | PASS conntrack và luồng HTTP/negative | ZBF tham chiếu; chưa chạy IOS |
| DHCP relay/DNS | PASS19 client/18 pool, ACK/gateway/DNS | Chưa nhập Services/chạy Packet Tracer |
| IDS/IPS | PASS Suricata marker alert/drop + positive control | Không coi ACL là IDS |
| Persistence | PASS native template được mở lại và smoke137 kiểm | File TV2 gốc startup trống, chưa chạy |
| GPON/DSL physical/RF/WLC/AAA | Thiết kế/mô hình chức năng IP, không mô phỏng vật lý | Chưa chạy |
| VPN crypto, HA chassis/state sync | DESIGN ONLY / NOT RUN | DESIGN ONLY / NOT RUN |
| Throughput/ứng dụng thật | Chưa benchmark/tải đủ bệnh viện | Chưa chạy |

File TV2 gốc lưu metadata PacketTracer9.0.0.0810, core3650 commandset16.3.2/access2960 15.0-SE4; metadata không chứng minh tương thích parser. Nền tảng Cisco vẫn cần kiểm riêng nếu nhóm quyết định nộp `.pkt` thay GNS3.
