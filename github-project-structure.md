# Cấu trúc repository và quy trình quản lý BTL 2

Repository phục vụ mạng bệnh viện **Main - DBP - BHTQ**, 5 thành viên, triển khai từ **26/10/2026 đến 22/11/2026**, dự phòng rà soát đến **06/12/2026**, nộp BKeL trước hạn **11/12/2026** do nhóm cung cấp. Không có hạng mục slide.

Đọc [README.md](README.md) để xem thông số gốc, baseline kỹ thuật và truy vết 7 Step; dùng [tasks-assignment.md](tasks-assignment.md) để theo dõi checklist.

## 1. Cây thư mục chuẩn hóa

**Cấu trúc đã được khởi tạo bằng thư mục và mẫu tài liệu có trạng thái rõ ràng.** Cây dưới đây gồm cả các sản phẩm cuối còn phải triển khai: `report.pdf`, `.pkt`/project GNS3 và config thực chưa có. Thư mục chưa có sản phẩm có README hoặc `.gitkeep`; không dùng file nhị phân trống thay kết quả. Hai PDF nguồn giữ nguyên tên tại gốc.

```text
hospital-network-btl2/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── task.yml                     # Đầu việc có chủ trì, hạn và tiêu chí Done
│   │   └── bug.yml                      # Lỗi có bước tái hiện và test liên quan
│   ├── PULL_REQUEST_TEMPLATE.md         # Tác động, kiểm tra, reviewer và liên kết issue
│   ├── CODEOWNERS                       # Owner repo; cập nhật handle TV1-TV5 khi có
│   └── workflows/
│       └── docs-check.yml               # Kiểm tra Markdown/liên kết khi thiết lập CI
├── docs/
│   ├── 00-management/
│   │   ├── requirements-traceability.md # Step 1-7, điểm, sản phẩm và trạng thái
│   │   ├── decisions.md                 # Quyết định, giả định và lý do thay đổi
│   │   └── meeting-notes.md             # Tiến độ, vướng mắc, người xử lý và hạn
│   ├── 01-survey/                       # Step 1
│   │   ├── survey-checklist.md          # Vị trí, RF, điện, cáp, phòng và ứng dụng
│   │   ├── site-requirements.md         # Main 600/10, mỗi Aux 260/2; tải cao
│   │   └── floor-plans/                 # Mặt bằng A/B, Aux và vị trí MDF/IDF
│   ├── 02-design/                       # Step 1-2
│   │   ├── architecture.md             # Kiến trúc logic 3 site và ranh giới bảo mật
│   │   ├── ip-vlan-plan.md              # Network, mask, GW, DHCP, host và dự phòng
│   │   ├── physical-cabling.md          # Rack, patch panel, ODF, GPON/Ethernet
│   │   ├── wireless-plan.md            # Vùng phủ/dung lượng, SSID/VLAN và bảo mật
│   │   ├── equipment-bom.md            # Số lượng, spec, port, PoE, license và giá
│   │   ├── wan-options-cost.md         # Leased/MPLS/SD-WAN, TCO và quyết định
│   │   ├── server-dmz-plan.md          # Vai trò server, vùng, IP và luồng truy cập
│   │   ├── camera-plan.md              # Góc nhìn, VLAN, PoE, bitrate và lưu trữ
│   │   └── diagrams/                   # Nguồn sơ đồ chỉnh sửa được và bản xuất
│   │       ├── logical-3sites.mmd
│   │       ├── physical-main.drawio
│   │       ├── physical-aux.drawio
│   │       └── exports/
│   ├── 03-capacity/                     # Step 3
│   │   ├── assumptions.md              # Server tổng/mỗi máy, Wi-Fi, giờ cao điểm
│   │   ├── throughput.md               # Công thức, đơn vị, down/up, hệ số và ISP
│   │   └── capacity-inputs.csv          # Dữ liệu đầu vào, kịch bản, nguồn và ngày
│   ├── 04-security/                     # Bảo mật cho Step 1, 4, 5, 6
│   │   ├── security-policy.md          # Ma trận nguồn-đích-dịch vụ/quyền
│   │   ├── nat-pat.md                  # Inside/outside, PAT 2 ISP, DMZ mapping
│   │   ├── vpn-plan.md                 # Site-to-site và teleworker tại Main
│   │   ├── ids-ips-plan.md             # Thiết kế; kết quả chạy nếu nền tảng hỗ trợ
│   │   └── security-best-practices.md  # SSH/AAA, log, backup, phishing, hardening
│   ├── 05-evaluation/                   # Step 6
│   │   ├── evaluation.md               # Tin cậy, nâng cấp, phần mềm và an toàn
│   │   └── risks.md                    # SPOF, giới hạn công cụ, tồn tại và tương lai
│   └── 06-report/                       # Step 7
│       ├── contributions/              # Phần nội dung do từng thành viên bàn giao
│       │   ├── TV1-wan-routing.md
│       │   ├── TV2-lan-wireless.md
│       │   ├── TV3-security-systems.md
│       │   ├── TV4-capacity-testing.md
│       │   └── TV5-survey-evaluation.md
│       ├── source/                     # Nguồn báo cáo .docx/LaTeX hoặc tương đương
│       ├── draft/                      # Bản thô/bản xin rà soát do TV5 tổng hợp
│       ├── review-log.md               # Nhận xét, sửa lỗi và duyệt chót của TV1
│       └── final/
│           └── report.pdf              # Báo cáo chính thức được TV1 duyệt
├── simulation/                         # Step 4
│   ├── README.md                       # Phiên bản, cách mở, giới hạn và tái hiện
│   ├── integration-log.md              # Người ghép, module, thay đổi và test nhanh
│   ├── modules/                        # Module bàn giao, không thay file tổng
│   │   ├── tv1-wan/
│   │   ├── tv2-lan-wireless/
│   │   └── tv3-security/
│   ├── packet-tracer/
│   │   └── hospital-3sites.pkt          # Chỉ có khi chọn Packet Tracer
│   └── gns3/
│       └── hospital-3sites.gns3         # Chỉ có khi chọn GNS3; kèm cấu hình project
├── configs/                            # Cấu hình văn bản, theo site/thiết bị
│   ├── README.md                       # Mapping node/interface, thứ tự nạp và secrets
│   ├── main/
│   ├── dbp/
│   ├── bhtq/
│   └── isp-lab/                        # Router ISP/Web lab; không phải mạng thật
├── test_results/                       # Step 5
│   ├── test-matrix.md                  # TC01-TC06, expected/actual và phiên bản
│   ├── TC01-same-vlan/
│   ├── TC02-inter-vlan/
│   ├── TC03-inter-site/
│   ├── TC04-dmz/
│   ├── TC05-guest-isolation/
│   ├── TC06-internet-web/
│   └── supplemental/                  # DHCP, dual ISP, VPN, HA, IDS/IPS nếu có
├── scripts/
│   └── check_docs.py                   # Kiểm UTF-8, link nội bộ, fence và task ID
├── submission/                         # Step 7; không chứa slide
│   ├── manifest.md                     # Tên file, phiên bản, công cụ, ngày, người duyệt
│   ├── SHA256SUMS                      # Hash báo cáo và mô phỏng tại thời điểm khóa
│   ├── approval.md                     # TV1 duyệt PDF + mô phỏng, bản tái duyệt nếu có
│   └── bkel-receipt/                   # Xác nhận sau nộp; che thông tin nhạy cảm
├── Assignment 2-Network Design For A Company.pdf
├── Reference Multi-site network.pdf
├── README.md                           # Trang chủ và điều hướng
├── TASKS.md                            # Trang điều hướng đến tasks-assignment.md
├── tasks-assignment.md                 # Nguồn duy nhất của checklist 4 tuần × 5 TV
├── github-project-structure.md          # Quy ước repository và vòng đời bàn giao
└── .gitignore                          # File tạm/cache/image có license/secrets
```

Hai nhánh `simulation/packet-tracer/` và `simulation/gns3/` thể hiện các lựa chọn; **chỉ một nền tảng chính cần được hoàn thiện**. Nếu chọn GNS3, bàn giao đầy đủ project/config/metadata cần mở lại; một file `.gns3` trống dependency không đạt nghiệm thu. Không đưa image hệ điều hành có license vào Git nếu không có quyền chia sẻ.

`TASKS.md` đã được tạo, có nội dung điều hướng tương đương mẫu dưới đây; không chép checklist ra bản thứ hai:

```markdown
# Công việc dự án

Checklist chính thức: [tasks-assignment.md](tasks-assignment.md).
Thông số và đầu ra: [README.md](README.md).
```

Các thư mục trống chưa được Git lưu; chỉ tạo khi có sản phẩm hoặc README mô tả. Tên file mô phỏng/báo cáo chính giữ ổn định; phiên bản xác định bằng tag/commit và manifest thay vì các tên `final-final-v3`.

## 2. Chủ sở hữu và reviewer

| Phạm vi | Chủ trì | Reviewer/phối hợp | Điều kiện bàn giao |
| --- | --- | --- | --- |
| Repository, `.github/`, quản lý tiến độ | TV1 | TV5 | Issue/PR có người phụ trách, hạn và liên kết Step |
| Khảo sát, nguồn yêu cầu, truy vết | TV5 | TV1, TV2, TV3, TV4 theo chuyên môn | Tách dữ kiện gốc, giả định và kết quả khảo sát |
| IP plan, WAN, OSPF, dual xDSL và chi phí WAN | TV1 | TV2, TV3, TV4 | Không trùng subnet; route và default đúng; NAT đúng egress |
| LAN/Wi-Fi, BOM, sơ đồ vật lý và cabling | TV2 | TV1, TV3 | Đủ port/PoE/uplink và dự phòng 20%; VLAN khớp IP plan |
| Server/DMZ, NAT/firewall/ACL/VPN, security guide | TV3 | TV1, TV4 | Ma trận quyền rõ; có cấu hình và test/giới hạn tương ứng |
| Camera | TV3 về vùng/quyền/lưu trữ, TV2 về vị trí/cáp/PoE | TV5 | Không tự gán số lượng camera khi chưa khảo sát |
| Tính tải, file mô phỏng tổng và bằng chứng test | TV4 | TV1, TV2, TV3 | Công thức tái tính được; file mở lại được; bằng chứng gắn phiên bản |
| Đánh giá Step 6, nguồn và bản thô/bản PDF | **TV5** | Tất cả giao phần chuyên môn; TV1 duyệt | Báo cáo có đủ 7 Step, ảnh/log và giới hạn đã xác nhận |
| Duyệt chót PDF + mô phỏng | **TV1** | TV5 chuẩn bị hồ sơ, TV4 xác nhận kỹ thuật | Có biên bản duyệt đúng hash/phiên bản hai sản phẩm |
| Nộp BKeL | TV1 | TV5 lưu xác nhận, TV4 hỗ trợ đóng gói | Có xác nhận nộp đúng bản trước hạn 11/12/2026 |

TV1-TV5 là mã vai trò, chưa phải GitHub username. Chỉ cấu hình `CODEOWNERS` và assignee bằng tài khoản thật đã xác nhận; cấu hình branch protection khi quyền repo cho phép, không tuyên bố đã bật khi chưa thiết lập.

## 3. GitHub Issues, milestones và pull requests

### Milestones

| Milestone | Mở | Đến hạn | Cổng nghiệm thu |
| --- | --- | --- | --- |
| M1 - Quy hoạch & Tính toán | 26/10/2026 | 01/11/2026 | Khóa baseline thiết kế, giả định, tải và chọn nền tảng |
| M2 - Mô phỏng cơ bản | 02/11/2026 | 08/11/2026 | File tổng 3 site mở lại được, routing/NAT cơ bản chạy |
| M3 - Bảo mật & Kiểm thử | 09/11/2026 | 15/11/2026 | Đủ 6 nhóm test, lỗi/rủi ro có trạng thái và người xử lý |
| M4 - Báo cáo & Đóng gói | 16/11/2026 | 22/11/2026 | TV5 tổng hợp và xuất PDF; TV1 duyệt chót PDF + mô phỏng |

Mốc **06/12/2026** là hạn nội bộ khóa bản nộp sau dự phòng; **11/12/2026** là hạn BKeL do nhóm cung cấp. Có thể dùng issue riêng theo dõi hai mốc này, không kéo dài M4 thành 3 tuần và không tạo giai đoạn 5.

### Issue

- Tiêu đề: `[W1-TV1-02][Step 2] Khóa quy hoạch IP 3 site`, dùng task ID đúng trong checklist.
- Nội dung: bối cảnh/nguồn trang PDF, một chủ trì, người phối hợp, hạn theo giờ Việt Nam, dependency, sản phẩm/đường dẫn và tiêu chí nghiệm thu.
- Nhãn gợi ý: `phase:1` đến `phase:4`; `member:TV1` đến `member:TV5`; `step:1` đến `step:7`; `type:design`, `type:simulation`, `type:test`, `type:docs`, `type:bug`; `status:blocked` nếu cần. Đây là quy ước đề xuất, chưa tạo nhãn thật.
- Board gợi ý: `Todo → In progress → Review → Done`, có trường assignee, milestone, due date và dependency. Issue blocked phải ghi lý do, người gỡ và hạn xử lý.
- GitHub không có ngày hạn issue độc lập trong mọi giao diện; ghi hạn trong nội dung hoặc Project field, đồng thời gán milestone. Chỉ tích checklist sau khi PR/sản phẩm được duyệt.

### Pull request và mô phỏng nhị phân

1. Tạo nhánh `feat/tv1-wan-routing`, `feat/tv2-lan-wireless`, `feat/tv3-security`, `feat/tv4-simulation-testing`, `docs/tv5-report` hoặc nhánh nhỏ theo đầu việc.
2. Mỗi PR nêu thay đổi, task ID/issue, Step liên quan, config/topology bị tác động, kiểm tra và giới hạn; đính kèm ảnh/log khi thay đổi chức năng.
3. TV4 giữ quyền điều phối file mô phỏng tổng. TV1/TV2/TV3 giao module, cấu hình dạng text và chỉ dẫn port; tránh hai người cùng chỉnh một file `.pkt`. Đăng lịch giữ file trong `integration-log.md`.
4. Reviewer chuyên môn kiểm tra phần liên quan. TV1 duyệt tích hợp/release; phần TV1 tự viết cần có TV2/TV3/TV4 đọc chéo phù hợp trước khi TV1 xác nhận toàn bộ.
5. Sau merge, cập nhật checklist, thiết kế, test matrix và report contribution. Thay đổi subnet/ACL/đường đi phải cập nhật đồng thời bảng IP, config và test bị ảnh hưởng.

Không commit mật khẩu thật, tài khoản BKeL, cấu hình mạng vận hành hoặc thông tin bệnh nhân. Cấu hình nộp là cấu hình lab với bí mật minh họa đã ghi rõ. Hai PDF nguồn phục vụ học tập; [R] có thông báo bản quyền sử dụng trong môn học, nên kiểm tra quyền chia sẻ nguồn trước khi công khai repository. Việc này không cản trở tạo và sử dụng nội bộ ba file quản lý.

## 4. Chuẩn sản phẩm và bằng chứng

### Thiết kế và tính toán

- Mỗi bảng ghi nguồn `[A]/[R] + trang`, giả định và quyết định phê duyệt; không lẫn baseline đề xuất với thông số bắt buộc.
- BOM có số lượng, đặc tính điển hình, port/speed, PoE, quang/license, giá/thuế/nguồn/ngày và tổng CAPEX/OPEX/TCO; chưa có báo giá thì đánh dấu chờ xác nhận, không bịa số tiền.
- Sơ đồ có tên site/node, VLAN, subnet, port/link type, tốc độ và ranh giới bảo mật; giữ file nguồn có thể sửa cùng ảnh xuất dùng cho báo cáo.
- Step 3 có 500/100 MB mỗi workstation, 1.000/2.000 MB server theo kịch bản, 500 MB Wi-Fi theo giả định, 80% trong 3 giờ cao điểm và 20% trong 5 năm; tách down/up, Internet/WAN/LAN và tải chưa biết.

### Test

Mỗi thư mục TC gồm `result.md`, ảnh trong `screenshots/` và log/config cần thiết trong `logs/`. Tên ảnh gợi ý: `TC03-main-to-dbp-ping-20261112.png`; nội dung ảnh phải có nhãn nguồn/đích đọc được, không chỉ một thông báo “Success”.

`result.md` chứa ID, Step, ngày/người chạy, phiên bản công cụ, tên/hash file mô phỏng, precondition, nguồn/đích, IP/VLAN, thao tác/lệnh, expected/actual, trạng thái và đường dẫn bằng chứng. `test-matrix.md` tổng hợp trạng thái `NOT RUN`, `PASS`, `FAIL`, `BLOCKED`; chức năng chỉ thiết kế dùng `DESIGN ONLY/MODELED`, không dùng PASS.

Sáu nhóm bắt buộc: TC01 cùng VLAN; TC02 khác VLAN theo quyền; TC03 Main↔cả DBP và BHTQ; TC04 DMZ; TC05 khách bị chặn vào PC LAN có ca đối chứng; TC06 Internet Web qua Main. Load balancing/failover/VPN/IDS/IPS là bằng chứng bổ sung, không thay sáu nhóm gốc.

### Báo cáo

TV5 thống nhất bố cục: bìa/thành viên, mục lục, yêu cầu và khảo sát, kiến trúc, BOM/cabling/VLAN/IP/WAN, tính tải, triển khai mô phỏng/bảo mật, 6 kịch bản test, đánh giá/tồn tại/hướng phát triển, kết luận, nguồn và phụ lục cấu hình. Nội dung phải truy vết được Step 1-7 dù bố cục không dùng đúng 7 tên chương.

Mỗi thành viên giao phần chuyên môn vào `contributions/`, TV5 nhận và tổng hợp vào `source/`, xuất bản thô vào `draft/`, xử lý ý kiến tại `review-log.md` rồi xuất `final/report.pdf`. Kiểm tra font tiếng Việt, số bảng/hình, chú thích ảnh, mục lục, trang, link và tính nhất quán với file mô phỏng. **TV1 là người duyệt chót**, TV5 không tự xác nhận thay TV1.

## 5. Cổng chất lượng và đóng gói

| Cổng | Ngày | Điều kiện bắt buộc |
| --- | --- | --- |
| G1 | 01/11/2026 | Đủ khảo sát/giả định, IP không trùng, sizing 5 năm, kế hoạch WAN/ISP/cost, chọn công cụ |
| G2 | 08/11/2026 | File tổng mở lại được, baseline 3 site và Internet qua Main; module/config đồng bộ |
| G3 | 15/11/2026 | Đủ TC01-TC06 và bằng chứng; lỗi phải được sửa hoặc ghi rõ không đạt/chờ xử lý |
| G4 | 22/11/2026 | Báo cáo PDF + mô phỏng + nguồn; TV1 duyệt; manifest và checksum khớp bản thực tế |
| Khóa bản nộp | 06/12/2026 | Đã xử lý lỗi chặn, retest và tái duyệt mọi thay đổi sau G4 |
| Nộp BKeL | Trước hạn 11/12/2026 | File được nộp đúng bản đã duyệt; lưu xác nhận và đối chiếu manifest |

Các cổng là điều kiện nghiệm thu, không phải tuyên bố đã đạt. Nếu fail, mở issue, chỉ định chủ trì và hạn sửa trong lịch hiện có; không đổi trạng thái thành Done để giữ lịch đẹp.

Bộ bàn giao chính gồm `report.pdf`, file `.pkt` hoặc gói GNS3 dùng được, nguồn báo cáo và hướng dẫn tái hiện. Config, test evidence, manifest và checksum là tài liệu hỗ trợ. TV4 xác nhận mở mô phỏng trên môi trường đã ghi; TV5 kiểm PDF và danh mục; TV1 đối chiếu rồi duyệt đúng hai sản phẩm cuối. Không tạo slide.

Sau ngày 22/11, chỉ nhận thay đổi sửa lỗi/rà soát cần thiết, chạy lại test liên quan, xuất lại PDF nếu ảnh/số liệu đổi, tính lại checksum và TV1 tái duyệt. TV1 chủ động nộp trong 07/12-10/12 nếu BKeL mở; nếu chưa biết giờ đóng cổng ngày 11/12 thì kiểm tra BKeL, không tự giả định 23:59.
