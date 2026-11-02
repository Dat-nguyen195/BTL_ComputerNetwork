# Mô phỏng và cấu hình bàn giao

**Đã có mô hình GNS3 tích hợp ba cơ sở và evidence runtime.**

- [GNS3 project52 node](gns3/hospital-3sites.gns3), [cách dựng/chạy/mở GUI](gns3/README.md), [manifest source/config](gns3/runtime-manifest.json).
- [Ma trận và kết quả thực](../test_results/test-matrix.md), [runtime evidence](../test_results/runtime/README.md), [báo cáo PDF](../docs/06-report/final/report.pdf).
- [Cấu hình Cisco hợp nhất](generated/), [module TV2 gốc và adapter](modules/tv2-lan-wireless/README.md), [runbook Cisco](test-runbook.md). Đây là tham chiếu riêng, chưa được chạy trên IOS/Packet Tracer.

Mô hình GNS3 chạy FRR OSPF, Linux bridge VLAN, iptables ACL/conntrack, NAT/PBR hai ISP, DHCP relay/dnsmasq, HTTP và Suricata NFQUEUE. Có9 router/firewall,5 switch,38 endpoint,52 link và18 pool;14 server nội bộ theo10/2/2. Máy đại diện không thay thử tải đủ1.120 PC.

Không mô phỏng GPON/DSL PHY, RF/WLC/AAA, HA chassis/state sync, VPN crypto hoặc hệ thống HIS/PACS/LIS thật. [Capability matrix](capability-matrix.md) và [integration log](integration-log.md) ghi phạm vi cụ thể. File TV2 `.pkt` giữ nguyên; không sửa XML hoặc dùng bằng chứng Linux để khẳng định `.pkt` đạt.
