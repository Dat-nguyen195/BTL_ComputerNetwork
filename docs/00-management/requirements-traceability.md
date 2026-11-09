# Truy vết đặc tả và sản phẩm thực tế

**Bổ sung WAN đã kiểm:** MPLS L3VPN có module11 nút/10 link, Linux namespaces/QEMU chạy28/28 và sau dựng lại28/28; có PCAP hai nhãn. Project GNS3 riêng dùng chung cấu hình, chưa chạy native module mới. Chi tiết: [bằng chứng MPLS](../../test_results/mpls/README.md). Giá WAN có thêm nguồn lịch sử, vẫn chưa là báo giá hợp đồng hiện hành.


**Cập nhật 04/11/2026; đối chiếu trực tiếp đề gốc 5 trang.** [Review cuối](project-review.md) ghi đủ bảy Step và giới hạn. Phân biệt hồ sơ thiết kế, mô phỏng chức năng và bằng chứng triển khai thực.

| Step | Điểm | Sản phẩm hiện có | Trạng thái |
| --- | --- | --- | --- |
|1 |1 | [Site requirements](../01-survey/site-requirements.md), [survey](../01-survey/survey-checklist.md), [architecture](../02-design/architecture.md), [wireless](../02-design/wireless-plan.md) | Hồ sơ thiết kế đủ; khảo sát thực chưa có |
|2 |1 | [IP/VLAN](../02-design/ip-vlan-plan.md), [BOM](../02-design/equipment-bom.md), [cabling](../02-design/physical-cabling.md), [GPON](../02-design/gpon-design.md), [WAN/cost](../02-design/wan-options-cost.md) | Thiết kế có; model/quote/physical cần xác nhận |
|3 |1 | [Tính tải](../03-capacity/throughput.md), CSV, capacity.py và6 nhóm unit số học | Đã tính đủ kịch bản; chưa đo workload/ISP thật |
|4 |2 | [Native GNS3](../../simulation/gns3/hospital-3sites.gns3), image source và [hướng dẫn](../../simulation/gns3/README.md) | GNS3 52 node/52 link,209+137 kiểm trực tiếp ngày05/11; Packet Tracer tổng58 node/53 cáp và sáu Wi-Fi đã lưu/mở lại |
|5 |2 | [Sáu nhóm bắt buộc](../../test_results/test-matrix.md), [JSON/PCAP](../../test_results/runtime/README.md) | PASS GNS3 Linux; Packet Tracer có 32 quan sát đúng kỳ vọng và 4 HTTP ISP thủ công; RF/throughput chưa đo |
|6 |2 | [Evaluation](../05-evaluation/evaluation.md), [risks](../05-evaluation/risks.md), report và best practices | Đánh giá dựa thiết kế và runtime có giới hạn |
|7 |1 | [PDF](../06-report/final/report.pdf), [source LaTeX](../06-report/latex/report.tex), project và [manifest](../../submission/manifest.md) | Bộ nộp đã chốt kỹ thuật; nhóm tự upload BKeL và lưu biên nhận |

Quy mô600/260/260 PC,10/2/2 server, Main2x5 tầng và Aux2 tầng, tăng20% trong5 năm được giữ trong nguồn thiết kế. GPON được bổ sung cho80→96 PC hành chính trong tổng Main, không bỏ yêu cầu. Hai ISP/leased line được mô hình chức năng bằng Ethernet; không suy DSL/quang/RF thực từ mô phỏng IP. PhầnVPN là đề xuất đủ hai loại; crypto NOT RUN. Lớp L08, nhóm 2; danh sách năm người và phân công BTL2 cho Nguyễn Thành Đạt/Phạm Tiến Đạt được ghi trong [hồ sơ nhóm](team-members.md). Deadline BKeL vẫn cần đối chiếu cổng học phần.
