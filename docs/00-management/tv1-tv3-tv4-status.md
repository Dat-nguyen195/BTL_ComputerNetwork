# Phân tích và bàn giao TV1, TV3, TV4

**Cập nhật sau hoàn thiện:** [review hiện tại](project-review.md) ghi GNS352 node, runtime và PDF đã có; các checklist/trạng thái chuẩn bị bên dưới là bàn giao trước đợt này. Phê duyệt người phụ trách, khảo sát và triển khai vật lý vẫn cần xác nhận riêng.

**Ngày 02/11/2026. Phạm vi: hoàn thiện thiết kế, cấu hình, tính tải và hồ sơ có thể thực hiện trong repo.** Chưa có môi trường Packet Tracer/GNS3/IOS, project, runtime evidence, xác nhận reviewer hoặc PDF tổng của TV5. Không coi bộ text/config là đã hoàn thành Step4–5; không ký duyệt thay thành viên.

## Phát hiện và xử lý

| Điểm thiếu / rủi ro | Sản phẩm đã bổ sung |
| --- | --- |
| TV3/TV4 contributions chỉ là khung | Nội dung báo cáo đầy đủ, gắn nguồn/thiết kế/config/test/giới hạn |
| Server chưa có vai trò/IP từng máy |14 server đúng 10/2/2, DNS/DHCP/dịch vụ, inventory và 18 pool |
| Lọc tập trung tại FW bỏ sót east-west | ACL inbound từng client/server/mgmt/camera VLAN tại Core/Aux; ZBF tại FW |
| Guest chưa có positive control |61 flow ACL, TC05 cả 3 site, DNS/DHCP/Web ngoài được đối chứng |
| DMZ hai ISP có nguy cơ reply sai egress | Một static PAT ISP2:8080, PBR DMZ ưu tiên ISP2; ghi rõ chưa inbound HA |
| Tính tải thủ công và phạm vi server mơ hồ | Script CSV/stdlb,3 scope server,2 scope guest, unknown upload, overhead/shares và 6 nhóm kiểm số học |
| Chưa có hợp đồng nạp/port/đầu cuối |9 router +5 switch tối thiểu hợp nhất,14 link,30 endpoint,18 pool, manifest SHA256 |
| Test chỉ là mô tả chung | Runbook TC01–06, SUPP01–05, mẫu actual/hash/log/retest; vẫn NOT RUN |

## Đối chiếu task chính

`Có sản phẩm` dưới đây là đã soạn/cấu hình/kiểm tĩnh. Task chính có điều kiện review, runtime hoặc bàn giao vẫn mở theo quy tắc checklist. Chỉ các bước con đủ bằng chứng được tích; không tự thêm xác nhận của TV2/TV5 hoặc giả ngày họp.

| TV1 / task | Đã có | Còn để đóng task |
| --- | --- | --- |
| W1-TV1-01 | Repo, template, checklist, kiểm CI local | Handles/quyền và milestone/issue GitHub thực |
| W1-TV1-02 | IP/VLSM, không overlap, gateway/pool/server cụ thể | TV2 đọc chéo, TV3 xác nhận chính thức, khóa khảo sát |
| W1-TV1-03 | Thiết kế WAN đã được checklist ghi hoàn thành trước lần này | G1/runtime ở task riêng |
| W1-TV1-04 | Tải down/up, PBR group, TCO giả định, danh mục dữ liệu chờ có owner/hạn | Báo giá/khảo sát và reviewer thật |
| W1-TV1-05 | Capability matrix và điều kiện G1 | Thử model/công cụ, họp G1 xác nhận |
| W2-TV1-01 | OSPF/static/default hợp nhất; kiểm9 tình huống tĩnh | Nạp IOS, neighbor/route/TC03 actual |
| W2-TV1-02 | Edge/ISP/Web/PBR/PAT và overlay DMZ | Parser/feature/runtime dual ISP |
| W2-TV1-03 | Mapping/thứ tự nạp/module/integration log offline | TV4 nhận và ghép project |
| W2-TV1-04 | Smoke procedure WAN/Web và chi phí cập nhật | Smoke log và phản hồi thực |
| W2-TV1-05 | Contribution TV1 cập nhật | Project mở lại, review G2 |
| W3-TV1-01 | Cấu hình, expected TC03 bốn chiều | Actual route/ping/traceroute |
| W3-TV1-02 |9 ca lỗi trong model và SUPP01 | NAT/phiên/timer/failover runtime |
| W3-TV1-03 | Route + policy/NAT cùng bộ hợp nhất | TC06/route VPN runtime nếu triển khai |
| W3-TV1-04 | Danh mục lỗi/giới hạn, test matrix | Review evidence6 nhóm, G3 |
| W3-TV1-05 | Contribution WAN/IP/chi phí/SPOF | Bàn giao có nhận và test thực |
| W4-TV1-01 | Nội dung/bảng/config ứng viên kỹ thuật | Chốt sau khảo sát/review/runtime |
| W4-TV1-02 | Tiêu chí review có sẵn | PDF tổng TV5 và review theo trang |
| W4-TV1-03 | Offline check tự động, danh mục phần thiếu | Lỗi runtime/retest và xác nhận đồng bộ bản cuối |
| W4-TV1-04 | Approval giữ PENDING, có tiêu chí | PDF/project/hash/persistence và chữ ký thật |
| W4-TV1-05 | Lịch khóa/nộp giữ nguyên | Release/tag/bản ứng viên được duyệt thực |

| TV3 / task | Đã có | Còn để đóng task |
| --- | --- | --- |
| W1-TV3-01 | Server plan14 máy,10/2/2, địa chỉ/role/backup | Review vai trò/HA/RPO/RTO |
| W1-TV3-02 | Matrix và ACL in cả 3 site, rule order/binding | Review và kiểm runtime |
| W1-TV3-03 | PAT/egress/static mapping/exemption | TC04/06, translation/session thật |
| W1-TV3-04 | VPN VTI/teleworker, IDS/IPS và feature scope | Xác nhận chương trình/công cụ |
| W1-TV3-05 | Camera bitrate/retention/PoE, security guide | TV2 khảo sát/cáp/PoE và G1 |
| W2-TV3-01 | Inventory/services/DHCP/DNS nhập được | Tạo server trên project và smoke |
| W2-TV3-02 | PAT được giữ trong 9 config hợp nhất | NAT runtime ba site |
| W2-TV3-03 | ZBF + static PATISP2 và ma trận công bố | Parser/HTTP/stateful/drop evidence |
| W2-TV3-04 | Module + runbook/integration notes | TV4 nhận/ghép và smoke actual |
| W2-TV3-05 | Contribution và kế hoạch chi tiết | Bàn giao/review G2 |
| W3-TV3-01 | ACL gateway, ZBF và 61 flow tĩnh | Hardening đầy đủ và test runtime |
| W3-TV3-02 | TC04 outside/inside/negative, NAT before/after | PDU/translation/session thật |
| W3-TV3-03 | TC05 mỗi guest, ICMP/TCP + positive control | Deny counter/ứng dụng/ảnh thật |
| W3-TV3-04 | VPN/IDS-IPS plan và SUPP03/04 | Crypto/sensor/client và test nếu áp dụng |
| W3-TV3-05 | Security guide, backup/rollback/risks | Review, triển khai phần còn thiếu, G3 |
| W4-TV3-01 | Contribution đầy đủ, config/phụ lục | Khóa sau test/review; bàn giao chính thức |
| W4-TV3-02 | Hệ thống kiểm tĩnh và retest procedure | Actual lỗi/retest security |
| W4-TV3-03 | Phân biệt NAT/policy/design/runtime | PDF tổng và review theo trang; [R] gốc hiện thiếu |
| W4-TV3-04 | Không đưa secret vào config; hướng dẫn vận hành | Rà credential/ảnh trên bản runtime/cuối |
| W4-TV3-05 | Persistence procedure với security | Project đóng gói/mở lại và xác nhận G4 |

| TV4 / task | Đã có | Còn để đóng task |
| --- | --- | --- |
| W1-TV4-01 | CSV/assumptions đúng 1120 PC/14 server/3h | Chốt scope server/guest và khảo sát |
| W1-TV4-02 | Script/công thức/down-up/site/20% và 6 nhóm số học | Reviewer và tỷ lệ LAN/WAN/Internet thực |
| W1-TV4-03 | ISP từng chiều, một/hai đường, khoảng thiếu | Tải thiết yếu/báo giá/xDSL khả dụng |
| W1-TV4-04 | Precheck môi trường, cabling/port/inventory/capability | Cài/chọn công cụ/image hợp pháp, skeleton project |
| W1-TV4-05 | TC01–06 + SUPP01–05, precondition/expected | Review G1, actual ở giai đoạn sau |
| W2-TV4-01 | Tên node/port/VLAN/subnet,14 link,9+5config | File tổng và lịch thao tác project |
| W2-TV4-02 | Bộ ghép config/module/checker | Ghép LAN TV2 và dựng project thật |
| W2-TV4-03 | Smoke procedure, mẫu lỗi/retest | Smoke log/ticket runtime |
| W2-TV4-04 | Cách mở/nạp/mapping/giới hạn | Model/version/image được thử thực |
| W2-TV4-05 | Contribution và persistence procedure | Save/close/reopen, G2 |
| W3-TV4-01 | Baseline config manifest + capacity CSV | Khóa project/hash chạy test |
| W3-TV4-02 | TC01/02/03 hồ sơ và runbook | Actual/evidence/review TV1/TV2 |
| W3-TV4-03 | TC04/05/06 đủ nguồn/negative/positive | Actual/evidence/review TV3 |
| W3-TV4-04 | SUPP01–05 và expected | Runtime failover/VPN/IDS-IPS/HA theo scope |
| W3-TV4-05 | Cách version/evidence/persistence + contribution | Evidence manifest6 nhóm và G3 |
| W4-TV4-01 | Nội dung Step3–5 và gói tham chiếu | Project +6 evidence thật và bản ứng viên |
| W4-TV4-02 | Build/check/retest procedure | Tích hợp lỗi runtime, retest ứng viên |
| W4-TV4-03 | README dựng/nạp/mapping/known limitations | Cập nhật version/model/ảnh từ project thực |
| W4-TV4-04 | Hướng dẫn persistence/hash | Project mở lại được và log xác nhận |
| W4-TV4-05 | SHA256 gói config, submission vẫn PENDING | PDF/project cuối +manifest/hash đúng cặp |

## Dependency cần giải quyết

Các hạn sau là mốc xử lý đề xuất, chưa được thành viên cam kết.

| Dữ liệu / công việc | Người chủ trì | Hạn đề xuất | Tác động |
| --- | --- | --- | --- |
| Công cụ/model/image hợp pháp, feature support | TV4 + TV1/TV3 |04/11/2026 | Chặn project/runtime Step4–5 |
| LAN/trunk/SSID/BOM và L2 guest isolation | TV2 |05/11/2026 | Chặn tích hợp campus và kiểm Wi-Fi |
| Scope server/guest, khách đồng thời/ngày, Internet share, tải HIS/PACS/backup | TV4 + TV5 khảo sát |05/11/2026 | Chưa chốt sizing/ISP/leased line |
| Camera/retention/PoE và RPO/RTO | TV3 + TV2/TV5 |06/11/2026 | Chưa chốt lưu trữ/BOM/HA |
| Báo giá hai leased lines/hai xDSL, SLA/public IP/handoff/thuế | TV1 + TV2 |08/11/2026 | TCO chỉ minh họa, chưa mua/chốt gói |
| Phạm vi chương trình kỹ sư tài năng | TV1 + TV3 |04/11/2026 | Chốt yêu cầu triển khai IDS/IPS |
| Handles/quyền/milestones GitHub và xác nhận đọc chéo | TV1 + từng thành viên |04/11/2026 | Quản lý/review chính thức chưa đóng |
| PDF tổng do TV5 biên tập | TV5 |19/11/2026 | TV1/TV3 review và ký đúng hash |

## Điểm bắt đầu tiếp theo

TV4 chọn môi trường hỗ trợ và dựng theo [simulation README](../../simulation/README.md); TV2 ghép module LAN; TV1/TV3 kiểm CLI/route/policy; chạy [test matrix](../../test_results/test-matrix.md) rồi lưu hash/evidence/persistence. TV5 có thể biên tập ngay ba contributions nhưng giữ trạng thái chưa kiểm runtime. [Hồ sơ kiểm tĩnh](../../test_results/static/README.md) ghi kết quả thực chạy trong workspace; không thay xác nhận của reviewer.
