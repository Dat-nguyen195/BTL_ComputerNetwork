# Phân công công việc - 4 giai đoạn × 5 thành viên

**Bổ sung WAN đã kiểm:** MPLS L3VPN có module11 nút/10 link, Linux namespaces/QEMU chạy28/28 và sau dựng lại28/28; có PCAP hai nhãn. Project GNS3 riêng dùng chung cấu hình, chưa chạy native module mới. Chi tiết: [bằng chứng MPLS](test_results/mpls/README.md). Giá WAN có thêm nguồn lịch sử, vẫn chưa là báo giá hợp đồng hiện hành.


**Thông tin nhóm đã chốt theo nhóm trưởng:** lớp L08, nhóm 2; BTL2 do Nguyễn Thành Đạt (nhóm trưởng, 2410709) và Phạm Tiến Đạt (2410723) thực hiện. Ba thành viên Nguyễn Phúc Bảo Đạt, Bùi Công Danh, Nguyễn Minh Đạt thực hiện BTL1. Xem [danh sách và email](docs/00-management/team-members.md). TV1–TV5 là năm vai trò trong kế hoạch ban đầu.


**Kết quả kỹ thuật Packet Tracer04/11/2026:** native58 node/53 cáp/sáu Wi-Fi đã lưu/mở lại; 32/32 quan sát phù hợp kỳ vọng,19 client DHCP và18 pool có sức chứa. Bốn HTTP chọn ISP1 thủ công/khôi phục ISP2 đạt; không có tự động failover trên Packet Tracer. Chi tiết ở [hồ sơ Packet Tracer](test_results/packet-tracer/README.md). Phê duyệt nhóm/thông tin nhân sự/BKeL vẫn chờ xác nhận. Các ghi nhận đang dựng/đang chờ bên dưới là lịch sử.

**Dự án:** Thiết kế và mô phỏng mạng bệnh viện Main - DBP - BHTQ. Nguồn kỹ thuật, bảng IP, tính tải và 7 Step nằm trong [README.md](README.md); đường dẫn sản phẩm theo [github-project-structure.md](github-project-structure.md).

**Bắt đầu:** Thứ Hai **26/10/2026**. **Kết thúc 4 tuần triển khai:** **22/11/2026**. **Target Completion nội bộ:** **06/12/2026** sau dự phòng rà soát. **BKeL:** nộp trước hạn **11/12/2026** do nhóm cung cấp. Toàn bộ ngày/giờ dùng múi giờ Việt Nam. Không có đầu việc slide.

**Đối chiếu ngày 03/11/2026:** đã đọc đủ100 task, kiểm sản phẩm/nguồn/evidence và đồng bộ các bước con bên dưới. [Bảng trạng thái100 task](docs/00-management/completion-status.md) ghi sản phẩm và điều kiện còn lại. GNS3 đã có52 node/52 link và evidence209 kiểm tích hợp +137 kiểm reopen lịch sử; PDF LaTeX12 trang đã có QA. Đây là bằng chứng đã lưu, không phải lần chạy mới trên máy Windows này.

**Phạm vi bổ sung của chủ repo:** đã có cả GNS3 và Packet Tracer. Native Packet Tracer tổng đã lưu/mở lại và đạt bộ kiểm riêng; chi tiết tại [runbook](simulation/packet-tracer/README.md). Giới hạn chuyển ISP thủ công được giữ rõ, không áp kết quả GNS3 sang Packet Tracer.

**Đối chiếu Packet Tracer04/11:**58 node/53 cáp/sáu Wi-Fi,32/32 quan sát sau reopen,19 DHCP client và18 pool có sức chứa; bốn HTTP chọn ISP1/khôi phục ISP2 đạt. [Lịch sử/evidence](test_results/packet-tracer/README.md) giữ24 job dây,32 job Wi-Fi đầu, warmup và lần cuối. Task chính vẫn theo điều kiện sản phẩm/reviewer, không thay chữ ký hoặc xác nhận của nhóm.

Task chính giữ điều kiện reviewer/biên bản như quy tắc dưới đây; bước con có sản phẩm không thay chữ ký TV1–TV5. Các ghi nhận26/10 và02/11 tại các review lịch sử không còn là trạng thái triển khai hiện tại.

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
  - [x] Sản phẩm đã có: [.github](.github/).
  - [ ] Còn để nghiệm thu: Quyền/handle và milestone GitHub chưa xác nhận.
- [ ] **W1-TV1-02** - Chốt IP/VLSM tổng thể cho 3 site, VLAN theo nhóm phòng ban và transit/VPN pool, DHCP/gateway/reserved; kiểm không overlap và đủ **20% tăng trưởng trong 5 năm**. **Hạn 29/10; đầu ra:** `docs/02-design/ip-vlan-plan.md`; TV2 đọc chéo.
  - [x] Sản phẩm đã có: [ip-vlan-plan.md](docs/02-design/ip-vlan-plan.md).
  - [ ] Còn để nghiệm thu: TV2/TV3 đọc chéo và khóa giả định.
- [x] **W1-TV1-03** - Thiết kế **2 leased lines Main-DBP/Main-BHTQ**, OSPF, default route Internet tập trung, vai trò SD-WAN/MPLS và các điểm giới hạn mô phỏng. **Hạn 30/10; đầu ra:** phần WAN trong `architecture.md` và sơ đồ WAN.
  - [x] Sản phẩm đã có: [architecture.md](docs/02-design/architecture.md).
  - [ ] Còn để nghiệm thu: Đã được checklist ghi hoàn tất; nghiệm thu runtime ở task riêng.
- [ ] **W1-TV1-04** - Phối hợp TV4 tính năng lực từng chiều của **2 xDSL**, chọn cơ chế load balancing/failover theo phiên; so sánh WAN khả dụng, ưu/nhược, CAPEX/OPEX/TCO và nguồn báo giá hoặc mục chờ xác nhận. **Hạn 30/10; đầu ra:** `wan-options-cost.md` và yêu cầu ISP.
  - [x] Sản phẩm đã có: [wan-options-cost.md](docs/02-design/wan-options-cost.md).
  - [ ] Còn để nghiệm thu: Báo giá/SLA và số liệu workload cần nhóm xác nhận.
- [ ] **W1-TV1-05** - Rà soát G1 cùng cả nhóm: dữ kiện/giả định, IP, sizing, chi phí, rủi ro công cụ; chốt Packet Tracer hoặc GNS3 và ghi mục nào chỉ thiết kế. **Hạn 01/11; đầu ra:** biên bản G1 và baseline được duyệt.
  - [x] Sản phẩm đã có: [meeting-notes.md](docs/00-management/meeting-notes.md).
  - [ ] Còn để nghiệm thu: Chưa có biên bản G1 được nhóm xác nhận.

### TV2 - LAN & Wireless Engineer

- [ ] **W1-TV2-01** - Lập kiến trúc LAN A/B **mỗi tòa 5 tầng × 10 phòng**, phòng trung tâm cách **50 m**; mỗi Aux **2 tầng, IT/CCL ở tầng 1**. Phân biệt vị trí vật lý với nhóm VLAN nghiệp vụ. **Hạn 28/10; đầu ra:** sơ đồ logic và mặt bằng giả định có nhãn.
  - [x] Sản phẩm đã có: [physical-main.drawio](docs/02-design/diagrams/physical-main.drawio).
  - [ ] Còn để nghiệm thu: Mặt bằng là giả định; chờ đọc chéo.
- [ ] **W1-TV2-02** - Phân bổ VLAN phòng ban/SSID và cổng trunk/access cho **600 PC Main, 260 PC mỗi Aux**; phối hợp TV1 kiểm host, DHCP và dự phòng. **Hạn 29/10; đầu ra:** bảng VLAN/port và nhận xét IP plan.
  - [x] Sản phẩm đã có: [lan-port-plan.md](docs/02-design/lan-port-plan.md).
  - [ ] Còn để nghiệm thu: TV2 xác nhận IP/port plan.
- [ ] **W1-TV2-03** - Thiết kế GPON/Ethernet: MDF/IDF, patch panel/ODF, tuyến quang/cáp đồng, OLT/splitter/ONT nếu dùng GPON, 1/10/40GbE theo tầng mạng. **Hạn 30/10; đầu ra:** `physical-cabling.md` và sơ đồ nguồn.
  - [x] Sản phẩm đã có: [physical-cabling.md](docs/02-design/physical-cabling.md).
  - [ ] Còn để nghiệm thu: GPON/quang là thiết kế; chưa khảo sát.
- [ ] **W1-TV2-04** - Lập BOM/spec và port/PoE/uplink budget hiện tại/5 năm; không giới hạn Main ở 12 thiết bị nếu số cổng không đủ; phối hợp TV3 tính camera/NVR và server/DMZ. **Hạn 30/10; đầu ra:** `equipment-bom.md`, phần cáp/PoE trong `camera-plan.md`.
  - [x] Sản phẩm đã có: [equipment-bom.md](docs/02-design/equipment-bom.md).
  - [ ] Còn để nghiệm thu: Chờ giá/model/khảo sát và đọc chéo.
- [ ] **W1-TV2-05** - Quy hoạch Wi-Fi phủ Main, kiểm nhu cầu Aux; tách nhân viên/khách, dự kiến AP theo RF/dung lượng, không tự gán số khách; đọc chéo baseline G1. **Hạn 01/11; đầu ra:** `wireless-plan.md`, sơ đồ SSID/VLAN và vùng cần khảo sát.
  - [x] Sản phẩm đã có: [wireless-plan.md](docs/02-design/wireless-plan.md).
  - [ ] Còn để nghiệm thu: Chưa đo RF/AAA/roaming; chờ G1.

### TV3 - Security & Systems Specialist

- [ ] **W1-TV3-01** - Phân bổ vai trò **10 server Main, 2 server mỗi Aux**, tách Server Farm/DMZ; ghi DHCP/DNS, HIS/RIS-PACS/LIS/CRM/database/backup và IP tĩnh. **Hạn 29/10; đầu ra:** `server-dmz-plan.md`.
  - [x] Sản phẩm đã có: [server-dmz-plan.md](docs/02-design/server-dmz-plan.md).
  - [ ] Còn để nghiệm thu: Chờ xác nhận chuyên môn.
- [ ] **W1-TV3-02** - Lập ma trận nguồn-đích-dịch vụ cho liên VLAN, DMZ, quản trị, Wi-Fi khách; đặt firewall/ACL và ranh giới chính sách, chặn guest tới LAN ở cả 3 site. **Hạn 29/10; đầu ra:** `docs/04-security/security-policy.md`.
  - [x] Sản phẩm đã có: [security-policy.md](docs/04-security/security-policy.md).
  - [ ] Còn để nghiệm thu: Chờ đọc chéo quyền nghiệp vụ.
- [ ] **W1-TV3-03** - Thiết kế PAT tại Main cho tất cả site, hai egress xDSL, static PAT DMZ và NAT exemption cho luồng nội bộ/VPN; đối chiếu inside/outside và các lỗi/caveat của [R]. **Hạn 30/10; đầu ra:** `nat-pat.md`.
  - [x] Sản phẩm đã có: [nat-pat.md](docs/04-security/nat-pat.md).
  - [ ] Còn để nghiệm thu: Chờ đọc chéo; IOS chưa chạy.
- [ ] **W1-TV3-04** - Đề xuất site-to-site VPN và teleworker VPN; đánh giá firewall/IDS/IPS/chống phishing/HA, khả năng chạy trên công cụ và điều kiện chương trình kỹ sư tài năng. **Hạn 30/10; đầu ra:** `vpn-plan.md`, `ids-ips-plan.md`, danh sách chức năng chạy/thiết kế.
  - [x] Sản phẩm đã có: [vpn-plan.md](docs/04-security/vpn-plan.md).
  - [ ] Còn để nghiệm thu: VPN crypto DESIGN ONLY; IDS/IPS có rule mẫu GNS3.
- [ ] **W1-TV3-05** - Cùng TV2 thiết kế camera VLAN/quyền xem/NVR/bitrate/lưu trữ; soạn khung security best practices và đọc chéo G1. **Hạn 01/11; đầu ra:** `camera-plan.md`, `security-best-practices.md` bản đầu.
  - [x] Sản phẩm đã có: [camera-plan.md](docs/02-design/camera-plan.md).
  - [ ] Còn để nghiệm thu: Camera/bitrate/retention là giả định; chờ TV2/G1.

### TV4 - Simulation & Testing Lead

- [ ] **W1-TV4-01** - Lập đầu vào Step 3: 1.120 workstation/14 server, tải PC 500/100 MB, server 1.000/2.000 MB theo các cách hiểu, Wi-Fi 500 MB và số khách chưa biết; ghi nguồn/giả định. **Hạn 28/10; đầu ra:** `docs/03-capacity/assumptions.md`, `capacity-inputs.csv`.
  - [x] Sản phẩm đã có: [assumptions.md](docs/03-capacity/assumptions.md).
  - [ ] Còn để nghiệm thu: Workload/khách/Internet share chờ xác nhận.
- [ ] **W1-TV4-02** - Tính riêng down/up cho site và tổng: **80% tải trong 09:00-11:00 + 15:00-16:00 = 3 giờ**, tăng trưởng tổng 20%; làm rõ MB/Mbps, overhead/headroom và tỷ lệ LAN/WAN/Internet. **Hạn 29/10; đầu ra:** `throughput.md`; chuyển kết quả sớm cho TV1/TV2.
  - [x] Sản phẩm đã có: [throughput.md](docs/03-capacity/throughput.md).
  - [ ] Còn để nghiệm thu: 6 nhóm unit số học có; chờ xác nhận giả định.
- [ ] **W1-TV4-03** - Đề xuất băng thông ISP/leased line theo biến khách, từng chiều và tải quan trọng khi hỏng một xDSL; không tự khẳng định gói xDSL đủ tốc độ. **Hạn 30/10; đầu ra:** bảng kịch bản năng lực và khoảng thiếu.
  - [x] Sản phẩm đã có: [wan-options-cost.md](docs/02-design/wan-options-cost.md).
  - [ ] Còn để nghiệm thu: Không khẳng định xDSL thương mại đủ tải.
- [ ] **W1-TV4-04** - Thử khả năng thiết bị/phần mềm cần dùng trước khi khóa công cụ; dựng skeleton Main/DBP/BHTQ, mapping node/interface và lịch bàn giao module. **Hạn 30/10; đầu ra:** `simulation/README.md`, `integration-log.md`, khung mô phỏng.
  - [x] Sản phẩm đã có: [hospital-3sites.gns3](simulation/gns3/hospital-3sites.gns3).
  - [ ] Còn để nghiệm thu: GNS3 có52 node; Packet Tracer đang dựng riêng.
- [ ] **W1-TV4-05** - Soạn ma trận **TC01-TC06** cùng các test DHCP/dual ISP/VPN bổ sung; đặt expected, precondition, mẫu evidence và trạng thái NOT RUN; kiểm G1. **Hạn 01/11; đầu ra:** `test_results/test-matrix.md`.
  - [x] Sản phẩm đã có: [test-matrix.md](test_results/test-matrix.md).
  - [ ] Còn để nghiệm thu: TC01–06 có GNS3 evidence; chờ G1.

### TV5 - Documentation & Report Specialist, chủ trì báo cáo

- [ ] **W1-TV5-01** - Chủ trì phân tích Step 1 và checklist khảo sát: phòng/tầng, MDF/IDF, điện/UPS, cáp, RF, vùng đông người, ứng dụng, camera, nhà mạng/SLA; ghi rõ phần chưa khảo sát. **Hạn 28/10; đầu ra:** `survey-checklist.md`, `site-requirements.md`.
  - [x] Sản phẩm đã có: [survey-checklist.md](docs/01-survey/survey-checklist.md).
  - [ ] Còn để nghiệm thu: Có checklist; chưa khảo sát thực địa.
- [ ] **W1-TV5-02** - Lập bảng truy vết **7 Step và điểm 1-1-1-2-2-2-1**, nguồn trang PDF, chủ trì, đầu ra và tiêu chí nghiệm thu; ghi thay đổi nhóm 5 người/lịch 2026/không slide. **Hạn 29/10; đầu ra:** `requirements-traceability.md`.
  - [x] Sản phẩm đã có: [requirements-traceability.md](docs/00-management/requirements-traceability.md).
  - [ ] Còn để nghiệm thu: Đã có danh sách nhóm và phân công BTL2 hai người; hạn BKeL vẫn cần đối chiếu.
- [ ] **W1-TV5-03** - Lập đề cương báo cáo, quy ước font, heading, bảng/hình, nguồn và template phần đóng góp; thống nhất nơi nhận nội dung TV1-TV4. **Hạn 29/10; đầu ra:** `docs/06-report/source/`, `contributions/` và lịch thu thập.
  - [x] Sản phẩm đã có: [README.md](docs/06-report/source/README.md).
  - [ ] Còn để nghiệm thu: Nguồn Markdown/LaTeX và5 contributions đã có; chờ nhóm.
- [ ] **W1-TV5-04** - Thu thập kết quả khảo sát/thiết kế/tính toán của từng người, viết bản thô đầu tiên phần giới thiệu và Step 1-3, kiểm nhất quán quy mô và thuật ngữ bệnh viện. **Hạn 31/10; đầu ra:** `docs/06-report/draft/` bản 0.1.
  - [x] Sản phẩm đã có: [report.tex](docs/06-report/latex/report.tex).
  - [ ] Còn để nghiệm thu: Bản hiện tại thay bản nháp lịch sử0.1; chưa có biên bản phát hành cũ.
- [ ] **W1-TV5-05** - Chuẩn bị khung đánh giá Step 6 theo tin cậy, nâng cấp, phần mềm, an toàn/bảo mật; tổng hợp vướng mắc G1 và phát hành biên bản để TV1 duyệt. **Hạn 01/11; đầu ra:** `evaluation.md`, `risks.md`, meeting notes.
  - [x] Sản phẩm đã có: [evaluation.md](docs/05-evaluation/evaluation.md).
  - [ ] Còn để nghiệm thu: Có evaluation/risks; G1 chưa xác nhận.

**Cổng G1 - 01/11:** TV1 xác nhận kiến trúc/IP, TV2 xác nhận port/cabling/Wi-Fi, TV3 xác nhận vùng bảo mật, TV4 xác nhận tính tải và khả năng công cụ, TV5 xác nhận truy vết/bản thô. Nếu chưa có báo giá/khảo sát thực địa, danh mục chờ xác nhận phải có chủ trì và hạn.

## Giai đoạn 2 - Mô phỏng cơ bản

**Tuần 2: 02/11/2026 - 08/11/2026, đúng 7 ngày.** Trọng tâm Step 4, kiểm thử smoke test Step 5. Module/config giao cho TV4 trước hoặc trong ngày 05/11; tích hợp và sửa lỗi 06/11-08/11.

### TV1 - Trưởng nhóm, WAN & Routing Lead

- [ ] **W2-TV1-01** - Cấu hình kết nối Main-DBP/Main-BHTQ và OSPF, quảng bá subnet cần thiết, default hướng Main; ghi route chiều về và điều kiện quảng bá default. **Hạn 04/11; đầu ra:** module WAN và `configs/main/`, `configs/dbp/`, `configs/bhtq/` phần routing.
  - [x] Sản phẩm đã có: [result.md](test_results/TC03-inter-site/result.md).
  - [ ] Còn để nghiệm thu: OSPF GNS3 đã chạy; IOS/Packet Tracer chưa chạy.
- [ ] **W2-TV1-02** - Dựng Internet edge hai xDSL/ISP lab, cơ chế phân phối luồng và dự phòng theo thiết bị hỗ trợ; phối hợp TV3 gắn NAT đúng egress. **Hạn 05/11; đầu ra:** cấu hình edge/ISP, mô tả phần mô hình hóa so với xDSL thật.
  - [x] Sản phẩm đã có: [dual-isp-failover.md](test_results/supplemental/dual-isp-failover.md).
  - [ ] Còn để nghiệm thu: PBR/NAT upstream GNS3 đã chạy; CLI Packet Tracer cần thử.
- [ ] **W2-TV1-03** - Giao module/config, sơ đồ interface và thứ tự nạp cho TV4; hỗ trợ ghép route với LAN/firewall, sửa loop/blackhole và ngăn local breakout tại Aux. **Hạn 06/11; đầu ra:** module WAN được tích hợp, integration log.
  - [x] Sản phẩm đã có: [integration-log.md](simulation/integration-log.md).
  - [ ] Còn để nghiệm thu: Mô hình tổng GNS3 đã tích hợp; chờ TV4 xác nhận bàn giao.
- [ ] **W2-TV1-04** - Kiểm tra route/OSPF neighbor, ping/traceroute Main↔DBP và Main↔BHTQ; bổ sung phương án chi phí và quyết định WAN sau phản hồi nhóm. **Hạn 07/11; đầu ra:** smoke log WAN và `wan-options-cost.md` cập nhật.
  - [x] Sản phẩm đã có: [results.json](test_results/runtime/after-firewall-restart-runtime/results.json).
  - [ ] Còn để nghiệm thu: Có route/OSPF/ping/traceroute; chi phí thật chờ xác nhận.
- [ ] **W2-TV1-05** - Rà soát tiến độ/PR và G2; xác nhận file tổng 3 site mở lại được, baseline routing và Internet qua Main nhất quán. **Hạn 08/11; đầu ra:** biên bản G2 và phần đóng góp WAN/routing bản đầu.
  - [x] Sản phẩm đã có: [persistence.md](test_results/supplemental/persistence.md).
  - [ ] Còn để nghiệm thu: Có reopen lịch sử; biên bản G2 chờ nhóm.

### TV2 - LAN & Wireless Engineer

- [ ] **W2-TV2-01** - Dựng access/distribution/core đại diện A/B, VLAN, trunk/access, SVI hoặc router-on-a-stick theo baseline; đánh nhãn tầng/phòng/port. **Hạn 04/11; đầu ra:** module LAN Main và cấu hình switch.
  - [x] Sản phẩm đã có: [README.md](simulation/modules/tv2-lan-wireless/README.md).
  - [ ] Còn để nghiệm thu: Main .pkt gốc là module một phần; bản tổng Packet Tracer chưa có.
- [ ] **W2-TV2-02** - Dựng LAN DBP và BHTQ, VLAN và uplink 2 tầng; ghi bảng ánh xạ PC đại diện sang quy mô 260 máy mỗi site. **Hạn 04/11; đầu ra:** module Aux và sơ đồ vật lý tương ứng.
  - [x] Sản phẩm đã có: [hospital-3sites.gns3](simulation/gns3/hospital-3sites.gns3).
  - [ ] Còn để nghiệm thu: Aux GNS3 đã có; Aux Packet Tracer chưa dựng.
- [ ] **W2-TV2-03** - Cấu hình DHCP/relay cùng TV3, SSID nhân viên/khách và VLAN tương ứng theo khả năng công cụ; kiểm địa chỉ/gateway đúng subnet, không chép gateway DiAn lỗi từ [R]. **Hạn 05/11; đầu ra:** LAN/Wi-Fi module và bảng pool.
  - [x] Sản phẩm đã có: [dhcp-dns.md](test_results/supplemental/dhcp-dns.md).
  - [ ] Còn để nghiệm thu: Đủ18 pool trong GNS3; SSID/RF Packet Tracer chưa thử.
- [ ] **W2-TV2-04** - Giao module/config cho TV4, kiểm trunk, VLAN, DHCP và smoke test cùng/khác VLAN; điều chỉnh port/PoE/BOM theo topology thực tế. **Hạn 07/11; đầu ra:** log LAN, module được tích hợp, BOM/cabling cập nhật.
  - [x] Sản phẩm đã có: [result.md](test_results/TC01-same-vlan/result.md).
  - [ ] Còn để nghiệm thu: LAN GNS3 có test; bàn giao TV2/G2 chưa xác nhận.
- [ ] **W2-TV2-05** - Hoàn thiện sơ đồ logic/vật lý/cabling nguồn có thể sửa và bản xuất; viết nội dung LAN/Wi-Fi/BOM cho TV5 và đọc chéo G2. **Hạn 08/11; đầu ra:** `TV2-lan-wireless.md`, diagrams và tham số cấu hình.
  - [x] Sản phẩm đã có: [TV2-lan-wireless.md](docs/06-report/contributions/TV2-lan-wireless.md).
  - [ ] Còn để nghiệm thu: Có drawio/SVG/contribution; G2 chờ nhóm.

### TV3 - Security & Systems Specialist

- [ ] **W2-TV3-01** - Dựng Server Farm/DMZ đại diện theo phân bổ 10/2/2, cấu hình IP tĩnh, DHCP/DNS/HTTP cần thiết; ghi cách đại diện ứng dụng bệnh viện chưa mô phỏng được. **Hạn 04/11; đầu ra:** module server/security, `server-dmz-plan.md` cập nhật.
  - [x] Sản phẩm đã có: [server-dmz-plan.md](docs/02-design/server-dmz-plan.md).
  - [ ] Còn để nghiệm thu: 14 server10/2/2 trong GNS3; clinical apps chỉ HTTP đại diện.
- [ ] **W2-TV3-02** - Cấu hình PAT cơ bản tại Main cho các subnet được phép ở cả 3 site; phối hợp TV1 bảo đảm inside/outside và egress/route chiều về đúng. **Hạn 05/11; đầu ra:** cấu hình NAT và bảng kiểm lệnh.
  - [x] Sản phẩm đã có: [result.md](test_results/TC06-internet-web/result.md).
  - [ ] Còn để nghiệm thu: PAT GNS3 có evidence; IOS chưa chạy.
- [ ] **W2-TV3-03** - Cấu hình static PAT dịch vụ DMZ và rule cho dịch vụ được phép; dựng khung firewall/zone/ACL, tách rule NAT khỏi rule bảo mật. **Hạn 05/11; đầu ra:** module DMZ/firewall và ma trận dịch vụ được công bố.
  - [x] Sản phẩm đã có: [result.md](test_results/TC04-dmz/result.md).
  - [ ] Còn để nghiệm thu: DMZ/static PAT GNS3 có evidence; IOS chưa chạy.
- [ ] **W2-TV3-04** - Giao module/config cho TV4; kiểm HTTP, bảng NAT và luồng liên site không bị NAT ngoài ý muốn; sửa xung đột ACL/routing trước hardening tuần 3. **Hạn 07/11; đầu ra:** smoke log NAT/DMZ, integration log.
  - [x] Sản phẩm đã có: [integration-log.md](simulation/integration-log.md).
  - [ ] Còn để nghiệm thu: Có log tích hợp GNS3; chờ xác nhận TV4.
- [ ] **W2-TV3-05** - Viết phần Server Farm/DMZ/NAT ban đầu cho TV5, cập nhật kế hoạch VPN/IDS/IPS theo công cụ thực tế và tham gia G2. **Hạn 08/11; đầu ra:** `TV3-security-systems.md`, kế hoạch bảo mật bản cập nhật.
  - [x] Sản phẩm đã có: [TV3-security-systems.md](docs/06-report/contributions/TV3-security-systems.md).
  - [ ] Còn để nghiệm thu: Contribution có; VPN crypto DESIGN ONLY; chờ G2.

### TV4 - Simulation & Testing Lead

- [ ] **W2-TV4-01** - Chuẩn bị file mô phỏng tổng, đặt tên node/port/site, nhãn VLAN/subnet; thống nhất bàn giao module và giữ lịch chỉnh file `.pkt` để tránh ghi đè. **Hạn 03/11; đầu ra:** khung tổng và integration log.
  - [x] Sản phẩm đã có: [hospital-3sites.gns3](simulation/gns3/hospital-3sites.gns3).
  - [ ] Còn để nghiệm thu: File tổng GNS3 có; Packet Tracer chưa có native tổng.
- [ ] **W2-TV4-02** - Nhận và ghép LAN/Server/WAN Main, DBP, BHTQ; kiểm mapping interface, subnet, router ID, trunk và kết nối ISP/Web lab. **Hạn 06/11; đầu ra:** `hospital-3sites.pkt` hoặc project GNS3 tích hợp.
  - [x] Sản phẩm đã có: [runtime-manifest.json](simulation/gns3/runtime-manifest.json).
  - [ ] Còn để nghiệm thu: 52 node/52 link GNS3; Packet Tracer assembly chỉ đầu vào.
- [ ] **W2-TV4-03** - Chạy smoke test DHCP/VLAN, route 3 site, Web qua Main và NAT; tạo issue kèm bước tái hiện cho lỗi, phân người sửa và chạy lại sau ghép. **Hạn 07/11; đầu ra:** log tích hợp, danh sách lỗi và test matrix cập nhật.
  - [x] Sản phẩm đã có: [README.md](test_results/runtime/README.md).
  - [ ] Còn để nghiệm thu: Smoke GNS3 có actual/log; không phải lần chạy mới trên Windows.
- [ ] **W2-TV4-04** - Ghi phiên bản phần mềm/model và cách mở lại, PC/server đại diện, chức năng mô hình hóa hoặc không hỗ trợ; đối chiếu thiết bị với bảng tính thông lượng. **Hạn 07/11; đầu ra:** `simulation/README.md`, capacity/config notes.
  - [x] Sản phẩm đã có: [README.md](simulation/gns3/README.md).
  - [ ] Còn để nghiệm thu: Version2.2.55/Linux/FRR và giới hạn đã ghi.
- [ ] **W2-TV4-05** - Lưu file, mở lại để kiểm persistence, đóng baseline G2 và chuyển nội dung tính tải/triển khai cho TV5. **Hạn 08/11; đầu ra:** file tổng có phiên bản, `TV4-capacity-testing.md` bản đầu, biên bản kiểm mở lại.
  - [x] Sản phẩm đã có: [reopen.json](test_results/runtime/persistence/reopen.json).
  - [ ] Còn để nghiệm thu: Reopen137 kiểm là lịch sử trước sửa PID; G2 chờ nhóm.

### TV5 - Documentation & Report Specialist, chủ trì báo cáo

- [ ] **W2-TV5-01** - Thu nội dung TV1-TV4 theo template, rà soát nguồn/tham số, phát hiện chỗ lệch IP/VLAN/số máy và lập danh sách cần bổ sung. **Hạn 05/11; đầu ra:** contributions và sổ thiếu nội dung có người xử lý.
  - [x] Sản phẩm đã có: [TV1-wan-routing.md](docs/06-report/contributions/TV1-wan-routing.md).
  - [ ] Còn để nghiệm thu: Đủ5 contribution; chưa có xác nhận giao nhận cá nhân.
- [ ] **W2-TV5-02** - **Chủ trì tổng hợp báo cáo thô**: Step 1-3 hoàn chỉnh và Step 4 bản đầu; chèn sơ đồ, BOM và công thức có giả định, không ghi smoke test là test nghiệm thu cuối. **Hạn 07/11; đầu ra:** báo cáo thô 0.2 trong `draft/`.
  - [x] Sản phẩm đã có: [report.tex](docs/06-report/latex/report.tex).
  - [ ] Còn để nghiệm thu: Báo cáo hiện tại thay nháp0.2; không tạo giả ngày phát hành cũ.
- [ ] **W2-TV5-03** - Chuẩn hóa heading, mục lục, số bảng/hình, thuật ngữ và danh mục tài liệu; yêu cầu người có chuyên môn xác nhận nội dung trước khi ghép. **Hạn 07/11; đầu ra:** nguồn báo cáo có định dạng thống nhất và review log.
  - [x] Sản phẩm đã có: [README.md](docs/06-report/latex/README.md).
  - [ ] Còn để nghiệm thu: Có heading/mục lục/font/QA12 trang; chờ chuyên môn.
- [ ] **W2-TV5-04** - Cập nhật Step 6 sơ bộ: SPOF, hạn chế 2 leased lines không dự phòng chéo, năng lực xDSL, tương thích phần mềm và khoảng cách thiết kế/mô phỏng. **Hạn 08/11; đầu ra:** `evaluation.md`, `risks.md` bản 0.2.
  - [x] Sản phẩm đã có: [risks.md](docs/05-evaluation/risks.md).
  - [ ] Còn để nghiệm thu: Có SPOF/xDSL/phần mềm/giới hạn; chờ G2.
- [ ] **W2-TV5-05** - Tổng hợp tiến độ G2, kiểm đầy đủ truy vết 7 Step và hướng dẫn mở file; gửi bản thô cho TV1 rà soát. **Hạn 08/11; đầu ra:** báo cáo thô, biên bản G2 và issue tuần 3.
  - [x] Sản phẩm đã có: [requirements-traceability.md](docs/00-management/requirements-traceability.md).
  - [ ] Còn để nghiệm thu: Đủ truy vết/hướng dẫn; G2 chưa họp/xác nhận.

**Cổng G2 - 08/11:** Mô phỏng 3 site mở lại được, định tuyến và Internet tập trung hoạt động ở mức cơ bản; config và báo cáo thô khớp topology. Các test chính thức về security/load balancing sẽ có bằng chứng ở G3; không tích xong nếu baseline còn lỗi chặn tích hợp.

## Giai đoạn 3 - Bảo mật & Kiểm thử

**Tuần 3: 09/11/2026 - 15/11/2026, đúng 7 ngày.** Trọng tâm Step 5 và phần bảo mật, cung cấp dữ liệu Step 6. Khóa cấu hình test ban đầu 11/11; thực hiện 12/11-14/11; nghiệm thu bằng chứng 15/11.

### TV1 - Trưởng nhóm, WAN & Routing Lead

- [ ] **W3-TV1-01** - Hoàn thiện OSPF và route/default có điều kiện, kiểm hai chiều giữa Main với cả DBP/BHTQ; hỗ trợ TV4 chạy **TC03** đủ hai chi nhánh. **Hạn 12/11; đầu ra:** config routing cuối và log TC03.
  - [x] Sản phẩm đã có: [result.md](test_results/TC03-inter-site/result.md).
  - [ ] Còn để nghiệm thu: Đủ Main↔DBP/BHTQ trong GNS3; IOS chưa thử.
- [ ] **W3-TV1-02** - Kiểm chứng load balancing bằng nhiều phiên qua hai xDSL và NAT đúng egress; ngắt từng tuyến, ghi khả năng tạo phiên mới, phiên cũ bị ảnh hưởng và giới hạn SLA. **Hạn 13/11; đầu ra:** test bổ sung dual ISP trong `supplemental/`.
  - [x] Sản phẩm đã có: [dual-isp-failover.md](test_results/supplemental/dual-isp-failover.md).
  - [ ] Còn để nghiệm thu: Có upstream fault/convergence; local-link/session cũ chưa thử.
- [ ] **W3-TV1-03** - Cùng TV3/TV4 kiểm Internet của tất cả site qua Main, default chiều về, route VPN và các lỗi routing phát hiện khi ACL bật. **Hạn 14/11; đầu ra:** cấu hình sửa lỗi, log retest liên quan TC03/TC06.
  - [x] Sản phẩm đã có: [result.md](test_results/TC06-internet-web/result.md).
  - [ ] Còn để nghiệm thu: Web3 site/PAT có; VPN crypto chưa chạy.
- [ ] **W3-TV1-04** - Rà soát kỹ thuật và bằng chứng 6 nhóm test, phân biệt triển khai thật/mô hình hóa/design only, theo dõi lỗi chặn và chủ trì xử lý. **Hạn 15/11; đầu ra:** biên bản G3 và danh sách lỗi được phân loại.
  - [x] Sản phẩm đã có: [project-review.md](docs/00-management/project-review.md).
  - [ ] Còn để nghiệm thu: Có review kỹ thuật; G3/đọc chéo nhóm chưa xác nhận.
- [ ] **W3-TV1-05** - Giao phần WAN/IP/OSPF/load balancing/chi phí đã hoàn chỉnh cho TV5; đánh giá khả năng chịu lỗi và nâng cấp 5 năm với giả định đã duyệt. **Hạn 15/11; đầu ra:** `TV1-wan-routing.md` và nhận xét Step 6.
  - [x] Sản phẩm đã có: [TV1-wan-routing.md](docs/06-report/contributions/TV1-wan-routing.md).
  - [ ] Còn để nghiệm thu: Có nội dung/tải/chi phí/SPOF; giả định và bàn giao chờ nhóm.

### TV2 - LAN & Wireless Engineer

- [ ] **W3-TV2-01** - Chuẩn bị và phối hợp chạy **TC01** cùng VLAN, **TC02** khác VLAN theo ma trận cho phép; dùng PC ở switch khác nhau khi có, kiểm SVI/trunk/DHCP. **Hạn 12/11; đầu ra:** config LAN ổn định và log/đầu vào bằng chứng cho TV4.
  - [x] Sản phẩm đã có: [result.md](test_results/TC01-same-vlan/result.md).
  - [ ] Còn để nghiệm thu: TC01/TC02 GNS3 có log; Packet Tracer chưa chạy.
- [ ] **W3-TV2-02** - Kiểm SSID/VLAN nhân viên và khách, DHCP/gateway/DNS; phối hợp TV3 bảo đảm khách không nối nhầm VLAN nội bộ và cung cấp máy khách từng site cho **TC05/TC06**. **Hạn 12/11; đầu ra:** bảng SSID/VLAN và precondition test.
  - [x] Sản phẩm đã có: [dhcp-dns.md](test_results/supplemental/dhcp-dns.md).
  - [ ] Còn để nghiệm thu: VLAN/DHCP/DNS GNS3 có; WLAN association/RF chưa thử.
- [ ] **W3-TV2-03** - Sửa lỗi LAN/Wi-Fi từ test tích hợp; rà soát port budget, PoE, uplink và dư địa 20%, đối chiếu sơ đồ vật lý với file mô phỏng. **Hạn 14/11; đầu ra:** config/sơ đồ/BOM đồng bộ, log retest.
  - [x] Sản phẩm đã có: [campus-budget.csv](docs/02-design/campus-budget.csv).
  - [ ] Còn để nghiệm thu: Port/PoE/growth và sơ đồ đồng bộ; RF chưa thử.
- [ ] **W3-TV2-04** - Cùng TV3 kiểm thiết kế camera, VLAN/quyền NVR và nhu cầu băng thông/lưu trữ; tách thông số chưa khảo sát khỏi kết quả chạy trong mô phỏng. **Hạn 14/11; đầu ra:** `camera-plan.md` và nhận xét tính khả thi.
  - [x] Sản phẩm đã có: [camera-plan.md](docs/02-design/camera-plan.md).
  - [ ] Còn để nghiệm thu: Camera/NVR/storage là thiết kế; chưa đo bitrate thực.
- [ ] **W3-TV2-05** - Bàn giao phần LAN/Wi-Fi/BOM/cabling chính thức và ảnh sơ đồ rõ chữ cho TV5; đọc chéo tiêu chí nâng cấp, reliability và G3. **Hạn 15/11; đầu ra:** `TV2-lan-wireless.md` hoàn chỉnh và nhận xét Step 6.
  - [x] Sản phẩm đã có: [TV2-lan-wireless.md](docs/06-report/contributions/TV2-lan-wireless.md).
  - [ ] Còn để nghiệm thu: Nguồn/hình có; bàn giao/đọc chéo G3 chờ nhóm.

### TV3 - Security & Systems Specialist

- [ ] **W3-TV3-01** - Hoàn thiện firewall/ACL theo ma trận quyền, ưu tiên chặn guest tới PC/server/quản trị/liên site nhưng cho DHCP/DNS và Internet cần thiết; lưu đúng hướng/interface áp rule. **Hạn 11/11; đầu ra:** config hardening và `security-policy.md`.
  - [x] Sản phẩm đã có: [result.md](test_results/TC05-guest-isolation/result.md).
  - [ ] Còn để nghiệm thu: Guest ACL/firewall/DNS/Web GNS3 có; IOS chưa chạy.
- [ ] **W3-TV3-02** - Phối hợp chạy **TC04** dịch vụ DMZ, thêm đường truy cập từ ngoài qua static PAT khi công bố; chụp translation và firewall hit, giải thích đổi địa chỉ/cổng theo [R]. **Hạn 12/11; đầu ra:** cấu hình DMZ/NAT và evidence đầu vào cho TV4.
  - [x] Sản phẩm đã có: [result.md](test_results/TC04-dmz/result.md).
  - [ ] Còn để nghiệm thu: DMZ/published service/NAT có log GNS3.
- [ ] **W3-TV3-03** - Phối hợp chạy **TC05**: guest không tới LAN, gồm ICMP và TCP tới host đang hoạt động; thêm ca đối chứng guest vẫn ra Web ngoài, internal vẫn dùng được dịch vụ. **Hạn 13/11; đầu ra:** ACL hit/log và test negative/positive ở các site có guest.
  - [x] Sản phẩm đã có: [result.md](test_results/TC05-guest-isolation/result.md).
  - [ ] Còn để nghiệm thu: ICMP/TCP âm+dương và DROP counters có ở3 site GNS3.
- [ ] **W3-TV3-04** - Triển khai/test site-to-site và teleworker VPN trong khả năng nền tảng; thử firewall/IDS/IPS nếu áp dụng yêu cầu kỹ sư tài năng, ghi rõ phần chưa chạy và cách khắc phục bằng công cụ phù hợp. **Hạn 14/11; đầu ra:** `supplemental/` và hồ sơ VPN/IDS/IPS.
  - [x] Sản phẩm đã có: [vpn.md](test_results/supplemental/vpn.md).
  - [ ] Còn để nghiệm thu: VPN crypto/HA chưa chạy; IDS/IPS rule mẫu có.
- [ ] **W3-TV3-05** - Hoàn thiện security best practices: SSH/AAA, secrets, log/NTP, backup/restore, cập nhật, chống phishing và phân quyền camera; giao nội dung/bằng chứng bảo mật cho TV5 và G3. **Hạn 15/11; đầu ra:** `TV3-security-systems.md`, security guide và đánh giá rủi ro.
  - [x] Sản phẩm đã có: [security-best-practices.md](docs/04-security/security-best-practices.md).
  - [ ] Còn để nghiệm thu: Có guide/contribution; AAA/NTP/backup thực chưa thử đủ.

### TV4 - Simulation & Testing Lead

- [ ] **W3-TV4-01** - Khóa phiên bản chạy test, xác nhận precondition/expected, định danh node/IP/VLAN và trạng thái ban đầu; cập nhật công thức tải khi có thay đổi đã được duyệt. **Hạn 11/11; đầu ra:** test matrix gắn phiên bản, capacity baseline cuối.
  - [x] Sản phẩm đã có: [runtime-manifest.json](simulation/gns3/runtime-manifest.json).
  - [ ] Còn để nghiệm thu: Có source/live/project hashes; bản sinh portable giữ nguyên runtime bytes.
- [ ] **W3-TV4-02** - Điều phối chạy và lưu ảnh/log **TC01 cùng VLAN, TC02 liên VLAN, TC03 liên site với cả DBP và BHTQ**; nhận xác nhận chuyên môn TV2/TV1. **Hạn 13/11; đầu ra:** `TC01-*/`, `TC02-*/`, `TC03-*/` có result và bằng chứng.
  - [x] Sản phẩm đã có: [results.json](test_results/runtime/after-firewall-restart-runtime/results.json).
  - [ ] Còn để nghiệm thu: TC01–03 actual có; chờ TV1/TV2 chuyên môn.
- [ ] **W3-TV4-03** - Điều phối **TC04 DMZ, TC05 cô lập khách, TC06 Web Internet qua Main từ mỗi site**; chụp NAT/PDU theo [R], lưu negative/positive control, không chỉ ảnh ping. **Hạn 14/11; đầu ra:** `TC04-*/`, `TC05-*/`, `TC06-*/` đủ evidence.
  - [x] Sản phẩm đã có: [results.json](test_results/runtime/after-firewall-restart-runtime/results.json).
  - [ ] Còn để nghiệm thu: TC04–06 actual/PCAP có; chờ TV3 chuyên môn.
- [ ] **W3-TV4-04** - Chạy test bổ sung dual ISP/VPN/HA và IDS/IPS nếu hỗ trợ/yêu cầu; mở issue lỗi, ghép cấu hình sửa và retest liên quan, thống nhất trạng thái PASS/FAIL/NOT RUN. **Hạn 15/11; đầu ra:** test matrix, `supplemental/`, bug log và file mô phỏng cập nhật.
  - [x] Sản phẩm đã có: [README.md](test_results/supplemental/README.md).
  - [ ] Còn để nghiệm thu: ISP/IDS mẫu PASS GNS3; VPN/HA NOT RUN; PT đã có bộ 32 quan sát và bốn HTTP ISP thủ công riêng.
- [ ] **W3-TV4-05** - Mở lại file sau save, kiểm ảnh/log gắn đúng phiên bản; bàn giao bộ bằng chứng 6 nhóm test, giới hạn mô phỏng và phần Step 3-5 hoàn chỉnh cho TV5. **Hạn 15/11; đầu ra:** `TV4-capacity-testing.md`, manifest evidence và baseline G3.
  - [x] Sản phẩm đã có: [TV4-capacity-testing.md](docs/06-report/contributions/TV4-capacity-testing.md).
  - [ ] Còn để nghiệm thu: Có evidence/reopen/contribution; source PID mới chưa reopen lại trọn trên máy này.

### TV5 - Documentation & Report Specialist, chủ trì báo cáo

- [ ] **W3-TV5-01** - Theo dõi đủ 6 nhóm test, yêu cầu TV4 bổ sung caption/nguồn/đích/expected/actual và trạng thái; đồng bộ link tới evidence, không tự sửa kết quả kỹ thuật. **Hạn 14/11; đầu ra:** bảng truy vết test tới báo cáo.
  - [x] Sản phẩm đã có: [test-matrix.md](test_results/test-matrix.md).
  - [ ] Còn để nghiệm thu: Liên kết6 test tới evidence/report có; chờ TV4 xác nhận.
- [ ] **W3-TV5-02** - Thu phần hoàn chỉnh TV1-TV4, tổng hợp bản thô đầy đủ Step 1-5, chuẩn hóa chương tính tải, NAT và kiểm thử, ghi rõ dữ kiện/giả định/design only. **Hạn 15/11; đầu ra:** báo cáo thô 0.3 trong `draft/`.
  - [x] Sản phẩm đã có: [report.tex](docs/06-report/latex/report.tex).
  - [ ] Còn để nghiệm thu: Đủ Step1–5; bản hiện tại thay nháp0.3.
- [ ] **W3-TV5-03** - Chủ trì **Step 6**: dùng dữ liệu test để đánh giá tin cậy, nâng cấp, đa dạng phần mềm, an toàn/bảo mật; lập bảng yêu cầu → bằng chứng → kết luận/giới hạn. **Hạn 15/11; đầu ra:** `evaluation.md` có nhận xét thành viên kỹ thuật.
  - [x] Sản phẩm đã có: [evaluation.md](docs/05-evaluation/evaluation.md).
  - [ ] Còn để nghiệm thu: Có đánh giá Step6; chờ nhận xét thành viên.
- [ ] **W3-TV5-04** - Tổng hợp vấn đề còn lại và hướng phát triển: xDSL có thể thiếu tải, SPOF WAN, khảo sát Wi-Fi/camera, mở rộng 20%, HA, SD-WAN/MPLS và monitoring; chỉ rõ ưu tiên, ảnh hưởng, chủ trì. **Hạn 15/11; đầu ra:** `risks.md` và phần tương lai trong báo cáo.
  - [x] Sản phẩm đã có: [risks.md](docs/05-evaluation/risks.md).
  - [ ] Còn để nghiệm thu: Có vấn đề/hướng phát triển; giả định chờ xác nhận.
- [ ] **W3-TV5-05** - Kiểm thuật ngữ, nguồn trang, số bảng/hình và tính nhất quán báo cáo-topology-test; gửi bản thô đầy đủ cho TV1 rà soát và ghi quyết định G3. **Hạn 15/11; đầu ra:** review log và danh sách sửa tuần 4.
  - [x] Sản phẩm đã có: [review-log.md](docs/06-report/review-log.md).
  - [ ] Còn để nghiệm thu: Có QA kỹ thuật; G3 chưa có quyết định nhóm.

**Cổng G3 - 15/11:** Có hồ sơ cho cả TC01-TC06; mỗi kết quả có actual và bằng chứng. Lỗi FAIL/NOT RUN hoặc yêu cầu security chưa chạy phải được nêu công khai và có kế hoạch xử lý, không tuyên bố “đạt toàn bộ”. Nếu có lỗi chặn, ưu tiên sửa đầu tuần 4 trước khi phát hành bản cuối.

## Giai đoạn 4 - Tổng hợp Báo cáo & Đóng gói

**Tuần 4: 16/11/2026 - 22/11/2026, đúng 7 ngày.** Trọng tâm Step 6-7 và nghiệm thu. Chốt nội dung thành viên **17/11**, bản PDF để review **19/11**, xử lý phản hồi **20/11**, đóng gói/kiểm mở lại **21/11**, **TV1 duyệt chót cả báo cáo và mô phỏng 22/11**.

### TV1 - Trưởng nhóm, WAN & Routing Lead

- [ ] **W4-TV1-01** - Chốt phần IP/WAN/OSPF/dual xDSL, quyết định so sánh chi phí và nội dung đánh giá; bàn giao mọi bảng/hình/config còn thiếu cho TV5. **Hạn 17/11; đầu ra:** contribution TV1 cuối và baseline routing.
  - [x] Sản phẩm đã có: [TV1-wan-routing.md](docs/06-report/contributions/TV1-wan-routing.md).
  - [ ] Còn để nghiệm thu: Có nội dung cuối kỹ thuật; chờ chốt giả định/bàn giao.
- [ ] **W4-TV1-02** - Đọc chéo bản PDF tổng hợp do TV5 gửi, đối chiếu đủ 7 Step/điểm, 3 site, yêu cầu tăng trưởng, VPN/camera và 6 test; ghi nhận xét cụ thể theo trang/mục. **Hạn 19/11; đầu ra:** `docs/06-report/review-log.md`.
  - [x] Sản phẩm đã có: [review-log.md](docs/06-report/review-log.md).
  - [ ] Còn để nghiệm thu: QA trợ lý có; TV1 chưa xác nhận PDF.
- [ ] **W4-TV1-03** - Điều phối sửa lỗi chặn và quyết định xử lý giới hạn còn lại; đọc kết quả retest và kiểm phiên bản config/topology/report đồng bộ. **Hạn 20/11; đầu ra:** issue đã xử lý hoặc giới hạn được ghi rõ, xác nhận kỹ thuật trước đóng gói.
  - [x] Sản phẩm đã có: [project-review.md](docs/00-management/project-review.md).
  - [ ] Còn để nghiệm thu: Có giới hạn và retest GNS3; PT tổng có 32 quan sát sau reopen và bốn HTTP ISP thủ công; tự động failover/HA chưa kiểm trên PT.
- [ ] **W4-TV1-04** - **RÀ SOÁT / DUYỆT CHÓT riêng từng sản phẩm: báo cáo PDF và file mô phỏng**; đối chiếu bản mở lại, manifest/hash và bằng chứng trước khi ký. **Hạn 22/11; đầu ra:** `submission/approval.md` có phiên bản/hash của cả hai, kết luận G4.
  - [x] Hồ sơ chuẩn bị: [approval.md](submission/approval.md); chưa phải xác nhận phê duyệt.
  - [ ] Còn để nghiệm thu: PENDING TV1 duyệt riêng PDF và mô phỏng đúng hash.
- [ ] **W4-TV1-05** - Chốt quản lý release/bản ứng viên, phân người xử lý giai đoạn dự phòng và lịch khóa 06/12/nộp trước 11/12; không nộp nhầm bản chưa duyệt. **Hạn 22/11; đầu ra:** tag/release theo quyền repo, kế hoạch rà soát và nộp BKeL.
  - [x] Hồ sơ chuẩn bị: [manifest.md](submission/manifest.md); chưa phải xác nhận phê duyệt.
  - [ ] Còn để nghiệm thu: Gói ứng viên có; tag/release/quyền/nộp chờ nhóm.

### TV2 - LAN & Wireless Engineer

- [ ] **W4-TV2-01** - Giao nội dung và sơ đồ LAN/Wi-Fi/GPON-Ethernet/BOM cuối; kiểm port budget, tốc độ 1/10/40GbE, vị trí phòng trung tâm và hai Aux đúng đặc tả. **Hạn 17/11; đầu ra:** contribution, sơ đồ nguồn và ảnh xuất cuối.
  - [x] Sản phẩm đã có: [TV2-lan-wireless.md](docs/06-report/contributions/TV2-lan-wireless.md).
  - [ ] Còn để nghiệm thu: BOM/cabling/GPON có nguồn/hình; chờ giao nhận.
- [ ] **W4-TV2-02** - Đối chiếu bảng VLAN/subnet/DHCP, nhãn tầng/phòng, SSID với config và mô phỏng; sửa lỗi LAN còn lại cùng TV4, kiểm lại TC01/TC02/TC05/TC06 khi bị ảnh hưởng. **Hạn 18/11; đầu ra:** bảng/config đồng bộ và log retest.
  - [x] Sản phẩm đã có: [test-matrix.md](test_results/test-matrix.md).
  - [ ] Còn để nghiệm thu: Config/VLAN GNS3 đã đối chiếu; PT/SSID chưa chạy.
- [ ] **W4-TV2-03** - Đọc phần LAN/Wi-Fi/thiết bị/đi dây/camera trong PDF, xác nhận hình rõ chữ và không khẳng định khảo sát RF/GPON/40GbE đã test nếu chưa chạy. **Hạn 19/11; đầu ra:** review chuyên môn gửi TV5.
  - [x] Hồ sơ chuẩn bị: [review-log.md](docs/06-report/review-log.md); chưa phải xác nhận phê duyệt.
  - [ ] Còn để nghiệm thu: TV2 chưa xác nhận phần PDF.
- [ ] **W4-TV2-04** - Hoàn thiện phụ lục thiết bị, cabling, port/VLAN mapping và hướng mở module LAN; hỗ trợ TV5 giải đáp và sửa nội dung sau review TV1. **Hạn 20/11; đầu ra:** phụ lục LAN/BOM và phản hồi review đã đóng.
  - [x] Sản phẩm đã có: [lan-port-plan.md](docs/02-design/lan-port-plan.md).
  - [ ] Còn để nghiệm thu: Có port/cabling/phụ lục; chưa có phản hồi đọc chéo để đóng.
- [ ] **W4-TV2-05** - Cùng TV4 kiểm LAN/Wi-Fi sau mở lại bản đóng gói, xác nhận thiết kế mở rộng 5 năm và ghi rủi ro cần khảo sát sau này. **Hạn 21/11; đầu ra:** xác nhận LAN cho G4 và danh sách dự phòng.
  - [x] Sản phẩm đã có: [persistence.md](test_results/supplemental/persistence.md).
  - [ ] Còn để nghiệm thu: Reopen GNS3 có lịch sử; WLAN/RF chưa thử; chờ G4.

### TV3 - Security & Systems Specialist

- [ ] **W4-TV3-01** - Giao nội dung cuối Server Farm/DMZ/NAT/PAT/firewall/ACL/VPN/camera và best-practice guide; xác nhận tổng server 10/2/2 và luồng Internet tại Main. **Hạn 17/11; đầu ra:** contribution TV3, config và phụ lục security.
  - [x] Sản phẩm đã có: [TV3-security-systems.md](docs/06-report/contributions/TV3-security-systems.md).
  - [ ] Còn để nghiệm thu: Có config/contribution/server10/2/2; chờ giao nhận.
- [ ] **W4-TV3-02** - Xử lý lỗi security còn lại, đối chiếu rule với TC04/TC05/TC06 và VPN test; chạy lại test liên quan cùng TV4 khi sửa NAT/ACL/route. **Hạn 18/11; đầu ra:** config security cuối và log retest.
  - [x] Sản phẩm đã có: [results.json](test_results/runtime/after-firewall-restart-runtime/results.json).
  - [ ] Còn để nghiệm thu: Có retest GNS3 sau sửaPID; VPN/PT chưa thử.
- [ ] **W4-TV3-03** - Đọc bản PDF phần security/NAT theo [R], kiểm chú thích địa chỉ/cổng, ACL không bị nhầm với NAT; phân biệt khả năng đã triển khai và thiết kế IDS/IPS/HA. **Hạn 19/11; đầu ra:** review chuyên môn gửi TV5.
  - [x] Hồ sơ chuẩn bị: [review-log.md](docs/06-report/review-log.md); chưa phải xác nhận phê duyệt.
  - [ ] Còn để nghiệm thu: TV3 chưa xác nhận PDF/NAT/security.
- [ ] **W4-TV3-04** - Kiểm bí mật/tài khoản trong config và ảnh, dùng dữ liệu lab; hoàn thiện hướng dẫn vận hành, backup/restore, quyền VPN và danh sách hạn chế bảo mật. **Hạn 20/11; đầu ra:** config phù hợp chia sẻ, guide và risk notes cuối.
  - [x] Sản phẩm đã có: [security-best-practices.md](docs/04-security/security-best-practices.md).
  - [ ] Còn để nghiệm thu: Guide/lab data có; chờ kiểm/duyệt chuyên môn.
- [ ] **W4-TV3-05** - Cùng TV4 kiểm mở lại bản đóng gói và xác nhận guest isolation/DMZ/NAT còn đúng; hỗ trợ TV5 đóng phản hồi và chuẩn bị hồ sơ TV1 duyệt. **Hạn 21/11; đầu ra:** xác nhận security cho G4.
  - [x] Hồ sơ chuẩn bị: [approval.md](submission/approval.md); chưa phải xác nhận phê duyệt.
  - [ ] Còn để nghiệm thu: TV3/TV4 chưa ký G4; chưa reopen trọn sourcePID mới trên máy này.

### TV4 - Simulation & Testing Lead

- [ ] **W4-TV4-01** - Giao phần Step 3-5 cuối, file mô phỏng tổng, bảng tính tải và bộ evidence 6 test có phiên bản cho TV5; nêu đầy đủ giới hạn/known issues. **Hạn 17/11; đầu ra:** contribution TV4 và baseline ứng viên.
  - [x] Sản phẩm đã có: [TV4-capacity-testing.md](docs/06-report/contributions/TV4-capacity-testing.md).
  - [ ] Còn để nghiệm thu: Có baseline/config/evidence; thêm PT vẫn đang triển khai.
- [ ] **W4-TV4-02** - Tích hợp sửa lỗi tuần 4 từ TV1-TV3; chạy lại TC bị ảnh hưởng và test nhanh đủ 6 nhóm trên đúng bản ứng viên, không tái dùng ảnh từ topology cũ khi khác kết quả. **Hạn 20/11; đầu ra:** test matrix/evidence cập nhật, integration log.
  - [x] Sản phẩm đã có: [results.json](test_results/runtime/after-firewall-restart-runtime/results.json).
  - [ ] Còn để nghiệm thu: GNS3 retest có; chưa chạy mới trên Windows hoặc PT.
- [ ] **W4-TV4-03** - Hoàn thiện `simulation/README.md`: phiên bản, dependency/node, cách mở, IP đích và lệnh test, mapping thiết bị đại diện, phần không hỗ trợ; đối chiếu phần này trong PDF. **Hạn 20/11; đầu ra:** hướng dẫn tái hiện và review gửi TV5.
  - [x] Sản phẩm đã có: [demo-guide.md](simulation/gns3/demo-guide.md).
  - [ ] Còn để nghiệm thu: Có version/dependency/mapping/lệnh/giới hạn; PT có assembly runbook.
- [ ] **W4-TV4-04** - Lưu/đóng/mở lại bản mô phỏng đóng gói trên môi trường ghi nhận, kiểm config persist và dependency GNS3 nếu chọn; bàn giao bản có checksum để TV1 duyệt. **Hạn 21/11; đầu ra:** file `.pkt` hoặc gói GNS3 dùng được và log kiểm mở lại.
  - [x] Sản phẩm đã có: [reopen.json](test_results/runtime/persistence/reopen.json).
  - [ ] Còn để nghiệm thu: Reopen GNS3 lịch sử137; cần demo lại trên máy trình bày.
- [ ] **W4-TV4-05** - Cùng TV5 lập manifest/version/hash, kiểm đúng cặp PDF-mô phỏng và evidence; phối hợp TV1 nghiệm thu kỹ thuật G4. **Hạn 22/11; đầu ra:** `submission/manifest.md`, `SHA256SUMS`, xác nhận kỹ thuật cho TV1.
  - [x] Sản phẩm đã có: [manifest.md](submission/manifest.md).
  - [ ] Còn để nghiệm thu: Manifest/checksum kiểm được; G4 chờ TV1/nhóm.

### TV5 - Documentation & Report Specialist, chủ trì báo cáo

- [ ] **W4-TV5-01** - **Chủ trì thu nhận đầy đủ phần nội dung cuối của TV1-TV4**, bổ sung phần khảo sát/đánh giá mình phụ trách; khóa danh sách thiếu nội dung và tổng hợp báo cáo thô hoàn chỉnh. **Hạn 17/11; đầu ra:** source và draft đầy đủ 7 Step.
  - [x] Sản phẩm đã có: [report.tex](docs/06-report/latex/report.tex).
  - [ ] Còn để nghiệm thu: Đủ7 Step/5 contributions; chưa có xác nhận giao nhận nhóm.
- [ ] **W4-TV5-02** - **Tổng hợp, biên tập và căn chỉnh báo cáo chính thức**: bìa/nhân sự, mục lục, heading, bảng/hình, công thức, nguồn, phụ lục, font tiếng Việt và phân trang; xuất PDF review cho cả nhóm/TV1. **Hạn 19/11; đầu ra:** PDF review và nguồn chỉnh sửa được.
  - [x] Sản phẩm đã có: [metadata.tex](docs/06-report/latex/metadata.tex).
  - [ ] Còn để nghiệm thu: Đã cập nhật L08, nhóm 2, năm thành viên/email và hai người BTL2; tên giảng viên chưa được cung cấp.
- [ ] **W4-TV5-03** - Thu và xử lý nhận xét chuyên môn/TV1, hoàn tất Step 6 gồm reliability/nâng cấp/phần mềm/safety/security, vấn đề còn lại và hướng phát triển; rà soát không còn kết luận thiếu bằng chứng. **Hạn 20/11; đầu ra:** review log và PDF đã hiệu chỉnh.
  - [x] Sản phẩm đã có: [review-log.md](docs/06-report/review-log.md).
  - [ ] Còn để nghiệm thu: Có evaluation/QA; chuyên môn và TV1 chờ xác nhận.
- [ ] **W4-TV5-04** - Xuất `docs/06-report/final/report.pdf`, kiểm trực quan từng trang, mục lục, hình và link; cùng TV4 đóng gói PDF/nguồn/mô phỏng/config/evidence, đối chiếu manifest. **Hạn 21/11; đầu ra:** bộ hồ sơ cuối gửi TV1 **duyệt chót**, chưa tự gắn trạng thái approved.
  - [x] Sản phẩm đã có: [report.pdf](docs/06-report/final/report.pdf).
  - [ ] Còn để nghiệm thu: PDF/QA/source/gói có; bản Packet Tracer tổng chưa hoàn tất.
- [ ] **W4-TV5-05** - Ghi kết quả duyệt PDF + mô phỏng của TV1 ngày 22/11, sửa/phát hành lại nếu cần và cập nhật checksum; chuẩn bị danh mục nộp BKeL, nơi lưu xác nhận và kế hoạch rà soát đến 06/12. **Hạn 22/11; đầu ra:** hồ sơ G4 và bản ứng viên đã được TV1 duyệt.
  - [x] Hồ sơ chuẩn bị: [approval.md](submission/approval.md); chưa phải xác nhận phê duyệt.
  - [ ] Còn để nghiệm thu: Chưa có TV1 duyệt/G4/BKeL receipt; không tự ký.

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
