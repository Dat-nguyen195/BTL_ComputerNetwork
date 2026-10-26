# Phân công công việc - 4 giai đoạn × 5 thành viên

**Dự án:** Thiết kế và mô phỏng mạng bệnh viện Main - DBP - BHTQ. Nguồn kỹ thuật, bảng IP, tính tải và 7 Step nằm trong [README.md](README.md); đường dẫn sản phẩm theo [github-project-structure.md](github-project-structure.md).

**Bắt đầu:** Thứ Hai **26/10/2026**. **Kết thúc 4 tuần triển khai:** **22/11/2026**. **Target Completion nội bộ:** **06/12/2026** sau dự phòng rà soát. **BKeL:** nộp trước hạn **11/12/2026** do nhóm cung cấp. Toàn bộ ngày/giờ dùng múi giờ Việt Nam. Không có đầu việc slide.

**Cập nhật TV1 ngày 26/10/2026:** hoàn thành **1/20 task chính: W1-TV1-03 (thiết kế WAN)**. Các bước con đã có sản phẩm/kiểm tra được tích riêng; task chính còn mở nếu chưa đủ toàn bộ đầu ra. Chưa có project, runtime evidence hoặc xác nhận đọc chéo TV2/TV3/TV4. Chi tiết tại [tv1-review-status.md](docs/00-management/tv1-review-status.md).

## Quy tắc thực hiện và cân bằng tải

- Mỗi giai đoạn có checklist riêng cho **TV1, TV2, TV3, TV4, TV5**. Task ID `Wn-TVx-yy` dùng để tạo issue/PR và truy vết; mặc định mọi task chưa hoàn thành.
- Mỗi người dự kiến **12 giờ/tuần**, tổng **48 giờ/người/4 tuần**, cả nhóm **240 giờ**. Đây là ngân sách lập kế hoạch, không phải số giờ đã thực hiện; số task bằng nhau không có nghĩa độ khó bằng nhau. TV1 điều chỉnh hỗ trợ khi effort lệch, vẫn giữ chủ trì chuyên môn.
- Người chủ trì thực hiện và giao bằng chứng, reviewer đọc chéo; **TV4 tích hợp mô phỏng tổng**, mỗi người vẫn giao module/config của mình. **TV5 chủ trì thu thập và biên tập báo cáo**, không phải tự viết thay toàn bộ phần kỹ thuật.
- Tích `- [x]` chỉ khi sản phẩm đúng đường dẫn, kiểm tra phù hợp đã chạy, tài liệu liên quan được cập nhật và reviewer chấp nhận. Bị chặn phải ghi dependency, người gỡ và hạn xử lý trong issue.
- Cuối mỗi tuần có cổng nghiệm thu. Không đưa `PASS` vào test chưa chạy hoặc ghi SD-WAN/MPLS/GPON/IDS/IPS đã triển khai chỉ từ một topology tương đương.

| Thành viên | Tuần 1 | Tuần 2 | Tuần 3 | Tuần 4 | Tổng dự kiến |
| --- | --- | --- | --- | --- | --- |
| TV1 - WAN & Routing / Trưởng nhóm | 12h | 12h | 12h | 12h | 48h |
| TV2 - LAN & Wireless | 12h | 12h | 12h | 12h | 48h |
| TV3 - Security & Systems | 12h | 12h | 12h | 12h | 48h |
| TV4 - Simulation & Testing | 12h | 12h | 12h | 12h | 48h |
| TV5 - Documentation & Report | 12h | 12h | 12h | 12h | 48h |
| **Cả nhóm** | **60h** | **60h** | **60h** | **60h** | **240h** |

## Giai đoạn 1 - Quy hoạch & Tính toán

**Tuần 1: 26/10/2026 - 01/11/2026, đúng 7 ngày.** Trọng tâm Step 1, Step 2, Step 3; chuẩn bị Step 4-5. Giao baseline cuối ngày 30/10 để đọc chéo 31/10 và nghiệm thu 01/11.

### TV1 - Trưởng nhóm, WAN & Routing Lead

- [ ] **W1-TV1-01** - Khởi tạo cấu trúc repo và quy tắc issue/PR, phân quyền/handle khi có; lập 4 milestone đúng ngày, liên kết checklist và sổ quyết định. **Hạn 26/10; đầu ra:** `.github/`, `TASKS.md`, `docs/00-management/`.
  - [x] Cấu trúc repo, template issue/PR, workflow kiểm tra, `TASKS.md`, kế hoạch và sổ quyết định đã có trong workspace.
  - [ ] Cần xác nhận đủ tài khoản/quyền và 4 milestone thực tế trên GitHub trước khi đóng task chính.
- [ ] **W1-TV1-02** - Chốt IP/VLSM tổng thể cho 3 site, VLAN theo nhóm phòng ban và transit/VPN pool, DHCP/gateway/reserved; kiểm không overlap và đủ **20% tăng trưởng trong 5 năm**. **Hạn 29/10; đầu ra:** `docs/02-design/ip-vlan-plan.md`; TV2 đọc chéo.
  - [x] Đã lập bảng IP ba site, transit, gateway/reserved/DHCP và VPN pool dự trù trong `ip-vlan-plan.md`.
  - [x] Đã kiểm tĩnh 33 subnet VLAN/transit không overlap và tính sức chứa workstation tăng trưởng tổng 20%.
  - [ ] Chờ TV2 đọc chéo, TV3 xác nhận pool/gateway DMZ và khóa số liệu khảo sát trước khi chốt IP plan.
- [x] **W1-TV1-03** - Thiết kế **2 leased lines Main-DBP/Main-BHTQ**, OSPF, default route Internet tập trung, vai trò SD-WAN/MPLS và các điểm giới hạn mô phỏng. **Hạn 30/10; đầu ra:** phần WAN trong `architecture.md` và sơ đồ WAN.
  - [x] Đã có kiến trúc/sơ đồ Mermaid, interface mapping, OSPF, default có tracking, vai trò MPLS/SD-WAN và giới hạn mô hình trong `architecture.md`; đã rà soát logic và kiểm tĩnh. Nghiệm thu nhóm G1 và kiểm runtime thuộc các task tiếp theo.
- [ ] **W1-TV1-04** - Phối hợp TV4 tính năng lực từng chiều của **2 xDSL**, chọn cơ chế load balancing/failover theo phiên; so sánh WAN khả dụng, ưu/nhược, CAPEX/OPEX/TCO và nguồn báo giá hoặc mục chờ xác nhận. **Hạn 30/10; đầu ra:** `wan-options-cost.md` và yêu cầu ISP.
  - [x] Đã lập bảng down/up và kịch bản hai ISP/một ISP, cơ chế PBR/failover và yêu cầu ISP theo giả định baseline.
  - [x] Đã so sánh bốn phương án WAN, tính CAPEX/OPEX/TCO minh họa và ghi rõ giá/SLA/thuế chưa có nguồn.
  - [ ] Chờ TV4 xác nhận tải/phân loại LAN–WAN–Internet và hoàn tất danh mục dữ liệu/báo giá chờ xác nhận có chủ trì/hạn để chốt phương án.
- [ ] **W1-TV1-05** - Rà soát G1 cùng cả nhóm: dữ kiện/giả định, IP, sizing, chi phí, rủi ro công cụ; chốt Packet Tracer hoặc GNS3 và ghi mục nào chỉ thiết kế. **Hạn 01/11; đầu ra:** biên bản G1 và baseline được duyệt.
  - [x] Đã liệt kê tính năng/model cần thử và phần mô hình hóa/chỉ thiết kế trong hướng dẫn module.
  - [ ] Chưa thử nền tảng thực tế, chốt công cụ hoặc có biên bản G1 được nhóm xác nhận.

### TV2 - LAN & Wireless Engineer

- [ ] **W1-TV2-01** - Lập kiến trúc LAN A/B **mỗi tòa 5 tầng × 10 phòng**, phòng trung tâm cách **50 m**; mỗi Aux **2 tầng, IT/CCL ở tầng 1**. Phân biệt vị trí vật lý với nhóm VLAN nghiệp vụ. **Hạn 28/10; đầu ra:** sơ đồ logic và mặt bằng giả định có nhãn.
- [ ] **W1-TV2-02** - Phân bổ VLAN phòng ban/SSID và cổng trunk/access cho **600 PC Main, 260 PC mỗi Aux**; phối hợp TV1 kiểm host, DHCP và dự phòng. **Hạn 29/10; đầu ra:** bảng VLAN/port và nhận xét IP plan.
- [ ] **W1-TV2-03** - Thiết kế GPON/Ethernet: MDF/IDF, patch panel/ODF, tuyến quang/cáp đồng, OLT/splitter/ONT nếu dùng GPON, 1/10/40GbE theo tầng mạng. **Hạn 30/10; đầu ra:** `physical-cabling.md` và sơ đồ nguồn.
- [ ] **W1-TV2-04** - Lập BOM/spec và port/PoE/uplink budget hiện tại/5 năm; không giới hạn Main ở 12 thiết bị nếu số cổng không đủ; phối hợp TV3 tính camera/NVR và server/DMZ. **Hạn 30/10; đầu ra:** `equipment-bom.md`, phần cáp/PoE trong `camera-plan.md`.
- [ ] **W1-TV2-05** - Quy hoạch Wi-Fi phủ Main, kiểm nhu cầu Aux; tách nhân viên/khách, dự kiến AP theo RF/dung lượng, không tự gán số khách; đọc chéo baseline G1. **Hạn 01/11; đầu ra:** `wireless-plan.md`, sơ đồ SSID/VLAN và vùng cần khảo sát.

### TV3 - Security & Systems Specialist

- [ ] **W1-TV3-01** - Phân bổ vai trò **10 server Main, 2 server mỗi Aux**, tách Server Farm/DMZ; ghi DHCP/DNS, HIS/RIS-PACS/LIS/CRM/database/backup và IP tĩnh. **Hạn 29/10; đầu ra:** `server-dmz-plan.md`.
- [ ] **W1-TV3-02** - Lập ma trận nguồn-đích-dịch vụ cho liên VLAN, DMZ, quản trị, Wi-Fi khách; đặt firewall/ACL và ranh giới chính sách, chặn guest tới LAN ở cả 3 site. **Hạn 29/10; đầu ra:** `docs/04-security/security-policy.md`.
- [ ] **W1-TV3-03** - Thiết kế PAT tại Main cho tất cả site, hai egress xDSL, static PAT DMZ và NAT exemption cho luồng nội bộ/VPN; đối chiếu inside/outside và các lỗi/caveat của [R]. **Hạn 30/10; đầu ra:** `nat-pat.md`.
- [ ] **W1-TV3-04** - Đề xuất site-to-site VPN và teleworker VPN; đánh giá firewall/IDS/IPS/chống phishing/HA, khả năng chạy trên công cụ và điều kiện chương trình kỹ sư tài năng. **Hạn 30/10; đầu ra:** `vpn-plan.md`, `ids-ips-plan.md`, danh sách chức năng chạy/thiết kế.
- [ ] **W1-TV3-05** - Cùng TV2 thiết kế camera VLAN/quyền xem/NVR/bitrate/lưu trữ; soạn khung security best practices và đọc chéo G1. **Hạn 01/11; đầu ra:** `camera-plan.md`, `security-best-practices.md` bản đầu.

### TV4 - Simulation & Testing Lead

- [ ] **W1-TV4-01** - Lập đầu vào Step 3: 1.120 workstation/14 server, tải PC 500/100 MB, server 1.000/2.000 MB theo các cách hiểu, Wi-Fi 500 MB và số khách chưa biết; ghi nguồn/giả định. **Hạn 28/10; đầu ra:** `docs/03-capacity/assumptions.md`, `capacity-inputs.csv`.
- [ ] **W1-TV4-02** - Tính riêng down/up cho site và tổng: **80% tải trong 09:00-11:00 + 15:00-16:00 = 3 giờ**, tăng trưởng tổng 20%; làm rõ MB/Mbps, overhead/headroom và tỷ lệ LAN/WAN/Internet. **Hạn 29/10; đầu ra:** `throughput.md`; chuyển kết quả sớm cho TV1/TV2.
- [ ] **W1-TV4-03** - Đề xuất băng thông ISP/leased line theo biến khách, từng chiều và tải quan trọng khi hỏng một xDSL; không tự khẳng định gói xDSL đủ tốc độ. **Hạn 30/10; đầu ra:** bảng kịch bản năng lực và khoảng thiếu.
- [ ] **W1-TV4-04** - Thử khả năng thiết bị/phần mềm cần dùng trước khi khóa công cụ; dựng skeleton Main/DBP/BHTQ, mapping node/interface và lịch bàn giao module. **Hạn 30/10; đầu ra:** `simulation/README.md`, `integration-log.md`, khung mô phỏng.
- [ ] **W1-TV4-05** - Soạn ma trận **TC01-TC06** cùng các test DHCP/dual ISP/VPN bổ sung; đặt expected, precondition, mẫu evidence và trạng thái NOT RUN; kiểm G1. **Hạn 01/11; đầu ra:** `test_results/test-matrix.md`.

### TV5 - Documentation & Report Specialist, chủ trì báo cáo

- [ ] **W1-TV5-01** - Chủ trì phân tích Step 1 và checklist khảo sát: phòng/tầng, MDF/IDF, điện/UPS, cáp, RF, vùng đông người, ứng dụng, camera, nhà mạng/SLA; ghi rõ phần chưa khảo sát. **Hạn 28/10; đầu ra:** `survey-checklist.md`, `site-requirements.md`.
- [ ] **W1-TV5-02** - Lập bảng truy vết **7 Step và điểm 1-1-1-2-2-2-1**, nguồn trang PDF, chủ trì, đầu ra và tiêu chí nghiệm thu; ghi thay đổi nhóm 5 người/lịch 2026/không slide. **Hạn 29/10; đầu ra:** `requirements-traceability.md`.
- [ ] **W1-TV5-03** - Lập đề cương báo cáo, quy ước font, heading, bảng/hình, nguồn và template phần đóng góp; thống nhất nơi nhận nội dung TV1-TV4. **Hạn 29/10; đầu ra:** `docs/06-report/source/`, `contributions/` và lịch thu thập.
- [ ] **W1-TV5-04** - Thu thập kết quả khảo sát/thiết kế/tính toán của từng người, viết bản thô đầu tiên phần giới thiệu và Step 1-3, kiểm nhất quán quy mô và thuật ngữ bệnh viện. **Hạn 31/10; đầu ra:** `docs/06-report/draft/` bản 0.1.
- [ ] **W1-TV5-05** - Chuẩn bị khung đánh giá Step 6 theo tin cậy, nâng cấp, phần mềm, an toàn/bảo mật; tổng hợp vướng mắc G1 và phát hành biên bản để TV1 duyệt. **Hạn 01/11; đầu ra:** `evaluation.md`, `risks.md`, meeting notes.

**Cổng G1 - 01/11:** TV1 xác nhận kiến trúc/IP, TV2 xác nhận port/cabling/Wi-Fi, TV3 xác nhận vùng bảo mật, TV4 xác nhận tính tải và khả năng công cụ, TV5 xác nhận truy vết/bản thô. Nếu chưa có báo giá/khảo sát thực địa, danh mục chờ xác nhận phải có chủ trì và hạn.

## Giai đoạn 2 - Mô phỏng cơ bản

**Tuần 2: 02/11/2026 - 08/11/2026, đúng 7 ngày.** Trọng tâm Step 4, kiểm thử smoke test Step 5. Module/config giao cho TV4 trước hoặc trong ngày 05/11; tích hợp và sửa lỗi 06/11-08/11.

### TV1 - Trưởng nhóm, WAN & Routing Lead

- [ ] **W2-TV1-01** - Cấu hình kết nối Main-DBP/Main-BHTQ và OSPF, quảng bá subnet cần thiết, default hướng Main; ghi route chiều về và điều kiện quảng bá default. **Hạn 04/11; đầu ra:** module WAN và `configs/main/`, `configs/dbp/`, `configs/bhtq/` phần routing.
  - [x] Đã viết cấu hình tham chiếu Main-GW/DBP/BHTQ và Core/FW routing, gồm OSPF, route chiều về, default có track và bảo vệ vòng lặp.
  - [ ] Chưa nạp trên IOS/công cụ mô phỏng và bàn giao module project hoạt động.
- [ ] **W2-TV1-02** - Dựng Internet edge hai xDSL/ISP lab, cơ chế phân phối luồng và dự phòng theo thiết bị hỗ trợ; phối hợp TV3 gắn NAT đúng egress. **Hạn 05/11; đầu ra:** cấu hình edge/ISP, mô tả phần mô hình hóa so với xDSL thật.
  - [x] Đã viết cấu hình tham chiếu Edge, ISP1/ISP2, INET-Core chung, PBR, probe phía sau ISP và PAT theo egress; đã kiểm tĩnh các tình huống lỗi.
  - [ ] Chưa kiểm feature support, dựng project và xác nhận routing/NAT trên công cụ cùng TV3.
- [ ] **W2-TV1-03** - Giao module/config, sơ đồ interface và thứ tự nạp cho TV4; hỗ trợ ghép route với LAN/firewall, sửa loop/blackhole và ngăn local breakout tại Aux. **Hạn 06/11; đầu ra:** module WAN được tích hợp, integration log.
  - [x] Đã chuẩn bị config text, sơ đồ giao diện, bảng host mẫu và thứ tự nạp trong `simulation/modules/tv1-wan/README.md`.
  - [ ] Chưa có lần TV4 nhận/ghép module project, log tích hợp và kết quả sửa lỗi trên mô phỏng.
- [ ] **W2-TV1-04** - Kiểm tra route/OSPF neighbor, ping/traceroute Main↔DBP và Main↔BHTQ; bổ sung phương án chi phí và quyết định WAN sau phản hồi nhóm. **Hạn 07/11; đầu ra:** smoke log WAN và `wan-options-cost.md` cập nhật.
- [ ] **W2-TV1-05** - Rà soát tiến độ/PR và G2; xác nhận file tổng 3 site mở lại được, baseline routing và Internet qua Main nhất quán. **Hạn 08/11; đầu ra:** biên bản G2 và phần đóng góp WAN/routing bản đầu.

### TV2 - LAN & Wireless Engineer

- [ ] **W2-TV2-01** - Dựng access/distribution/core đại diện A/B, VLAN, trunk/access, SVI hoặc router-on-a-stick theo baseline; đánh nhãn tầng/phòng/port. **Hạn 04/11; đầu ra:** module LAN Main và cấu hình switch.
- [ ] **W2-TV2-02** - Dựng LAN DBP và BHTQ, VLAN và uplink 2 tầng; ghi bảng ánh xạ PC đại diện sang quy mô 260 máy mỗi site. **Hạn 04/11; đầu ra:** module Aux và sơ đồ vật lý tương ứng.
- [ ] **W2-TV2-03** - Cấu hình DHCP/relay cùng TV3, SSID nhân viên/khách và VLAN tương ứng theo khả năng công cụ; kiểm địa chỉ/gateway đúng subnet, không chép gateway DiAn lỗi từ [R]. **Hạn 05/11; đầu ra:** LAN/Wi-Fi module và bảng pool.
- [ ] **W2-TV2-04** - Giao module/config cho TV4, kiểm trunk, VLAN, DHCP và smoke test cùng/khác VLAN; điều chỉnh port/PoE/BOM theo topology thực tế. **Hạn 07/11; đầu ra:** log LAN, module được tích hợp, BOM/cabling cập nhật.
- [ ] **W2-TV2-05** - Hoàn thiện sơ đồ logic/vật lý/cabling nguồn có thể sửa và bản xuất; viết nội dung LAN/Wi-Fi/BOM cho TV5 và đọc chéo G2. **Hạn 08/11; đầu ra:** `TV2-lan-wireless.md`, diagrams và tham số cấu hình.

### TV3 - Security & Systems Specialist

- [ ] **W2-TV3-01** - Dựng Server Farm/DMZ đại diện theo phân bổ 10/2/2, cấu hình IP tĩnh, DHCP/DNS/HTTP cần thiết; ghi cách đại diện ứng dụng bệnh viện chưa mô phỏng được. **Hạn 04/11; đầu ra:** module server/security, `server-dmz-plan.md` cập nhật.
- [ ] **W2-TV3-02** - Cấu hình PAT cơ bản tại Main cho các subnet được phép ở cả 3 site; phối hợp TV1 bảo đảm inside/outside và egress/route chiều về đúng. **Hạn 05/11; đầu ra:** cấu hình NAT và bảng kiểm lệnh.
- [ ] **W2-TV3-03** - Cấu hình static PAT dịch vụ DMZ và rule cho dịch vụ được phép; dựng khung firewall/zone/ACL, tách rule NAT khỏi rule bảo mật. **Hạn 05/11; đầu ra:** module DMZ/firewall và ma trận dịch vụ được công bố.
- [ ] **W2-TV3-04** - Giao module/config cho TV4; kiểm HTTP, bảng NAT và luồng liên site không bị NAT ngoài ý muốn; sửa xung đột ACL/routing trước hardening tuần 3. **Hạn 07/11; đầu ra:** smoke log NAT/DMZ, integration log.
- [ ] **W2-TV3-05** - Viết phần Server Farm/DMZ/NAT ban đầu cho TV5, cập nhật kế hoạch VPN/IDS/IPS theo công cụ thực tế và tham gia G2. **Hạn 08/11; đầu ra:** `TV3-security-systems.md`, kế hoạch bảo mật bản cập nhật.

### TV4 - Simulation & Testing Lead

- [ ] **W2-TV4-01** - Chuẩn bị file mô phỏng tổng, đặt tên node/port/site, nhãn VLAN/subnet; thống nhất bàn giao module và giữ lịch chỉnh file `.pkt` để tránh ghi đè. **Hạn 03/11; đầu ra:** khung tổng và integration log.
- [ ] **W2-TV4-02** - Nhận và ghép LAN/Server/WAN Main, DBP, BHTQ; kiểm mapping interface, subnet, router ID, trunk và kết nối ISP/Web lab. **Hạn 06/11; đầu ra:** `hospital-3sites.pkt` hoặc project GNS3 tích hợp.
- [ ] **W2-TV4-03** - Chạy smoke test DHCP/VLAN, route 3 site, Web qua Main và NAT; tạo issue kèm bước tái hiện cho lỗi, phân người sửa và chạy lại sau ghép. **Hạn 07/11; đầu ra:** log tích hợp, danh sách lỗi và test matrix cập nhật.
- [ ] **W2-TV4-04** - Ghi phiên bản phần mềm/model và cách mở lại, PC/server đại diện, chức năng mô hình hóa hoặc không hỗ trợ; đối chiếu thiết bị với bảng tính thông lượng. **Hạn 07/11; đầu ra:** `simulation/README.md`, capacity/config notes.
- [ ] **W2-TV4-05** - Lưu file, mở lại để kiểm persistence, đóng baseline G2 và chuyển nội dung tính tải/triển khai cho TV5. **Hạn 08/11; đầu ra:** file tổng có phiên bản, `TV4-capacity-testing.md` bản đầu, biên bản kiểm mở lại.

### TV5 - Documentation & Report Specialist, chủ trì báo cáo

- [ ] **W2-TV5-01** - Thu nội dung TV1-TV4 theo template, rà soát nguồn/tham số, phát hiện chỗ lệch IP/VLAN/số máy và lập danh sách cần bổ sung. **Hạn 05/11; đầu ra:** contributions và sổ thiếu nội dung có người xử lý.
- [ ] **W2-TV5-02** - **Chủ trì tổng hợp báo cáo thô**: Step 1-3 hoàn chỉnh và Step 4 bản đầu; chèn sơ đồ, BOM và công thức có giả định, không ghi smoke test là test nghiệm thu cuối. **Hạn 07/11; đầu ra:** báo cáo thô 0.2 trong `draft/`.
- [ ] **W2-TV5-03** - Chuẩn hóa heading, mục lục, số bảng/hình, thuật ngữ và danh mục tài liệu; yêu cầu người có chuyên môn xác nhận nội dung trước khi ghép. **Hạn 07/11; đầu ra:** nguồn báo cáo có định dạng thống nhất và review log.
- [ ] **W2-TV5-04** - Cập nhật Step 6 sơ bộ: SPOF, hạn chế 2 leased lines không dự phòng chéo, năng lực xDSL, tương thích phần mềm và khoảng cách thiết kế/mô phỏng. **Hạn 08/11; đầu ra:** `evaluation.md`, `risks.md` bản 0.2.
- [ ] **W2-TV5-05** - Tổng hợp tiến độ G2, kiểm đầy đủ truy vết 7 Step và hướng dẫn mở file; gửi bản thô cho TV1 rà soát. **Hạn 08/11; đầu ra:** báo cáo thô, biên bản G2 và issue tuần 3.

**Cổng G2 - 08/11:** Mô phỏng 3 site mở lại được, định tuyến và Internet tập trung hoạt động ở mức cơ bản; config và báo cáo thô khớp topology. Các test chính thức về security/load balancing sẽ có bằng chứng ở G3; không tích xong nếu baseline còn lỗi chặn tích hợp.

## Giai đoạn 3 - Bảo mật & Kiểm thử

**Tuần 3: 09/11/2026 - 15/11/2026, đúng 7 ngày.** Trọng tâm Step 5 và phần bảo mật, cung cấp dữ liệu Step 6. Khóa cấu hình test ban đầu 11/11; thực hiện 12/11-14/11; nghiệm thu bằng chứng 15/11.

### TV1 - Trưởng nhóm, WAN & Routing Lead

- [ ] **W3-TV1-01** - Hoàn thiện OSPF và route/default có điều kiện, kiểm hai chiều giữa Main với cả DBP/BHTQ; hỗ trợ TV4 chạy **TC03** đủ hai chi nhánh. **Hạn 12/11; đầu ra:** config routing cuối và log TC03.
- [ ] **W3-TV1-02** - Kiểm chứng load balancing bằng nhiều phiên qua hai xDSL và NAT đúng egress; ngắt từng tuyến, ghi khả năng tạo phiên mới, phiên cũ bị ảnh hưởng và giới hạn SLA. **Hạn 13/11; đầu ra:** test bổ sung dual ISP trong `supplemental/`.
- [ ] **W3-TV1-03** - Cùng TV3/TV4 kiểm Internet của tất cả site qua Main, default chiều về, route VPN và các lỗi routing phát hiện khi ACL bật. **Hạn 14/11; đầu ra:** cấu hình sửa lỗi, log retest liên quan TC03/TC06.
- [ ] **W3-TV1-04** - Rà soát kỹ thuật và bằng chứng 6 nhóm test, phân biệt triển khai thật/mô hình hóa/design only, theo dõi lỗi chặn và chủ trì xử lý. **Hạn 15/11; đầu ra:** biên bản G3 và danh sách lỗi được phân loại.
- [ ] **W3-TV1-05** - Giao phần WAN/IP/OSPF/load balancing/chi phí đã hoàn chỉnh cho TV5; đánh giá khả năng chịu lỗi và nâng cấp 5 năm với giả định đã duyệt. **Hạn 15/11; đầu ra:** `TV1-wan-routing.md` và nhận xét Step 6.
  - [x] Đã soạn contribution WAN/IP/OSPF/dual ISP/chi phí, phân tích SPOF và tăng trưởng trong `TV1-wan-routing.md`.
  - [ ] Chờ kết quả test, xác nhận giả định và bàn giao nội dung chính thức cho TV5; hiện vẫn là bản thảo kỹ thuật.

### TV2 - LAN & Wireless Engineer

- [ ] **W3-TV2-01** - Chuẩn bị và phối hợp chạy **TC01** cùng VLAN, **TC02** khác VLAN theo ma trận cho phép; dùng PC ở switch khác nhau khi có, kiểm SVI/trunk/DHCP. **Hạn 12/11; đầu ra:** config LAN ổn định và log/đầu vào bằng chứng cho TV4.
- [ ] **W3-TV2-02** - Kiểm SSID/VLAN nhân viên và khách, DHCP/gateway/DNS; phối hợp TV3 bảo đảm khách không nối nhầm VLAN nội bộ và cung cấp máy khách từng site cho **TC05/TC06**. **Hạn 12/11; đầu ra:** bảng SSID/VLAN và precondition test.
- [ ] **W3-TV2-03** - Sửa lỗi LAN/Wi-Fi từ test tích hợp; rà soát port budget, PoE, uplink và dư địa 20%, đối chiếu sơ đồ vật lý với file mô phỏng. **Hạn 14/11; đầu ra:** config/sơ đồ/BOM đồng bộ, log retest.
- [ ] **W3-TV2-04** - Cùng TV3 kiểm thiết kế camera, VLAN/quyền NVR và nhu cầu băng thông/lưu trữ; tách thông số chưa khảo sát khỏi kết quả chạy trong mô phỏng. **Hạn 14/11; đầu ra:** `camera-plan.md` và nhận xét tính khả thi.
- [ ] **W3-TV2-05** - Bàn giao phần LAN/Wi-Fi/BOM/cabling chính thức và ảnh sơ đồ rõ chữ cho TV5; đọc chéo tiêu chí nâng cấp, reliability và G3. **Hạn 15/11; đầu ra:** `TV2-lan-wireless.md` hoàn chỉnh và nhận xét Step 6.

### TV3 - Security & Systems Specialist

- [ ] **W3-TV3-01** - Hoàn thiện firewall/ACL theo ma trận quyền, ưu tiên chặn guest tới PC/server/quản trị/liên site nhưng cho DHCP/DNS và Internet cần thiết; lưu đúng hướng/interface áp rule. **Hạn 11/11; đầu ra:** config hardening và `security-policy.md`.
- [ ] **W3-TV3-02** - Phối hợp chạy **TC04** dịch vụ DMZ, thêm đường truy cập từ ngoài qua static PAT khi công bố; chụp translation và firewall hit, giải thích đổi địa chỉ/cổng theo [R]. **Hạn 12/11; đầu ra:** cấu hình DMZ/NAT và evidence đầu vào cho TV4.
- [ ] **W3-TV3-03** - Phối hợp chạy **TC05**: guest không tới LAN, gồm ICMP và TCP tới host đang hoạt động; thêm ca đối chứng guest vẫn ra Web ngoài, internal vẫn dùng được dịch vụ. **Hạn 13/11; đầu ra:** ACL hit/log và test negative/positive ở các site có guest.
- [ ] **W3-TV3-04** - Triển khai/test site-to-site và teleworker VPN trong khả năng nền tảng; thử firewall/IDS/IPS nếu áp dụng yêu cầu kỹ sư tài năng, ghi rõ phần chưa chạy và cách khắc phục bằng công cụ phù hợp. **Hạn 14/11; đầu ra:** `supplemental/` và hồ sơ VPN/IDS/IPS.
- [ ] **W3-TV3-05** - Hoàn thiện security best practices: SSH/AAA, secrets, log/NTP, backup/restore, cập nhật, chống phishing và phân quyền camera; giao nội dung/bằng chứng bảo mật cho TV5 và G3. **Hạn 15/11; đầu ra:** `TV3-security-systems.md`, security guide và đánh giá rủi ro.

### TV4 - Simulation & Testing Lead

- [ ] **W3-TV4-01** - Khóa phiên bản chạy test, xác nhận precondition/expected, định danh node/IP/VLAN và trạng thái ban đầu; cập nhật công thức tải khi có thay đổi đã được duyệt. **Hạn 11/11; đầu ra:** test matrix gắn phiên bản, capacity baseline cuối.
- [ ] **W3-TV4-02** - Điều phối chạy và lưu ảnh/log **TC01 cùng VLAN, TC02 liên VLAN, TC03 liên site với cả DBP và BHTQ**; nhận xác nhận chuyên môn TV2/TV1. **Hạn 13/11; đầu ra:** `TC01-*/`, `TC02-*/`, `TC03-*/` có result và bằng chứng.
- [ ] **W3-TV4-03** - Điều phối **TC04 DMZ, TC05 cô lập khách, TC06 Web Internet qua Main từ mỗi site**; chụp NAT/PDU theo [R], lưu negative/positive control, không chỉ ảnh ping. **Hạn 14/11; đầu ra:** `TC04-*/`, `TC05-*/`, `TC06-*/` đủ evidence.
- [ ] **W3-TV4-04** - Chạy test bổ sung dual ISP/VPN/HA và IDS/IPS nếu hỗ trợ/yêu cầu; mở issue lỗi, ghép cấu hình sửa và retest liên quan, thống nhất trạng thái PASS/FAIL/NOT RUN. **Hạn 15/11; đầu ra:** test matrix, `supplemental/`, bug log và file mô phỏng cập nhật.
- [ ] **W3-TV4-05** - Mở lại file sau save, kiểm ảnh/log gắn đúng phiên bản; bàn giao bộ bằng chứng 6 nhóm test, giới hạn mô phỏng và phần Step 3-5 hoàn chỉnh cho TV5. **Hạn 15/11; đầu ra:** `TV4-capacity-testing.md`, manifest evidence và baseline G3.

### TV5 - Documentation & Report Specialist, chủ trì báo cáo

- [ ] **W3-TV5-01** - Theo dõi đủ 6 nhóm test, yêu cầu TV4 bổ sung caption/nguồn/đích/expected/actual và trạng thái; đồng bộ link tới evidence, không tự sửa kết quả kỹ thuật. **Hạn 14/11; đầu ra:** bảng truy vết test tới báo cáo.
- [ ] **W3-TV5-02** - Thu phần hoàn chỉnh TV1-TV4, tổng hợp bản thô đầy đủ Step 1-5, chuẩn hóa chương tính tải, NAT và kiểm thử, ghi rõ dữ kiện/giả định/design only. **Hạn 15/11; đầu ra:** báo cáo thô 0.3 trong `draft/`.
- [ ] **W3-TV5-03** - Chủ trì **Step 6**: dùng dữ liệu test để đánh giá tin cậy, nâng cấp, đa dạng phần mềm, an toàn/bảo mật; lập bảng yêu cầu → bằng chứng → kết luận/giới hạn. **Hạn 15/11; đầu ra:** `evaluation.md` có nhận xét thành viên kỹ thuật.
- [ ] **W3-TV5-04** - Tổng hợp vấn đề còn lại và hướng phát triển: xDSL có thể thiếu tải, SPOF WAN, khảo sát Wi-Fi/camera, mở rộng 20%, HA, SD-WAN/MPLS và monitoring; chỉ rõ ưu tiên, ảnh hưởng, chủ trì. **Hạn 15/11; đầu ra:** `risks.md` và phần tương lai trong báo cáo.
- [ ] **W3-TV5-05** - Kiểm thuật ngữ, nguồn trang, số bảng/hình và tính nhất quán báo cáo-topology-test; gửi bản thô đầy đủ cho TV1 rà soát và ghi quyết định G3. **Hạn 15/11; đầu ra:** review log và danh sách sửa tuần 4.

**Cổng G3 - 15/11:** Có hồ sơ cho cả TC01-TC06; mỗi kết quả có actual và bằng chứng. Lỗi FAIL/NOT RUN hoặc yêu cầu security chưa chạy phải được nêu công khai và có kế hoạch xử lý, không tuyên bố “đạt toàn bộ”. Nếu có lỗi chặn, ưu tiên sửa đầu tuần 4 trước khi phát hành bản cuối.

## Giai đoạn 4 - Tổng hợp Báo cáo & Đóng gói

**Tuần 4: 16/11/2026 - 22/11/2026, đúng 7 ngày.** Trọng tâm Step 6-7 và nghiệm thu. Chốt nội dung thành viên **17/11**, bản PDF để review **19/11**, xử lý phản hồi **20/11**, đóng gói/kiểm mở lại **21/11**, **TV1 duyệt chót cả báo cáo và mô phỏng 22/11**.

### TV1 - Trưởng nhóm, WAN & Routing Lead

- [ ] **W4-TV1-01** - Chốt phần IP/WAN/OSPF/dual xDSL, quyết định so sánh chi phí và nội dung đánh giá; bàn giao mọi bảng/hình/config còn thiếu cho TV5. **Hạn 17/11; đầu ra:** contribution TV1 cuối và baseline routing.
- [ ] **W4-TV1-02** - Đọc chéo bản PDF tổng hợp do TV5 gửi, đối chiếu đủ 7 Step/điểm, 3 site, yêu cầu tăng trưởng, VPN/camera và 6 test; ghi nhận xét cụ thể theo trang/mục. **Hạn 19/11; đầu ra:** `docs/06-report/review-log.md`.
- [ ] **W4-TV1-03** - Điều phối sửa lỗi chặn và quyết định xử lý giới hạn còn lại; đọc kết quả retest và kiểm phiên bản config/topology/report đồng bộ. **Hạn 20/11; đầu ra:** issue đã xử lý hoặc giới hạn được ghi rõ, xác nhận kỹ thuật trước đóng gói.
- [ ] **W4-TV1-04** - **RÀ SOÁT / DUYỆT CHÓT riêng từng sản phẩm: báo cáo PDF và file mô phỏng**; đối chiếu bản mở lại, manifest/hash và bằng chứng trước khi ký. **Hạn 22/11; đầu ra:** `submission/approval.md` có phiên bản/hash của cả hai, kết luận G4.
- [ ] **W4-TV1-05** - Chốt quản lý release/bản ứng viên, phân người xử lý giai đoạn dự phòng và lịch khóa 06/12/nộp trước 11/12; không nộp nhầm bản chưa duyệt. **Hạn 22/11; đầu ra:** tag/release theo quyền repo, kế hoạch rà soát và nộp BKeL.

### TV2 - LAN & Wireless Engineer

- [ ] **W4-TV2-01** - Giao nội dung và sơ đồ LAN/Wi-Fi/GPON-Ethernet/BOM cuối; kiểm port budget, tốc độ 1/10/40GbE, vị trí phòng trung tâm và hai Aux đúng đặc tả. **Hạn 17/11; đầu ra:** contribution, sơ đồ nguồn và ảnh xuất cuối.
- [ ] **W4-TV2-02** - Đối chiếu bảng VLAN/subnet/DHCP, nhãn tầng/phòng, SSID với config và mô phỏng; sửa lỗi LAN còn lại cùng TV4, kiểm lại TC01/TC02/TC05/TC06 khi bị ảnh hưởng. **Hạn 18/11; đầu ra:** bảng/config đồng bộ và log retest.
- [ ] **W4-TV2-03** - Đọc phần LAN/Wi-Fi/thiết bị/đi dây/camera trong PDF, xác nhận hình rõ chữ và không khẳng định khảo sát RF/GPON/40GbE đã test nếu chưa chạy. **Hạn 19/11; đầu ra:** review chuyên môn gửi TV5.
- [ ] **W4-TV2-04** - Hoàn thiện phụ lục thiết bị, cabling, port/VLAN mapping và hướng mở module LAN; hỗ trợ TV5 giải đáp và sửa nội dung sau review TV1. **Hạn 20/11; đầu ra:** phụ lục LAN/BOM và phản hồi review đã đóng.
- [ ] **W4-TV2-05** - Cùng TV4 kiểm LAN/Wi-Fi sau mở lại bản đóng gói, xác nhận thiết kế mở rộng 5 năm và ghi rủi ro cần khảo sát sau này. **Hạn 21/11; đầu ra:** xác nhận LAN cho G4 và danh sách dự phòng.

### TV3 - Security & Systems Specialist

- [ ] **W4-TV3-01** - Giao nội dung cuối Server Farm/DMZ/NAT/PAT/firewall/ACL/VPN/camera và best-practice guide; xác nhận tổng server 10/2/2 và luồng Internet tại Main. **Hạn 17/11; đầu ra:** contribution TV3, config và phụ lục security.
- [ ] **W4-TV3-02** - Xử lý lỗi security còn lại, đối chiếu rule với TC04/TC05/TC06 và VPN test; chạy lại test liên quan cùng TV4 khi sửa NAT/ACL/route. **Hạn 18/11; đầu ra:** config security cuối và log retest.
- [ ] **W4-TV3-03** - Đọc bản PDF phần security/NAT theo [R], kiểm chú thích địa chỉ/cổng, ACL không bị nhầm với NAT; phân biệt khả năng đã triển khai và thiết kế IDS/IPS/HA. **Hạn 19/11; đầu ra:** review chuyên môn gửi TV5.
- [ ] **W4-TV3-04** - Kiểm bí mật/tài khoản trong config và ảnh, dùng dữ liệu lab; hoàn thiện hướng dẫn vận hành, backup/restore, quyền VPN và danh sách hạn chế bảo mật. **Hạn 20/11; đầu ra:** config phù hợp chia sẻ, guide và risk notes cuối.
- [ ] **W4-TV3-05** - Cùng TV4 kiểm mở lại bản đóng gói và xác nhận guest isolation/DMZ/NAT còn đúng; hỗ trợ TV5 đóng phản hồi và chuẩn bị hồ sơ TV1 duyệt. **Hạn 21/11; đầu ra:** xác nhận security cho G4.

### TV4 - Simulation & Testing Lead

- [ ] **W4-TV4-01** - Giao phần Step 3-5 cuối, file mô phỏng tổng, bảng tính tải và bộ evidence 6 test có phiên bản cho TV5; nêu đầy đủ giới hạn/known issues. **Hạn 17/11; đầu ra:** contribution TV4 và baseline ứng viên.
- [ ] **W4-TV4-02** - Tích hợp sửa lỗi tuần 4 từ TV1-TV3; chạy lại TC bị ảnh hưởng và test nhanh đủ 6 nhóm trên đúng bản ứng viên, không tái dùng ảnh từ topology cũ khi khác kết quả. **Hạn 20/11; đầu ra:** test matrix/evidence cập nhật, integration log.
- [ ] **W4-TV4-03** - Hoàn thiện `simulation/README.md`: phiên bản, dependency/node, cách mở, IP đích và lệnh test, mapping thiết bị đại diện, phần không hỗ trợ; đối chiếu phần này trong PDF. **Hạn 20/11; đầu ra:** hướng dẫn tái hiện và review gửi TV5.
- [ ] **W4-TV4-04** - Lưu/đóng/mở lại bản mô phỏng đóng gói trên môi trường ghi nhận, kiểm config persist và dependency GNS3 nếu chọn; bàn giao bản có checksum để TV1 duyệt. **Hạn 21/11; đầu ra:** file `.pkt` hoặc gói GNS3 dùng được và log kiểm mở lại.
- [ ] **W4-TV4-05** - Cùng TV5 lập manifest/version/hash, kiểm đúng cặp PDF-mô phỏng và evidence; phối hợp TV1 nghiệm thu kỹ thuật G4. **Hạn 22/11; đầu ra:** `submission/manifest.md`, `SHA256SUMS`, xác nhận kỹ thuật cho TV1.

### TV5 - Documentation & Report Specialist, chủ trì báo cáo

- [ ] **W4-TV5-01** - **Chủ trì thu nhận đầy đủ phần nội dung cuối của TV1-TV4**, bổ sung phần khảo sát/đánh giá mình phụ trách; khóa danh sách thiếu nội dung và tổng hợp báo cáo thô hoàn chỉnh. **Hạn 17/11; đầu ra:** source và draft đầy đủ 7 Step.
- [ ] **W4-TV5-02** - **Tổng hợp, biên tập và căn chỉnh báo cáo chính thức**: bìa/nhân sự, mục lục, heading, bảng/hình, công thức, nguồn, phụ lục, font tiếng Việt và phân trang; xuất PDF review cho cả nhóm/TV1. **Hạn 19/11; đầu ra:** PDF review và nguồn chỉnh sửa được.
- [ ] **W4-TV5-03** - Thu và xử lý nhận xét chuyên môn/TV1, hoàn tất Step 6 gồm reliability/nâng cấp/phần mềm/safety/security, vấn đề còn lại và hướng phát triển; rà soát không còn kết luận thiếu bằng chứng. **Hạn 20/11; đầu ra:** review log và PDF đã hiệu chỉnh.
- [ ] **W4-TV5-04** - Xuất `docs/06-report/final/report.pdf`, kiểm trực quan từng trang, mục lục, hình và link; cùng TV4 đóng gói PDF/nguồn/mô phỏng/config/evidence, đối chiếu manifest. **Hạn 21/11; đầu ra:** bộ hồ sơ cuối gửi TV1 **duyệt chót**, chưa tự gắn trạng thái approved.
- [ ] **W4-TV5-05** - Ghi kết quả duyệt PDF + mô phỏng của TV1 ngày 22/11, sửa/phát hành lại nếu cần và cập nhật checksum; chuẩn bị danh mục nộp BKeL, nơi lưu xác nhận và kế hoạch rà soát đến 06/12. **Hạn 22/11; đầu ra:** hồ sơ G4 và bản ứng viên đã được TV1 duyệt.

**Cổng G4 - 22/11:** TV5 hoàn tất báo cáo; TV4 xác nhận file mô phỏng mở lại được; TV2/TV3 xác nhận nội dung chuyên môn; **TV1 duyệt chót PDF và mô phỏng theo đúng phiên bản/hash**. Đóng gói chưa đồng nghĩa đã nộp BKeL. Không cần slide.

## Dự phòng rà soát và nộp bài - không phải giai đoạn 5

Khoảng **23/11/2026 - 06/12/2026** chỉ dành rà soát/sửa lỗi sau 4 tuần triển khai. Không dời việc biên soạn chính từ tuần 4 sang giai đoạn này. Nếu không phát sinh lỗi, giữ nguyên bản đã duyệt; nếu có sửa đổi, cập nhật version, retest phần liên quan, xuất lại báo cáo khi cần và xin **TV1 tái duyệt đúng sản phẩm đã đổi**.

| Phụ trách | 23/11 - 06/12/2026 | Sau khóa bản đến trước hạn 11/12/2026 |
| --- | --- | --- |
| TV1 | Theo dõi lỗi, quyết định ưu tiên; tái duyệt; khóa bản nộp chậm nhất **06/12** | Chủ trì nộp BKeL, dự kiến **07/12-10/12** khi cổng mở; kiểm giờ đóng thực tế |
| TV2 | Sửa LAN/Wi-Fi/cabling/BOM nếu có phản hồi, cập nhật phần báo cáo liên quan | Sẵn sàng xử lý lỗi mở/đối chiếu nếu được phát hiện |
| TV3 | Sửa ACL/NAT/VPN/security nếu có phản hồi, cập nhật hướng dẫn và giới hạn | Hỗ trợ kiểm đúng bản security/config được nộp |
| TV4 | Ghép sửa đổi, retest, kiểm mở file và cập nhật evidence/checksum | Kiểm gói mô phỏng đúng bản TV1 nộp |
| TV5 | Kiểm PDF, đồng bộ nguồn/nội dung và hồ sơ duyệt/manifest | Lưu xác nhận BKeL và đối chiếu tên file/hash khi có thể |

Ngân sách 240 giờ là cho 4 tuần chính; effort dự phòng chỉ ghi nhận khi phát sinh, không tự coi mọi thành viên phải làm thêm hai tuần đầy đủ. **Hoàn tất nội bộ chót 06/12/2026**; nhiệm vụ Step 7 chỉ đóng sau khi có xác nhận nộp đúng PDF và mô phỏng trước hạn BKeL.
