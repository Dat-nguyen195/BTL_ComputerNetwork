# Cấu hình thiết bị

Mỗi site lưu một file text cho từng node, ví dụ `MAIN-WAN-R1.cfg`; tên node phải khớp mô phỏng. Hiện chưa có cấu hình triển khai.

Mỗi lần bàn giao ghi: node/model, phiên bản phần mềm, interface mapping, VLAN/IP, thứ tự nạp và test liên quan. TV1 phụ trách routing/edge, TV2 LAN/Wi-Fi, TV3 firewall/NAT/server/VPN; TV4 ghép và kiểm.

Chỉ dùng secret lab minh họa đã ghi rõ; không commit mật khẩu thật. Lưu running/startup config phù hợp, kiểm persist sau mở lại. Thay đổi IP/ACL/route phải cập nhật thiết kế và retest.
