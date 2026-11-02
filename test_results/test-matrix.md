# Ma trận kiểm thử - Step 5

**TV4 điều phối; 02/11/2026. Runtime: tất cả NOT RUN; chưa có project.** Đã có cấu hình, precondition, nguồn/đích mẫu và [runbook chi tiết](../simulation/test-runbook.md). Địa chỉ client là ví dụ, phải ghi lease thực trong actual.

| ID | Nguồn → đích / dịch vụ | Expected chính | Chuẩn bị | Trạng thái | Hồ sơ |
| --- | --- | --- | --- | --- | --- |
| TC01 | Main-PC10-A ↔ PC10-B, ICMP | Cùng VLAN10 liên lạc hai chiều | TV2 | NOT RUN | [result](TC01-same-vlan/result.md) |
| TC02 | Main-PC10 ↔ PC20; PC10→HIS80 | ICMP/HTTP được phép; DB không mở cho client | TV2/TV3 | NOT RUN | [result](TC02-inter-vlan/result.md) |
| TC03 | PC10 Main ↔ DBP và Main ↔ BHTQ | Đủ4 chiều, đúng OSPF/WAN, không NAT nội bộ | TV1 | NOT RUN | [result](TC03-inter-site/result.md) |
| TC04 | PC10→DMZ80; Web-Lab→ISP2:8080 | HTTP qua PAT/ZBF; reply ISP2; cổng khác bị chặn | TV3/TV1 | NOT RUN | [result](TC04-dmz/result.md) |
| TC05 | Guest mỗi site→PC cả 3 site/HIS80; đối chứng DNS/DHCP/Web | Nội bộ bị chặn và có counter; dịch vụ cấp mạng/Internet khách vẫn dùng | TV3/TV2 | NOT RUN | [result](TC05-guest-isolation/result.md) |
| TC06 | PC10 + Guest của cả 3 site→Web-Lab IP/tên | HTTP qua Main, DNS đúng, PAT theo egress | TV4/TV1/TV3 | NOT RUN | [result](TC06-internet-web/result.md) |
| SUPP-01 | Nhiều nguồn/phiên, từng ISP/local/upstream/both/recovery | Track/PBR/default đúng; đo phiên cũ/mới; không cam kết50/50 | TV1/TV3 | NOT RUN | [dual ISP](supplemental/dual-isp-failover.md) |
| SUPP-02 | Client mỗi pool→DHCP/DNS; renew | Đúng18 pool/gateway/DNS; không trùng IP | TV3/TV2 | NOT RUN | [DHCP/DNS](supplemental/dhcp-dns.md) |
| SUPP-03 | VPN Main↔Aux, teleworker→HIS/CRM | SA/crypto, least privilege, thu hồi account; hiện DESIGN ONLY | TV3/TV1 | NOT RUN | [VPN](supplemental/vpn.md) |
| SUPP-04 | Marker HTTP DMZ + positive control | IDS alert/IPS drop có EVE/verdict; hiện DESIGN ONLY | TV3/TV4 | NOT RUN | [IDS/IPS](supplemental/ids-ips.md) |
| SUPP-05 | Startup/project sau save/close/reopen | Cấu hình persist, smoke6 nhóm, hash đúng | TV4 | NOT RUN | [Persistence](supplemental/persistence.md) |

Trạng thái runtime dùng NOT RUN/PASS/FAIL/BLOCKED; capability design ghi riêng DESIGN ONLY/MODELED. Mỗi actual phải có run ID, thời điểm/người chạy, công cụ/version, project/hash, nguồn/đích, lệnh, output và ảnh/log. Test FAIL sửa rồi retest; test chưa chạy không gán PASS. [Kiểm tra tĩnh](static/README.md) có báo cáo riêng, không thay sáu nhóm bắt buộc.
