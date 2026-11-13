# Đánh giá hệ thống Cisco

Native102/97, kết nối ba site, VLAN/OSPF, DHCP/DNS, NAT/PAT/DMZ, ACL Guest, Wi-Fi đại diện, SSH và camera IoT có raw ngày12/11. [Ma trận](../final-acceptance-matrix.md) xác định từng phạm vi.

Hai ISP chỉ chọn/khôi phục thủ công; PBR/probe tự động, IDS/IPS, VPN crypto và HA chưa nghiệm thu. Băng thông là số học theo giả định; chưa đo throughput/RF/GPON PHY. HIS/PACS/DB là vai trò/HTTP marker, không phải ứng dụng thật. Camera chưa ghi/lưu video.

Dự trù tăng20% trong5năm, cổng/BOM/PoE và camera có calculator; cần chốt tải thực, báo giá/SLA, quyền riêng tư, backup/restore và thời gian lưu. Core/FW/Edge đơn và leased line mỗi Aux còn SPOF. Xem [rủi ro](risks.md) và [phạm vi](../cisco-scope.md).
