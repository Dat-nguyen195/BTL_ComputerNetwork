# Phụ lục kiểm thử Packet Tracer

Cập nhật 04/11/2026; bằng chứng kỹ thuật, chưa thay phê duyệt nhóm.

## Bộ thử sau mở lại

| Nhóm | Phạm vi | Số lượt |
| --- | --- | ---: |
| TC01 | Cùng VLAN, hai chiều | 2 |
| TC02 | Liên VLAN và HIS | 3 |
| TC03 | Main - DBP/BHTQ, hai chiều | 4 |
| TC04 | DMZ và PAT tĩnh từ bên ngoài | 2 |
| TC05 | Guest bị chặn LAN/HIS, có đối chứng | 9 |
| TC06 | Web/DNS tập trung cho PC/Guest | 6 |
| WIFI | Staff qua Wi-Fi đến HIS/Web | 6 |

Tám ping cho phép đều 4/4; ba ping Guest không phản hồi. HTTP cho phép đúng marker; HTTP Guest thất bại có đối chứng và ACL tăng.

## Sáu kết nối Wi-Fi

| Máy | IPv4 | SSID | BSSID AP |
| --- | --- | --- | --- |
| Main-Guest | 10.10.100.11 | Main_Guest | 0200.0035.0002 |
| Main-Staff | 10.10.120.11 | Main_Staff | 0200.0036.0002 |
| DBP-Guest | 10.20.100.11 | DBP_Guest | 0200.0037.0002 |
| DBP-Staff | 10.20.120.11 | DBP_Staff | 0200.0038.0002 |
| BHTQ-Guest | 10.30.100.11 | BHTQ_Guest | 0200.0039.0002 |
| BHTQ-Staff | 10.30.120.11 | BHTQ_Staff | 0200.003A.0002 |

## Giới hạn

- ISP2 là đường PAT chính. ISP1 dự phòng chuyển thủ công; chưa chứng minh tự động failover, IP SLA hoặc PBR trên Packet Tracer. Bằng chứng GNS3 cho các tính năng đó được lưu riêng.
- Main-FW dùng 2811/profile 2800_advip_12.4, module NM-1FE-TX và ba cổng vật lý LAN/OUTSIDE/DMZ. Tám router còn lại dùng 2911; không chuyển kết quả probe 2911 thành kết luận cho mọi profile.
- Sáu liên kết dùng card AC, WPA2-PSK/AES với khóa lab công khai HospitalLab2026Only. Chưa đo RF, roaming, AAA/Enterprise hoặc tải vô tuyến thực.
- Ethernet thay chức năng hai leased line và các đường ISP. Không đo tốc độ xDSL/GPON, tải HIS/PACS, VPN crypto hoặc HA thiết bị từ mô hình này.
- Mã responseType 7 của HTTP Guest được giữ nguyên, không suy đoán tên enum. Kết luận chặn dựa thêm vào trang rỗng, đối chứng truy cập thành công và bộ đếm ACL tăng trong lần chạy.

## Truy vết

Project: `simulation/packet-tracer/hospital-3sites.pkt`.
SHA256: `45ff85657fc08186f4863d541ac7b12de1bd09a72fbf305c445c01f3cf839289`.
Evidence: `test_results/packet-tracer/after-reopen/`.
Giờ thu thập UTC: `2026-11-04T11:02:36.852305+00:00`.

Sinh bằng `python scripts/build_packet_report.py`; phải có ReportLab và font Arial hoặc DejaVu. Chỉ sinh sau khi checker evidence đạt. QA hình ảnh thực hiện riêng sau render.
