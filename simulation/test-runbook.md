# Runbook kiểm thử TV1/TV3/TV4

**02/11/2026. Tất cả ca dưới là procedure/expected, chưa phải actual.** Lấy IP thực từ DHCP; các địa chỉ client dưới đây là mẫu theo inventory. Chuẩn bị mô phỏng theo [README](README.md), ghi version/model/hash, route và dịch vụ đã hoạt động. Mỗi ca ghi timestamp, IP/VLAN nguồn–đích, lệnh/thao tác, actual, ảnh/log và reviewer. Test bị lỗi phải retest trên đúng bản sau sửa.

## Kiểm nền trước TC01–TC06

Lưu ở router: `show ip interface brief`, `show ip route`, `show ip ospf neighbor`; Core/Aux `show ip access-lists`; Edge `show track`, `show ip sla statistics`, `show route-map`, `show ip nat statistics`; FW `show zone security`, `show zone-pair security`, `show policy-map type inspect zone-pair sessions` nếu platform hỗ trợ. Client: IP/mask/gateway/DNS/lease thực. Không chép output dự kiến làm log.

## TC01: cùng VLAN

Main-PC10-A/B lấy hai lease khác nhau trong 10.10.10.7–126/25, gateway10.10.10.1. Ping hai chiều; xem ARP và access VLAN, thử trên hai access switch nếu module TV2 có. Expected cùng VLAN liên lạc trực tiếp, không đi WAN/PAT. Giữ actual của hai nguồn riêng. Host khác VLAN hoặc IP trùng không được dùng làm bằng chứng TC01.

## TC02: liên VLAN có quyền

Main-PC10→Main-PC20 và ngược lại: ping; expected permit ICMP giữa10.10.10.0/25 và 10.10.20.0/25. Main-PC10 mở `http://10.10.70.11` hoặc `http://his.hospital.test`: expected trang HIS LAB. Main-PC30 mở PACS .12 và Main-PC40 mở LIS .13; PC10 không có quyền PACS11112/DB5432. Test cổng chỉ có ý nghĩa khi dịch vụ đích đã được bật hoặc có counter ACL chứng minh, không kết luận firewall đúng từ TCP timeout trên cổng chưa có listener. Lưu hit counter before/after tại Core và kết quả ứng dụng.

## TC03: Main↔cả hai Aux

Chạy đủ bốn chiều PC10 Main→DBP, DBP→Main, Main→BHTQ, BHTQ→Main. Ping và `tracert` trên PC-PT; trên IOS dùng `traceroute`. Expected đường Main-Core→Main-GW→đúng Aux, chiều về tương ứng; có OSPF route cụ thể. Traceroute có thể thiếu hop nếu công cụ/chính sách ICMP không trả TTL-exceeded; ghi hiện tượng và đối chiếu route, không tự bỏ ACL. Xem NAT trong lúc chạy: IP nội bộ không bị dịch. Ngắt từng leased line là ca lỗi riêng: site tương ứng mất kết nối, nhánh kia còn; không tuyên bố có VPN/tuyến dự phòng.

## TC04: DMZ nội bộ và công bố

Trước kiểm ngoài, Main-PC10 mở `http://10.10.80.10`, xác nhận service80 và route DMZ hoạt động. Từ **Web-Lab192.0.2.100** hoặc client trên Web-Access mở `http://198.51.100.2:8080`; expected cùng trang WebDMZ. Chụp PDU/translation tại Edge: destination public:8080 đổi thành 10.10.80.10:80; FW nhìn private sau DNAT. Kiểm session OUTSIDE→DMZ và reply ra ISP2. Negative: SSH22/DMZ .11/DB không được công bố, counter/drop phù hợp. Nội bộ dùng địa chỉ/DNS private, không test hairpin. Tắt ISP2 thì inbound service dự kiến mất; đây là giới hạn, không phải lỗi HA đã được thiết kế.

## TC05: guest bị chặn và đối chứng

Lặp cho Main-Guest, DBP-Guest, BHTQ-Guest. Trước mỗi lần, xác nhận PC10 ở cả ba site ping được từ nguồn nghiệp vụ có quyền; HIS HTTP hoạt động từ PC10. Từ guest ping PC10 local và hai site khác, thử HTTP tới HIS .70.11, DMZ .80.10, quản trị/NVR khi có listener; expected bị chặn. TCP negative dùng HIS80 đang hoạt động, không mặc định PC thường có Web server. Ghi đúng ACL `<SITE>-V100-IN`, counter deny trước/sau. Guest phải đồng thời lấy/renew DHCP, resolve `web.hospital.test`, mở `http://192.0.2.100` và hostname; expected được. Không có positive control thì ca chặn chưa đủ bằng chứng. Kiểm client isolation cùng SSID riêng với TV2; TC này chỉ chứng minh qua gateway IPv4.

## TC06: Internet tập trung

Mỗi PC10 Main/DBP/BHTQ và ba guest mở `http://192.0.2.100`, rồi `http://web.hospital.test`. Ghi cả thử IP và tên để tách lỗi DNS. Expected HTTP thành công, Aux qua leased line→Main-Core→FW→Edge, PAT theo egress. Main-PC10/DBP-PC10 ưu tiên ISP1; Main-PC20/BHTQ-PC10/GuestMain ưu tiên ISP2 khi cả hai tốt. Lưu NAT table, route-map/track và session FW. Không dùng một phiên để kết luận cân bằng tải50/50. Trong Simulation mode chụp source/destination IP/port tại client, gateway, Edge before/after và Web; giá trị cổng phải lấy từ actual.

## Ca bổ sung và đóng bản

[Dual ISP](../test_results/supplemental/dual-isp-failover.md): nhiều nguồn/phiên, lỗi local từng ISP, lỗi upstream khi local up, mất cả hai, phục hồi và Web health-target hỏng; ghi riêng phiên mới/cũ, thời gian đo và default thu hồi tại Aux. [DHCP/DNS](../test_results/supplemental/dhcp-dns.md), [VPN](../test_results/supplemental/vpn.md), [IDS/IPS](../test_results/supplemental/ids-ips.md), [persistence](../test_results/supplemental/persistence.md) có hồ sơ riêng.

Sau sửa NAT/ACL/routing phải retest các ca bị ảnh hưởng; không tái dùng ảnh có topology/hash cũ. `copy running-config startup-config`, lưu/đóng/mở project; kiểm lại TC01–TC06 và default/security sau mở. Ghi checksum bản cuối, dependency nếu GNS3 và mọi lỗi còn lại; TV1 chỉ duyệt khi có sản phẩm thực.
