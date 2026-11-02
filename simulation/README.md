# Mô phỏng ba site: gói cấu hình và cách tái hiện

**TV4 điều phối; cập nhật 02/11/2026. CÓ GÓI THAM CHIẾU, CHƯA CÓ PROJECT `.pkt`/GNS3 HOẶC RUNTIME EVIDENCE.** Môi trường hiện tại có Python3/Docker nhưng không tìm thấy executable Packet Tracer/GNS3/Dynamips hoặc IOS image. Không tạo file đổi đuôi giả làm mô phỏng.

| Thành phần | Đã chuẩn bị | Trạng thái |
| --- | --- | --- |
| Routing/Internet | 9 cấu hình IOS hợp nhất với WAN/OSPF/PBR/IP SLA/PAT | Kiểm tĩnh đạt; IOS parser chưa chạy |
| Security | ACL gateway ba site, ZBF ba vùng, static PAT DMZ ISP2 | Có config; session/runtime chưa chạy |
| Switch đại diện | 5 cấu hình 2960, VLAN/trunk/access, port map | Có config; không thay campus thật của TV2 |
| Đầu cuối | 30 mục: 14 server bệnh viện, 1 Web ngoài, 11 client mẫu, 1 admin, 3 NVR dự trù | Có địa chỉ/mapping; chưa tạo node |
| DHCP | 18 pool tại Infra Main/DBP/BHTQ | Có bảng nhập Services; chưa có lease |
| Project/version/model/image | Chưa có | Cần TV4 dựng và ghi version/model thực |
| VPN/IDS/IPS/HA | Kế hoạch và ca kiểm thử | DESIGN ONLY |
| Persistence / checksum project | Chưa có project | NOT RUN |

## Dựng lab và nạp cấu hình

1. Chạy `python3 scripts/build_lab.py`, rồi `python3 scripts/verify.py` từ repo root. [manifest.json](generated/manifest.json) chứa SHA256 của cấu hình/bảng **tham chiếu**, không phải checksum mô phỏng. Sửa source trong `configs/`, `scripts/build_lab.py`, `lab/`; không sửa tay file generated rồi bỏ qua build.
2. Kiểm khả năng theo [capability matrix](capability-matrix.md). Mục không nhận lệnh phải ghi lỗi/phiên bản. Dùng Packet Tracer nếu đủ tính năng cần chứng minh; nếu không, chọn GNS3 với image hợp pháp hỗ trợ. Không âm thầm bỏ IP SLA/ZBF để đóng ca PASS.
3. Tạo 9 router theo [module WAN](modules/tv1-wan/README.md), 5 switch lab, các endpoint cần kiểm. Router tham chiếu2911, switch2960; ba WAN gateway cần Serial module. Mỗi model khác phải cập nhật interface mapping và build source tương ứng. Main-GW là đầu DCE dự kiến; kiểm `show controllers serial` trước giữ clock rate.
4. Nối theo [cabling.csv](lab/cabling.csv). Main LAN trunk không có VLAN80; DMZ switch nối Main-FW G0/2, Web switch nối INET-Core G0/2. [switch-ports.csv](generated/switch-ports.csv) chỉ rõ access port và VLAN từng endpoint. Một switch đại diện/site không phải thiết kế đáp ứng 600/260 PC.
5. Nạp **cấu hình hợp nhất** trong [generated/configs](generated/configs/) đúng hostname, nạp switch trong [generated/switches](generated/switches/). Có các block interface lặp để bổ sung ACL/zone sau routing; không bỏ đoạn cuối. Không nạp lại base WAN sau cùng. Không paste IOS ZBF vào ASA.
6. Thứ tự kiểm: INET-Core/ISP1/ISP2/Web → Edge → FW/Core → WAN/Aux → switch → server/client. Dùng console; VTY tắt. Chạy `show ip interface brief`, ping từng link, `show ip ospf neighbor`, `show ip route`. Ba adjacency mong đợi: Core–Main-GW, Main-GW–DBP, Main-GW–BHTQ.
7. Tạo server tĩnh theo [endpoints.csv](lab/endpoints.csv), dịch vụ/DNS theo [server plan](../docs/02-design/server-dmz-plan.md), DHCP theo [18 pool](generated/dhcp-pools.csv). Web-Lab `.100/26`, gateway `.65`, bật HTTP/DNS/ICMP. HTTP HIS/PACS/LIS/CRM chỉ là trang stand-in. Main-DB không bật HTTP. NVR/cache/proxy là nhãn thiết kế, không tự coi đã có ứng dụng.
8. Client lấy DHCP, ghi **lease thật** vào evidence. Các IP `.10/.11` trong inventory là ví dụ, không bảo đảm DHCP cấp đúng giá trị đó. Nếu dùng IP tĩnh nằm trong pool để smoke test, giữ DHCP tắt cho pool đó; chuyển lại DHCP và bỏ IP tĩnh trước test nhiều client để tránh trùng. Không giảm pool /25 vốn cần đủ 120 lease để dành IP test lâu dài.
9. Chạy [runbook](test-runbook.md), điền actual và evidence theo đúng bản. Các ca bảo mật phải dùng đích đang hoạt động và có positive control. Chạy kiểm tĩnh không thay cho TC runtime.
10. `copy running-config startup-config`, lưu project, đóng/mở lại và chạy [persistence test](../test_results/supplemental/persistence.md). Lấy hash file `.pkt`/gói GNS3 sau khi lưu bản được test; ghi version và dependency trong integration log. TV1 chỉ duyệt sản phẩm cuối đúng hash.

## Phạm vi chức năng

OSPF/routing/PBR/ACL/ZBF/NAT cần kiểm IOS thực; hiện chỉ có kiểm tĩnh. Ethernet tới ISP mô hình chức năng xDSL; Serial2 Mbps mô hình leased line; không dùng chúng để đo năng lực150–200 Mbps hoặc chứng minh 1/10/40GbE/GPON. HTTP không mô phỏng HIS/DICOM/TLS thật. MPLS/SD-WAN, IPsec, teleworker, IDS/IPS và HA chưa triển khai. Guest isolation cùng SSID/L2, campus A/B/GPON/RF và BOM còn phụ thuộc TV2.

Cấu hình ACL chỉ IPv4 và TCP established không phải session firewall cho east-west. Main-FW có ZBF transit nhưng self-zone chưa harden đầy đủ. DMZ chỉ công bố ISP2:8080; ISP2 hỏng thì inbound service mất, dù outbound có thể failover ISP1. Các hạn chế này phải giữ trong báo cáo.
