# Review toàn dự án sau hoàn thiện GNS3

**02/11/2026.** Đã đối chiếu đề gốc5 trang, bảy Step và sáu nhóm demo. [Báo cáo PDF](../06-report/final/report.pdf), [source chỉnh sửa](../06-report/source/report.md), [project GNS3](../../simulation/gns3/hospital-3sites.gns3) và [evidence](../../test_results/runtime/README.md) đã có thật.

**Kết luận:** mô hình chức năng ba cơ sở hoạt động trong phạm vi đã thử; sáu nhóm demo, OSPF, đủ18 pool DHCP/DNS, IDS/IPS rule mẫu, NAT/PBR, lỗi upstream ISP và mở lại project đều đạt ở hai run cuối. Không khẳng định triển khai bệnh viện thật đã sẵn sàng hoặc mọi yêu cầu vật lý/HA đã chạy.

| Step / trang đề | Đáp ứng hiện tại | Giới hạn hoặc việc ngoài workspace |
| --- | --- | --- |
|1 /3 | Phân tích3 site, checklist, phân vùng/server/DMZ/firewall, vùng tải cao và wireless plan | Chưa khảo sát/RF/roaming/AAA; không tự biến checklist thành biên bản |
|2 /3 | IP/VLSM, BOM, cabling/drawio/SVG, hai leased line/OSPF, WAN/cost, thiết kế GPON hybrid | GPON classB+/OLT/ONT là thiết kế; báo giá, SLA, tuyến và model thực cần xác nhận |
|3 /3 | Công cụ tính down/up/peak/growth,3 server scope và khách/overhead/shares; đề xuất năng lực |583,11/142,22Mbps là envelope giả định; xDSL PHY/gói thực chưa xác nhận đủ tải, mất1 đường500Mbps thiếu83,11Mbps down |
|4 /3 | Native GNS3 có52 node/52 link, mở lại đúng template từ source | Linux/FRR thay IOS; Ethernet thay DSL/leased PHY; host đại diện thay đủ1.120 PC |
|5 /3–4 | Sáu nhóm bắt buộc PASS;209 kiểm tích hợp +137 sau reopen; PCAP/log/hash thật | Không đo tải thực/TLS/clinical apps, local-link ISP và NAT session continuity |
|6 /3–4 | Đánh giá reliability/upgrade/software/security/risk/hướng phát triển; Suricata cảnh báo/chặn mẫu | HA chassis/state sync, VPN crypto, L2 isolation, feed/phishing thực chưa thử |
|7 /4 | PDF+source+GNS3+code+evidence và gói có checksum | Nhóm duyệt tên/lớp/MSSV/nhân sự rồi nộp BKeL; chưa có biên nhận |

Đề yêu cầu **đề xuất** VPN site-to-site và teleworker: [kế hoạch VPN](../04-security/vpn-plan.md) đáp ứng phần thiết kế, không ghi crypto PASS. Yêu cầu thêm của chương trình kỹ sư tài năng có firewall/ACL và IDS/IPS rule mẫu đã chạy trong GNS3, cùng [best practices](../04-security/security-best-practices.md); không coi một rule mẫu là kiểm đầy đủ mọi tấn công.

## Phát hiện được giải quyết và lỗi còn lại

- F01: đã gỡ TC01 PASS thiếu evidence từ Tiendat; PASS mới chỉ dựa log GNS3 có hash.
- F02/F03/F04/F05: giữ `.pkt` gốc và adapter; đã có mô hình ba site độc lập, VLAN/ACL/DMZ/WAN chạy được. Binary gốc không được sửa hoặc nghiệm thu IOS.
- F06/F07: static PAT chỉISP2 và đường reply đúng; hai ISP không tạo HA chassis, LACP đúng điều kiện logical switch, sơ đồ/cáp được tách rõ.
- F08/F09: sửa sizing PoE/cổng/AP/camera/NVR, thêm [GPON hybrid](../02-design/gpon-design.md) có số lượng và budget. Chưa có phép đo quang hoặc giá chính thức.
- F10: giữ uncertainty workload/guest/Internet share; không chọn gói thương mại bằng dữ liệu chưa có.
- F11/F12: có Suricata alert/drop, PDF/source/evidence/reopen; VPN/HA/RF/AAA vẫn giới hạn đã ghi. Approval và biên nhận BKeL không bị tạo giả.
- Lỗi vận hành ghi nhận: có gián đoạn khi rút/quảng bá lại default sau mất ISP. Hai FAIL đầu tiên được giữ; bộ thử sau đo thời gian phục hồi8,707s/6,521s và lưu samples outage, không cam kết zero-downtime.

## Việc cần xác nhận trước nộp/triển khai

Nhóm kiểm thông tin đăng ký và quy định2–3 người trong đề so với vai tròTV1–TV5; yêu cầu nhân sự/lịch của nhóm được giữ riêng, không tự xác nhận giảng viên đã duyệt. Kiểm bản PDF/project đúng checksum, chạy demo trên máy sẽ trình bày và tự nộp BKeL. Với triển khai thực cần khảo sát, báo giá/SLA, năng lực xDSL thực, GPON/RF/HA/crypto và ứng dụng y tế.

[Review trước GNS3](project-review-before-gns3.md) và [review TV2](tv2-review.md) giữ lịch sử phát hiện, không phải trạng thái cuối. Các phê duyệt học phần của thành viên/giảng viên vẫn cần người có trách nhiệm thực hiện.
