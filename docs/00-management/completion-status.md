# Đối chiếu hoàn thiện100 task

**Thông tin nhóm đã chốt theo nhóm trưởng:** lớp L08, nhóm 2; BTL2 do Nguyễn Thành Đạt (nhóm trưởng, 2410709) và Phạm Tiến Đạt (2410723) thực hiện. Ba thành viên Nguyễn Phúc Bảo Đạt, Bùi Công Danh, Nguyễn Minh Đạt thực hiện BTL1. Xem [danh sách và email](team-members.md). TV1–TV5 là năm vai trò trong kế hoạch ban đầu.


**Kết quả kỹ thuật Packet Tracer04/11/2026:** native58 node/53 cáp/sáu Wi-Fi đã lưu/mở lại; 32/32 quan sát phù hợp kỳ vọng,19 client DHCP và18 pool có sức chứa. Bốn HTTP chọn ISP1 thủ công/khôi phục ISP2 đạt; không có tự động failover trên Packet Tracer. Chi tiết ở [hồ sơ Packet Tracer](../../test_results/packet-tracer/README.md). Phê duyệt nhóm/thông tin nhân sự/BKeL vẫn chờ xác nhận. Các ghi nhận đang dựng/đang chờ bên dưới là lịch sử.

**03/11/2026, giờ Việt Nam.** Bảng này giải thích checklist chính tại [tasks-assignment.md](../../tasks-assignment.md), không tạo thêm một bảng phê duyệt. `CÓ SẢN PHẨM` nghĩa là tài liệu/mã/evidence đã có, còn điều kiện ở cột cuối. `MỘT PHẦN` có đầu ra hoặc phạm vi kiểm chưa đủ. `CHỜ NHÓM` cần người phụ trách quyết định/duyệt. Không đồng nhất các trạng thái này với task đã được nghiệm thu.

GNS3 có runtime lưu ngày02/11; Windows hiện tại không chạy lại mạng đó. Packet Tracer9.0.1 đã có native tổng và32 quan sát sau reopen, sáu BSSID/IP,19 DHCP client; bốn HTTP chọn ISP thủ công/khôi phục ISP2 đạt. Báo cáo chính được bổ sung bảng IP/VLAN, BOM, sơ đồ vật lý và demo trong lần chốt 05/11; phụ lục Packet Tracer hai trang có QA riêng. L08, nhóm 2 và hai người thực hiện BTL2 đã có. Tên giảng viên chưa được cung cấp nên tự ẩn trên bìa.

| ID | Tình trạng kỹ thuật | Sản phẩm/bằng chứng | Còn để nghiệm thu |
| --- | --- | --- | --- |
| W1-TV1-01 | MỘT PHẦN | [.github](../../.github/) | Quyền/handle và milestone GitHub chưa xác nhận |
| W1-TV1-02 | CÓ SẢN PHẨM | [ip-vlan-plan.md](../../docs/02-design/ip-vlan-plan.md) | TV2/TV3 đọc chéo và khóa giả định |
| W1-TV1-03 | CÓ SẢN PHẨM | [architecture.md](../../docs/02-design/architecture.md) | Đã được checklist ghi hoàn tất; nghiệm thu runtime ở task riêng |
| W1-TV1-04 | CÓ SẢN PHẨM | [wan-options-cost.md](../../docs/02-design/wan-options-cost.md) | Báo giá/SLA và số liệu workload cần nhóm xác nhận |
| W1-TV1-05 | MỘT PHẦN | [meeting-notes.md](../../docs/00-management/meeting-notes.md) | Chưa có biên bản G1 được nhóm xác nhận |
| W1-TV2-01 | CÓ SẢN PHẨM | [physical-main.drawio](../../docs/02-design/diagrams/physical-main.drawio) | Mặt bằng là giả định; chờ đọc chéo |
| W1-TV2-02 | CÓ SẢN PHẨM | [lan-port-plan.md](../../docs/02-design/lan-port-plan.md) | TV2 xác nhận IP/port plan |
| W1-TV2-03 | CÓ SẢN PHẨM | [physical-cabling.md](../../docs/02-design/physical-cabling.md) | GPON/quang là thiết kế; chưa khảo sát |
| W1-TV2-04 | CÓ SẢN PHẨM | [equipment-bom.md](../../docs/02-design/equipment-bom.md) | Chờ giá/model/khảo sát và đọc chéo |
| W1-TV2-05 | CÓ SẢN PHẨM | [wireless-plan.md](../../docs/02-design/wireless-plan.md) | Chưa đo RF/AAA/roaming; chờ G1 |
| W1-TV3-01 | CÓ SẢN PHẨM | [server-dmz-plan.md](../../docs/02-design/server-dmz-plan.md) | Chờ xác nhận chuyên môn |
| W1-TV3-02 | CÓ SẢN PHẨM | [security-policy.md](../../docs/04-security/security-policy.md) | Chờ đọc chéo quyền nghiệp vụ |
| W1-TV3-03 | CÓ SẢN PHẨM | [nat-pat.md](../../docs/04-security/nat-pat.md) | Chờ đọc chéo; IOS chưa chạy |
| W1-TV3-04 | CÓ SẢN PHẨM | [vpn-plan.md](../../docs/04-security/vpn-plan.md) | VPN crypto DESIGN ONLY; IDS/IPS có rule mẫu GNS3 |
| W1-TV3-05 | CÓ SẢN PHẨM | [camera-plan.md](../../docs/02-design/camera-plan.md) | Camera/bitrate/retention là giả định; chờ TV2/G1 |
| W1-TV4-01 | CÓ SẢN PHẨM | [assumptions.md](../../docs/03-capacity/assumptions.md) | Workload/khách/Internet share chờ xác nhận |
| W1-TV4-02 | CÓ SẢN PHẨM | [throughput.md](../../docs/03-capacity/throughput.md) | 6 nhóm unit số học có; chờ xác nhận giả định |
| W1-TV4-03 | CÓ SẢN PHẨM | [wan-options-cost.md](../../docs/02-design/wan-options-cost.md) | Không khẳng định xDSL thương mại đủ tải |
| W1-TV4-04 | CÓ SẢN PHẨM | [hospital-3sites.gns3](../../simulation/gns3/hospital-3sites.gns3) | GNS3 có52 node; Packet Tracer tổng58 node và evidence32+4 đã có |
| W1-TV4-05 | CÓ SẢN PHẨM | [test-matrix.md](../../test_results/test-matrix.md) | TC01–06 có GNS3 evidence; chờ G1 |
| W1-TV5-01 | CÓ SẢN PHẨM | [survey-checklist.md](../../docs/01-survey/survey-checklist.md) | Có checklist; chưa khảo sát thực địa |
| W1-TV5-02 | CÓ SẢN PHẨM | [requirements-traceability.md](../../docs/00-management/requirements-traceability.md) | Chờ nhóm xác nhận đăng ký5 người/lịch/hạn |
| W1-TV5-03 | CÓ SẢN PHẨM | [README.md](../../docs/06-report/source/README.md) | Nguồn Markdown/LaTeX và5 contributions đã có; chờ nhóm |
| W1-TV5-04 | CÓ SẢN PHẨM | [report.tex](../../docs/06-report/latex/report.tex) | Bản hiện tại thay bản nháp lịch sử0.1; chưa có biên bản phát hành cũ |
| W1-TV5-05 | CÓ SẢN PHẨM | [evaluation.md](../../docs/05-evaluation/evaluation.md) | Có evaluation/risks; G1 chưa xác nhận |
| W2-TV1-01 | CÓ SẢN PHẨM | [result.md](../../test_results/TC03-inter-site/result.md) | OSPF/ping hai chiều có trên cả hai; Packet Tracer sau warmup/reopen đạt, chờ nhóm đọc chéo |
| W2-TV1-02 | CÓ SẢN PHẨM | [dual-isp-failover.md](../../test_results/supplemental/dual-isp-failover.md) | PBR/NAT upstream GNS3 đã chạy; probe Packet Tracer từ chối IP SLA/PBR, dự phòng thủ công |
| W2-TV1-03 | CÓ SẢN PHẨM | [integration-log.md](../../simulation/integration-log.md) | Mô hình tổng GNS3 đã tích hợp; chờ TV4 xác nhận bàn giao |
| W2-TV1-04 | CÓ SẢN PHẨM | [results.json](../../test_results/runtime/after-firewall-restart-runtime/results.json) | Có route/OSPF/ping/traceroute; chi phí thật chờ xác nhận |
| W2-TV1-05 | CÓ SẢN PHẨM | [persistence.md](../../test_results/supplemental/persistence.md) | Có reopen lịch sử; biên bản G2 chờ nhóm |
| W2-TV2-01 | CÓ SẢN PHẨM | [README.md](../../simulation/packet-tracer/README.md) | Native Packet Tracer58 node/53 cáp/sáu Wi-Fi đã kiểm; chờ TV2/TV4 duyệt |
| W2-TV2-02 | CÓ SẢN PHẨM | [hospital-3sites.gns3](../../simulation/gns3/hospital-3sites.gns3) | Aux có trên cả hai nền tảng; Wi-Fi/HIS/Web Packet Tracer sau reopen đạt; chờ nhóm |
| W2-TV2-03 | MỘT PHẦN | [dhcp-dns.md](../../test_results/supplemental/dhcp-dns.md) | Packet Tracer18 pool có sức chứa, ba mặc định sức chứa0 và sáu BSSID/IP giữ sau reopen; RF/AAA chưa đo |
| W2-TV2-04 | CÓ SẢN PHẨM | [result.md](../../test_results/TC01-same-vlan/result.md) | LAN GNS3 có test; bàn giao TV2/G2 chưa xác nhận |
| W2-TV2-05 | CÓ SẢN PHẨM | [TV2-lan-wireless.md](../../docs/06-report/contributions/TV2-lan-wireless.md) | Có drawio/SVG/contribution; G2 chờ nhóm |
| W2-TV3-01 | CÓ SẢN PHẨM | [server-dmz-plan.md](../../docs/02-design/server-dmz-plan.md) | 14 server10/2/2 trong GNS3; clinical apps chỉ HTTP đại diện |
| W2-TV3-02 | CÓ SẢN PHẨM | [result.md](../../test_results/TC06-internet-web/result.md) | PAT GNS3 và HTTP/PAT Packet Tracer có evidence riêng; chờ nhóm đọc chéo |
| W2-TV3-03 | CÓ SẢN PHẨM | [result.md](../../test_results/TC04-dmz/result.md) | DMZ/static PAT có HTTP đúng marker trên cả hai; Packet Tracer sau reopen đạt |
| W2-TV3-04 | CÓ SẢN PHẨM | [integration-log.md](../../simulation/integration-log.md) | Có log tích hợp GNS3; chờ xác nhận TV4 |
| W2-TV3-05 | CÓ SẢN PHẨM | [TV3-security-systems.md](../../docs/06-report/contributions/TV3-security-systems.md) | Contribution có; VPN crypto DESIGN ONLY; chờ G2 |
| W2-TV4-01 | CÓ SẢN PHẨM | [hospital-3sites.gns3](../../simulation/gns3/hospital-3sites.gns3) | Có native tổng cả hai; Packet Tracer đạt32 quan sát sau reopen và bốn HTTP ISP thủ công; chờ TV4/TV1 |
| W2-TV4-02 | CÓ SẢN PHẨM | [runtime-manifest.json](../../simulation/gns3/runtime-manifest.json) | GNS3:52 node/52 link; Packet Tracer:58 node/53 cáp/sáu Wi-Fi; provenance riêng đã kiểm |
| W2-TV4-03 | CÓ SẢN PHẨM | [README.md](../../test_results/runtime/README.md) | Smoke GNS3 có actual/log; không phải lần chạy mới trên Windows |
| W2-TV4-04 | CÓ SẢN PHẨM | [README.md](../../simulation/gns3/README.md) | Version2.2.55/Linux/FRR và giới hạn đã ghi |
| W2-TV4-05 | CÓ SẢN PHẨM | [reopen.json](../../test_results/runtime/persistence/reopen.json) | Reopen137 kiểm là lịch sử trước sửa PID; G2 chờ nhóm |
| W2-TV5-01 | CÓ SẢN PHẨM | [TV1-wan-routing.md](../../docs/06-report/contributions/TV1-wan-routing.md) | Đủ5 contribution; chưa có xác nhận giao nhận cá nhân |
| W2-TV5-02 | CÓ SẢN PHẨM | [report.tex](../../docs/06-report/latex/report.tex) | Báo cáo hiện tại thay nháp0.2; không tạo giả ngày phát hành cũ |
| W2-TV5-03 | CÓ SẢN PHẨM | [README.md](../../docs/06-report/latex/README.md) | Có heading/mục lục/font và QA PDF; LaTeX dùng XeLaTeX |
| W2-TV5-04 | CÓ SẢN PHẨM | [risks.md](../../docs/05-evaluation/risks.md) | Có SPOF/xDSL/phần mềm/giới hạn; chờ G2 |
| W2-TV5-05 | CÓ SẢN PHẨM | [requirements-traceability.md](../../docs/00-management/requirements-traceability.md) | Đủ truy vết/hướng dẫn; G2 chưa họp/xác nhận |
| W3-TV1-01 | CÓ SẢN PHẨM | [result.md](../../test_results/TC03-inter-site/result.md) | Main↔Aux có trên cả hai; Packet Tracer sau warmup/reopen mỗi ping4/4 |
| W3-TV1-02 | CÓ SẢN PHẨM | [dual-isp-failover.md](../../test_results/supplemental/dual-isp-failover.md) | Có upstream fault/convergence; local-link/session cũ chưa thử |
| W3-TV1-03 | CÓ SẢN PHẨM | [result.md](../../test_results/TC06-internet-web/result.md) | Web3 site/PAT có; VPN crypto chưa chạy |
| W3-TV1-04 | CÓ SẢN PHẨM | [project-review.md](../../docs/00-management/project-review.md) | Có review kỹ thuật; G3/đọc chéo nhóm chưa xác nhận |
| W3-TV1-05 | CÓ SẢN PHẨM | [TV1-wan-routing.md](../../docs/06-report/contributions/TV1-wan-routing.md) | Có nội dung/tải/chi phí/SPOF; giả định và bàn giao chờ nhóm |
| W3-TV2-01 | CÓ SẢN PHẨM | [result.md](../../test_results/TC01-same-vlan/result.md) | TC01/TC02 có log cả hai; Packet Tracer sau warmup/reopen đạt; chờ nhóm |
| W3-TV2-02 | MỘT PHẦN | [dhcp-dns.md](../../test_results/supplemental/dhcp-dns.md) | Sáu WLAN/19 DHCP client và Web/DNS Packet Tracer giữ sau reopen; RF/AAA/roaming chưa đo |
| W3-TV2-03 | CÓ SẢN PHẨM | [campus-budget.csv](../../docs/02-design/campus-budget.csv) | Port/PoE/growth và sơ đồ đồng bộ; RF chưa thử |
| W3-TV2-04 | CÓ SẢN PHẨM | [camera-plan.md](../../docs/02-design/camera-plan.md) | Camera/NVR/storage là thiết kế; chưa đo bitrate thực |
| W3-TV2-05 | CÓ SẢN PHẨM | [TV2-lan-wireless.md](../../docs/06-report/contributions/TV2-lan-wireless.md) | Nguồn/hình có; bàn giao/đọc chéo G3 chờ nhóm |
| W3-TV3-01 | CÓ SẢN PHẨM | [result.md](../../test_results/TC05-guest-isolation/result.md) | Guest ACL/firewall/DNS/Web GNS3 có; IOS chưa chạy |
| W3-TV3-02 | CÓ SẢN PHẨM | [result.md](../../test_results/TC04-dmz/result.md) | DMZ/published service/NAT có log GNS3 |
| W3-TV3-03 | CÓ SẢN PHẨM | [result.md](../../test_results/TC05-guest-isolation/result.md) | ICMP/TCP âm+dương và DROP counters có ở3 site GNS3 |
| W3-TV3-04 | MỘT PHẦN | [vpn.md](../../test_results/supplemental/vpn.md) | VPN crypto/HA chưa chạy; IDS/IPS rule mẫu có |
| W3-TV3-05 | CÓ SẢN PHẨM | [security-best-practices.md](../../docs/04-security/security-best-practices.md) | Có guide/contribution; AAA/NTP/backup thực chưa thử đủ |
| W3-TV4-01 | CÓ SẢN PHẨM | [runtime-manifest.json](../../simulation/gns3/runtime-manifest.json) | Có source/live/project hashes; bản sinh portable giữ nguyên runtime bytes |
| W3-TV4-02 | CÓ SẢN PHẨM | [results.json](../../test_results/runtime/after-firewall-restart-runtime/results.json) | TC01–03 actual có; chờ TV1/TV2 chuyên môn |
| W3-TV4-03 | CÓ SẢN PHẨM | [results.json](../../test_results/runtime/after-firewall-restart-runtime/results.json) | TC04–06 actual/PCAP có; chờ TV3 chuyên môn |
| W3-TV4-04 | MỘT PHẦN | [README.md](../../test_results/supplemental/README.md) | ISP/IDS mẫu PASS GNS3; VPN/HA và PT NOT RUN |
| W3-TV4-05 | CÓ SẢN PHẨM | [TV4-capacity-testing.md](../../docs/06-report/contributions/TV4-capacity-testing.md) | Có evidence/reopen/contribution; source PID mới chưa reopen lại trọn trên máy này |
| W3-TV5-01 | CÓ SẢN PHẨM | [test-matrix.md](../../test_results/test-matrix.md) | Liên kết6 test tới evidence/report có; chờ TV4 xác nhận |
| W3-TV5-02 | CÓ SẢN PHẨM | [report.tex](../../docs/06-report/latex/report.tex) | Đủ Step1–5; bản hiện tại thay nháp0.3 |
| W3-TV5-03 | CÓ SẢN PHẨM | [evaluation.md](../../docs/05-evaluation/evaluation.md) | Có đánh giá Step6; chờ nhận xét thành viên |
| W3-TV5-04 | CÓ SẢN PHẨM | [risks.md](../../docs/05-evaluation/risks.md) | Có vấn đề/hướng phát triển; giả định chờ xác nhận |
| W3-TV5-05 | CÓ SẢN PHẨM | [review-log.md](../../docs/06-report/review-log.md) | Có QA kỹ thuật; G3 chưa có quyết định nhóm |
| W4-TV1-01 | CÓ SẢN PHẨM | [TV1-wan-routing.md](../../docs/06-report/contributions/TV1-wan-routing.md) | Có nội dung cuối kỹ thuật; chờ chốt giả định/bàn giao |
| W4-TV1-02 | CÓ SẢN PHẨM | [review-log.md](../../docs/06-report/review-log.md) | QA trợ lý có; TV1 chưa xác nhận PDF |
| W4-TV1-03 | CÓ SẢN PHẨM | [project-review.md](../../docs/00-management/project-review.md) | Có giới hạn và retest GNS3; PT mới chưa kiểm |
| W4-TV1-04 | CHỜ NHÓM | [approval.md](../../submission/approval.md) | PENDING TV1 duyệt riêng PDF và mô phỏng đúng hash |
| W4-TV1-05 | CHỜ NHÓM | [manifest.md](../../submission/manifest.md) | Gói ứng viên có; tag/release/quyền/nộp chờ nhóm |
| W4-TV2-01 | CÓ SẢN PHẨM | [TV2-lan-wireless.md](../../docs/06-report/contributions/TV2-lan-wireless.md) | BOM/cabling/GPON có nguồn/hình; chờ giao nhận |
| W4-TV2-02 | CÓ SẢN PHẨM | [test-matrix.md](../../test_results/test-matrix.md) | Config/VLAN GNS3 đã đối chiếu; PT có sáu Wi-Fi và32+4 quan sát |
| W4-TV2-03 | CHỜ NHÓM | [review-log.md](../../docs/06-report/review-log.md) | TV2 chưa xác nhận phần PDF |
| W4-TV2-04 | CÓ SẢN PHẨM | [lan-port-plan.md](../../docs/02-design/lan-port-plan.md) | Có port/cabling/phụ lục; chưa có phản hồi đọc chéo để đóng |
| W4-TV2-05 | CÓ SẢN PHẨM | [persistence.md](../../test_results/supplemental/persistence.md) | Reopen GNS3 có lịch sử; WLAN/RF chưa thử; chờ G4 |
| W4-TV3-01 | CÓ SẢN PHẨM | [TV3-security-systems.md](../../docs/06-report/contributions/TV3-security-systems.md) | Có config/contribution/server10/2/2; chờ giao nhận |
| W4-TV3-02 | CÓ SẢN PHẨM | [results.json](../../test_results/runtime/after-firewall-restart-runtime/results.json) | Có retest GNS3 sau sửaPID; VPN/PT chưa thử |
| W4-TV3-03 | CHỜ NHÓM | [review-log.md](../../docs/06-report/review-log.md) | TV3 chưa xác nhận PDF/NAT/security |
| W4-TV3-04 | CÓ SẢN PHẨM | [security-best-practices.md](../../docs/04-security/security-best-practices.md) | Guide/lab data có; chờ kiểm/duyệt chuyên môn |
| W4-TV3-05 | CHỜ NHÓM | [approval.md](../../submission/approval.md) | TV3/TV4 chưa ký G4; chưa reopen trọn sourcePID mới trên máy này |
| W4-TV4-01 | CÓ SẢN PHẨM | [TV4-capacity-testing.md](../../docs/06-report/contributions/TV4-capacity-testing.md) | Có baseline/config/evidence; thêm PT vẫn đang triển khai |
| W4-TV4-02 | MỘT PHẦN | [results.json](../../test_results/runtime/after-firewall-restart-runtime/results.json) | GNS3 retest trực tiếp ngày05/11 trên Linux; PT giữ evidence32+4 ngày04/11 |
| W4-TV4-03 | CÓ SẢN PHẨM | [demo-guide.md](../../simulation/gns3/demo-guide.md) | Có version/dependency/mapping/lệnh/giới hạn; PT có assembly runbook |
| W4-TV4-04 | MỘT PHẦN | [reopen.json](../../test_results/runtime/persistence/reopen.json) | Reopen GNS3 lịch sử137; cần demo lại trên máy trình bày |
| W4-TV4-05 | CÓ SẢN PHẨM | [manifest.md](../../submission/manifest.md) | Manifest/checksum kiểm được; G4 chờ TV1/nhóm |
| W4-TV5-01 | CÓ SẢN PHẨM | [report.tex](../../docs/06-report/latex/report.tex) | Đủ7 Step/5 contributions; chưa có xác nhận giao nhận nhóm |
| W4-TV5-02 | MỘT PHẦN | [metadata.tex](../../docs/06-report/latex/metadata.tex) | Có PDF/LaTeX/logo, L08/nhóm2 và hai người thực hiện; dòng giảng viên chưa có dữ liệu được ẩn |
| W4-TV5-03 | CÓ SẢN PHẨM | [review-log.md](../../docs/06-report/review-log.md) | Có evaluation/QA; chuyên môn và TV1 chờ xác nhận |
| W4-TV5-04 | CÓ SẢN PHẨM | [report.pdf](../../docs/06-report/final/report.pdf) | PDF chính đầy đủ, phụ lục Packet Tracer2 trang, native cả hai và gói/checksum có; chờ phê duyệt nhóm/BKeL |
| W4-TV5-05 | CHỜ NHÓM | [approval.md](../../submission/approval.md) | Chưa có TV1 duyệt/G4/BKeL receipt; không tự ký |

## Dependency cần xử lý

| Việc | Người gỡ/chủ trì | Mốc xử lý |
| --- | --- | --- |
| Dựng/lưu/mở lại `.pkt` tổng và TC01–06 riêng; phần mềm9.0.1 đã cài | Trợ lý triển khai; ba quyền module thử đã được người dùng cấp | Đã có bản tổng58 node, sáu Wi-Fi,32 quan sát sau reopen và4 HTTP ISP thủ công; bản đã thử được khóa theo hash |
| GNS3 demo trên máy trình bày, kiểm dependency/Docker và reopen bản source mới | TV4/người dùng | Trước G2 ngày08/11 và kiểm lại trước G4 |
| Khóa dữ liệu giả định, khảo sát/báo giá/SLA chưa có | TV1–TV5 theo chuyên môn | Rà G1 còn thiếu ngay; khóa trước báo cáo19/11 |
| Điền giảng viên/lớp/họ tên/MSSV và quy định đăng ký nhóm | Người dùng/TV5 | Trước PDF review19/11 |
| Đọc chéo, họp G1–G4, TV1 duyệt PDF và từng mô phỏng đúng hash | Người phụ trách thật | G4 ngày22/11; khóa06/12 |
| Nộp BKeL và lưu biên nhận thật | TV1/TV5 | Trước hạn11/12 theo nhóm cung cấp |

Lệnh Windows: `powershell -File scripts/check.ps1 -Package` để kiểm offline và sinh/kiểm ZIP. Việc này không chạy mạng hoặc tự đóng task phê duyệt.

