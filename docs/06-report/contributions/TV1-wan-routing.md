# Nội dung TV1: quy hoạch IP, WAN và định tuyến

**Người viết:** TV1. **Người nhận/biên tập:** TV5. **Cập nhật:** 26/10/2026. **Trạng thái:** BẢN THẢO KỸ THUẬT ĐÃ HIỆU CHỈNH, CHỜ ĐỌC CHÉO VÀ KIỂM THỬ. **Ngày bàn giao chính thức/PR:** chưa có. Không coi ngày hạn 17/11 là ngày đã thực hiện.

## 1. Yêu cầu và giả định

Nguồn [A] được tổng hợp tại [README](../../../README.md): Main 600 PC/10 server; DBP và BHTQ mỗi site 260 PC/2 server; hai leased lines; hai xDSL cân bằng tải tại Main; Internet tập trung; tăng trưởng tổng 20% trong 5 năm. Phân nhóm phòng ban/VLAN và vai trò server là baseline đề xuất, không phải kết quả khảo sát thực địa. FTTH/DIA là phương án thay thế cần chấp thuận, chưa được coi là yêu cầu gốc.

## 2. Địa chỉ và dung lượng

Khối dự trữ Main `10.10/16`, DBP `10.20/16`, BHTQ `10.30/16`, transit `10.255.0.0/24`, pool VPN `10.255.100.0/24`. Chỉ cấu hình subnet cụ thể, không gán /16 chồng lên VLAN. VPN chưa triển khai; `.1` dự trữ, `.2–.254` là 253 địa chỉ dự trù, TV3 xác nhận cách sử dụng pool và route về.

Main sau 5 năm: 720 PC; mỗi Aux: 312 PC; server theo site làm tròn lên: 12+3+3=18. VLAN PC /25 có 126 host, `.1–.6` dành gateway/hạ tầng, DHCP `.7–.126` có 120 IP. Nhóm Main 100 PC tăng lên 120 đã dùng hết pool; khi thêm thiết bị cần chia hoặc mở rộng subnet và cập nhật ACL/DHCP/route. Guest/Staff/camera cần khảo sát số thiết bị riêng, tránh tính trùng workstation.

Chi tiết [IP plan](../../02-design/ip-vlan-plan.md); script kiểm tĩnh không thay kiểm DHCP/địa chỉ trên mô phỏng.

## 3. WAN, OSPF và default

Theo [kiến trúc](../../02-design/architecture.md), OSPF area0 nối Main-Core–Main-GW–DBP/BHTQ, passive mặc định và mở đúng các liên kết. Cost WAN10, Core–GW1; route học theo subnet cụ thể, không tự tổng hợp /16 từ lệnh `network`. DMZ80 nối firewall, Core chỉ redistribute đúng static DMZ, không phát default thứ hai.

Lab Serial cấu hình 2 Mbps và cost định tuyến riêng, chỉ mô hình chức năng leased line; không phải phép đo năng lực 150–200 Mbps. Edge/FW dùng static route trả về ba site. Firewall tham chiếu là router để kiểm đường đi; TV3 còn phải triển khai policy/VPN/ACL/DMZ thật. Chưa có bằng chứng kiểm thử an toàn mạng.

Main-GW có IP SLA10 tới Web `192.0.2.100`, default track10 và `default-information originate metric 10` không `always`. Static /32 tới Web độc lập với default giúp probe hoạt động lại sau khi thu hồi route. Khi cả hai ISP mất và track down, default OSPF cần biến mất ở Aux sau hội tụ; route liên site vẫn còn nếu leased lines tốt.

## 4. Hai ISP và NAT

ISP1/ISP2 cùng nối INET-Core và cùng truy cập một Web-Lab `192.0.2.100`, không đổi đích giữa các ca failover. Hai SLA của Edge probe `.11/.22` phía sau từng ISP, /32 ghim đúng egress kèm Null0 fallback. PBR chọn ISP theo nguồn; không cam kết 50/50. PAT route-map chọn đúng interface ngoài; lưu lượng nội bộ được loại khỏi NAT. TV3 phải duy trì điều này khi thay firewall, tránh double NAT làm mất phân loại nguồn.

Timer tham chiếu: probe 3s, timeout1s, track delay down6/up6. Đây không phải số đo hội tụ hoặc “ba lần ping thất bại”. Phiên TCP/PAT cũ có thể bị ngắt khi IP ngoài thay đổi; phải ghi riêng phiên mới/phiên cũ và thời gian đo. Một Web health target có thể gây false negative nếu server/ICMP đích lỗi; vận hành thực cần đánh giá nhiều đích.

## 5. Tải và chi phí

Kịch bản bảo thủ, chưa có khách: design Internet tổng 583,11/142,22 Mbps theo [TV4](../../03-capacity/throughput.md), chưa đo và chưa đại diện đầy đủ tải PACS/camera/backup. Ví dụ hai ISP 500/500 Mbps là giả định; khi chỉ còn một ISP thiếu ít nhất 83,11 Mbps down so với baseline, cần chính sách ưu tiên tải hoặc nâng năng lực.

[So sánh WAN/TCO](../../02-design/wan-options-cost.md) giữ bốn phương án Metro-E, MPLS, SD-WAN, IPsec. Các TCO 1,745/1,948/2,105/1,775 tỷ VNĐ là số **giả định minh họa**, chưa có báo giá/thuế/hiệu lực. Không chốt nhà mạng, SLA hoặc lựa chọn kinh tế từ bảng này.

## 6. Kiểm chứng và hồ sơ cần bổ sung

| Hồ sơ | Trạng thái hiện tại | Cần có để kết luận |
| --- | --- | --- |
| [TC03](../../../test_results/TC03-inter-site/result.md) | NOT RUN | Ping/traceroute Main↔cả hai Aux, route/neighbor hai chiều, nguồn/đích và phiên bản |
| [TC06](../../../test_results/TC06-internet-web/result.md) | NOT RUN | HTTP/Web từ ba site và guest theo policy; đường đi qua Main và NAT đúng egress |
| [Dual ISP](../../../test_results/supplemental/dual-isp-failover.md) | NOT RUN | Cùng đích HTTP qua hai ISP, upstream failure, rút default, phục hồi, phiên cũ/mới |
| Kiểm tĩnh config | Chạy `python3 scripts/check_wan.py` | Chỉ kiểm các điều kiện config/route trong mô hình script; không kết luận IOS/NAT/OSPF runtime |

Chưa có project mô phỏng, ảnh/log runtime, hash bản test hoặc xác nhận reviewer. Không đưa số RTT, thời gian chuyển tuyến hay output CLI tự soạn vào mục actual.

## 7. Giới hạn và hướng phát triển

Mỗi Aux có một leased line; mất tuyến là mất đường về Main, hai ISP ở Main không thay thế tuyến này. Core/FW/Edge trong lab là thiết bị đơn; hai ISP chưa chứng minh HA toàn hệ thống. Đề xuất tuyến dự phòng/VPN và thiết bị HA cần thêm hạ tầng, ngân sách và test riêng. MPLS/SD-WAN/IPsec/teleworker/IDS-IPS chưa triển khai bằng bộ config WAN này; không coi PBR/OSPF là mô phỏng đầy đủ các tính năng đó.

## 8. Bàn giao cho TV5/TV4

- Thiết kế: [IP](../../02-design/ip-vlan-plan.md), [WAN](../../02-design/architecture.md), [chi phí](../../02-design/wan-options-cost.md).
- Cấu hình, mapping, thứ tự nạp và điểm kiểm tra: [module WAN](../../../simulation/modules/tv1-wan/README.md).
- TV4 cần chọn môi trường/model có IP SLA, tracking, PBR verify-availability, NAT route-map và redistribution; lưu project rồi thu evidence.
- TV2/TV3 đọc chéo IP, gateway DMZ, campus LAN và firewall rules; TV1 sửa phần chuyên môn sau phản hồi.
- Reviewer/ngày/PR chính thức: chờ xác nhận. TV5 tổng hợp bản báo cáo; TV1 chỉ duyệt khi có PDF và mô phỏng đúng hash.
