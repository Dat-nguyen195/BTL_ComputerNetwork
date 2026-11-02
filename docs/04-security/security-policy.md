# Chính sách bảo mật và điểm đặt rule

**TV3; cập nhật 02/11/2026. CÓ CẤU HÌNH THAM CHIẾU; runtime NOT RUN.** Danh sách phòng ban là giả định; cần bệnh viện duyệt quyền trước triển khai thật.

## Vùng, địa chỉ và trách nhiệm thực thi

Main-Core và gateway Aux định tuyến liên VLAN trực tiếp. Vì vậy chỉ đặt firewall ở Main-FW sẽ bỏ sót luồng PC→server nội bộ và luồng liên site. [Cấu hình hợp nhất](../../simulation/generated/configs/) đặt ACL **inbound** tại `GigabitEthernet0/0.<VLAN>` ở cả ba site; chuyển thành `interface Vlan<VLAN>` nếu TV2 dùng switch L3. Main-FW dùng IOS Zone-Based Firewall (ZBF): G0/0=LAN, G0/1=OUTSIDE, G0/2=DMZ. Main-Edge giữ NAT/PBR.

| Phạm vi | Nguồn | Đích / dịch vụ khởi tạo | Kết quả / nơi áp |
| --- | --- | --- | --- |
| Cấp mạng | Client VLAN10–60/100/120 theo site | DHCP broadcast UDP68→67; renew tới Infra cùng site UDP68→67 | Permit trước deny private, ACL client |
| DNS nhân viên | VLAN nghiệp vụ/Staff | Infra cùng site TCP/UDP53 | Permit đúng host |
| DNS khách | Guest100 mỗi site | Web-Lab 192.0.2.100 TCP/UDP53 | Permit; không được dùng DNS nội bộ |
| HIS, CRM | Tất cả VLAN nghiệp vụ/Staff | 10.10.70.11 và .14 TCP80/443 | Permit theo IP/port; 80 là dịch vụ lab |
| PACS | Main VLAN30, Aux VLAN10 | 10.10.70.12 TCP80/11112 | 80 thay thế; DICOM11112 chỉ dự trù |
| LIS | Main VLAN40, Aux VLAN20 | 10.10.70.13 TCP80/443 | Permit |
| DMZ nội bộ | Nghiệp vụ/Staff | 10.10.80.10 TCP80 | ACL client + LAN→DMZ inspect |
| Kiểm liên VLAN/site | Main10/Main20/DBP10/BHTQ10 | ICMP giữa bốn subnet /25 này | Permit hai chiều; các PC khác theo policy |
| Guest cách ly | Guest cả ba site | PC/server/DMZ/quản trị/camera/VPN ở mọi site | Deny RFC1918; chỉ ngoại lệ DHCP nói trên |
| Internet | Nghiệp vụ/Staff/Guest theo subnet thật | TCP80/443; ICMP tới Web-Lab | ACL client; LAN→OUTSIDE inspect; PAT tại Edge |
| Quản trị | Chỉ Main-Admin 10.10.90.11 | Mạng riêng; DMZ chỉ SSH22 | ACL MGMT; LAN→DMZ; SSH hiện chưa bật |
| Internet→DMZ | Client ngoài, ví dụ Web-Lab | 198.51.100.2:8080 → 10.10.80.10:80 | Static PAT + OUTSIDE→DMZ inspect |
| Internet→LAN | Phiên mới từ ngoài | Mọi host LAN/Server Farm | Không có zone-pair khởi tạo; drop |
| DMZ→LAN | Phiên mới từ DMZ | LAN/DB | Không có zone-pair; drop; chỉ trả lời phiên được inspect |
| Camera/NVR | VLAN110 | NTP tới 10.10.70.17; trả lời admin | ACL CAMERA; không ra Internet |
| Infra/Server | DHCP/DNS đúng host; server subnet | DHCP/DNS reply, TCP ACK/RST, ICMP echo-reply; update HTTP/S; NTP/syslog tới Monitor | ACL SERVER; backup Aux .70.7→Main .70.16 TCP22 dự trù |
| Teleworker | VPN pool 10.255.100.0/24 | HIS/CRM theo vai trò | DESIGN ONLY; chưa bật permit cho pool |

Từ chối các kết nối không liệt kê. Internet permit nằm **sau** deny các mạng riêng; mọi permit client đều ràng buộc source subnet để hạn chế giả mạo IP khác VLAN. DHCP ban đầu là ngoại lệ source `0.0.0.0`. Không xem ACL chọn NAT 100 hoặc ACL chọn PBR 101/102 là quyền truy cập.

## Rule order và các điểm phải đọc đúng

`<SITE>-V<VLAN>-IN`: DHCP → DNS đúng host → ứng dụng/ICMP được duyệt → deny mạng riêng/link-local → Web Internet/ICMP Web-Lab → deny all log. `<SITE>-SERVER-IN`: DHCP/DNS reply → TCP established/ICMP reply → dịch vụ do server được phép khởi tạo → deny private → cập nhật HTTP/S → deny all. `<SITE>-MGMT-IN`: chỉ admin Main được khởi tạo; Aux cho trả lời admin. `<SITE>-CAMERA-IN`: trả lời admin và NTP; deny phần còn lại.

ACL `established` chỉ kiểm bit ACK/RST, **không có bảng trạng thái phiên**; không dùng nó thay firewall cho mạng bệnh viện thật. Main-FW dùng `inspect` để theo dõi phiên đi qua từng cặp vùng; mặc định drop có log. Theo [Cisco ZBF](https://www.cisco.com/c/en/us/support/docs/security/ios-firewall/98628-zone-design-guide.html), zone-pair có hướng; `inspect` theo dõi trả lời, còn `pass` cần chính sách chiều ngược. Bản này dùng inspect, không tạo rule `permit ip any any` giữa các vùng.

ZBF không bảo vệ luồng cùng VLAN hoặc tự bảo vệ đầy đủ self-zone. VTY ở bộ lab tắt, HTTP quản trị tắt; SSH/AAA cần cấu hình riêng sau khi có tài khoản/certificate. Chưa cấu hình IPv6; phải giữ guest ở IPv4 trong lab hoặc bổ sung chính sách IPv6 tương đương trước bật dual-stack. Client isolation trên cùng SSID/VLAN là việc của AP/switch TV2; ACL router không ngăn hai guest cùng broadcast domain.

## Kiểm chứng và thay đổi

`python3 scripts/check_security.py` kiểm các flow đầu vào ở [security-cases.csv](../../test_results/static/security-cases.csv), first-match ACL, binding/hướng, pool và hợp đồng ZBF/PAT. Đây là kiểm tĩnh, không tạo session IOS. TV4 chạy [TC02](../../test_results/TC02-inter-vlan/result.md), [TC04](../../test_results/TC04-dmz/result.md), [TC05](../../test_results/TC05-guest-isolation/result.md), [TC06](../../test_results/TC06-internet-web/result.md); lưu `show ip access-lists`, `show policy-map type inspect zone-pair sessions`, bảng NAT và ứng dụng. Một ping thất bại không đủ chứng minh deny nếu đích chưa hoạt động.

Sau mỗi sửa rule: build lại, kiểm tĩnh, chạy lại ca cho phép/chặn bị ảnh hưởng, ghi hash và reviewer thật. Không có chữ ký reviewer hoặc PASS runtime ở thời điểm này.
