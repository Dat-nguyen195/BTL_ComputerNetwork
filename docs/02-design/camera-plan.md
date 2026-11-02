# Camera: tích hợp cáp/PoE TV2 và quyền/lưu trữ TV3

**TV2/TV3; hiệu chỉnh02/11/2026. THIẾT KẾ GIẢ ĐỊNH / CHƯA CAMERA-NVR RUNTIME.** Tiếp nhận giả địnhTiendat4 camera/tầng (Main40, Aux8/site), H.265/4 MP,4 Mbps/camera,30 ngày. Không ghi đây là số lượng/retention khảo sát hoặc yêu cầu pháp lý. Dự trù tăng20% và làm tròn từng tầng:5 camera/tầng, Main50/Aux10. Đầu vào/kết quả trong [campus CSV](campus-inputs.csv)/[budget](campus-budget.csv).

## VLAN, quyền và luồng video

Mỗi site VLAN110 /24, gateway `.110.1`, NVR appliance `.110.11`; camera tĩnh dự trù `.110.100–.254`. Chưa bật DHCP camera trong baseline. NVR không nằm trong 14 server ứng dụng; Main nối switch Server Farm hỗ trợVLAN110, Aux dùng1 port access tại MDF tầng1. DMZswitch không phục vụ NVR/camera.

| Nguồn | Đích /dịch vụ | Chính sách |
| --- | --- | --- |
| Camera | NVR cùng site/VLAN110 | Ghi hình local; port RTSP/ONVIF theo vendor sau chọn model |
| Main-Admin10.10.90.11 | NVR/camera được cấp quyền | Qua mạng riêng; ACL CAMERA cho trả lời; ứng dụng/xác thực chưa triển khai |
| Nhân viên/khách/Internet | Camera/NVR | Không có quyền mặc định; không port-forward NVR ra Internet |
| Camera/NVR | Main-Monitor10.10.70.17 | UDP123 đồng bộ giờ; Internet trực tiếp bị chặn |

Luồng ghi local không đi WAN/ISP; xem/backup từ xa mới cộng lượng stream thực và kiểm quyền riêng. Camera/NVR cùng VLAN trao đổi L2 nên ACL gateway không bảo vệ mọi luồng đó; cần account/quyền ứng dụng và switch isolation/host policy khi cần. Không đặt camera ở khu nhạy cảm trước khi bệnh viện xác nhận quyền riêng tư.

## Cáp và PoE

Mỗi camera1 port access và 1 Cat6 drop về IDF tầng, tốc độ đàm phán theo model. Dự trù PSE15,4 W/camera: hiện4/tầng61,6 W,5 năm5/tầng77 W. CộngAP30 W:151,6 W hiện tại và 197 W/tầng5 năm. C9200L-48P-4X +PSU1 kW có 740 W, không phải370 W; [BOM](equipment-bom.md) ghi nguồn và ngân sách từng tầng. Kiểm tải từng cổng/switch/UPS, cáp/rack/ODF và điều kiện hỏng nguồn, không dùng tổngPoE để tự xác nhậnHA.

## Lưu trữ thập phân và tăng trưởng

```text
B_record_Mbps = camera_count * bitrate_Mbps
Raw_GB = B_record_Mbps * 10^6 / 8 * 86400 * retention_days / 10^9
Required_usable_GB = Raw_GB * (1 + recording_overhead) / usable_fill_ratio
B_uplink = B_record_Mbps * (1 + network_overhead) / utilization_target
```

Giả định recording overhead5%, chỉ dùng80% dung lượng sauRAID; khác với tăng20% số camera. Không trộn công thức×1,2 của bản cũ với 5%/80% mà không giải thích. RAID không thay backup. Recording bitrate VBR cần đo trung bình/peak; không lấy thông số model chưa chọn làm benchmark.

| Site | Camera nay→5 năm | Video nay→5 năm | Raw30 ngày hiện tại | Required usable hiện tại→5 năm |
| --- | --- | --- | --- | --- |
| Main |40→50 |160→200 Mbps |51.840 GB |68.040→85.050 GB |
| DBP |8→10 |32→40 Mbps |10.368 GB |13.608→17.010 GB |
| BHTQ |8→10 |32→40 Mbps |10.368 GB |13.608→17.010 GB |

Ví dụ số học: Main12 ×10 TB RAID6 cho100 TB lý thuyết trước filesystem; Aux4 ×12 TB RAID6 cho24 TB. Kiểm usable thật, NVRbay/channels/maximum ingest/ổ được hãng hỗ trợ, rebuild/hot spare và license trước mua. Ví dụ10 ×8 TB RAID6=64 TB của bản Tiendat **thiếu ngay hiện tại** dưới bộ giả định5%/80%; không giữ cấu hình đó rồi tuyên bố đủ 62,2 TB/HA. Main cần≥64 kênh/Aux≥16 kênh để chứa50/10 camera dự trù; model/giá chưa chốt.

TV2/TV5 khảo sát vị trí/cáp/RF/điện; TV3 xác nhận quyền/retention, thử ghi/xem/restore; TV4 kiểm tảiWAN khi xem từ xa và lưu evidence. Hiện số liệu chỉ là thiết kế, không có video/storage/PoE runtime log.
