# Nội dung TV3: server, DMZ và bảo mật

**Cập nhật 02/11/2026. Nội dung kỹ thuật và cấu hình tham chiếu đã soạn; chưa bàn giao có ký nhận/review, chưa kiểm IOS runtime. Người nhận/biên tập: TV5; người duyệt cuối: TV1.**

## Yêu cầu và phạm vi

Phần này phục vụ Step1–2 (vùng/dịch vụ), Step4 (cấu hình), Step5 (TC04/05/06) và Step6 (đánh giá). Yêu cầu bệnh viện gồm 10 server Main,2 mỗi Aux, tách Server Farm/DMZ, Internet tập trung, VPN site-to-site/teleworker, camera và an toàn mạng. Các vai trò server/phòng ban/port là thiết kế đề xuất. HTTP trong lab dùng dữ liệu giả, chưa phải HIS/RIS-PACS/LIS/CRM thực.

## Phân bổ server và dịch vụ

Main có 8 server nội bộ10.10.70.10–17 và 2 DMZ10.10.80.10–11; Aux có Infra .70.6 và Local .70.7. Tổng đúng 14; tăng trưởng làm tròn từng site12+3+3=18. Gateway Server Farm .70.1 tại Core/gateway; gateway DMZ .80.1 tại Main-FW. [Server plan](../../02-design/server-dmz-plan.md) có vai trò từng máy, DNS record, backup và giới hạn. NVR là appliance tách BOM, không cộng vào14 server ứng dụng.

Infra từng site cấp DHCP/DNS;18 pool cho nghiệp vụ/guest/staff theo [dhcp-pools.csv](../../../simulation/generated/dhcp-pools.csv). /25 dùng .7–.126 đủ 120 lease; guest /23 có 500 lease, staff /24 có 244. Đây là sức chứa địa chỉ, không chứng minh nhu cầu đồng thời hay khả năng AP. Guest dùng DNS Web-Lab bên ngoài; chỉ ngoại lệ DHCP tới đúng Infra, không mở Server Farm cho guest.

## Firewall, ACL và NAT

Luồng liên VLAN/liên site đi trực tiếp tại Core nên phải lọc tại gateway từng site. Các ACL inbound ràng buộc source subnet, mở DHCP/DNS đúng host, HIS/CRM theo role, PACS/LIS theo nhóm, deny mạng riêng rồi mới cho Web Internet. Guest bị chặn tới PC/server/DMZ/admin/camera/VPN cả ba site; client isolation cùng VLAN/SSID còn cần TV2. [Security policy](../../04-security/security-policy.md) định nghĩa quyền và hướng rule.

Main-FW dùng IOS ZBF ba vùng: LAN G0/0, OUTSIDE G0/1, DMZ G0/2. Inspect LAN→Internet, LAN→DMZ, OUTSIDE→WebDMZ và DMZ→Internet update; mặc định drop/log. Không có policy cho phiên mới OUTSIDE→LAN hoặc DMZ→LAN. FW không NAT. ACL east-west `established` chỉ kiểm bit ACK/RST; cần stateful segmentation/host firewall cho triển khai thật và bảo vệ app→DB cùng VLAN.

Main-Edge PAT cả ba site theo interface egress; loại NAT nội bộ10/8. Static PAT duy nhất `198.51.100.2:8080 → 10.10.80.10:80`. FW nhận địa chỉ private sau DNAT nên ACL match private80. DMZ có PBR ưu tiên ISP2 để reply cùng đường; chưa công bố ISP1 và chưa có inbound HA. ISP2 hỏng thì Web công bố mất dù outbound có thể qua ISP1. [NAT plan](../../04-security/nat-pat.md) giải thích source/destination/port và giới hạn hairpin.

Các source trong [configs/security](../../../configs/security/README.md) ghép bằng [build_lab.py](../../../scripts/build_lab.py) vào9 cấu hình router cuối. Không nạp base WAN sau file hợp nhất. Có5 switch tối thiểu hỗ trợ TV4, không thay thiết kế campus TV2.

## VPN, IDS/IPS, camera và vận hành

[VPN plan](../../04-security/vpn-plan.md) đề xuất VTI/IPsec IKEv2 trên hai leased lines, chuyển OSPF sang tunnel khi kích hoạt; teleworker kết thúc tại FW, pool10.255.100.0/24, MFA/certificate và quyền HIS/CRM tối thiểu. Route pool, NAT exemption, underlay/MTU/certificate phải kiểm; hiện chưa có crypto/SA/client, giữ DESIGN ONLY.

[IDS/IPS plan](../../04-security/ids-ips-plan.md) đề xuất sensor DMZ sau DNAT, IDS thụ động và IPS inline kiểm riêng bằng HTTP marker vô hại; cần EVE alert/verdict + positive control. Chưa có Suricata/rule validation/log thật; không coi ACL/ZBF là đã triển khai IDS/IPS. Chống phishing gồm mail/DNS/endpoint/MFA/đào tạo, chưa tích hợp sản phẩm.

[Camera plan](../../02-design/camera-plan.md) dùng VLAN110/NVR tại từng site, quyền admin và công thức bitrate/retention/PoE/RAID; số camera/codec/retention chưa khảo sát. Luồng local không tự cộng vào WAN/ISP. [Best practices](../../04-security/security-best-practices.md) quy định account, log/NTP, backup/restore, cập nhật và rollback. VTY hiện tắt; SSH/AAA/secrets vận hành chưa cấu hình.

## Kiểm chứng và giới hạn

`python3 scripts/verify.py` kiểm tính nhất quán cấu hình,61 flow ACL và hợp đồng ZBF/PAT/DHCP bằng mô hình tĩnh; **không chạy IOS, session stateful, DHCP lease hoặc HTTP**. Kết quả tại [hồ sơ kiểm tĩnh](../../../test_results/static/README.md). [TC04](../../../test_results/TC04-dmz/result.md), [TC05](../../../test_results/TC05-guest-isolation/result.md), [TC06](../../../test_results/TC06-internet-web/result.md) và SUPP02–04 đều NOT RUN. Runbook có negative/positive control; không tự ghi PASS, RTT hoặc NAT port.

Core/FW/Edge đơn là SPOF; VLAN70 có giao tiếp L2 không qua gateway; self-zone/IPv6 chưa harden; HA/WAF/VPN/IDS/IPS còn thiết kế. Chưa có reviewer xác nhận, chương trình kỹ sư tài năng chưa được chốt và chưa có báo giá/model cuối. TV5 phải giữ các giới hạn này khi đưa vào Step6.

## Bàn giao

Nội dung/bảng: server plan, security matrix, NAT before/after, VPN/IDS/camera/best practices. Config:9 router hợp nhất,5 switch tối thiểu,18 pool và mapping endpoint. TV4 cần dựng project, thử CLI, thu evidence và retest sau sửa. Ngày/người nhận/PR/reviewer chính thức: chưa có xác nhận; không thay bằng ngày hạn17/11.
