# Bộ bàn giao kỹ thuật

**Đã có sản phẩm và kiểm thử; chưa nộp BKeL.**

| Sản phẩm | Đường dẫn | Trạng thái |
| --- | --- | --- |
| Báo cáo PDF | [report.pdf](../docs/06-report/final/report.pdf) | Nội dung đủ7 Step và phụ lục evidence; đã render QA |
| Nguồn báo cáo | [Markdown/SVG](../docs/06-report/source/README.md) | Có thể chỉnh sửa/build lại |
| Mô hình chính | [hospital-3sites.gns3](../simulation/gns3/hospital-3sites.gns3) | GNS3 2.2.55,52 node/52 link, mở lại đã thử |
| Mã nguồn dựng/chạy | [GNS3 runtime/controller](../simulation/gns3/README.md) và scripts | Dockerfile/config/FRR/Linux, không cần IOS license |
| Bằng chứng | [runtime JSON/PCAP/provenance](../test_results/runtime/README.md) |209 +137 kiểm đạt ở hai run cuối; giữ lỗi hội tụ ban đầu |
| File TV2 gốc | [tiendat-lan-original.pkt](../simulation/modules/tv2-lan-wireless/tiendat-lan-original.pkt) | Bảo toàn byte/hash; module Main một phần, chưa chạy PT |
| Gói bàn giao | `hospital-network-delivery.zip` | Sinh bằng package_submission.py, gồm source/PDF/project/evidence |
| Checksum | `SHA256SUMS`, `package-manifest.json` | Hash nội dung và gói, không thay chữ ký duyệt |
| Duyệt/nộp | [approval](approval.md), `bkel-receipt/` | PENDING người phụ trách; không tạo receipt giả |

Từ root repo: `python3 scripts/package_submission.py --check` kiểm gói đã tạo; `sha256sum -c submission/SHA256SUMS` kiểm file trực tiếp. Gói có manifest nội bộ; checksum ngoài còn bao gồm ZIP và package manifest. Sau sửa source/PDF cần chạy kiểm liên quan, rebuild report nếu cần, rồi `python3 scripts/package_submission.py` để cập nhật gói/hash. Không đưa file đặc tả local bị gitignore, IOS image, cache, khóa hoặc runtime container vào ZIP.

Trước nộp nhóm kiểm thông tin lớp/MSSV/nhân sự, yêu cầu2–3 người của đề so với kế hoạch vai tròTV1–TV5 và phê duyệt học phần. Chạy demo trên máy trình bày, đối chiếu checksum, tự nộp BKeL và lưu biên nhận. GNS3 mô phỏng chức năng, chưa chứng minh GPON/DSL PHY/RF, HA chassis, VPN crypto hoặc workload bệnh viện thực.
