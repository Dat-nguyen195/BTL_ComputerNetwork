# Phạm vi mô phỏng Cisco Packet Tracer

Ngày 13/11/2026, theo lựa chọn của nhóm, bộ bàn giao chỉ giữ Cisco Packet Tracer. Mô hình chính `simulation/packet-tracer/hospital-3sites.pkt` có SHA256 `183953558f045e378ddbbed3205da84e357865381f03f95b4dc625cf79e0b31a`, 102 node/97 cáp; không thay đổi native trong lần chuẩn hóa tài liệu này.

Báo cáo, mã thu/kiểm evidence, hướng dẫn cài đặt, CLI dự án và gói bàn giao chỉ sử dụng công cụ phục vụ Packet Tracer và tài liệu. Các lab bổ sung, controller/container, script chạy nền, bản sao report cũ và chứng cứ không thuộc nền tảng đã chọn không nằm trong repo/bộ nộp hiện tại.

| Nội dung | Trạng thái |
| --- | --- |
| VLAN, OSPF, liên site, DHCP/DNS, NAT/PAT/DMZ, ACL Guest | Đã có raw Cisco và kiểm offline |
| Wi-Fi | Association, BSSID và DHCP trên client đại diện; chưa đo RF |
| Camera | 14 mẫu Ethernet, đăng ký/quyền quản lý IoT; chưa ghi/lưu video |
| SSH | Main-Admin tới Main-Core và hai đối chứng; chưa hardening toàn bộ |
| Hai ISP | Chọn/khôi phục thủ công, không ghi là failover tự động |
| PBR/probe, IDS/IPS, phishing, VPN, HA, GPON PHY, throughput | Đề xuất/chưa nghiệm thu native |

MPLS và SD-WAN chỉ còn là phương án WAN so sánh trong thiết kế theo đề bài; mô phỏng chính dùng hai leased line routed và OSPF. Không có lab provider riêng trong bộ nộp. Tài liệu gốc/đề tham khảo là đầu vào được giữ nguyên, không chỉnh để thay yêu cầu.

Kết quả runtime ngày 12/11 giữ nguyên; cập nhật tài liệu và checker ngày 13/11 không được gán thành test mạng mới. Bản sao trước chuẩn hóa được lưu ngoài repository để khôi phục khi cần.
