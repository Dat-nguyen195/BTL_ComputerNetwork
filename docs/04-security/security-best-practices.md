# Hướng dẫn vận hành bảo mật

**TV3; 02/11/2026. Hướng dẫn đề xuất; chỉ ACL/ZBF/NAT/relay đã có cấu hình tham chiếu. Chưa nghiệm thu runtime.**

| Hạng mục | Cách thực hiện / tiêu chí kiểm | Tình trạng baseline |
| --- | --- | --- |
| Quản trị | Console lab; khi bật SSH dùng account riêng/AAA, SSHv2, khóa phù hợp image, VTY chỉ admin 10.10.90.11; thử login được phép và từ chối | VTY tắt; chưa có SSH/AAA/account |
| Secrets | Khóa/certificate/backup nhạy cảm ở kho bí mật; dùng secret hash được nền tảng hỗ trợ; không ghi password thật vào repo/ảnh | Bộ tham chiếu không chứa credential vận hành |
| Phân đoạn | ACL in trên gateway cả ba site; DMZ80 ở FW; kiểm guest tới host đang chạy và positive DNS/DHCP/Web | Có config; chưa chạy |
| L2/Wi-Fi | Access/trunk tường minh, tắt cổng dư, giới hạn VLAN; DHCP snooping/DAI/BPDU Guard nếu hỗ trợ; SSID guest isolation; Enterprise cho staff | TV2 triển khai/đọc chéo |
| Log/NTP | Main-Monitor 10.10.70.17, thời gian đồng nhất; giới hạn log deny và retention sau đo; không thu thông tin bệnh nhân | Dịch vụ/khả năng công cụ chưa kiểm |
| Sao lưu | Lưu running/startup, lưu project; bản backup cấu hình và DB tách quyền; thử restore trên lab trước duyệt | Quy trình đã soạn, chưa restore |
| Cập nhật | Theo dõi vendor, thử bản vá trong lab, ghi image/version/hash và rollback; kiểm license khi chọn thiết bị | Chưa chọn image/model cuối |
| VPN | MFA, quyền theo vai trò, thu hồi account/certificate; route/NAT exemption và MTU; không mở toàn mạng cho pool | DESIGN ONLY |
| Mail/Web | Lọc mail/DNS/URL, MFA, cập nhật endpoint, đào tạo nhận diện phishing | DESIGN ONLY |
| Camera | NVR từng site, VLAN110, account riêng, cấm Internet trực tiếp; quyền xem/xuất theo vai trò và log | DESIGN ONLY về ứng dụng/PoE |
| Server | HTTPS/certificate, host firewall, DB chỉ app cần thiết, service account tối thiểu; tách app/DB khi cần | HTTP chỉ là lab; app→DB cùng VLAN cần host policy |
| IPv6 | Bổ sung policy tương đương trước bật dual-stack; kiểm đường tránh ACL IPv4 | Lab hiện IPv4 |

## Nạp và rollback có kiểm soát

1. Chạy `python3 scripts/build_lab.py` rồi `python3 scripts/verify.py`; xem diff các file hợp nhất và manifest. Không nạp các file base WAN sau file hợp nhất làm mất policy.
2. Chụp/lưu cấu hình trước đổi, commit/hash và phiên bản project. Dùng console, giữ bản lab phục hồi riêng. Mật khẩu/serial/key phải được che trước lưu evidence.
3. Nạp đúng hostname/model/interface; không paste IOS vào ASA. Kiểm CLI lỗi ngay, chưa lưu đè bản tốt nếu thiếu lệnh. Nếu Packet Tracer không hỗ trợ ZBF/NAT route-map/PBR/IP SLA, ghi BLOCKED cho tính năng và chuyển môi trường có image hợp pháp.
4. Kiểm luồng được phép trước, luồng bị chặn sau; TC04/05/06 và ca dual ISP có thể bị ảnh hưởng bởi mọi đổi NAT/ACL. Không bỏ firewall để đạt ping rồi kết luận bảo mật đạt.
5. Nếu lỗi: trở lại project/startup snapshot trước đổi bằng console; kiểm route, DHCP/DNS/Web và guest isolation. Ghi lỗi, phiên bản trước/sau, người sửa và test chạy lại.
6. Khi ổn định: `copy running-config startup-config`, lưu project, đóng/mở lại, chạy smoke test; TV4 lưu log persistence/hash. Chỉ người được phân công mới xác nhận review/duyệt.

## Sự cố và hồ sơ

Deny bất thường: xác định nguồn/đích/thời điểm, kiểm DHCP/VLAN/route trước ACL, đối chiếu hit counter và session. Không bật debug packet toàn mạng khi chưa kiểm tác động. Sự cố nghi ngờ account: cô lập tài khoản, giữ log cần thiết, thay khóa/certificate và kiểm truy cập sau thu hồi. Không tự gửi dữ liệu mạng bệnh viện ra dịch vụ công cộng.

Trước bàn giao: rà credential/key trong text và ảnh; đối chiếu topology–IP–config–test; ghi mọi hạn chế còn lại trong contribution. Bản này không chứng nhận tuân thủ pháp lý hoặc HA. Nghiệm thu theo [test matrix](../../test_results/test-matrix.md) và [approval](../../submission/approval.md).
