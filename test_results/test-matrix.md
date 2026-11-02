# Ma trận kiểm thử - Step5

**Runtime GNS3 Linux/FRR đã chạy và mở lại project ngày02/11/2026.** [Evidence đầy đủ](runtime/README.md). Config IOS/Packet Tracer vẫn là tham chiếu chưa chạy; mỗi PASS dưới đây chỉ áp dụng mô hình GNS3 này.

| ID | Nội dung | Kết quả GNS3 | Hồ sơ |
| --- | --- | --- | --- |
| TC01 | Main-PC10-A↔B cùng VLAN | PASS | [result](TC01-same-vlan/result.md) |
| TC02 | PC10↔PC20 và PC10→HIS80 | PASS | [result](TC02-inter-vlan/result.md) |
| TC03 | Main↔DBP/Main↔BHTQ hai chiều, thêm Aux↔Aux và traceroute | PASS | [result](TC03-inter-site/result.md) |
| TC04 | HTTP nội bộ→DMZ, ngoài→ISP2:8080, cổng khác không công bố | PASS | [result](TC04-dmz/result.md) |
| TC05 | Guest cả ba site bị chặn tới PC/LAN/HIS/DMZ; Web/DNS vẫn dùng; counters DROP | PASS | [result](TC05-guest-isolation/result.md) |
| TC06 | PC/Guest cả ba site→Web-Lab theo tên | PASS | [result](TC06-internet-web/result.md) |
| SUPP01 | PBR hai nhóm, lỗi upstream ISP1/ISP2/cả hai và phục hồi | PASS trong phạm vi đã thử; local-link/session cũ chưa thử | [dual ISP](supplemental/dual-isp-failover.md) |
| SUPP02 |19 client lấy lease trên đủ18 pool, gateway/DNS/ACK đúng | PASS | [DHCP/DNS](supplemental/dhcp-dns.md) |
| SUPP03 | VPN site-to-site và teleworker | DESIGN ONLY / NOT RUN | [VPN](supplemental/vpn.md) |
| SUPP04 | Suricata IDS alert, IPS drop mẫu HTTP và positive control | PASS rule mẫu; chưa benchmark/feed tấn công thật | [IDS/IPS](supplemental/ids-ips.md) |
| SUPP05 | Chép đúng template, save/close/reopen và chạy lại137 kiểm | PASS | [persistence](supplemental/persistence.md) |

Không suy PASS RF, quang, DSL, throughput, HA hoặc dữ liệu y tế từ những ca trên. Hai FAIL của lần đầu được giữ trong `runtime/initial-runtime/`; run sau đo hội tụ đầu cuối và lưu samples gián đoạn. Không có kiểm tra nào tự tạo approval hoặc biên nhận BKeL.
