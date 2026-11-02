# Camera: phân vùng, quyền xem và tính lưu trữ

**TV3 chủ trì bảo mật/lưu trữ; TV2 cáp/PoE; TV4 đối chiếu tải. 02/11/2026. DESIGN ONLY.** Chưa khảo sát số camera, vị trí, bitrate, codec, retention hay yêu cầu quyền riêng tư.

Mỗi site có VLAN110 /24, gateway `.110.1`, NVR appliance `.110.11`, camera tĩnh dự trù `.110.100–.254`; đây là vùng địa chỉ, không phải xác nhận cần 155 camera. Baseline chưa bật DHCP camera. Mỗi NVR ghi tại chỗ; chỉ đưa luồng WAN vào sizing khi có xem từ xa/backup thực sự. NVR không nằm trong 14 server ứng dụng, phải có dòng BOM riêng.

| Nguồn | Đích / dịch vụ | Chính sách |
| --- | --- | --- |
| Camera trong site | NVR cùng VLAN110 | Luồng ghi hình cục bộ; port theo vendor sau chọn model |
| Main-Admin 10.10.90.11 | NVR/camera được cấp quyền | Quản trị qua mạng riêng; ACL CAMERA cho phép trả lời; ứng dụng xác thực chưa triển khai |
| Nhân viên/khách/Internet | Camera/NVR | Không có quyền mặc định; không port-forward NVR ra Internet |
| Camera/NVR | Main-Monitor 10.10.70.17 | UDP123 đồng bộ giờ; Internet trực tiếp bị chặn |

Camera và NVR cùng VLAN trao đổi L2, ACL gateway không kiểm soát luồng đó; cần quyền ứng dụng, switch isolation/host firewall nếu phải hạn chế trong VLAN. Chưa cấu hình RTSP/ONVIF thực; không tự đoán port quản trị của model chưa chọn.

## Công thức định cỡ

```text
B_record_Mbps = sum(N_i * bitrate_i)
B_uplink_Mbps = B_record_Mbps * (1 + overhead_network) / utilization_target
Raw_GB = B_record_Mbps * 10^6 / 8 * 86400 * retention_days / 10^9
Required_usable_GB = Raw_GB * (1 + recording_overhead) / usable_fill_ratio
N_5years = ceil(N_now * 1.2)
PoE_required_W = sum(N_i * max_device_power_W_i) + reserve_W
```

MB/GB thập phân; usable sau RAID phải đủ Required_usable_GB, sau đó mới quy đổi số ổ và dung lượng raw array. RAID không thay backup; bitrate VBR cần kiểm cả trung bình và peak. Không cộng toàn bộ B_record vào ISP khi camera chỉ ghi local.

Ví dụ **giả định để kiểm công thức**: 32 camera ×4 Mbps, 30 ngày → 128 Mbps, 41.472 GB raw video (41,472 TB); recording overhead5%, fill80% → 54.432 GB usable. Tăng trưởng `ceil(32×1,2)=39` camera → 156 Mbps, 50.544 GB raw và 66.339 GB usable cùng giả định. Đây không phải số lượng/dung lượng đã khảo sát. Với giả định max12 W/camera: 384 W hiện tại, 468 W sau tăng trưởng, còn phải thêm reserve/thiết bị khác.

TV2 kiểm số port/cáp, ngân sách PoE cả switch, công suất từng cổng, UPS, uplink và tuyến quang tới MDF/IDF; không chỉ nhân tên công suất nguồn. TV3 xác nhận vùng riêng tư, quyền xem/xuất, lưu bao lâu và audit. TV4 đo test-stream và xem từ xa sau khi chọn thiết bị; hiện không có video/storage/PoE runtime evidence.
