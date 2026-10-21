# Quy hoạch VLAN và địa chỉ IP

**Chủ trì:** TV1; TV2 đọc chéo. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU.

**Đề xuất, cần khóa sau khảo sát:** Main dùng khối `10.10.0.0/16`; DBP `10.20.0.0/16`; BHTQ `10.30.0.0/16`; WAN transit dành `10.255.0.0/24`. Các khối /16 là vùng địa chỉ dự trữ; chỉ tạo các subnet sử dụng bên dưới, không cấu hình đồng thời /16 trên interface LAN.

Phân bổ 6 nhóm Main × 100 PC và 3 nhóm mỗi Aux (90/90/80 PC) là giả định quản lý ban đầu. Tên nhóm là nhãn nghiệp vụ gợi ý, chưa phải danh sách phòng ban khảo sát được. VLAN gắn phòng ban; cổng access và SSID được map theo nhu cầu, không mặc định mỗi tầng là một phòng ban.

| Site | VLAN | Nhóm/vùng | Subnet/CIDR | Gateway | PC hiện tại → 5 năm |
| --- | --- | --- | --- | --- | --- |
| Main | 10 | Tiếp nhận/khám bệnh | `10.10.10.0/25` | `10.10.10.1` | 100 → 120 |
| Main | 20 | Điều trị/nội trú | `10.10.20.0/25` | `10.10.20.1` | 100 → 120 |
| Main | 30 | Chẩn đoán hình ảnh | `10.10.30.0/25` | `10.10.30.1` | 100 → 120 |
| Main | 40 | Xét nghiệm | `10.10.40.0/25` | `10.10.40.1` | 100 → 120 |
| Main | 50 | Dược/nghiệp vụ | `10.10.50.0/25` | `10.10.50.1` | 100 → 120 |
| Main | 60 | Hành chính/điều hành | `10.10.60.0/25` | `10.10.60.1` | 100 → 120 |
| Main | 70 | Server Farm | `10.10.70.0/27` | `10.10.70.1` | Dự kiến 8/10 server Main |
| Main | 80 | DMZ | `10.10.80.0/27` | `10.10.80.1` | Dự kiến 2/10 server Main |
| Main | 90 | Quản trị thiết bị | `10.10.90.0/24` | `10.10.90.1` | Theo BOM |
| Main | 100 | Wi-Fi khách | `10.10.100.0/23` | `10.10.100.1` | Chưa có số lượng khách |
| Main | 110 | Camera/NVR | `10.10.110.0/24` | `10.10.110.1` | Theo khảo sát |
| Main | 120 | Wi-Fi nhân viên | `10.10.120.0/24` | `10.10.120.1` | Chưa có số lượng thiết bị riêng |
| DBP | 10 | Nghiệp vụ 1 | `10.20.10.0/25` | `10.20.10.1` | 90 → 108 |
| DBP | 20 | Nghiệp vụ 2 | `10.20.20.0/25` | `10.20.20.1` | 90 → 108 |
| DBP | 30 | Nghiệp vụ 3 | `10.20.30.0/25` | `10.20.30.1` | 80 → 96 |
| DBP | 70 | Server cục bộ | `10.20.70.0/28` | `10.20.70.1` | 2 → 3 server |
| DBP | 90 | Quản trị thiết bị | `10.20.90.0/24` | `10.20.90.1` | Theo BOM |
| DBP | 100 | Wi-Fi khách dự kiến | `10.20.100.0/23` | `10.20.100.1` | Xác nhận phạm vi phủ sóng |
| DBP | 110 | Camera/NVR | `10.20.110.0/24` | `10.20.110.1` | Theo khảo sát |
| DBP | 120 | Wi-Fi nhân viên | `10.20.120.0/24` | `10.20.120.1` | Theo khảo sát |
| BHTQ | 10 | Nghiệp vụ 1 | `10.30.10.0/25` | `10.30.10.1` | 90 → 108 |
| BHTQ | 20 | Nghiệp vụ 2 | `10.30.20.0/25` | `10.30.20.1` | 90 → 108 |
| BHTQ | 30 | Nghiệp vụ 3 | `10.30.30.0/25` | `10.30.30.1` | 80 → 96 |
| BHTQ | 70 | Server cục bộ | `10.30.70.0/28` | `10.30.70.1` | 2 → 3 server |
| BHTQ | 90 | Quản trị thiết bị | `10.30.90.0/24` | `10.30.90.1` | Theo BOM |
| BHTQ | 100 | Wi-Fi khách dự kiến | `10.30.100.0/23` | `10.30.100.1` | Xác nhận phạm vi phủ sóng |
| BHTQ | 110 | Camera/NVR | `10.30.110.0/24` | `10.30.110.1` | Theo khảo sát |
| BHTQ | 120 | Wi-Fi nhân viên | `10.30.120.0/24` | `10.30.120.1` | Theo khảo sát |

| Kết nối | Subnet | Đầu Main | Đầu chi nhánh |
| --- | --- | --- | --- |
| Leased line 1 Main-DBP | `10.255.0.0/30` | `10.255.0.1` | `10.255.0.2` |
| Leased line 2 Main-BHTQ | `10.255.0.4/30` | `10.255.0.5` | `10.255.0.6` |

TV1 cấp riêng các subnet transit core/firewall/edge và VPN pool trong vùng chưa dùng trước khi tích hợp; không lấy địa chỉ từ pool DHCP của người dùng. Hai /30 trên mô tả handoff logic; topology có PE/CE cần thêm subnet riêng cho từng đoạn thực tế.

- Mask: `/25 = 255.255.255.128`, `/27 = 255.255.255.224`, `/28 = 255.255.255.240`, `/24 = 255.255.255.0`, `/23 = 255.255.254.0`, `/30 = 255.255.255.252`.
- VLAN PC /25 có 126 địa chỉ host: dự trữ `.1-.6` cho gateway/HA và hạ tầng, DHCP `.7-.126` có **120 địa chỉ**, đủ nhóm lớn nhất Main sau tăng trưởng. Không dành thêm IP tĩnh trong pool này mà không tính lại sức chứa.
- /27 có 30 host, /28 có 14 host. Server IP tĩnh ở vùng server; không dùng DHCP cấp ngẫu nhiên cho server. Wi-Fi /23 có 510 host, còn 509 sau một gateway; khả năng đáp ứng phải kiểm lại theo **số thiết bị đồng thời**, lease và dự phòng hạ tầng.
- Thiết bị Wi-Fi nhân viên đã nằm trong thống kê workstation không được tính tải hai lần. Điện thoại, tablet, thiết bị y tế, camera và khách ngoài thống kê cần được ghi riêng. Nếu vượt sức chứa, chia thêm subnet từ khối dự trữ và cập nhật ACL, DHCP, OSPF cùng lúc.

## Theo dõi cập nhật

- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
