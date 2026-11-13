# VPN liên site và teleworker

**TV3 phối hợp TV1; 02/11/2026. DESIGN ONLY / runtime NOT RUN.** Yêu cầu đề là đề xuất cả hai loại VPN; chưa có image hỗ trợ, certificate, client hoặc tài khoản để triển khai. Bộ config hợp nhất hiện giữ routed leased lines, chưa có crypto.

## Site-to-site: phương án route-based IPsec

| Tunnel dự trù | Underlay hiện có | Transit overlay đề xuất | Route và nguồn được bảo vệ |
| --- | --- | --- | --- |
| Main-GW↔DBP-GW | 10.255.0.1↔10.255.0.2 | 10.255.1.0/30, Main .1, DBP .2 | Subnet 10.10/16, 10.20/16, 10.30/16 thực sự được phép |
| Main-GW↔BHTQ-GW | 10.255.0.5↔10.255.0.6 | 10.255.1.4/30, Main .5, BHTQ .6 | Tương tự, mỗi nhánh qua Main |

`10.255.1.0/29` là **đề xuất dự trữ mới**, không phải interface/prefix đang hoạt động. Trước bật phải thêm vào IP plan và checker, kiểm không overlap VPN pool `10.255.100.0/24`. Chọn VTI + IKEv2 trên nền tảng hỗ trợ; chứng thư định danh từng peer, AES-GCM-256 cho ESP, DH/PFS group19 nếu cả hai đầu hỗ trợ. Proposal IKE cụ thể phải đối chiếu image; không đưa một bộ lệnh IOS XE mới vào 2911 rồi coi đã chạy. [Cisco IKEv2](https://www.cisco.com/c/en/us/td/docs/routers/ios-xe/security-vpn/security-vpn/m_sec-cfg-ikev2-flex.html) yêu cầu kiểm khả năng crypto của nền tảng.

Trình tự chuyển đổi: xác nhận reachability underlay; thiết lập certificate và IKE/IPsec; tạo VTI; chuyển adjacency OSPF liên site sang VTI và passive underlay để tránh bypass cleartext; giữ route trực tiếp tới peer ngoài tunnel; kiểm route cả hai chiều và ACL. Không giữ đồng thời đường OSPF ưu tiên cleartext rồi kết luận toàn bộ lưu lượng đã mã hóa. Không NAT trên leased lines. Nếu Aux↔Aux được duyệt, luồng đi qua Main phải decrypt rồi re-encrypt theo từng tunnel; không chỉ dùng selector Main↔Aux mà bỏ sót nguồn Aux còn lại.

Đo path MTU, thử packet lớn với DF và TCP; chọn MTU/MSS từ phép đo/overhead thực, không chốt 1400 cho mọi crypto. Đứt leased line vẫn làm mất VPN vì chưa có underlay dự phòng. IPsec không tạo thêm băng thông hoặc redundancy.

## Teleworker: kết thúc tại Main-FW

Endpoint công bố dự kiến dùng ISP2, không chạy trên Main-GW WAN private. Pool `10.255.100.2–10.255.100.254`, `.1` dự trữ; certificate gateway, tài khoản riêng và MFA/AAA. Chọn IKEv2 remote-access hoặc TLS VPN sau khi kiểm server/client tương thích. Nếu dùng IKEv2 phía sau Main-Edge, cần mapping/ACL UDP500/4500 đúng FW; **chưa thêm các rule đó vào baseline**. Không công bố RDP/SSH quản trị trực tiếp ra ngoài.

Split tunnel chỉ tới HIS/CRM đã duyệt; DNS/suffix và tuyến split được ghi trên client. Không cho teleworker tới DB, management, camera hoặc toàn bộ /16. Full tunnel là thay đổi thiết kế, phải tính lại Internet/NAT cho pool và quyền duyệt riêng.

| Thành phần cần bổ sung khi kích hoạt | Giá trị / điểm đặt |
| --- | --- |
| Route trả về pool tại Main-Core | `10.255.100.0/24` qua 10.255.0.14 |
| Route pool tại Main-Edge nếu cần chuyển tiếp | `10.255.100.0/24` qua 10.255.0.17 |
| Từ Aux tới pool | Chỉ quảng bá prefix pool nếu use case được duyệt, không redistribute toàn bộ static |
| ACL/VPN zone | Chỉ pool→HIS .11/CRM .14 TCP443; HTTP80 chỉ trong lab; deny DB/admin/camera |
| NAT exemption | Giữ source private cho pool↔internal; không để PAT trước khi mã hóa |
| Vòng đời | Tài khoản theo người, hết hạn, thu hồi certificate, log đăng nhập/thoát và session |
