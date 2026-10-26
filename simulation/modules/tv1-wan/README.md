# Module TV1 — WAN/routing và Internet tập trung

**Chủ trì:** TV1. **Tích hợp:** TV4. **Cập nhật:** 26/10/2026. **Trạng thái:** CÓ CẤU HÌNH THAM CHIẾU VÀ HƯỚNG DẪN / CHƯA CÓ PROJECT, CHƯA CHẠY IOS.

## 1. Đầu ra và điều kiện công cụ

Module chuẩn bị OSPF ba site, hai đường Internet mô hình hóa, PBR theo nguồn, IP SLA/track, PAT theo egress và default có điều kiện. Chưa có `.pkt` hoặc project GNS3, chưa thử lệnh trên model cụ thể. Kiểm tĩnh bằng Python không tạo file mô phỏng hoặc bằng chứng runtime.

Bộ tham chiếu dùng **9 router IOS**: Main-Core, Main-GW, Main-FW, Main-Edge, DBP-GW, BHTQ-GW, ISP1, ISP2, INET-Core; thêm switch VLAN/PC đại diện ba site và một Web server. Model dự kiến Cisco 2911, Serial module trên ba WAN gateway; interface mapping ở [architecture.md](../../../docs/02-design/architecture.md). Main-Core router-on-a-stick là bản lab WAN; thiết kế campus/switch L3 do TV2 ghép riêng. Main-FW là routing stand-in, **chưa có chính sách firewall/ACL/VPN**.

TV4 phải ghi platform/model/image/version thực tế và thử: `ip sla`, `track ... ip sla`, `delay`, `set ip next-hop verify-availability`, PAT `route-map`/`match interface`, OSPF point-to-point và selective static redistribution. Không tự suy từ số phiên bản Packet Tracer rằng mọi lệnh được hỗ trợ. Nếu thiếu tính năng, ghi BLOCKED hoặc DESIGN ONLY cho phần đó và chọn môi trường hỗ trợ (ví dụ GNS3 cùng image có quyền sử dụng); việc này chưa thực hiện trong workspace.

## 2. File cấu hình — mỗi file nạp đúng một node

| Node | File | Lưu ý |
| --- | --- | --- |
| Main-GW | [main-wan-router.cfg](../../../configs/main/main-wan-router.cfg) | DCE Serial tại Main; track10 kiểm Web và phát default OSPF |
| Main-Edge | [main-edge-router.cfg](../../../configs/main/main-edge-router.cfg) | PBR, hai probe ghim egress, PAT; không OSPF |
| DBP-GW | [dbp-wan-router.cfg](../../../configs/dbp/dbp-wan-router.cfg) | LAN subinterfaces và OSPF |
| BHTQ-GW | [bhtq-wan-router.cfg](../../../configs/bhtq/bhtq-wan-router.cfg) | LAN subinterfaces và OSPF |
| Main-Core | [main-core-transit-reference.cfg](../../../configs/main/main-core-transit-reference.cfg) | Lab router-on-a-stick; TV2 merge campus/ACL và map SVI nếu đổi model |
| Main-FW | [main-fw-routing-reference.cfg](../../../configs/main/main-fw-routing-reference.cfg) | IOS router chỉ định tuyến; TV3 thay bằng firewall/policy tương ứng; không nạp vào ASA |
| ISP1 | [isp-edge-lab.cfg](../../../configs/isp-lab/isp-edge-lab.cfg) | Tên cũ giữ tương thích; file này chỉ chứa ISP1 |
| ISP2 | [isp2-router.cfg](../../../configs/isp-lab/isp2-router.cfg) | Nối INET-Core qua `192.0.2.132/30` |
| INET-Core | [internet-core-router.cfg](../../../configs/isp-lab/internet-core-router.cfg) | Nối hai ISP, Web LAN và loopback probe `.11/.22` |

Cấu hình dùng console, VTY tắt; chưa cấu hình SSH/AAA. Không có mật khẩu vận hành. Chỉ nạp vào node lab mới hoặc hợp nhất có kiểm soát; TV1/TV2/TV3 thống nhất node dùng chung trước khi TV4 lưu file tổng.

## 3. Trình tự dựng và nạp

1. Chọn môi trường/model hỗ trợ các lệnh, ghi phiên bản vào `simulation/README.md`. Tạo node, gắn module Serial khi tắt nguồn theo công cụ; nối đúng [mapping](../../../docs/02-design/architecture.md). Kiểm DCE bằng `show controllers serial`; chỉ Main-GW giữ `clock rate` nếu đúng đầu DCE.
2. Nạp INET-Core, ISP1, ISP2, Main-Edge trước. Kiểm ping transit, hai loopback probe và Web LAN. Main-Edge phải ping được cùng Web `192.0.2.100` qua từng ISP trước khi nối LAN.
3. Tạo Web-Lab: IP `192.0.2.100`, mask `255.255.255.192`, gateway `192.0.2.65`; bật HTTP và DNS, record `web.hospital.test -> 192.0.2.100`. ICMP đến Web phải được phép để track10 hoạt động. DNS public ngoài lab chưa được dựng.
4. Nạp Main-FW routing reference rồi Main-Core. Đây là bước kiểm routing; khi TV3 thay bằng firewall phải giữ route chiều về ba site, cho phép probe và không NAT trước Edge. DMZ80 gateway nằm trên Main-FW, không đồng thời trên Core.
5. Nạp Main-GW, DBP-GW, BHTQ-GW; kiểm IP, trạng thái link và OSPF. Không nạp một file vào nhiều router với cùng hostname/IP.
6. Dựng switch access/trunk đại diện theo TV2: tạo đúng VLAN, trunk tới G0/0 của Core/Aux gateway. Trong lab tối thiểu có thể dùng IP tĩnh theo bảng dưới, chưa bật DHCP. Khi tích hợp DHCP thật, TV2 cần tránh cấp trùng IP tĩnh hoặc thay địa chỉ test bằng lease thật và cập nhật hồ sơ; không lấy thêm IP khỏi pool /25 vốn chỉ đủ 120 PC mà chưa tính lại.
7. Chạy kiểm tĩnh từ repo root: `python3 scripts/check_docs.py` và `python3 scripts/check_wan.py`. Sau đó chạy test **trên mô phỏng**, lưu actual/log/ảnh/hash; các test runtime hiện NOT RUN.
8. Lưu startup config từng node, lưu project, đóng/mở lại và chạy test nhanh. TV4 ghi integration log; chỉ cập nhật checklist khi đủ đầu ra và reviewer chấp nhận.

| Host đại diện | IP/mask | Gateway | DNS | Vai trò test |
| --- | --- | --- | --- | --- |
| Main-PC10 | `10.10.10.10/25` | `10.10.10.1` | `192.0.2.100` | PBR ưu tiên ISP1, TC03/06 |
| Main-PC20 | `10.10.20.10/25` | `10.10.20.1` | `192.0.2.100` | PBR ưu tiên ISP2 |
| Main-Guest | `10.10.100.11/23` | `10.10.100.1` | `192.0.2.100` | Cần TV3 policy trước TC05; routing lab chưa cô lập guest |
| DBP-PC10 | `10.20.10.10/25` | `10.20.10.1` | `192.0.2.100` | TC03/06, ưu tiên ISP1 |
| BHTQ-PC10 | `10.30.10.10/25` | `10.30.10.1` | `192.0.2.100` | TC03/06, ưu tiên ISP2 |
| Aux server nếu dựng | `10.20.70.10/28` hoặc `10.30.70.10/28` | `.70.1` cùng site | Theo TV3 | IP tĩnh; không đại diện đủ ứng dụng bệnh viện |

Một PC đại diện chức năng kết nối của VLAN; không đại diện bằng chứng đủ port/throughput cho 1.120 PC. Việc mô phỏng DSL/leased Ethernet vật lý và sizing thực phải ghi riêng với TV2/TV4.

## 4. Lệnh kiểm tra và expected

| Nơi kiểm | Lệnh/hoạt động | Expected; chưa phải actual |
| --- | --- | --- |
| Mọi router | `show ip interface brief`, `show ip route` | Địa chỉ/mask/link đúng mapping |
| Main-GW | `show ip ospf neighbor` | FULL với Core, DBP, BHTQ; Core–GW point-to-point |
| Aux | `show ip route ospf` | Subnet cụ thể Main/nhánh kia, không mặc định route tổng hợp /16; default O*E2 qua Main khi còn Internet |
| Edge | `show ip sla statistics`, `show track`, `show ip route 0.0.0.0` | Track1/2 phản ánh đích sau từng ISP; default gắn đúng track |
| Core/GW | `show track 10`, `show ip route 192.0.2.100` | Probe /32 tồn tại độc lập với default để phục hồi |
| Edge | `show route-map`, `show ip policy`, `show access-lists` | PBR source-group chọn ISP và fallback theo track |
| Edge | `show ip nat translations`, `show ip nat statistics` | Phiên Internet PAT đúng public egress; không PAT liên site |
| PC | `ping`, `tracert`/`traceroute`, HTTP tới IP và hostname | Đường đi qua Main; HTTP cùng đích trên hai ISP; DNS được phân biệt với routing |

Bắt đầu khi cả hai ISP up rồi test từng đường với **cùng đích HTTP `192.0.2.100`**. Kịch bản upstream: `shutdown` G0/1 của ISP1 hoặc ISP2, giữ G0/0 hướng Edge up; đích probe nằm ở INET-Core nên phải mất qua nhánh bị ngắt. Kịch bản mất hai ISP: default Edge và default Main-GW mất sau hội tụ, Aux không còn default OSPF; route nội bộ vẫn có. `/32` phục hồi tới Web còn tại GW/Core là có chủ đích.

Không tự đặt kết quả 50/50, RTT hay thời gian chuyển tuyến. Timer `frequency3/timeout1/delay6` không phải cam kết 9s. Thu lại số liệu và phân biệt phiên mới với phiên NAT/TCP cũ.

## 5. Khi đổi từ bản cấu hình trước review

- Thay probe sát gateway bằng `.11/.22` phía sau ISP; thêm host routes ghim và Null0 fallback.
- Main-GW default nay có track10; loại default tĩnh không track cũ nếu chỉnh trực tiếp node đã có cấu hình. Không để thêm một default không track còn sót hoặc `default-information originate always`.
- Xóa route `10/8` quay vào FW trên Edge, dùng ba /16 site; ISP lab dùng Web chung `.100` thuộc `192.0.2.64/26`, không dùng hai Web tách biệt cũ.
- DMZ80 gateway chuyển về FW; không để `10.10.80.1` đồng thời trên Core.
- Giữ discard route /16 tại Core/GW/Aux và route tổng hợp Aux tại Core để địa chỉ chưa cấp hoặc nhánh mất route không quay vòng qua default. Không redistribute các aggregate/discard vào OSPF.
- Khuyến nghị dựng lại lab mới từ các file hiện tại để tránh lệnh cũ còn sót; kiểm running-config thực trước test.

## 6. Bàn giao và giới hạn

Ghi project/hash, platform/image/version, interface mapping thực tế, ngày/người chạy, expected/actual, log/ảnh và nhận xét TV2/TV3. Hồ sơ: [TC03](../../../test_results/TC03-inter-site/result.md), [TC06](../../../test_results/TC06-internet-web/result.md), [dual ISP](../../../test_results/supplemental/dual-isp-failover.md). Cập nhật [integration log](../../integration-log.md).

Chưa có phép đo băng thông, kiểm IOS parser, OSPF hội tụ thật, phiên NAT, firewall security hoặc kiểm mở lại project. Không gọi router stand-in là firewall đạt nghiệm thu, PBR là SD-WAN hay Serial 2 Mbps là leased Ethernet 150 Mbps. Công việc còn lại được theo dõi trong [tình trạng TV1](../../../docs/00-management/tv1-review-status.md).
