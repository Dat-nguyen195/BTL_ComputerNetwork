# Module TV3: server, ACL, firewall và NAT

**02/11/2026. Cấu hình tham chiếu đã có; chưa tạo module project/runtime.**

Nguồn: [server plan](../../../docs/02-design/server-dmz-plan.md), [policy](../../../docs/04-security/security-policy.md), [NAT](../../../docs/04-security/nat-pat.md). [build_lab.py](../../../scripts/build_lab.py) ghép routing TV1 với ACL/relay tại Core/Aux, [ZBF overlay](../../../configs/security/main-fw-policy.inc) tại Main-FW và [PAT overlay](../../../configs/security/main-edge-dmz.inc) tại Edge. File cuối: [generated/configs](../../generated/configs/); không paste `.inc` vào node sai hoặc nạp thêm base sau cùng.

Main-FW IOS có ba vùng LAN/OUTSIDE/DMZ, không NAT. Main-Edge PAT hai egress và static PAT ISP2:8080→10.10.80.10:80. ACL nguồn tại từng gateway ngăn guest vượt liên VLAN/liên site; ZBF không nhìn thấy luồng east-west đi trực tiếp tại Core. VPN/IDS/IPS còn DESIGN ONLY.

TV4 dựng node/link/port theo [hướng dẫn tổng](../../README.md), nhập [DHCP pools](../../generated/dhcp-pools.csv), IP/dịch vụ theo [endpoints](../../lab/endpoints.csv), bật HTTP/DNS bằng dữ liệu giả. `.10/.11` ở client là mẫu, phải ghi lease thật, tránh IP tĩnh trùng pool.

Trình tự: kiểm `python3 scripts/verify.py`; nạp routing+security hợp nhất; kiểm neighbor/route; bật dịch vụ; positive HTTP/DHCP/DNS; negative guest/DMZ; NAT đúng egress; dual ISP; save/reopen. Chi tiết từng lệnh/bằng chứng trong [runbook](../../test-runbook.md). `show ip access-lists`, bảng NAT và ZBF sessions phải đi cùng kết quả ứng dụng.

Không lưu credential thật; VTY hiện tắt. Image/model hỗ trợ ZBF/NAT/PBR cần thử thực tế. Bàn giao chính thức cần người nhận, version/hash project, lỗi CLI và evidence TC04/05/06; chưa có chữ ký nhận hoặc PASS runtime.
