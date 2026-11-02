# Truy vết đặc tả và sản phẩm thực tế

**02/11/2026. Đối chiếu trực tiếp đề gốc5 trang.** [Review cuối](project-review.md) ghi đủ bảy Step và giới hạn. Phân biệt hồ sơ thiết kế, mô phỏng chức năng và bằng chứng triển khai thực.

| Step | Điểm | Sản phẩm hiện có | Trạng thái |
| --- | --- | --- | --- |
|1 |1 | [Site requirements](../01-survey/site-requirements.md), [survey](../01-survey/survey-checklist.md), [architecture](../02-design/architecture.md), [wireless](../02-design/wireless-plan.md) | Hồ sơ thiết kế đủ; khảo sát thực chưa có |
|2 |1 | [IP/VLAN](../02-design/ip-vlan-plan.md), [BOM](../02-design/equipment-bom.md), [cabling](../02-design/physical-cabling.md), [GPON](../02-design/gpon-design.md), [WAN/cost](../02-design/wan-options-cost.md) | Thiết kế có; model/quote/physical cần xác nhận |
|3 |1 | [Tính tải](../03-capacity/throughput.md), CSV, capacity.py và6 nhóm unit số học | Đã tính đủ kịch bản; chưa đo workload/ISP thật |
|4 |2 | [Native GNS3](../../simulation/gns3/hospital-3sites.gns3), image source và [hướng dẫn](../../simulation/gns3/README.md) | Đã chạy và mở lại file52 node/52 link |
|5 |2 | [Sáu nhóm bắt buộc](../../test_results/test-matrix.md), [JSON/PCAP](../../test_results/runtime/README.md) | PASS trong GNS3 Linux; không phải IOS/RF/throughput |
|6 |2 | [Evaluation](../05-evaluation/evaluation.md), [risks](../05-evaluation/risks.md), report và best practices | Đánh giá dựa thiết kế và runtime có giới hạn |
|7 |1 | [PDF](../06-report/final/report.pdf), [source](../06-report/source/report.md), project và [manifest](../../submission/manifest.md) | Đã chuẩn bị kỹ thuật; duyệt/nộp BKeL chờ nhóm |

Quy mô600/260/260 PC,10/2/2 server, Main2x5 tầng và Aux2 tầng, tăng20% trong5 năm được giữ trong nguồn thiết kế. GPON được bổ sung cho80→96 PC hành chính trong tổng Main, không bỏ yêu cầu. Hai ISP/leased line được mô hình chức năng bằng Ethernet; không suy DSL/quang/RF thực từ mô phỏng IP. PhầnVPN là đề xuất đủ hai loại; crypto NOT RUN. Mốc deadline/nhân sự theo yêu cầu nhóm cần đối chiếu đăng ký học phần riêng.
