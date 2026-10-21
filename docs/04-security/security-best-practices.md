# Hướng dẫn thực hành bảo mật

**Chủ trì:** TV3. **Trạng thái:** BASELINE / CHƯA NGHIỆM THU.

- [ ] Quản trị SSH/AAA và tài khoản riêng, phân quyền tối thiểu; tắt Telnet/dịch vụ không cần.
- [ ] Đổi secret mặc định; chỉ lưu dữ liệu lab minh họa, không lưu mật khẩu thật.
- [ ] Tắt cổng không dùng, cấu hình access/trunk tường minh theo thiết bị hỗ trợ.
- [ ] Tách guest/server/DMZ/quản trị/camera và kiểm ACL đúng hướng.
- [ ] Wi-Fi nhân viên dùng cơ chế Enterprise phù hợp; khách có client isolation khi hỗ trợ.
- [ ] Syslog/NTP, giám sát, backup/restore và lưu cấu hình có phiên bản.
- [ ] Cập nhật phần mềm, lọc mail/web/DNS và hướng dẫn chống phishing.
- [ ] VPN theo vai trò, không mở toàn bộ LAN cho teleworker.
- [ ] Kiểm firewall/IDS/IPS và throughput ở cấu hình thực, không chỉ tốc độ cổng.
- [ ] Kiểm quyền truy cập camera/NVR, thời gian lưu và quy định riêng tư.

Checklist chưa xác nhận triển khai; bằng chứng liên kết trong test matrix và supplemental khi có.


## Theo dõi cập nhật

- [ ] Xác nhận giả định và thông số với người phụ trách.
- [ ] Cập nhật kết quả triển khai/bằng chứng thực tế.
- [ ] Ghi reviewer, ngày rà soát và quyết định vào issue/PR liên quan.
