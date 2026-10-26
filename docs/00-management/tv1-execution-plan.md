# Kế hoạch thực hiện chi tiết của thành viên 1

**Vai trò:** Trưởng nhóm, WAN & Routing Lead. **Ngày lập:** 26/10/2026. **Trạng thái:** ĐÃ TRIỂN KHAI HOÀN TẤT VÀ NGHIỆM THU CÁC HẠNG MỤC TV1.

Kế hoạch triển khai trong **26/10–22/11/2026**, dự kiến **12 giờ/tuần × 4 tuần = 48 giờ**. Ngày trong tài liệu dùng giờ Việt Nam. Khoảng **23/11–06/12** dành cho lỗi phát sinh; khóa bản nộp chậm nhất **06/12**, dự kiến nộp **07/12–10/12**, trước hạn **11/12/2026** theo kế hoạch nhóm. Cần kiểm giờ đóng thực tế trên BKeL khi nộp.

Căn cứ: [phân công chính thức](../../tasks-assignment.md), [đặc tả dự án đã tổng hợp](../../README.md), [quy trình repository](../../github-project-structure.md) và các baseline trong `docs/02-design/`. Tài liệu này phân rã cách làm và điều kiện hoàn thành; cập nhật trạng thái task tại `tasks-assignment.md`, không lập checklist trạng thái thứ hai.

## 1. Mục tiêu và phạm vi của TV1

Kết thúc phần việc, TV1 phải bàn giao được một module WAN có cấu hình và hướng dẫn tái hiện: Main kết nối DBP/BHTQ qua hai leased lines; các mạng được phép liên thông; Internet của cả ba site đi qua Main; hai đường Internet có cơ chế phân phối luồng và xử lý sự cố đã được kiểm chứng trong khả năng công cụ. Đồng thời hoàn thiện quy hoạch IP, so sánh WAN/chi phí, nội dung báo cáo và hồ sơ duyệt sản phẩm cuối.

| TV1 chủ trì | Phối hợp và ranh giới trách nhiệm |
| --- | --- |
| IP/VLSM toàn hệ thống, transit, pool VPN | TV2 xác nhận VLAN/host/gateway; TV3 xác nhận server/VPN; TV1 cấp địa chỉ và kiểm trùng |
| WAN, OSPF, route nội bộ và default route | TV2 cung cấp LAN/SVI; TV3 xác nhận cách đi qua firewall và route chiều về |
| Định tuyến hai ISP, load balancing/failover | TV3 cấu hình NAT/PAT; hai người thống nhất egress và thứ tự thay đổi trên thiết bị dùng chung |
| So sánh WAN, yêu cầu đường truyền và chi phí | TV4 tính tải; TV2 cung cấp BOM; TV1 lập lựa chọn và các điều kiện còn thiếu |
| Module WAN và log chuyên môn | TV4 quản lý file mô phỏng tổng, tích hợp và lưu hồ sơ kiểm thử |
| Quản lý tiến độ, review và duyệt cuối | TV5 tổng hợp/xuất báo cáo; TV1 viết phần chuyên môn và duyệt đúng phiên bản PDF + mô phỏng |

Hiện repository đã có `.github/`, checklist và các tài liệu baseline; **rà soát, bổ sung phần thiếu thay vì khởi tạo lại**. Chưa có cấu hình triển khai, file mô phỏng hoặc bằng chứng test. Chưa suy ra rằng milestone, quyền repo hoặc branch protection trên GitHub đã được thiết lập từ các file local.

## 2. Thứ tự thực hiện và các quyết định cần khóa

Luồng công việc: **xác nhận đầu vào → khóa IP và giao diện → thử khả năng công cụ → dựng WAN → nối LAN/firewall → Internet một ISP → Internet hai ISP → kiểm thử lỗi → bàn giao báo cáo → duyệt và nộp**.

| Quyết định | Hạn | Người cung cấp/đọc chéo | Nội dung phải ghi lại |
| --- | --- | --- | --- |
| VLAN và nhu cầu host | 29/10 | TV2, TV3 | Số thiết bị, tăng trưởng, DHCP/IP tĩnh, địa chỉ gateway và HA nếu có |
| Ranh giới core–firewall–WAN–edge | 30/10 | TV2, TV3, TV4 | Node/interface, subnet từng đoạn, nơi định tuyến và kiểm soát truy cập |
| Năng lực đường truyền | 30/10 | TV4 | Down/up, tải liên site/Internet, kịch bản một ISP hỏng và tải còn thiếu |
| Nền tảng, model, phiên bản và tính năng | 01/11 | TV4, TV3 | Kết quả thử OSPF, NAT hai egress, theo dõi đường ra, phân phối luồng; phần MODELED/DESIGN ONLY |
| Cấu hình làm mốc kiểm thử | 11/11 | TV3, TV4 | Phiên bản cấu hình/mô phỏng, IP nguồn/đích, expected và cách thu bằng chứng |
| Cặp PDF–mô phỏng để duyệt | 22/11 | TV4, TV5 | Tên file, phiên bản, hash, log mở lại và lỗi/giới hạn còn lại |

Nếu thiếu dữ liệu, ghi giả định, người cần xác nhận và hạn vào [sổ quyết định](decisions.md). Có thể dựng lab tối thiểu với IP tạm đã ghi rõ; phải đồng bộ lại trước khi tích hợp. Không khóa phương án chi phí hay tuyên bố tính năng chạy được khi chưa có căn cứ.

## 3. Tuần 1 — Chốt thiết kế và đầu vào, 26/10–01/11

**Kết quả cần đạt:** TV2/TV3/TV4 có thể bắt đầu triển khai theo cùng một bảng IP và sơ đồ giao diện.

| Ngày | Giờ | Công việc cụ thể | Sản phẩm / điều kiện xong | Task gốc |
| --- | --- | --- | --- | --- |
| 26/10 | 1,5 | Đọc phân công; rà `.github/`, template issue/PR, checklist; lập danh sách task TV1 và dependency; chuẩn bị 4 milestone theo lịch. Chỉ gán tài khoản thật khi đã xác nhận | Quy tắc làm việc rõ, danh sách việc còn thiếu; ghi việc trên GitHub chưa thực hiện nếu thiếu quyền/thông tin | W1-TV1-01 |
| 27/10 | 2 | Lập bảng địa chỉ chi tiết từ baseline; tách workstation, server, guest, quản trị, camera và Wi-Fi nhân viên | Bản nháp IP có network/mask, host range, broadcast, gateway, reserved, DHCP và dung lượng | W1-TV1-02 |
| 28/10 | 2 | Đối chiếu host với TV2/TV3; cấp dự kiến transit và VPN pool; bắt đầu thử khả năng WAN/edge cùng TV4 trên model dự kiến | Danh sách thiếu dữ liệu; bản đồ các kết nối L3; ghi kết quả thử ban đầu | W1-TV1-02, W1-TV1-05 |
| 29/10 | 1,5 | Kiểm overlap, gateway/pool và sức chứa sau tăng trưởng; xử lý nhận xét TV2; bàn giao bảng IP để các module cùng dùng | `ip-vlan-plan.md` được đọc chéo, thay đổi/giả định được ghi nhận | W1-TV1-02 |
| 30/10 | 3 | Hoàn thiện sơ đồ WAN/route/default; nhận số tải TV4; lập bảng hai ISP và so sánh WAN/TCO; hoàn tất thử các tính năng quyết định lựa chọn công cụ | WAN diagram, interface mapping, `architecture.md`, `wan-options-cost.md`; baseline giao nhóm cuối ngày | W1-TV1-03, W1-TV1-04 |
| 31/10 | 1 | Đọc chéo cùng TV2/TV3/TV4; sửa đường đi qua firewall, route chiều về, subnet transit và các điểm công cụ không hỗ trợ | Nhận xét có hướng xử lý; tài liệu thống nhất | W1-TV1-02 đến W1-TV1-05 |
| 01/11 | 1 | Họp G1; chốt nền tảng với TV4 và phạm vi mô phỏng; giao baseline cho TV5 | Biên bản G1, quyết định công cụ và danh sách mục còn chờ xác nhận | W1-TV1-05 |
| **Tổng** | **12** | | | |

### 3.1. Cách hoàn thiện bảng IP

1. Giữ baseline Main `10.10.0.0/16`, DBP `10.20.0.0/16`, BHTQ `10.30.0.0/16` làm vùng dự trữ. Chỉ cấp các subnet cụ thể cho interface, không cấu hình /16 chồng lên VLAN đang dùng.
2. Với mỗi VLAN, ghi đủ: site, chức năng, số host hiện tại, số host 5 năm, network/CIDR/mask, gateway, reserved, DHCP start/end, IP tĩnh, broadcast, người sử dụng và ghi chú tăng trưởng.
3. Tính số host 5 năm bằng `ceil(host hiện tại × 1,2)`. Main đạt 720 workstation, mỗi Aux đạt 312. Kiểm ở từng VLAN, không chỉ kiểm tổng site.
4. Với baseline /25: 126 host khả dụng; `.1–.6` dành gateway/hạ tầng và `.7–.126` là 120 địa chỉ DHCP. VLAN 100 PC Main tăng lên 120 PC đã dùng hết pool này; nếu bổ sung host phải điều chỉnh hoặc chia thêm subnet, không tự lấy bớt pool.
5. Giữ hai WAN transit đang đề xuất: Main–DBP `10.255.0.0/30` với `.1/.2`; Main–BHTQ `10.255.0.4/30` với `.5/.6`. Các link L3 core/firewall/edge dùng subnet riêng sau khi xác nhận topology; VPN pool lấy vùng chưa dùng và thống nhất với TV3.
6. Kiểm mọi cặp subnet đang cấp không overlap; kiểm IP gateway thuộc host range, DHCP không chứa gateway/IP tĩnh/network/broadcast; đối chiếu pool VPN và route đến pool.
7. Gửi TV2 đọc chéo VLAN/host, TV3 đọc chéo server/VPN; đồng bộ mọi thay đổi với README, cấu hình và test liên quan khi triển khai.

### 3.2. Thiết kế WAN và định tuyến

- Sơ đồ phải thể hiện Main–DBP và Main–BHTQ là hai kết nối riêng, đường đi tới LAN mỗi site, vị trí firewall và hai hướng ISP. Ghi tên node, interface, subnet và mục đích từng link; không tự gán tên cổng khi chưa chọn model.
- Đề xuất lab ban đầu dùng OSPF một area 0 cho miền định tuyến nội bộ; đây là lựa chọn cần thử và chốt tại G1. Đặt router ID duy nhất, xác định các cặp láng giềng mong đợi và chỉ bật adjacency trên liên kết cần thiết.
- Các LAN được quảng bá theo quyền/thiết kế; không hình thành láng giềng trên VLAN người dùng. Ghi rõ khi firewall dùng static route nối các miền thay vì chạy OSPF xuyên firewall.
- Lập bảng route kỳ vọng cho mỗi router: mạng Main, DBP, BHTQ, next hop, cách học route, default route và đường trả về. Aux đi Internet qua Main; không tạo local breakout tại chi nhánh.
- Default ra Internet phải gắn với khả năng sử dụng đường ra. Khi cả hai ISP mất, đường default quảng bá cho Aux cần được thu hồi theo thiết kế; chỉ giữ một static default tồn tại không đủ chứng minh cơ chế này.
- ISP-facing interfaces không thuộc miền OSPF nội bộ. Phối hợp TV3 để lưu lượng liên site không bị PAT và traffic Internet được NAT đúng egress.

### 3.3. Hai xDSL và bảng chi phí

Nhận bảng tải từ TV4, giữ riêng down/up và ba chế độ: hai ISP hoạt động, chỉ ISP1, chỉ ISP2. Tách tải Internet khỏi lưu lượng nội bộ/liên site trước khi dùng số liệu để chọn đường truyền. Ghi rõ tải ưu tiên còn phục vụ được khi chỉ còn một ISP; không mặc định hai gói xDSL đáp ứng nhu cầu đã tính.

Trong lab, thử phân phối theo luồng bằng cơ chế thiết bị thực sự hỗ trợ; kiểm NAT cùng egress với TV3. Hai default route cùng chi phí chỉ là một phần cấu hình, chưa phải bằng chứng load balancing/failover. Phải thử nhiều nguồn/đích/phiên và cả tình huống lỗi upstream khi cổng local vẫn up. Nếu công cụ không hỗ trợ, TV1/TV4 chốt hướng xử lý tại G1: dùng môi trường phù hợp hoặc ghi giới hạn và trạng thái chưa kiểm chứng; không tự đánh dấu đạt yêu cầu.

Bảng WAN cần có ít nhất leased Ethernet/Metro-E, MPLS L3VPN, SD-WAN trên underlay phù hợp và IPsec overlay. So sánh phạm vi 3 site, băng thông, SLA, mã hóa, mở rộng, vận hành, CAPEX, OPEX và TCO 5 năm. SD-WAN là overlay, không bỏ chi phí underlay; MPLS và IPsec cần phân biệt vai trò.

Mỗi giá cần nguồn/ngày, phạm vi cung cấp, thuế, phí lắp đặt, thiết bị, license và bảo trì. Chưa có giá thì để biến số hoặc “chờ báo giá”. Dùng `TCO 5 năm = CAPEX + 60 × OPEX tháng + chi phí định kỳ khác chưa tính`, tránh cộng trùng license hoặc underlay. Việc thu thập báo giá thực hiện khi triển khai task; kế hoạch này không khẳng định giá thị trường hoặc gói nhà mạng cụ thể.

**Cổng G1:** IP đủ dung lượng và không overlap; topology/giao diện thống nhất; có phương án WAN/ISP/chi phí; có kết quả thử để chốt công cụ; mục còn thiếu có chủ trì và hạn.

## 4. Tuần 2 — Dựng module WAN và tích hợp, 02/11–08/11

| Ngày | Giờ | Công việc cụ thể | Sản phẩm / điều kiện xong | Task gốc |
| --- | --- | --- | --- | --- |
| 02/11 | 1,5 | Tạo bản làm việc module WAN; đặt node Main/DBP/BHTQ và interface theo baseline; nối hai transit; gán IP | Ping được hai đầu từng link trực tiếp, lưu mapping và cấu hình ban đầu | W2-TV1-01 |
| 03/11 | 2 | Cấu hình OSPF trên link đã thống nhất; router ID, network, passive interface phù hợp; dùng LAN đại diện đã cấp IP | Neighbor đúng thiết kế; có route đến LAN đại diện của ba site | W2-TV1-01 |
| 04/11 | 2 | Hoàn thiện quảng bá LAN, route chiều về và default qua Main; thử Main↔DBP và Main↔BHTQ | Cấu hình routing bàn giao đúng hạn; log neighbor/route/ping/traceroute | W2-TV1-01 |
| 05/11 | 2,5 | Dựng ISP/Web lab; kiểm HTTP một ISP cùng TV3 trước, sau đó thêm ISP thứ hai và cơ chế egress/NAT; lưu module để TV4 nhận | Config edge/ISP; bằng chứng kết nối cơ bản; phần xDSL mô hình hóa được mô tả | W2-TV1-02, W2-TV1-03 |
| 06/11 | 2 | TV4 ghép module; TV1 xử lý interface/route/default, TV3 xử lý NAT/firewall; cập nhật log tích hợp | WAN hoạt động trong file tổng; không loop/blackhole hoặc breakout tại Aux | W2-TV1-03 |
| 07/11 | 1 | Kiểm nhanh WAN và Web từ ba site; rà route/NAT chiều về; cập nhật lựa chọn WAN theo phản hồi nhóm | Smoke log; bảng chi phí/giới hạn cập nhật | W2-TV1-04 |
| 08/11 | 1 | Kiểm cùng TV4 sau lưu/đóng/mở lại; review G2; gửi phần WAN bản đầu cho TV5 | Baseline G2 và contribution TV1 bản đầu | W2-TV1-05 |
| **Tổng** | **12** | | | |

### 4.1. Gói TV1 bàn giao cho TV4

| Thành phần | Nơi lưu / nội dung |
| --- | --- |
| Module riêng | `simulation/modules/tv1-wan/`; file mở được bằng nền tảng đã chọn |
| Cấu hình text theo node | `configs/main/`, `configs/dbp/`, `configs/bhtq/`, `configs/isp-lab/`; tên file khớp node thực tế |
| Hướng dẫn module | Bổ sung `simulation/modules/tv1-wan/README.md`: model/phiên bản, dependency, cách mở/nạp, cách kiểm và giới hạn |
| Interface mapping | Node/interface A, node/interface B, subnet, IP hai đầu, loại link, vai trò OSPF/NAT/security và chủ trì cấu hình |
| Route kỳ vọng | Mạng đích, next hop/interface, cách học route, default và đường về theo từng node |
| Nhật ký bàn giao | `simulation/integration-log.md`: thời gian, phiên bản, người nhận, thay đổi và lỗi cần theo dõi |

Nếu routing và NAT cùng nằm trên một router, bàn giao một cấu hình hợp nhất sau khi TV1/TV3 đọc chéo; tránh nạp hai file toàn bộ khiến cấu hình người trước bị ghi đè. TV4 điều phối file mô phỏng tổng; TV1 giao module/config và lịch tích hợp.

### 4.2. Trình tự khoanh vùng lỗi

Kiểm theo thứ tự: **link/interface → IP/mask → láng giềng OSPF → route đi và về → ACL/firewall → NAT → DNS/HTTP**. Ping từng hop trước khi thử ứng dụng từ PC. Khi không truy cập Web, thử cả địa chỉ IP và hostname để phân biệt DNS với routing; một kết quả ping thành công không đủ kết luận HTTP thành công.

**Cổng G2:** file tổng mở lại được; liên thông cơ bản đủ Main–DBP/BHTQ; Web từ ba site qua Main; cấu hình text khớp mô phỏng. Test chính thức về security và lỗi đường truyền tiếp tục ở tuần 3.

## 5. Tuần 3 — Kiểm thử và hoàn thiện kỹ thuật, 09/11–15/11

| Ngày | Giờ | Công việc cụ thể | Sản phẩm / điều kiện xong | Task gốc |
| --- | --- | --- | --- | --- |
| 09/11 | 1,5 | Nhận ma trận ACL/VPN cập nhật; rà route hai chiều khi bật bảo mật; sửa lỗi routing từ G2 | Danh sách thay đổi và test cần chạy lại | W3-TV1-01, W3-TV1-03 |
| 10/11 | 1,5 | Hoàn thiện điều kiện default/failover; chuẩn bị host và dịch vụ để tạo nhiều phiên qua hai ISP | Kịch bản và điểm quan sát được thống nhất với TV3/TV4 | W3-TV1-01, W3-TV1-02 |
| 11/11 | 1 | Khóa bản kiểm thử; xác nhận nguồn/đích, quyền truy cập, expected, phiên bản/hash và mẫu log | Cấu hình làm mốc kiểm thử, không ghi đè trong lúc chạy test | W3-TV1-01 đến W3-TV1-03 |
| 12/11 | 2 | Cùng TV4 chạy TC03 đủ Main↔DBP, Main↔BHTQ; kiểm route/neighbor, ghi kết quả thực tế | Hồ sơ TC03 có bằng chứng từng hướng, lỗi có bước tái hiện | W3-TV1-01 |
| 13/11 | 2,5 | Kiểm nhiều phiên qua hai ISP; ngắt từng đường, lỗi upstream, mất cả hai và phục hồi; ghi phiên mới/phiên cũ | Hồ sơ dual ISP trong `test_results/supplemental/`; kết luận theo quan sát | W3-TV1-02 |
| 14/11 | 2 | Chạy TC06 cùng TV3/TV4 từ từng site và guest theo ma trận; kiểm NAT/VPN/ACL và chạy lại test bị ảnh hưởng | Log Web, route, NAT/đường đi; config và evidence đồng bộ | W3-TV1-03 |
| 15/11 | 1,5 | Review sáu nhóm test và lỗi còn lại; hoàn thiện contribution, nhận xét độ tin cậy/nâng cấp; họp G3 | Nội dung WAN gửi TV5; biên bản G3 và danh sách xử lý tuần 4 | W3-TV1-04, W3-TV1-05 |
| **Tổng** | **12** | | | |

### 5.1. Bộ kiểm thử TV1 cần chuẩn bị

Các hàng dưới là kịch bản dự kiến, **chưa chạy**. TC03/TC06 lưu ở hồ sơ có sẵn; các ca bổ sung lưu dưới `test_results/supplemental/` và được TV4 quản lý.

| Kịch bản | Thao tác / quan sát | Kết quả mong đợi và bằng chứng |
| --- | --- | --- |
| TC03: Main–DBP | Từ host được phép ở Main ping/traceroute đến DBP; thực hiện chiều DBP về Main | Hai chiều thông; có IP/VLAN nguồn–đích, route và đường đi phù hợp |
| TC03: Main–BHTQ | Làm tương tự với BHTQ | Đủ bằng chứng cho cả chi nhánh thứ hai, không dùng kết quả DBP thay thế |
| TC06: Internet tập trung | Từ Main, DBP, BHTQ và guest theo phạm vi test mở HTTP trên Web server ngoài lab | HTTP thành công, đường đi qua Main và NAT đúng egress; có kết quả theo từng nguồn |
| Phân phối luồng | Tạo nhiều phiên với nhiều cặp nguồn/đích/cổng; quan sát cả hai egress | Có traffic/translation đúng trên cả hai đường; ghi số phiên thực tế, không yêu cầu đúng 50/50 khi không có cơ sở |
| Mất ISP1 | Ghi trạng thái trước lỗi, ngắt ISP1, thử tạo phiên mới và kiểm phiên cũ | Phiên mới dùng ISP2 theo cơ chế đã chọn; đo thời gian quan sát; ghi phiên cũ có bị đứt |
| Mất ISP2 | Khôi phục trạng thái ban đầu, rồi ngắt ISP2 | Kiểm độc lập chiều ngược lại; phiên mới dùng ISP1 |
| Lỗi upstream | Giữ cổng local up nhưng làm mất đích theo dõi/khả năng đi tiếp của ISP lab | Cơ chế theo dõi phát hiện lỗi nếu được triển khai; không chỉ kiểm cable-down |
| Mất cả hai ISP | Ngắt cả hai đường, xem route/default ở Main và Aux | Thu hồi default theo thiết kế; Internet không truy cập được, liên site còn hoạt động nếu hai leased lines còn tốt |
| Phục hồi ISP | Khôi phục lần lượt các đường; kiểm route, phân phối phiên và NAT | Phiên mới hoạt động trở lại; lưu thời gian và hiện tượng dao động nếu có |
| Mất một leased line | Ngắt Main–DBP hoặc Main–BHTQ theo lượt | Ghi đúng site bị mất kết nối; nhánh kia không bị ảnh hưởng ngoài thiết kế; không tuyên bố có dự phòng cho nhánh mất đường |
| Sau bật ACL/VPN | Chạy lại lưu lượng nội bộ được phép và TC03/TC06 liên quan | Không bị PAT nội bộ ngoài ý muốn; route về đúng; chính sách chặn vẫn được giữ |

Mỗi lần chạy ghi ngày/người thực hiện, nền tảng/model/phiên bản, file mô phỏng/hash, điều kiện trước, nguồn/đích, thao tác, expected, actual, trạng thái và đường dẫn ảnh/log. Cần lưu route, láng giềng, counter/translation phù hợp cùng kết quả ứng dụng. Không dùng một ảnh ping hoặc một phiên TCP để kết luận cân bằng tải hay tốc độ tổng hai ISP.

Nếu FAIL: mở lỗi với bước tái hiện, xác định chủ trì, sửa trên phiên bản mới và chạy lại ca bị ảnh hưởng. Nếu tính năng chưa chạy được: ghi NOT RUN/BLOCKED hoặc DESIGN ONLY/MODELED đúng ngữ cảnh; ghi hướng xử lý và ảnh hưởng tới yêu cầu. Không chuyển thành PASS chỉ để đạt mốc thời gian.

**Cổng G3:** có hồ sơ cho cả TC01–TC06; TV1 xác nhận phần routing/Internet, review bằng chứng phần còn lại với chủ trì chuyên môn; contribution WAN có đủ thiết kế, config, kiểm chứng và giới hạn.

## 6. Tuần 4 — Báo cáo, duyệt và đóng gói, 16/11–22/11

| Ngày | Giờ | Công việc cụ thể | Sản phẩm / điều kiện xong | Task gốc |
| --- | --- | --- | --- | --- |
| 16/11 | 2 | Ưu tiên sửa lỗi WAN/ISP chặn nghiệm thu; TV4 ghép và retest; rà toàn bộ phần WAN trong báo cáo | Cấu hình ứng viên và danh mục bằng chứng cập nhật | W4-TV1-01, W4-TV1-03 |
| 17/11 | 2 | Chốt IP/WAN/OSPF/dual ISP/chi phí; giao bảng, sơ đồ, config và giải thích test cho TV5 | `TV1-wan-routing.md` hoàn chỉnh và phần kỹ thuật có thể đưa vào báo cáo | W4-TV1-01 |
| 18/11 | 1,5 | Đối chiếu topology–IP–config–test–contribution; kiểm hạn chế và đánh giá 5 năm | Các số liệu/địa chỉ/phiên bản nhất quán; thiếu sót có người xử lý | W4-TV1-03 |
| 19/11 | 2 | Đọc PDF review của TV5; rà đủ 7 Step, ba site, tăng trưởng, VPN/camera, sáu nhóm test; nhận xét theo trang/mục | `docs/06-report/review-log.md` có phản hồi cụ thể | W4-TV1-02 |
| 20/11 | 1,5 | Xác nhận phản hồi đã sửa; xem log retest và xử lý giới hạn còn lại | Đóng lỗi đã giải quyết; lỗi còn lại được phản ánh đúng trong tài liệu | W4-TV1-03 |
| 21/11 | 1,5 | Cùng TV4/TV5 kiểm gói: PDF, nguồn, mô phỏng, cấu hình, evidence, hướng dẫn, manifest/hash; xem log mở lại | Bộ ứng viên sẵn sàng để duyệt; sai lệch phải sửa trước khi ký | W4-TV1-04 |
| 22/11 | 1,5 | Duyệt riêng PDF và mô phỏng; ghi kết luận G4; chốt người theo dõi lỗi và lịch khóa/nộp | `submission/approval.md` theo đúng phiên bản/hash; kế hoạch dự phòng và release theo quyền repo | W4-TV1-04, W4-TV1-05 |
| **Tổng** | **12** | | | |

### 6.1. Nội dung TV1 giao cho TV5

Hoàn thiện [contribution TV1](../06-report/contributions/TV1-wan-routing.md) theo thứ tự:

1. Yêu cầu liên quan, nguồn trang theo hồ sơ dự án và các giả định đã dùng.
2. Bảng IP/subnet, cách tính dung lượng và lý do chọn kích thước mạng.
3. Sơ đồ WAN, interface mapping, OSPF và đường đi Internet qua Main.
4. Hai ISP: phân phối luồng, điều kiện default, phối hợp NAT và hành vi khi lỗi.
5. So sánh WAN/chi phí, nguồn giá hoặc biến còn chờ; giải thích lựa chọn.
6. Phương pháp và bằng chứng TC03, phần liên quan TC06, test dual ISP; trích config cần thiết.
7. Đánh giá SPOF, tác động đứt leased line/ISP, khả năng nâng cấp và phần chưa mô phỏng.
8. Danh mục hình/bảng/config/evidence và phản hồi đọc chéo đã xử lý.

### 6.2. Điều kiện TV1 ký duyệt

- **PDF:** đủ yêu cầu theo truy vết; bảng IP và sơ đồ khớp cấu hình; số liệu có nguồn/giả định; hình rõ chữ; kết luận test khớp actual; giới hạn được mô tả đúng.
- **Mô phỏng:** mở lại bằng môi trường đã ghi; cấu hình còn lưu; kiểm nhanh các ca cần thiết trên bản ứng viên; dependency đủ nếu dùng GNS3; lỗi chặn đã được xử lý.
- **Hồ sơ:** manifest liệt kê đúng file; checksum tính từ bản cuối; approval ghi riêng phiên bản/hash PDF và mô phỏng cùng kết luận. Mọi thay đổi sau đó phải cập nhật hash và tái duyệt sản phẩm bị đổi.

Nếu chưa đạt, ghi “chưa duyệt”, lý do, người sửa và hạn kiểm lại. TV1 duyệt cuối dựa trên sản phẩm/bằng chứng; kế hoạch này không thay thế việc nghiệm thu thực tế.

## 7. Nhịp phối hợp và quản lý 48 giờ

| Phối hợp | Đầu vào cần nhận | TV1 trả lại | Mốc chính |
| --- | --- | --- | --- |
| TV2 | VLAN, host, gateway/SVI, thiết bị và LAN uplink | IP plan, transit, route tới LAN và góp ý dung lượng | 29/10; 04–06/11 |
| TV3 | Server/VPN pool, vùng firewall, ma trận quyền, NAT | Route/default/egress, đường về; config hợp nhất trên node dùng chung | 29–30/10; 05–06/11; 09–14/11 |
| TV4 | Số tải, công cụ/model, mapping file tổng, lịch test | Module, config, hướng dẫn mở/nạp, expected và hỗ trợ test | 30/10; 05–06/11; 11–15/11; 21/11 |
| TV5 | Khung báo cáo, danh mục thiếu, PDF review, manifest | Contribution, hình/bảng, nhận xét và kết quả duyệt | 08/11; 15/11; 17/11; 19–22/11 |

Mỗi buổi dành khoảng 10 phút trong thời lượng đã phân bổ để cập nhật: đã làm gì, sản phẩm ở đâu, việc tiếp theo và vướng mắc. Cuối tuần dùng thời gian G1–G4 trong bảng để review. Khi có nguy cơ vượt 12 giờ/tuần, TV1 điều phối hỗ trợ và giảm thời gian trang trí/tối ưu không cần thiết, vẫn giữ kiểm thử và ghi nhận yêu cầu chưa đạt.

Trong khoảng dự phòng 23/11–06/12, chỉ xử lý lỗi/phản hồi phát sinh, retest và tái duyệt. Không tính mặc định thêm hai tuần làm việc đầy đủ vào ngân sách 48 giờ. TV1 nộp đúng bản đã duyệt khi BKeL mở; TV5 lưu xác nhận nộp và đối chiếu danh mục.

## 8. Buổi bắt đầu ngày 26/10 — 90 phút

| Phút | Việc làm | Kết quả cuối bước |
| --- | --- | --- |
| 0–20 | Đọc phần TV1 trong phân công, IP baseline và kiến trúc | Nắm phạm vi, hạn và các dữ kiện chưa chốt |
| 20–40 | Rà repo/template, chuẩn bị danh sách task/milestone theo quyền hiện có | Biết phần quản lý đã có và phần cần bổ sung |
| 40–60 | Chuẩn bị yêu cầu đầu vào cho TV2/TV3/TV4: VLAN/host, firewall/NAT, model và tải | Danh sách dependency có người phụ trách và hạn |
| 60–80 | Lập danh mục bảng IP, interface mapping, route kỳ vọng và hồ sơ bàn giao | Có khung sản phẩm để làm ngày 27/10 |
| 80–90 | Cập nhật ghi chú tiến độ, xác định việc tiếp theo và vướng mắc | Bắt đầu được buổi quy hoạch IP, không cần đợi toàn bộ nhóm hoàn tất |

**Ưu tiên đầu tiên:** khóa bảng IP và giao diện với TV2/TV3, đồng thời thử khả năng hai ISP với TV4 trong tuần 1. Hai việc này quyết định các module có tích hợp được và các yêu cầu WAN có kiểm chứng được trong lịch 4 tuần hay không.
