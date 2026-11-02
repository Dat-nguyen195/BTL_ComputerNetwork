# Đánh giá hệ thống - Step6

**Cập nhật sau runtime:** GNS3 Linux đã đạt209 kiểm tích hợp và137 sau reopen, có19 lease/18 pool, OSPF, NAT/PBR, Suricata và samples hội tụ8,707s/6,521s. [Review cuối](../00-management/project-review.md) và [PDF](../06-report/final/report.pdf) thay phần trạng thái runtime pending trong bảng review thiết kế lịch sử bên dưới. Chưa có bằng chứng RF/quang/DSL PHY/VPN/HA hoặc ứng dụng y tế thật.

**Rà soát thiết kế toàn dự án02/11/2026; TV5 tổng hợp, TV1 duyệt cuối. DESIGN REVIEWED / RUNTIME PENDING.** Đánh giá dưới đây dựa vào source/config/audit của bản tích hợp, chưa phải benchmark hoặc nghiệm thu mô phỏng.

| Tiêu chí | Kết quả rà soát thiết kế | Hạn chế /việc cần chứng minh |
| --- | --- | --- |
| Tin cậy | Có hai ISP, PBR/track/default có điều kiện; probe sau ISP và Web chung,9 kịch bản mô hình tĩnh | Chưa đo hội tụ/phiên NAT; Core/FW/Edge lab đơn, mỗi Aux một leased line; DMZ inbound chỉISP2; HA thiết bị chưa chạy |
| Nâng cấp5 năm | PC1344, server dự trù18; Main810/960 cổng, Aux334/384; AP/camera và PoE tính ceil từng tầng | PoolPC /25 đúng 120 lease, không dư nếu thêm thiết bị; guest/staff đồng thời, RF, workload bệnh viện và license chưa chốt |
| Phần mềm | Phân bổ HIS/RIS-PACS/LIS/CRM/DB/backup/infra đủ 10/2/2; tách DMZ | HTTP stand-in không chứng minh DICOM/DB/TLS, bản quyền, tích hợp ứng dụng hoặc RPO/RTO; lựa chọn licensed/open-source cần TV5/TV3 tổng hợp từ nhu cầu thực |
| Bảo mật | ACL tại gateway ba site vì east-west bypassFW; ZBF3 vùng, NAT tập trung, guest deny với positive controls | IPv4/stateless east-west, giao tiếp cùng VLAN và self-zone còn giới hạn; VPN/IDS/IPS/AAA/L2 guest isolation/phishing chưa triển khai |
| Vận hành | Có build/check/hash config, cabling/port map, runbook, rollback và kế hoạch lưu/mở lại | Module `.pkt` gốc startup trống,4 PC chưaIP; chưa có actual restore/reopen hoặc ảnh/log đúng project hash |
| Chi phí | WAN/TCO giữ giả định; BOM nêu model/spec/PoE/quang/license và dữ liệu chờ | Chưa báo giá/SLA/handoff/tuyến độc lập/thuế; không suy gói xDSL đủ từ tốc độ tổng hoặc chốt model mua bằng giá giả |
| Khớp yêu cầu | Có kiến trúc3 site, VLAN/IP, hai leased lines, sizing và 6 nhóm procedure | File native hiện chỉ Main một phần; GPON còn design/chờ xác nhận; PDF tổng và evidence chưa có |

## Vấn đề còn lại và hướng phát triển

Ưu tiên hiện tại là mở bản sao module TV2, sửa IP/port/startup, thêm server và ghép đủ ba site với cấu hình WAN/security; thử feature support trước khi chọn model. Sau đó chạy TC01–TC06 và dual ISP với positive/negative controls, lưu actual/ảnh/log/hash và kiểm reopen. Chưa có evidence thì không dự đoán RTT, hội tụ, throughput hoặc PASS.

Giai đoạn phát triển sau: đa tuyến leased line/underlay, HA có state sync cho firewall/edge/core, RPO/RTO và restore, giám sát tập trung, tách app/DB bằng host firewall/VRF, khảo sát RF/camera và sizing theo ứng dụng thật. GPON cần OLT/ODN/ONT/OS2/optical budget riêng; controller/AAA cần port/policy tương thích. Mỗi đề xuất phải có model/license/nguồn/chi phí và bài test riêng, không coi một sơ đồ có cặp thiết bị là đã đạt HA.

Xem [review toàn dự án](../00-management/project-review.md) và [risk register](risks.md). TV5 phải đưa giới hạn này vào báo cáo; TV1 chỉ duyệt PDF/mô phỏng cuối đúng hash sau evidence và reopen.
