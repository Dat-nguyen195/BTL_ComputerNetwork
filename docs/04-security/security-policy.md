# Ma trận chính sách bảo mật

**Chủ trì:** TV3. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU.

| Nguồn | Đích | Dịch vụ | Chính sách dự kiến |
| --- | --- | --- | --- |
| PC nghiệp vụ | VLAN khác | Theo nhu cầu nghiệp vụ | Chỉ permit luồng được duyệt |
| PC được cấp quyền | Server Farm | Dịch vụ bệnh viện cần dùng | Permit theo vai trò |
| Guest | PC/server/quản trị ở mọi site | Mọi dịch vụ | Deny và ghi hit/log |
| Guest | DHCP/DNS hợp lệ | Dịch vụ cấp mạng | Permit giới hạn đúng đích |
| Guest / PC | Web Internet | Dịch vụ được phép | Qua Main, PAT và firewall |
| Internet | DMZ | Cổng công bố | Permit theo static PAT và firewall |
| Internet | LAN/Server Farm | Mọi dịch vụ ngoài VPN được cấp | Deny |
| Quản trị được cấp | Thiết bị/NVR | SSH/quản trị theo nền tảng | Permit theo quyền |
| Teleworker VPN | LAN cần thiết | Theo vai trò | Permit tối thiểu, không mở toàn bộ LAN |

Đây là chính sách thiết kế; chưa có ACL/firewall chạy thực tế. Điền interface/hướng đặt ACL và rule order trước test. TC05 cần negative test và positive control, không chỉ một ping thất bại.


## Theo dõi cập nhật

- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
